# Montage des Reels

- `tpl.html` : gabarit 1080×1920 (thèmes conseil / temoignage / avis, couverture, sous-titres karaoké, carton final).
- `frames.js` : rend les états en PNG avec Playwright.
- `build.py spec.json sortie/` : assemble couverture (1,6 s) + extraits audio + sous-titres mot à mot + carton final (2,6 s), ajoute la musique lo-fi (`jingle_intro.wav` / `jingle_outro.wav`) et produit `<id>.mp4` + couverture 4:5 `<id>.jpg`.
- Spec : `id, theme, q, who, whosub, people[{emoji,cand}], speakers{clé:{emoji,name,role,cand}}, src, clips[{s,e,spk,words:[[mot,début,fin]]}]` (temps dans le fichier source).
- Transcription mot à mot : faster-whisper `medium` (fr, word_timestamps) — à lancer via une branche temporaire GitHub Actions avec l'audio chiffré (le dépôt est public).
