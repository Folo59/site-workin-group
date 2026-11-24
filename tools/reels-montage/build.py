#!/usr/bin/env python3
"""python3 build.py spec.json outdir
spec = {
 "id": "11-01-...", "theme": "conseil|temoignage|avis", "q": "...", "who": "...", "whosub": "...",
 "people": [{"emoji","cand"}],            # ordre de la couverture
 "speakers": {"claire": {"emoji","name","role","cand"}},
 "src": "/chemin/audio_ou_video",
 "clips": [ {"s": t0, "e": t1, "spk": "claire", "words": [[mot, ts, te], ...]} ]  # temps source
}
Produit outdir/<id>.mp4 et outdir/<id>.jpg (couverture 1080x1350)."""
import json, sys, os, subprocess, shutil, re

COVER = 1.6     # couverture
jingle = lambda k: os.path.join(HERE, 'sons', f"{os.environ['SON']}_{k}.wav") if os.environ.get('SON') else os.path.join(HERE, f'jingle_{k}.wav')
OUTRO = 2.6     # carton final
GAP = 0.25      # silence entre deux extraits
FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))

def run(cmd):
    subprocess.run(cmd, check=True)

def chunks(words, maxw=10, maxc=58):
    """découpe une suite de mots en blocs de 3 lignes max (~10 mots), en coupant de préférence en fin de phrase"""
    out, cur = [], []
    for w in words:
        cur.append(w)
        txt = ' '.join(x[0] for x in cur)
        end = w[0].rstrip()[-1:] in '.?!'
        if (end and len(cur) >= 4) or len(cur) >= maxw or len(txt) >= maxc:
            out.append(cur); cur = []
    if cur:
        if out and len(cur) <= 2 and len(' '.join(x[0] for x in out[-1] + cur)) <= maxc + 12:
            out[-1] += cur
        else:
            out.append(cur)
    return out

def main(spec_path, outdir):
    sp = json.load(open(spec_path))
    os.makedirs(outdir, exist_ok=True)
    tmp = os.path.join(outdir, 'tmp_' + sp['id']); shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    base = {k: sp[k] for k in ('theme', 'q', 'who', 'whosub', 'people')}
    states, starts = [dict(base, mode='cover')], [0.0]
    t = COVER
    audio_parts = []
    for ci, c in enumerate(sp['clips']):
        if ci:
            t += GAP
        off = t - c['s']                     # instant reel = instant source + off
        audio_parts.append((c['s'], c['e']))
        spk = sp['speakers'][c['spk']]
        for ch in chunks(c['words']):
            ws = [re.sub(r'(\w)([?!])$', '\\1\u00a0\\2', w[0]) for w in ch]
            for k, w in enumerate(ch):
                states.append(dict(base, mode='sub', speaker=spk, words=ws, cur=k)); starts.append(max(w[1] + off, t))
            states.append(dict(base, mode='sub', speaker=spk, words=ws, cur=len(ws))); starts.append(ch[-1][2] + off)
        t = c['e'] + off
    starts[1] = COVER
    for i in range(1, len(starts)):
        starts[i] = max(starts[i], starts[i - 1] + 1.0 / FPS)
    end_speech = max(t, starts[-1] + 0.3)
    states.append(dict(base, mode='outro')); starts.append(end_speech)
    total = end_speech + OUTRO
    starts.append(total)
    dur = [starts[i + 1] - starts[i] for i in range(len(states))]
    json.dump(states, open(os.path.join(tmp, 'states.json'), 'w'), ensure_ascii=False)
    run(['node', os.path.join(HERE, 'frames.js'), os.path.join(tmp, 'states.json'), tmp])
    with open(os.path.join(tmp, 'list.txt'), 'w') as f:
        for i, d in enumerate(dur):
            f.write(f"file 's{i:04d}.png'\nduration {d:.4f}\n")
        f.write(f"file 's{len(dur)-1:04d}.png'\n")
    # audio : silence de couverture + extraits + silence final
    flt, ins = [], []
    for i, (s, e) in enumerate(audio_parts):
        flt.append(f"[0:a]atrim={s}:{e},asetpts=PTS-STARTPTS,afade=t=in:d=0.04,afade=t=out:st={max(e-s-0.15,0)}:d=0.15[a{i}]")
    sil = lambda d, n: f"anullsrc=r=48000:cl=mono,atrim=0:{d}[{n}]"
    flt.append(sil(COVER, 'sc')); flt.append(sil(OUTRO, 'so')); flt.append(sil(GAP, 'sg'))
    seq = ['[sc]']
    for i in range(len(audio_parts)):
        if i:
            seq.append(f'[g{i}]')
        seq.append(f'[a{i}]')
    seq.append('[so]')
    if len(audio_parts) > 1:
        flt.append(f"[sg]asplit={len(audio_parts)-1}" + ''.join(f'[g{i}]' for i in range(1, len(audio_parts))))
    else:
        flt.append('[sg]anullsink')
    flt.append(''.join(seq) + f"concat=n={len(seq)}:v=0:a=1,aformat=sample_rates=48000:channel_layouts=mono,loudnorm=I=-15:TP=-1.5:LRA=11[aout]")
    run(['ffmpeg', '-v', 'error', '-y', '-i', sp['src'], '-filter_complex', ';'.join(flt), '-map', '[aout]', '-ar', '48000', '-c:a', 'pcm_s16le', os.path.join(tmp, 'a.wav')])
    if os.environ.get('JINGLE', '1') == '1':
        d = int(end_speech * 1000)
        run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(tmp, 'a.wav'), '-i', jingle('intro'), '-i', jingle('outro'),
             '-filter_complex', f"[1:a]volume=0.9[j1];[2:a]volume=0.9,adelay={d}[j2];[0:a][j1][j2]amix=inputs=3:duration=first:normalize=0[m]",
             '-map', '[m]', '-ar', '48000', '-c:a', 'pcm_s16le', os.path.join(tmp, 'a2.wav')])
        os.replace(os.path.join(tmp, 'a2.wav'), os.path.join(tmp, 'a.wav'))
    mp4 = os.path.join(outdir, sp['id'] + '.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', os.path.join(tmp, 'list.txt'), '-i', os.path.join(tmp, 'a.wav'),
         '-vf', f'fps={FPS},format=yuv420p', '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20', '-preset', 'medium', '-tune', 'stillimage',
         '-c:a', 'aac', '-b:a', '128k', '-t', f'{total:.3f}', '-movflags', '+faststart', mp4])
    # zones masquées par l'interface Instagram (haut, bas, colonne de droite)
    safe = mp4[:-4] + '.safe.mp4'
    run(['python3', os.path.join(HERE, 'safezone.py'), mp4, safe])
    os.replace(safe, mp4)
    # couverture 4:5
    cov = [dict(base, mode='cover', h=1350, file=sp['id'] + '.jpg')]
    json.dump(cov, open(os.path.join(tmp, 'cover.json'), 'w'), ensure_ascii=False)
    run(['node', os.path.join(HERE, 'frames.js'), os.path.join(tmp, 'cover.json'), outdir])
    print(mp4, f'{total:.1f}s', len(states), 'états')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
