# Génère l'infolettre HTML (compatible e-mail : tableaux, styles en ligne, 600 px)
import html, pathlib
NAVY='#29245c'; ROSE='#ea346f'; LILAS='#f1effa'; TXT='#1f1d3a'; GRIS='#6b6890'
IMG='https://workin-group.com/assets/infolettre'
FONT="font-family:'Poppins',Arial,Helvetica,sans-serif;"
e=html.escape

def p(t,extra=''):
    return f'<p style="text-align:left;margin:0 0 14px;{FONT}font-size:15px;line-height:1.6;color:{TXT};{extra}">{t}</p>'
def ul(items):
    li=''.join(f'<tr><td valign="top" style="width:18px;padding:0 0 10px;{FONT}font-size:15px;line-height:1.6;color:{ROSE};font-weight:700;">•</td><td style="text-align:left;padding:0 0 10px;{FONT}font-size:15px;line-height:1.6;color:{TXT};">{i}</td></tr>' for i in items)
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 6px;">{li}</table>'
def callout(t):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:4px 0 14px;"><tr><td style="text-align:left;border-left:4px solid {ROSE};background:{LILAS};padding:14px 16px;{FONT}font-size:15px;line-height:1.6;color:{NAVY};font-weight:600;border-radius:0 8px 8px 0;">{t}</td></tr></table>'
def source(t):
    return f'<p style="text-align:left;margin:0;{FONT}font-size:11.5px;line-height:1.5;color:{GRIS};">Source{"s" if ";" in t else ""} : {t}</p>'
def section(n,kicker,title,body):
    return f'''<tr><td style="text-align:left;padding:30px 26px 0;">
<p style="text-align:left;margin:0 0 8px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">{kicker}</p>
<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 14px;"><tr>
<td valign="top" width="30" style="width:30px;padding-top:1px;"><img src="{IMG}/num-{n}.png" width="30" height="30" alt="{n}" style="display:block;width:30px;height:30px;border:0;"></td>
<td valign="top" style="padding-left:12px;{FONT}font-size:20px;line-height:1.3;font-weight:700;color:{NAVY};">{title}</td></tr></table>
{body}</td></tr>'''
def button(label,href):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 0;"><tr><td align="center" style="text-align:center;"><table role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto;"><tr><td align="center" style="text-align:center;background:{ROSE};border-radius:30px;"><a href="{href}" style="display:inline-block;padding:14px 28px;{FONT}font-size:15px;font-weight:700;color:#ffffff;text-decoration:none;text-align:center;">{label}</a></td></tr></table></td></tr></table>'

stats=''.join(f'<div style="display:inline-block;vertical-align:top;width:100%;max-width:178px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="padding:5px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="text-align:left;background:{LILAS};border-radius:10px;padding:16px 14px;"><p style="text-align:left;margin:0 0 4px;{FONT}font-size:20px;font-weight:700;color:{ROSE};line-height:1.15;white-space:nowrap;">{a}</p><p style="text-align:left;margin:0;{FONT}font-size:12.5px;line-height:1.45;color:{NAVY};">{b}</p></td></tr></table></td></tr></table></div>' for a,b in [
 ('86 jours','ouvrables en moyenne pour une EIMT bas salaire'),('102 jours','ouvrables en moyenne pour une EIMT haut salaire'),('+ affichage','la période d’affichage préalable s’ajoute à ces délais')])

reflexes=[
 ('Reprenez la liste des permis de votre équipe, avec leurs dates d’expiration :','chaque prochain renouvellement en EIMT bas salaire peut désormais viser une durée plus longue.'),
 ('Une demande déposée avant le 6 novembre ?','Le communiqué ne vise que les demandes présentées à partir de cette date. Écrivez-nous : nous regardons votre dossier au cas par cas.'),
 ('Montréal et Laval restent visées par le refus de traitement pour les postes à bas salaire :','le taux de chômage de la région de Montréal est de 7,2 % pour les demandes déposées du 9 octobre 2026 au 7 janvier 2027, au-dessus du seuil de 6 %.'),
 ('Comptez large :','pour un poste à bas salaire, l’annonce doit être affichée au moins 8 semaines consécutives dans les 3 mois qui précèdent la demande d’EIMT, et ce temps d’affichage ne fait pas partie des délais de traitement publiés.')]
