import json
CSS="""*{box-sizing:border-box;margin:0;padding:0}body{font-family:Poppins,sans-serif;-webkit-font-smoothing:antialiased}
.s{position:relative;overflow:hidden;background:#29245c;color:#fff}
.tag{display:inline-block;background:#ea346f;color:#fff;font-weight:700;letter-spacing:.14em;text-transform:uppercase;border-radius:999px}
h1{font-weight:700;line-height:1.05;letter-spacing:-.02em}.r{color:#ea346f}
.blob{position:absolute;border-radius:50%;background:#ea346f;opacity:.9}
.poster{position:absolute;border-radius:18px;box-shadow:0 30px 60px rgba(0,0,0,.45);border:8px solid #fff}
.info{display:flex;flex-direction:column;gap:14px}
.info div{display:flex;gap:18px;align-items:flex-start}.info i{font-style:normal;flex:none}
.team{position:absolute;background:#fff;color:#29245c;font-weight:700;border-radius:999px;box-shadow:0 12px 30px rgba(0,0,0,.25)}
.team b{color:#ea346f}
.city{background:rgba(255,255,255,.08);border-radius:26px;padding:26px 30px}
.city b{display:block;font-size:40px}.city span{display:block;font-size:27px;color:#cfcbef;line-height:1.35;margin-top:4px}
.city em{font-style:normal;display:inline-block;background:#ea346f;color:#fff;border-radius:999px;padding:4px 18px;font-size:24px;font-weight:700;margin-top:10px}
"""
def page(w,h,body):
    return f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body><div class=s style='width:{w}px;height:{h}px'>{body}</div></body></html>"
C={
 'toulouse':dict(d='Mercredi 18 novembre',h='9&nbsp;h&nbsp;–&nbsp;18&nbsp;h',lieu='Palais consulaire',adr='2 rue d’Alsace-Lorraine, Toulouse',acc='Entrée libre et gratuite',ville='Toulouse'),
 'lyon':dict(d='Mercredi 25 novembre',h='9&nbsp;h&nbsp;–&nbsp;18&nbsp;h',lieu='Ninkasi Cordeliers',adr='1 rue Président Carnot, Lyon 2e',acc='Métro A, arrêt Cordeliers',ville='Lyon'),
 'lille':dict(d='Samedi 28 novembre',h='9&nbsp;h&nbsp;–&nbsp;17&nbsp;h&nbsp;30',lieu='Hôtel JOST',adr='10 rue Meurein, Lille',acc='Métro Gambetta',ville='Lille'),
 'paris':dict(d='Mercredi 2 décembre',h='9&nbsp;h&nbsp;–&nbsp;18&nbsp;h',lieu='Maison des associations de solidarité',adr='10 rue des Terres au Curé, Paris 13e',acc='Entrée gratuite sur inscription',ville='Paris'),
}
TITLES={'toulouse':'Demain, on vous attend à <span class=r>Toulouse</span>','lyon':'Mercredi, cap sur <span class=r>Lyon</span>','lille':'Samedi, on joue à domicile : <span class=r>Lille</span>','paris':'Dernière date : <span class=r>Paris</span>'}
out={}
# Posts ville 1080x1350
for k,c in C.items():
    body=f"""<div class=blob style='width:520px;height:520px;right:-180px;top:-180px;opacity:.18'></div>
<div style='position:absolute;left:80px;top:90px;right:80px'>
<span class=tag style='font-size:24px;padding:14px 26px'>Salon Canada · {c['ville']}</span>
<h1 style='font-size:76px;margin-top:34px'>{TITLES[k]}</h1>
<p style='font-size:32px;margin-top:22px;color:#cfcbef;line-height:1.35'>Étudier, s’installer, travailler, vivre au Canada</p></div>
<div class=info style='position:absolute;left:80px;top:600px;width:500px;font-size:34px;line-height:1.3;gap:22px'>
<div><i>📅</i><span><b>{c['d']}</b><br>{c['h']}</span></div>
<div><i>📍</i><span><b>{c['lieu']}</b><br><span style='color:#cfcbef'>{c['adr']}</span></span></div>
<div><i>✅</i><span>{c['acc']}</span></div></div>
<img class=poster src='{k}.png' style='width:430px;right:60px;top:520px;transform:rotate(4deg)'>
<div class=team style='left:80px;bottom:90px;font-size:34px;padding:26px 40px'>L’équipe <b>Workin</b> sera présente 👋</div>"""
    out[f'post-{k}']=(1080,1350,body)
