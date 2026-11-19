#!/usr/bin/env python3
"""Habillage « avis sur Workin » sur fond paysage du Québec.
Prend un Reel avis déjà monté (fond rose uni, safezone appliquée) et remplace le fond rose
par des vidéos (ex. Pexels, « fichier.mp4@début ») ou des photos du Québec animées, enchaînées en fondu et assombries.
- le rose uni devient transparent (le paysage apparaît, y compris dans le texte des pastilles blanches) ;
- le bleu marine (mot en cours, pastille de l'avatar candidat, filet du bas) passe en rose vif ;
- le rose pâle (mots à venir) devient du blanc translucide ;
- chaque pixel est traité comme un mélange rose↔marine ou rose↔blanc (bords lissés) ; les autres couleurs
  (emojis : yeux, cheveux, cravate…) sont conservées telles quelles ;
- le carton final (fond marine) est conservé tel quel.
Usage : python3 paysage.py entree.mp4 sortie.mp4 clip1.mp4@12 photo2.jpg ...
       python3 paysage.py couverture.jpg sortie.jpg photo.jpg   (couverture 4:5)"""
import sys, subprocess, json
import numpy as np

FPS = 30
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


P_RGB = np.array([0xe7, 0x33, 0x6d], np.float32)    # rose uni du fond
LINES = [  # (couleur d'origine, couleur finale) : le pixel est vu comme un mélange rose ↔ couleur
    (np.array([0x28, 0x23, 0x5a], np.float32), np.array([0xff, 0x5c, 0x93], np.float32)),  # marine → rose vif
    (np.array([255, 255, 255], np.float32), np.array([255, 255, 255], np.float32)),        # blanc (le rose pâle = blanc translucide)
]
TOL = 28.0   # distance max (0-255) à une droite de mélange ; au-delà, pixel conservé tel quel (emojis…)


def composite(fg, bg, tol=TOL):
    """remplace le rose par le fond ; les mélanges rose↔marine / rose↔blanc deviennent rose vif / blanc
    avec la transparence correspondante ; tout le reste (emojis : yeux, cheveux…) reste intact."""
    f = fg.astype(np.float32)
    best_d = np.full(f.shape[:2], 1e9, np.float32)
    alpha = np.ones(f.shape[:2], np.float32)
    col = f.copy()
    for src, dst in LINES:
        v = src - P_RGB
        t = np.clip(((f - P_RGB) @ v) / (v @ v), 0, 1)
        d = np.linalg.norm(f - (P_RGB + t[..., None] * v), axis=2)
        m = (d < tol) & (d < best_d)
        best_d = np.where(m, d, best_d)
        alpha = np.where(m, t, alpha)
        col = np.where(m[..., None], dst, col)
    a = alpha[..., None]
    return (col * a + bg.astype(np.float32) * (1 - a)).clip(0, 255).astype(np.uint8)


def main(src, dst, photos):
    d = duration(src)
    os_ = outro_start(src)
    ins, flt = background(photos, os_)
    W, H = 1080, 1920
    n = int(round(os_ * FPS))
    pb = subprocess.Popen(['ffmpeg', '-v', 'error', *ins, '-filter_complex', ';'.join(flt), '-map', '[bg]',
                           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    pf = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'fps={FPS}', '-t', f'{os_:.4f}',
                           '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    tmp = dst + '.part1.mp4'
    po = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-i', src,
                           '-filter_complex', f"[1:v]fps={FPS},trim=start={os_:.4f},setpts=PTS-STARTPTS,format=yuv420p[e];"
                                              f"[0:v]format=yuv420p[s];[s][e]concat=n=2:v=1:a=0[v]",
                           '-map', '[v]', '-map', '1:a', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '23',
                           '-maxrate', '2200k', '-bufsize', '4400k', '-preset', 'medium', '-c:a', 'copy',
                           '-movflags', '+faststart', '-t', f'{d:.3f}', dst], stdin=subprocess.PIPE)
    sz = W * H * 3
    last_bg = None
    for i in range(n):
        fb = pf.stdout.read(sz)
        if len(fb) < sz:
            break
        bb = pb.stdout.read(sz)
        if len(bb) == sz:
            last_bg = np.frombuffer(bb, np.uint8).reshape(H, W, 3)
        fr = np.frombuffer(fb, np.uint8).reshape(H, W, 3)
        po.stdin.write(composite(fr, last_bg).tobytes())
    po.stdin.close(); po.wait(); pf.kill(); pb.kill()
    print(json.dumps(dict(src=src, duree=round(d, 2), carton=round(os_, 2), fonds=photos)))


def cover(src, dst, photo):
    """couverture 4:5 (jpg) : même traitement sur une image fixe (tolérance un peu plus large : JPEG)."""
    W, H = 1080, 1350
    rd = lambda args: np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', *args, '-frames:v', '1', '-f', 'rawvideo',
                                                    '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout,
                                    np.uint8).reshape(H, W, 3)
    bg = rd(['-i', photo, '-vf', f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                                 f"drawbox=x=0:y=0:w=iw:h=ih:color={SHADE}:t=fill"])
    fg = rd(['-i', src, '-vf', f'scale={W}:{H}'])
    out = composite(fg, bg, tol=32)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-i', '-',
                    '-q:v', '2', dst], input=out.tobytes(), check=True)


if __name__ == '__main__':
    if sys.argv[1].endswith('.jpg'):
        cover(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3:])