ref=''.join(f'<tr><td valign="top" width="42" style="width:42px;padding:0 0 14px;"><img src="{IMG}/etape-{i}.png" width="28" height="28" alt="{i}" style="display:block;width:28px;height:28px;border:0;"></td><td style="text-align:left;padding:3px 0 14px;{FONT}font-size:15px;line-height:1.6;color:{TXT};"><strong style="color:{NAVY};">{a}</strong> {b}</td></tr>' for i,(a,b) in enumerate(reflexes,1))

links=[('EDSC · Communiqué · 06-11-2026','Réformes ciblées au Programme des travailleurs étrangers temporaires','Le texte officiel des changements annoncés.','https://www.canada.ca/fr/emploi-developpement-social/nouvelles/2026/11/le-gouvernement-du-canada-annonce-des-reformes-ciblees-au-programme-des-travailleurs-etrangers-temporaires-afin-de-repondre-aux-besoins-du-marche-d.html'),
 ('CIC News · 09-11-2026','Canada doubles maximum duration of low-wage TFWP work permits (en anglais)','Une lecture commentée de la mesure.','https://www.cicnews.com/2026/11/canada-doubles-maximum-duration-of-low-wage-tfwp-work-permits-1182361.html'),
 ('IRCC · Page officielle','Organisations reconnues d’Expérience internationale Canada (en anglais)','La liste des organisations et ce qu’elles offrent.','https://www.canada.ca/en/immigration-refugees-citizenship/services/work-canada/iec/recognized-organizations.html')]
lk=''.join(f'<tr><td style="text-align:left;padding:0 0 16px;"><p style="text-align:left;margin:0 0 2px;{FONT}font-size:11px;letter-spacing:1px;text-transform:uppercase;color:{GRIS};font-weight:600;">{a}</p><a href="{u}" style="{FONT}font-size:15px;font-weight:700;color:{NAVY};text-decoration:underline;text-decoration-color:{ROSE};">{b}</a><p style="text-align:left;margin:2px 0 0;{FONT}font-size:13.5px;line-height:1.5;color:{TXT};">{c}</p></td></tr>' for a,b,c,u in links)

def secteur(t,body):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 14px;"><tr><td style="text-align:left;border:1px solid #e3e0f2;border-radius:10px;padding:18px 20px;"><p style="text-align:left;margin:0 0 6px;{FONT}font-size:16px;font-weight:700;color:{NAVY};">{t}</p><p style="text-align:left;margin:0;{FONT}font-size:14.5px;line-height:1.6;color:{TXT};">{body}</p></td></tr></table>'

body=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>L’infolettre immigration de vos embauches · Novembre 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:0;background:#eeecf6;}} a{{color:{NAVY};}}
@media (max-width:620px){{ .wrap{{width:100%!important;}} .px{{padding-left:20px!important;padding-right:20px!important;}} .stack{{display:block!important;width:100%!important;}} .hide-m{{display:none!important;}} .card-m{{max-width:100%!important;}} .logo-m{{max-width:100%!important;text-align:center!important;}} .logo-t{{float:none!important;margin:0 auto!important;}} .logo-c{{text-align:center!important;}} .logo-i{{margin:0 auto!important;}} .center-m{{text-align:left!important;padding-top:14px!important;padding-left:0!important;border-left:0!important;}} }}
</style></head>
<body style="margin:0;padding:0;background:#eeecf6;">
<!--email_off-->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">EIMT bas salaire : jusqu’à deux ans au lieu d’un. Nouveaux délais, traitement simplifié et une porte Jeunes professionnels ouverte jusqu’au 24 novembre.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eeecf6;"><tr><td align="center" style="padding:16px 8px;">
<table role="presentation" class="wrap" width="100%" align="center" cellpadding="0" cellspacing="0" style="text-align:left;width:100%;max-width:600px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;">

