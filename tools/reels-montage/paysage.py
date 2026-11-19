#!/usr/bin/env python3
"""Habillage « avis sur Workin » sur fond paysage du Québec.
Prend un Reel avis déjà monté (fond rose uni, safezone appliquée) et remplace le fond rose
par des vidéos (ex. Pexels, « fichier.mp4@début ») ou des photos du Québec animées, enchaînées en fondu et assombries.
- le rose uni devient transparent (le paysage apparaît, y compris dans le texte des pastilles blanches) ;
- le bleu marine (mot en cours, pastille de l'avatar candidat, filet du bas) passe en rose vif ;
- le rose pâle (mots à venir) passe en lavande grisée ;
- le carton final (fond marine) est conservé tel quel.
Usage : python3 paysage.py entree.mp4 sortie.mp4 clip1.mp4@12 photo2.jpg ...
       python3 paysage.py couverture.jpg sortie.jpg photo.jpg   (couverture 4:5)"""
import sys, subprocess, json
import numpy as np

FPS = 30
PINK = '0xe7336d'
NAVY = '0x28235a'
HOT = '0xff5c93'
FUT_SRC = '0xf6a3bf'   # mots à venir (rose pâle)
FUT = '0xb4afc9'       # → lavande grisée
SHADE = '0x1d1a45@0.58'
XF = 0.8   # fondu entre deux photos


def duration(p):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', p],
                                capture_output=True, text=True).stdout)


def outro_start(p):
    """premier instant où l'image est entièrement marine (carton final)."""
    d = duration(p)
    st = max(d - 5, 0)
    r = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{st:.3f}', '-i', p, '-vf', f'fps={FPS},scale=54:96',
                        '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True)
    f = np.frombuffer(r.stdout, np.uint8).reshape(-1, 96, 54, 3).astype(int)
    for i, fr in enumerate(f):
        c = fr[5:15, 2:50].reshape(-1, 3).mean(0)          # bande haute
        if c[0] < 70 and c[2] > 60 and abs(c[0] - 40) < 30:
            return st + i / FPS
    return d


def background(photos, dur):
    n = len(photos)
    seg = (dur + XF * (n - 1)) / n
    ins, flt = [], []
    for i, ph in enumerate(photos):
        if not ph.lower().endswith(('.jpg', '.jpeg', '.png')):
            # vidéo (ex. Pexels) : « fichier.mp4@début » ; recadrée au centre en 9:16
            path, _, st = ph.partition('@')
            ins += ['-stream_loop', '-1', '-ss', st or '0', '-t', f'{seg + 0.5:.3f}', '-i', path]
            flt.append(f"[{i}:v]fps={FPS},crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920,setsar=1,"
                       f"trim=duration={seg:.3f},setpts=PTS-STARTPTS,format=yuv420p[p{i}]")
            continue
        ins += ['-loop', '1', '-framerate', str(FPS), '-t', f'{seg:.3f}', '-i', ph]
        fr = int(seg * FPS) + 2
        zin = i % 2 == 0
        z = f"'min(1.0+0.12*on/{fr},1.12)'" if zin else f"'max(1.12-0.12*on/{fr},1.0)'"
        flt.append(f"[{i}:v]scale=-2:2400,crop=1350:2400:(iw-1350)/2:0,setsar=1,"
                   f"zoompan=z={z}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps={FPS},"
                   f"trim=duration={seg:.3f},setpts=PTS-STARTPTS,format=yuv420p[p{i}]")
    last = 'p0'
    for i in range(1, n):
        off = i * (seg - XF)
        flt.append(f"[{last}][p{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}]")
        last = f'x{i}'
    flt.append(f"[{last}]drawbox=x=0:y=0:w=iw:h=ih:color={SHADE}:t=fill,trim=duration={dur:.3f}[bg]")
    return ins, flt


def main(src, dst, photos):
    d = duration(src)
    os_ = outro_start(src)
    ins, flt = background(photos, os_)
    k = len(photos)
    flt += [
        f"[{k}:v]fps={FPS},split=2[main][end]",
        f"[main]trim=end={os_:.4f},setpts=PTS-STARTPTS,format=rgba,split=3[m1][m2][m3]",
        f"[m1]colorkey={PINK}:0.16:0.06[fg]",
        f"[m2]colorkey={NAVY}:0.12:0.08,alphaextract,negate[nm]",
        f"color=c={HOT}:s=1080x1920:r={FPS}:d={os_:.4f},format=rgba[hot]",
        "[hot][nm]alphamerge[hotm]",
        f"[m3]colorkey={FUT_SRC}:0.09:0.06,alphaextract,negate[fm]",
        f"color=c={FUT}:s=1080x1920:r={FPS}:d={os_:.4f},format=rgba[fut]",
        "[fut][fm]alphamerge[futm]",
        "[bg][fg]overlay=format=auto[a]",
        "[a][hotm]overlay=format=auto[b]",
        "[b][futm]overlay=format=auto,format=yuv420p[v1]",
        f"[end]trim=start={os_:.4f},setpts=PTS-STARTPTS,format=yuv420p[v2]",
        "[v1][v2]concat=n=2:v=1:a=0[v]",
    ]
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-i', src, '-filter_complex', ';'.join(flt),
                    '-map', '[v]', '-map', f'{k}:a', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20',
                    '-preset', 'medium', '-c:a', 'copy', '-movflags', '+faststart', '-t', f'{d:.3f}', dst], check=True)
    print(json.dumps(dict(src=src, duree=round(d, 2), carton=round(os_, 2), photos=photos)))


def cover(src, dst, photo):
    """couverture 4:5 (jpg) : même traitement sur une seule photo fixe."""
    fc = (f"[0:v]scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350,setsar=1,format=rgba,"
          f"drawbox=x=0:y=0:w=iw:h=ih:color={SHADE}:t=fill[bg];"
          f"[1:v]format=rgba,split=3[m1][m2][m3];"
          f"[m1]colorkey={PINK}:0.18:0.06[fg];"
          f"[m2]colorkey={NAVY}:0.12:0.08,alphaextract,negate[nm];"
          f"color=c={HOT}:s=1080x1350,format=rgba[hot];[hot][nm]alphamerge[hotm];"
          f"[m3]colorkey={FUT_SRC}:0.09:0.06,alphaextract,negate[fm];"
          f"color=c={FUT}:s=1080x1350,format=rgba[fut];[fut][fm]alphamerge[futm];"
          f"[bg][fg]overlay[a];[a][hotm]overlay[b];[b][futm]overlay,format=yuvj420p[v]")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', photo, '-i', src, '-filter_complex', fc,
                    '-map', '[v]', '-frames:v', '1', '-q:v', '2', dst], check=True)


if __name__ == '__main__':
    if sys.argv[1].endswith('.jpg'):
        cover(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3:])
