#!/usr/bin/env python3
"""Recadre un Reel déjà monté pour respecter les zones masquées par l'interface Instagram
(haut ≈ 250 px, bas ≈ 480 px, colonne de droite ≈ 150 px).
- couverture : contenu réduit à 88 % et recentré ;
- sous-titres : bandeau du haut (pastille + question) descendu de 140 px ; bloc intervenant + texte
  réduit à 88 % (marge droite élargie) ; bouton « Offres d'emploi » supprimé (il passait sous la légende) ;
- carton final : inchangé.
Usage : python3 safezone.py entree.mp4 sortie.mp4"""
import sys, subprocess, json
import numpy as np

FPS = 30

def frames(path, start, dur, crop):
    w, h, x, y = crop
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{start:.3f}', '-t', f'{dur:.3f}', '-i', path,
                        '-vf', f'fps={FPS},crop={w}:{h}:{x}:{y}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(-1, h, w, 3).astype(int)

def duration(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True).stdout)

def analyse(path):
    d = duration(path)
    # fin de couverture : la pastille des sous-titres apparaît en haut à gauche
    f = frames(path, 0, 3.5, (210, 40, 90, 160)).mean(axis=(1, 2))
    diff = np.abs(f - f[0]).sum(axis=1)
    ce = next(i for i, v in enumerate(diff) if v > 40) / FPS
    # début du carton final : pastille rose « WORKIN GROUP » sur fond marine
    st = max(d - 4.5, 0)
    a = frames(path, st, 4.5, (40, 20, 180, 602)).mean(axis=(1, 2))
    b = frames(path, st, 4.5, (40, 40, 900, 300)).mean(axis=(1, 2))
    os_ = None
    for i in range(min(len(a), len(b))):
        if a[i][0] > 200 and 100 < a[i][1] < 170 and b[i][0] < 60:
            os_ = st + i / FPS
            break
    if os_ is None:
        os_ = d
    bg = frames(path, ce + 0.2, 0.1, (4, 4, 700, 520))[0].mean(axis=(0, 1))
    return d, ce, os_, '0x%02x%02x%02x' % tuple(int(v) for v in bg)

def main(src, dst):
    d, ce, os_, bg = analyse(src)
    # le fond est pris dans la vidéo elle-même (zone vide), pour éviter tout écart de couleur
    fc = (
        f"[0:v]fps={FPS},format=yuv420p,split=3[a][b][c];"
        # couverture
        f"[a]trim=end={ce:.4f},setpts=PTS-STARTPTS,split=3[a0][a1][a2];"
        f"[a2]crop=40:40:600:480,scale=1050:1895[ap];"
        f"[a1]crop=1050:1600:30:150,scale=924:1408[ac];"
        f"[a0][ap]overlay=x=30:y=0[ab];[ab][ac]overlay=x=36:y=246[v1];"
        # sous-titres
        f"[b]trim=start={ce:.4f}:end={os_:.4f},setpts=PTS-STARTPTS,split=4[b0][b1][b2][b3];"
        f"[b3]crop=40:40:600:480,scale=1050:1895[bp];"
        f"[b1]crop=1050:250:30:130[bt];"
        f"[b2]crop=1050:800:30:600,scale=924:704[bm];"
        f"[b0][bp]overlay=x=30:y=0[bb];[bb][bt]overlay=x=30:y=270[bb2];[bb2][bm]overlay=x=36:y=600[v2];"
        # carton final
        f"[c]trim=start={os_:.4f},setpts=PTS-STARTPTS[v3];"
        f"[v1][v2][v3]concat=n=3:v=1:a=0,format=yuv420p[v]"
    )
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-filter_complex', fc, '-map', '[v]', '-map', '0:a',
                    '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20', '-preset', 'medium', '-tune', 'stillimage',
                    '-c:a', 'copy', '-movflags', '+faststart', dst], check=True)
    print(json.dumps(dict(src=src, duree=round(d, 2), couverture=round(ce, 2), carton=round(os_, 2), fond=bg)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