# Stories jour J 1080x1920
for k,c in C.items():
    body=f"""<div class=blob style='width:700px;height:700px;right:-260px;top:-200px;opacity:.18'></div>
<div style='position:absolute;left:90px;right:90px;top:270px'>
<span class=tag style='font-size:28px;padding:16px 30px'>C’est aujourd’hui</span>
<h1 style='font-size:128px;margin-top:44px'>Salon Canada<br><span class=r>{c['ville']}</span></h1>
<div class=info style='font-size:46px;line-height:1.3;margin-top:50px;gap:26px'>
<div><i>🕘</i><span><b>{c['h']}</b></span></div>
<div><i>📍</i><span><b>{c['lieu']}</b><br><span style='color:#cfcbef;font-size:38px'>{c['adr']}</span></span></div></div></div>
<img class=poster src='{k}.png' style='width:560px;right:80px;top:960px;transform:rotate(-4deg)'>
<div class=team style='left:90px;top:1420px;font-size:44px;padding:34px 46px;max-width:480px;border-radius:44px;line-height:1.25'>Venez rencontrer l’équipe <b>Workin</b> 👋</div>"""
    out[f'story-{k}']=(1080,1920,body)
# Tournée post + story
cities=''.join(f"<div class=city><b>{c['ville']}</b><span>{c['d']} · {c['h']}<br>{c['lieu']}</span></div>" for c in C.values())
out['post-tournee']=(1080,1350,f"""<div class=blob style='width:520px;height:520px;right:-180px;top:-180px;opacity:.18'></div>
<div style='position:absolute;left:80px;right:80px;top:80px'><span class=tag style='font-size:24px;padding:14px 26px'>Salons Canada · Air Canada</span>
<h1 style='font-size:72px;margin-top:30px'>4 salons, 4 villes :<br>l’équipe <span class=r>Workin</span> y sera</h1>
<div style='display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:50px'>{cities.replace('<div class=city>','<div class=city style="padding:34px 34px">').replace('<b>','<b style="font-size:50px">').replace('<span>','<span style="font-size:29px">')}</div>
<p style='font-size:30px;margin-top:40px;color:#cfcbef;line-height:1.4'>Étudier, s’installer, travailler, vivre au Canada.<br>Venez nous poser vos questions sur le travail au Québec 👋</p></div>
<div class=team style='left:80px;bottom:80px;font-size:34px;padding:26px 40px'>L’équipe <b>Workin</b> sera présente 👋</div>""")
out['story-tournee']=(1080,1920,f"""<div class=blob style='width:700px;height:700px;right:-260px;top:-200px;opacity:.18'></div>
<div style='position:absolute;left:90px;right:90px;top:270px'><span class=tag style='font-size:28px;padding:16px 30px'>On part en tournée</span>
<h1 style='font-size:96px;margin-top:40px'>4 salons Canada,<br>l’équipe <span class=r>Workin</span> y sera</h1>
<div style='display:flex;flex-direction:column;gap:26px;margin-top:56px'>{cities.replace('<div class=city>','<div class=city style="padding:32px 40px">').replace('<b>','<b style="font-size:56px">').replace('<span>','<span style="font-size:36px">')}</div></div>""")
for n,(w,h,b) in out.items(): open(n+'.html','w').write(page(w,h,b))
json.dump({n:[w,h] for n,(w,h,b) in out.items()},open('list.json','w'))