<!-- EN-TÊTE -->
<tr><td class="px" style="text-align:left;background:{NAVY};padding:24px 26px 18px;">
<div style="font-size:0;line-height:0;text-align:center;">
<div class="logo-m" style="display:inline-block;vertical-align:middle;width:100%;max-width:256px;padding:0 0 18px;text-align:center;">
<table class="logo-t" role="presentation" cellpadding="0" cellspacing="0" align="center" style="margin:0 auto;"><tr><td class="logo-c" align="center" style="text-align:center;padding:0;"><img class="logo-i" src="{IMG}/logo-workin-blanc-v2.png" width="150" alt="Workin Group" style="display:block;width:150px;height:auto;border:0;margin:0 auto;"></td></tr></table>
</div><div class="card-m" style="display:inline-block;vertical-align:middle;width:100%;max-width:280px;padding:0 0 4px;text-align:left;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100%;"><tr><td style="text-align:left;background:#38326f;border:1px solid #4d4789;border-radius:14px;padding:14px 14px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100%;margin:0 0 12px;"><tr>
<td valign="middle" width="58" style="width:58px;padding-right:10px;"><img src="{IMG}/loic-rond.png" width="58" height="58" alt="Loïc Spyckerelle" style="display:block;width:58px;height:58px;border:0;"></td>
<td valign="middle" style="text-align:left;"><p style="text-align:left;margin:0;{FONT}font-size:14px;font-weight:700;line-height:1.3;color:#ffffff;">Loïc Spyckerelle</p><p style="text-align:left;margin:2px 0 0;{FONT}font-size:11.5px;line-height:1.4;color:#d9d6f0;">Fondateur de Workin Group</p></td>
</tr></table><table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="width:100%;margin:0 0 0;"><tr>
<td valign="middle" width="58" style="width:58px;padding-right:10px;"><img src="{IMG}/eric-saie-rond.png" width="58" height="58" alt="Eric Saie" style="display:block;width:58px;height:58px;border:0;"></td>
<td valign="middle" style="text-align:left;"><p style="text-align:left;margin:0;{FONT}font-size:14px;font-weight:700;line-height:1.3;color:#ffffff;">Eric Saie</p><p style="text-align:left;margin:2px 0 0;{FONT}font-size:11.5px;line-height:1.4;color:#d9d6f0;">Consultant réglementé en immigration canadienne</p></td>
</tr></table>
</td></tr></table>
</div></div>
<div style="height:20px;line-height:20px;font-size:0;border-top:1px solid #443e7e;margin-top:14px;">&nbsp;</div>
<p style="text-align:left;margin:0 0 6px;{FONT}font-size:22px;line-height:1.25;font-weight:700;color:#ffffff;">L’infolettre immigration de vos embauches</p>
<p style="text-align:left;margin:0;{FONT}font-size:13.5px;line-height:1.5;color:#d9d6f0;">Le point du Pôle Immigration sur ce qui change pour vos travailleurs étrangers</p>

<div style="height:16px;line-height:16px;font-size:0;">&nbsp;</div>
<div style="font-size:0;line-height:0;text-align:left;"><div style="display:inline-block;vertical-align:top;margin:0 8px 8px 0;"><table role="presentation" width="116" cellpadding="0" cellspacing="0" style="width:116px;"><tr><td align="center" style="text-align:center;background:{ROSE};border-radius:20px;padding:7px 0;{FONT}font-size:10.5px;letter-spacing:1px;font-weight:700;line-height:1.3;color:#ffffff;white-space:nowrap;">NOVEMBRE 2026</td></tr></table></div><div style="display:inline-block;vertical-align:top;margin:0 8px 8px 0;"><table role="presentation" width="172" cellpadding="0" cellspacing="0" style="width:172px;"><tr><td align="center" style="text-align:center;border:1px solid #ffffff;border-radius:20px;padding:6px 0;{FONT}font-size:10.5px;letter-spacing:.3px;font-weight:600;line-height:1.3;color:#ffffff;white-space:nowrap;">CRIC R533143 · CIIQ 11929</td></tr></table></div></div>

</td></tr>
<tr><td style="text-align:left;height:6px;background:{ROSE};font-size:0;line-height:0;">&nbsp;</td></tr>

<!-- INTRO -->
<tr><td class="px" style="text-align:left;padding:30px 26px 0;">
{p('Bonjour,')}
{p('Ce mois-ci, Ottawa a changé une règle qui touche directement vos travailleurs à bas salaire : la durée maximale des nouvelles EIMT passe à deux ans. Voici ce que cela change pour vous, les nouveaux délais publiés, et une porte à ne pas manquer avant le 24 novembre pour vos futurs Jeunes professionnels.')}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 0;"><tr><td style="text-align:left;background:{LILAS};border-radius:10px;padding:18px 22px;">
<p style="text-align:left;margin:0 0 8px;{FONT}font-size:13px;font-weight:700;color:{NAVY};text-transform:uppercase;letter-spacing:1px;">Au sommaire</p>
<p style="text-align:left;margin:0;{FONT}font-size:14.5px;line-height:1.8;color:{TXT};">1. EIMT bas salaire : jusqu’à deux ans au lieu d’un<br>2. Traitement simplifié : la voie rapide pour vos postes spécialisés<br>3. Délais des EIMT : les chiffres d’octobre<br>4. Ce que ce changement veut dire pour vos équipes<br>5. Jeunes professionnels : une seconde porte s’ouvre le 17 novembre</p>
</td></tr></table></td></tr>

{section(1,'À la une','EIMT bas salaire : jusqu’à deux ans au lieu d’un',
 p('Emploi et Développement social Canada (EDSC) l’a annoncé le 6 novembre 2026 : <strong>les demandes d’EIMT présentées à cette date ou après auront une durée maximale de deux ans</strong>, au lieu d’un an jusqu’ici pour le volet des postes à bas salaire.')+
 ul(['<strong>Concrètement :</strong> un même dossier peut couvrir deux années d’emploi, ce qui espace d’autant les renouvellements.',
     'Seules les demandes présentées depuis le 6 novembre sont visées par le communiqué.',
     'Le même jour, le personnel de l’éducation à la petite enfance a été ajouté à la liste des exceptions au refus de traitement dans les régions où le chômage atteint 6 % ou plus.',
     '<strong>À suivre :</strong> d’autres changements sont annoncés pour le 1er mars 2027, sous condition de la participation des provinces, dont la possibilité, à leur demande, de porter à 15 % de l’effectif la part des travailleurs étrangers temporaires.'])+
 callout('Une EIMT bas salaire à déposer prochainement ? C’est le moment de revoir avec nous la durée du poste et du contrat.')+
 source('EDSC, communiqué « Le gouvernement du Canada annonce des réformes ciblées au Programme des travailleurs étrangers temporaires afin de répondre aux besoins du marché du travail », 06-11-2026, consulté le 14-11-2026.'))}

{section(2,'À connaître','Traitement simplifié : la voie rapide pour vos postes spécialisés',
 p('Pour une liste précise de métiers, vous pouvez déposer une EIMT <strong>sans fournir de preuve d’efforts de recrutement</strong> au moment du dépôt. C’est le traitement simplifié, une entente entre Ottawa et Québec.')+
 ul(['<strong>Exemples de métiers visés :</strong> bouchers, boulangers-pâtissiers, superviseurs des services alimentaires, mécaniciens, électriciens, charpentiers-menuisiers, infirmiers, ingénieurs — la liste officielle en compte 60, revue chaque année par le Québec (version en vigueur depuis le 24 février 2026, jusqu’au 23 février 2027).',
     '<strong>Attention, cuisiniers :</strong> ce métier a été retiré de la liste le 24 février 2026. Pour un poste de cuisinier, c’est la voie régulière, avec preuve de recrutement, qui s’applique.',
     '<strong>Durée :</strong> jusqu’à 3 ans pour un poste admissible à haut salaire. Pour un poste à bas salaire, la page officielle indique encore 1 an : nous vérifions chaque dossier avant de déposer.'])+
 callout('Un boucher, un boulanger-pâtissier, un mécanicien, un électricien à embaucher ? Écrivez-nous : nous vérifions si le poste est sur la liste du traitement simplifié.')+
 source('Québec, « Liste des professions admissibles au traitement simplifié », mise à jour le 24-02-2026 ; EDSC, « Traitement simplifié pour les demandes d’évaluation de l’impact sur le marché du travail pour les employeurs du Québec », page modifiée le 22-10-2026 ; consultées le 18-11-2026.'))}

{section(3,'Actualité','Délais des EIMT : les chiffres d’octobre',
 p('EDSC a mis à jour ses délais moyens de traitement. Pour octobre 2026 :')+
 f'<div style="font-size:0;line-height:0;margin:0 -5px 10px;">{stats}</div>'+
 callout('Les délais publiés pour septembre étaient de 82 et 98 jours ouvrables : ils ont légèrement augmenté. Une EIMT se prépare toujours plusieurs mois à l’avance.')+
 source('EDSC, « Labour Market Impact Assessment application processing times », page modifiée le 12-11-2026, consultée le 14-11-2026 ; chiffres de septembre : même page, version modifiée le 07-10-2026, consultée le 09-11-2026.'))}

{section(4,'Conseils pratiques','Ce que ce changement veut dire pour vos équipes',
 f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{ref}</table>'+
 source('EDSC, communiqué du 06-11-2026 ; EDSC, « Refusal to process a Labour Market Impact Assessment application », page modifiée le 27-10-2026 ; EDSC, « Program requirements for low-wage positions » ; EDSC, « Labour Market Impact Assessment application processing times », page modifiée le 12-11-2026 ; consultés le 14-11-2026.'))}

<!-- NOTRE SPÉCIALITÉ -->
<tr><td class="px" style="text-align:left;padding:32px 26px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="text-align:left;background:{NAVY};border-radius:14px;padding:26px 26px 24px;">
<p style="text-align:left;margin:0 0 6px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">Notre spécialité</p>
<p style="text-align:left;margin:0 0 14px;{FONT}font-size:20px;font-weight:700;line-height:1.3;color:#ffffff;">Jeunes professionnels : une seconde porte s’ouvre le 17 novembre</p>
<p style="text-align:left;margin:0 0 12px;{FONT}font-size:14.5px;line-height:1.6;color:#e3e1f3;">Les bassins de la saison 2026 sont fermés, et la date d’ouverture de la saison 2027 n’est pas encore publiée. En attendant, une autre voie existe : les organisations reconnues par IRCC.</p>
{''.join(f'<p style="text-align:left;margin:0 0 12px;{FONT}font-size:14.5px;line-height:1.6;color:#e3e1f3;"><strong style="color:#ffffff;">{a}</strong> {b}</p>' for a,b in [
 ('Deux participations de plus :','un participant d’Expérience internationale Canada qui passe par une organisation reconnue peut obtenir deux participations supplémentaires à vie.'),
 ('SWAP, organisation reconnue qui offre la catégorie Jeunes professionnels,','ouvre sa liste d’attente 2027 du mardi 17 novembre à midi au mardi 24 novembre à midi (heure de l’Est). Les sélections se font au hasard, début janvier.'),
 ('Conditions :','avoir de 18 à 35 ans, une offre d’emploi dans un poste de catégorie FEER 0 à 3, et ne pas avoir déjà reçu de lettre d’introduction pour la saison 2027.'),
 ('Workin vous accompagne à chaque étape :','inscription de vos candidats sur la liste, offre d’emploi au Portail des employeurs, montage complet du dossier.')])}
<div style="height:6px;line-height:6px;font-size:0;">&nbsp;</div>
{button('Un futur Jeune professionnel ? Écrivez-nous avant le 24 novembre','mailto:eric%40workin-group.com?subject=Jeune%20professionnel%20-%20liste%20d%27attente%202027')}
<p style="text-align:left;margin:16px 0 0;{FONT}font-size:11px;line-height:1.5;color:#b9b5dc;">Sources : IRCC, « International Experience Canada: Rounds of invitations », page modifiée le 09-11-2026 ; IRCC, « Recognized organizations », page modifiée le 18-12-2025 ; SWAP, « RO Work Canada Working Holiday + Young Professional » ; consultées le 14-11-2026.</p>
</td></tr></table></td></tr>

<!-- PAR SECTEUR -->
<tr><td class="px" style="text-align:left;padding:30px 26px 0;">
<p style="text-align:left;margin:0 0 12px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">Par secteur</p>
{secteur('Restauration et hôtellerie','Cuisiniers, aides-cuisiniers, employés de salle sous EIMT bas salaire : les prochaines demandes peuvent viser jusqu’à deux ans. Pour un établissement de la région de Montréal, le refus de traitement reste en place pour ces postes : écrivez-nous pour regarder les voies possibles.')}
{secteur('Services de garde éducatifs','Depuis le 6 novembre, le personnel de l’éducation à la petite enfance fait partie des exceptions au refus de traitement dans les régions où le chômage atteint 6 % ou plus, dont Montréal. Un poste d’éducatrice ou d’éducateur à pourvoir ? Parlons-en.')}
</td></tr>

<!-- POUR ALLER PLUS LOIN -->
<tr><td class="px" style="text-align:left;padding:20px 26px 0;">
<p style="text-align:left;margin:0 0 14px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">Pour aller plus loin · À lire ailleurs</p>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{lk}</table>
</td></tr>


<!-- SIGNATURE -->
<tr><td class="px" style="text-align:left;padding:14px 26px 30px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid #e3e0f2;"><tr><td style="text-align:left;padding-top:22px;">
{p('Une question sur l’un de vos dossiers ou sur un recrutement à venir ? Nous restons à votre disposition par courriel.')}
{p('Bonne journée,','margin-bottom:16px;')}
<table role="presentation" cellpadding="0" cellspacing="0"><tr>
<td valign="top" style="padding-right:14px;"><img src="{IMG}/eric-saie-rond-petit.png" width="56" height="56" alt="" style="display:block;width:56px;height:56px;border:0;"></td>
<td valign="top">
<p style="text-align:left;margin:0;{FONT}font-size:15px;font-weight:700;color:{NAVY};">Eric Saie</p>
<p style="text-align:left;margin:0;{FONT}font-size:13px;line-height:1.5;color:{TXT};">Responsable du Pôle Immigration — CRIC #R533143 · CIIQ #11929<br>
<a href="tel:+15149450070" style="color:{TXT};text-decoration:none;">+1 514 945-0070</a> · <a href="mailto:eric%40workin-group.com" style="color:{NAVY};">eric&#64;workin-group.com</a><br>
Montréal, Canada et Lille, France · <a href="https://workin-group.com/" style="color:{ROSE};font-weight:600;">workin-group.com</a></p>
</td></tr></table>

<p style="text-align:center;margin:26px 0 0;{FONT}font-size:18px;font-style:italic;font-weight:600;color:{ROSE};">Notre engagement, Votre succès</p>

</td></tr></table></td></tr>

<!-- MENTION -->
<tr><td class="px" style="text-align:left;background:{LILAS};padding:18px 26px;">
<p style="text-align:left;margin:0;{FONT}font-size:11.5px;line-height:1.55;color:{GRIS};">Cette infolettre fournit une information générale à jour au 18 novembre 2026. Elle ne constitue pas un avis sur votre situation particulière : chaque dossier s’examine au cas par cas.</p>
</td></tr>
</table>
</td></tr></table>
<!--/email_off-->
</body></html>'''
out=pathlib.Path(__file__).parent/'infolettre-2026-11.html'
out.write_text(body,encoding='utf-8'); print(out, len(body))
