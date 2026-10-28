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
 ('82 jours','ouvrables en moyenne pour une EIMT bas salaire'),('98 jours','ouvrables en moyenne pour une EIMT haut salaire'),('+ affichage','la période d’affichage préalable n’est pas comprise dans ces délais')])

reflexes=[
 ('Faites la liste des permis de votre équipe, avec leur date d’expiration.','C’est elle qui fixe tout le calendrier : chaque renouvellement se compte à rebours depuis cette date.'),
 ('Lancez l’EIMT le plus tôt possible.','IRCC demande à l’employeur de présenter sa nouvelle demande d’EIMT dès que possible, et EDSC accepte une EIMT bas salaire jusqu’à 6 mois avant la date prévue d’entrée en fonction.'),
 ('Au Québec, pensez au CAQ.','Pour un poste qui exige une EIMT, le renouvellement passe à la fois par une nouvelle EIMT auprès d’EDSC et par un certificat d’acceptation du Québec (CAQ) auprès du gouvernement du Québec.'),
 ('Le travailleur dépose sa prolongation avant l’expiration de son permis.','S’il le fait à temps et que ses conditions restent les mêmes, il conserve son statut et peut continuer à travailler aux mêmes conditions jusqu’à la décision.'),
 ('Changement d’employeur ou de conditions importantes ?','IRCC recommande alors de déposer la demande au moins 30 jours avant l’expiration du permis actuel.'),
 ('Poste dispensé d’EIMT, au Québec :','pas d’EIMT ni de CAQ, mais dans la plupart des cas une nouvelle offre d’emploi à présenter par l’employeur au Portail des employeurs.')]
ref=''.join(f'<tr><td valign="top" width="42" style="width:42px;padding:0 0 14px;"><img src="{IMG}/etape-{i}.png" width="28" height="28" alt="{i}" style="display:block;width:28px;height:28px;border:0;"></td><td style="text-align:left;padding:3px 0 14px;{FONT}font-size:15px;line-height:1.6;color:{TXT};"><strong style="color:{NAVY};">{a}</strong> {b}</td></tr>' for i,(a,b) in enumerate(reflexes,1))

links=[('Le Courrier Frontenac · 07-10-2026','Les délais d’EIMT mettent des entreprises et des emplois en péril','La lettre du député Luc Berthold et les cas d’entreprises de sa région.','https://courrierfrontenac.qc.ca/actualites/les-delais-deimt-mettent-des-entreprises-et-des-emplois-en-peril/'),
 ('CIC News · 13-10-2026','LMIA processing times trend downward (en anglais)','Le détail des délais moyens d’EIMT par volet, mois par mois.','https://cicnews.com/2026/10/lmia-processing-times-trend-downward-1081284.html'),
 ('IRCC · Page officielle','Expérience internationale Canada : rondes d’invitations','L’état des bassins, mis à jour par IRCC.','https://ircc.canada.ca/francais/travailler/eic/selection.asp'),
 ('EDSC · Page officielle','Refus de traiter une demande d’EIMT (en anglais)','La liste des régions visées et la date de sa prochaine mise à jour.','https://www.canada.ca/en/employment-social-development/services/foreign-workers/refusal.html')]
lk=''.join(f'<tr><td style="text-align:left;padding:0 0 16px;"><p style="text-align:left;margin:0 0 2px;{FONT}font-size:11px;letter-spacing:1px;text-transform:uppercase;color:{GRIS};font-weight:600;">{a}</p><a href="{u}" style="{FONT}font-size:15px;font-weight:700;color:{NAVY};text-decoration:underline;text-decoration-color:{ROSE};">{b}</a><p style="text-align:left;margin:2px 0 0;{FONT}font-size:13.5px;line-height:1.5;color:{TXT};">{c}</p></td></tr>' for a,b,c,u in links)

def secteur(t,body):
    return f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 14px;"><tr><td style="text-align:left;border:1px solid #e3e0f2;border-radius:10px;padding:18px 20px;"><p style="text-align:left;margin:0 0 6px;{FONT}font-size:16px;font-weight:700;color:{NAVY};">{t}</p><p style="text-align:left;margin:0;{FONT}font-size:14.5px;line-height:1.6;color:{TXT};">{body}</p></td></tr></table>'

body=f'''<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>L’infolettre immigration de vos embauches · Octobre 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{{margin:0;padding:0;background:#eeecf6;}} a{{color:{NAVY};}}
@media (max-width:620px){{ .wrap{{width:100%!important;}} .px{{padding-left:20px!important;padding-right:20px!important;}} .stack{{display:block!important;width:100%!important;}} .hide-m{{display:none!important;}} .center-m{{text-align:left!important;padding-top:14px!important;padding-left:0!important;border-left:0!important;}} }}
</style></head>
<body style="margin:0;padding:0;background:#eeecf6;">
<!--email_off-->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">Saison Jeunes professionnels fermée, délais d’EIMT, Montréal bloquée jusqu’en janvier, et six réflexes pour vos renouvellements.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#eeecf6;"><tr><td align="center" style="padding:16px 8px;">
<table role="presentation" class="wrap" width="100%" align="center" cellpadding="0" cellspacing="0" style="text-align:left;width:100%;max-width:600px;margin:0 auto;background:#ffffff;border-radius:14px;overflow:hidden;">

<!-- EN-TÊTE -->
<tr><td class="px" style="text-align:left;background:{NAVY};padding:24px 26px 18px;">
<div style="font-size:0;line-height:0;text-align:left;">
<div style="display:inline-block;vertical-align:middle;width:100%;max-width:256px;padding:0 0 18px;text-align:left;">
<table role="presentation" cellpadding="0" cellspacing="0" align="left" style="margin:0;"><tr><td align="left" style="text-align:left;padding:0;"><img src="{IMG}/logo-workin-group-blanc.png" width="150" alt="Workin Group" align="left" style="display:block;width:150px;height:auto;border:0;margin:0;float:none;"></td></tr></table>
</div><div style="display:inline-block;vertical-align:middle;width:100%;max-width:280px;padding:0 0 4px;text-align:left;">
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
<div style="font-size:0;line-height:0;text-align:left;"><div style="display:inline-block;vertical-align:top;margin:0 8px 8px 0;"><table role="presentation" width="104" cellpadding="0" cellspacing="0" style="width:104px;"><tr><td align="center" style="text-align:center;background:{ROSE};border-radius:20px;padding:7px 0;{FONT}font-size:10.5px;letter-spacing:1px;font-weight:700;line-height:1.3;color:#ffffff;white-space:nowrap;">OCTOBRE 2026</td></tr></table></div><div style="display:inline-block;vertical-align:top;margin:0 8px 8px 0;"><table role="presentation" width="172" cellpadding="0" cellspacing="0" style="width:172px;"><tr><td align="center" style="text-align:center;border:1px solid #ffffff;border-radius:20px;padding:6px 0;{FONT}font-size:10.5px;letter-spacing:.3px;font-weight:600;line-height:1.3;color:#ffffff;white-space:nowrap;">CRIC R533143 · CIIQ 11929</td></tr></table></div></div>

</td></tr>
<tr><td style="text-align:left;height:6px;background:{ROSE};font-size:0;line-height:0;">&nbsp;</td></tr>

<!-- INTRO -->
<tr><td class="px" style="text-align:left;padding:30px 26px 0;">
{p('Bonjour,')}
{p('Chaque mois, le Pôle Immigration de Workin vous résume l’actualité qui touche directement vos embauches de travailleurs étrangers, et ce qu’elle change concrètement pour vous. Ce mois-ci, trois nouvelles comptent, et quelques réflexes à prendre dès maintenant pour vos renouvellements.')}
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 0;"><tr><td style="text-align:left;background:{LILAS};border-radius:10px;padding:18px 22px;">
<p style="text-align:left;margin:0 0 8px;{FONT}font-size:13px;font-weight:700;color:{NAVY};text-transform:uppercase;letter-spacing:1px;">Au sommaire</p>
<p style="text-align:left;margin:0;{FONT}font-size:14.5px;line-height:1.8;color:{TXT};">1. Jeunes professionnels : la saison 2026 est fermée<br>2. Délais des EIMT : un député demande à Ottawa d’agir<br>3. EIMT bas salaire : Montréal bloquée jusqu’en janvier<br>4. Renouvellements : six réflexes pour ne pas être pris de court</p>
</td></tr></table></td></tr>

{section(1,'À la une','Jeunes professionnels : la saison 2026 est fermée',
 p('Immigration Canada (IRCC) l’annonce sur sa page des rondes d’invitations : <strong>les bassins de la saison 2026 d’Expérience internationale Canada sont fermés.</strong>')+
 ul(['<strong>Un candidat déjà invité</strong> peut toujours compléter et déposer sa demande de permis de travail.',
     '<strong>Un candidat non invité</strong> voit son profil retiré du bassin. Il pourra en créer un nouveau à la réouverture, pour la saison 2027.',
     '<strong>La date de réouverture n’est pas encore annoncée.</strong> Nous la surveillons et vous la communiquerons dès sa publication.'])+
 callout('Les invitations se font par rondes successives, jusqu’à épuisement des places ou fin de la saison. Un dossier prêt le jour de la réouverture permet de déposer le profil sans attendre : c’est maintenant qu’il se prépare.')+
 source('IRCC, « International Experience Canada: Rounds of invitations », page modifiée le 19-10-2026, consultée le 27-10-2026.'))}

{section(2,'Actualité','Délais des EIMT : un député demande à Ottawa d’agir',
 p('Le Courrier Frontenac rapporte, le 7 octobre, que le député fédéral Luc Berthold (Mégantic—L’Érable—Lotbinière) a écrit à la ministre fédérale responsable de l’Emploi pour lui demander de réduire les délais de traitement des études d’impact sur le marché du travail (EIMT), en faisant état d’entreprises de sa circonscription pénalisées par ces délais.')+
 p('Côté chiffres, Emploi et Développement social Canada (EDSC) publie ses délais moyens de traitement. Pour septembre 2026 :')+
 f'<div style="font-size:0;line-height:0;margin:0 -5px 10px;">{stats}</div>'+
 callout('En clair : une EIMT se compte en mois, pas en semaines. Les renouvellements se lancent tôt (voir nos six réflexes plus bas).')+
 source('Le Courrier Frontenac, « Les délais d’EIMT mettent des entreprises et des emplois en péril », 07-10-2026 ; EDSC, « Labour Market Impact Assessment application processing times », page modifiée le 07-10-2026, consultée le 27-10-2026.'))}

{section(3,'Réglementation','EIMT bas salaire : Montréal bloquée jusqu’en janvier',
 p('EDSC peut refuser de traiter une EIMT pour un poste à bas salaire lorsque le lieu de travail se trouve dans une région métropolitaine où le taux de chômage atteint 6 % ou plus. La liste en vigueur couvre les demandes déposées du 9 octobre 2026 au 7 janvier 2027.')+
 ul(['<strong>Au Québec, sont visées :</strong> Montréal (7,2 %) et Ottawa-Gatineau (7,9 %).',
     '<strong>Restent sous le seuil :</strong> Trois-Rivières (5,7 %), Québec (4,3 %), Sherbrooke (4,2 %), Drummondville (3,8 %) et Saguenay (3,7 %).',
     'Par ailleurs, EDSC indique que certaines demandes d’EIMT pour des postes à bas salaire ne sont pas traitées dans les régions économiques de Montréal et de Laval jusqu’au 31 décembre 2026.',
     'Certains secteurs et certains postes sont exemptés de la mesure. Prochaine mise à jour de la liste : 8 janvier 2027.'])+
 callout('Votre établissement est à Montréal ou à Laval ? Écrivez-nous : nous regardons avec vous les voies possibles pour votre poste.')+
 source('EDSC, « Refusal to process a Labour Market Impact Assessment application », page modifiée le 09-10-2026 ; EDSC, « Hiring temporary foreign workers in the province of Quebec », page modifiée le 24-07-2026 ; consultées le 27-10-2026.'))}

{section(4,'Conseils pratiques','Renouvellements : six réflexes pour ne pas être pris de court',
 f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0">{ref}</table>'+
 source('IRCC, « Extend a temporary worker’s permit », page modifiée le 14-10-2026 ; EDSC, « Hire a temporary foreign worker in a low-wage position », page modifiée le 07-10-2026 ; IRCC, Centre d’aide, « I work in Quebec. How can I extend my work permit? », page modifiée le 28-09-2026 ; consultées le 27-10-2026.'))}

<!-- NOTRE SPÉCIALITÉ -->
<tr><td class="px" style="text-align:left;padding:32px 26px 0;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td style="text-align:left;background:{NAVY};border-radius:14px;padding:26px 26px 24px;">
<p style="text-align:left;margin:0 0 6px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">Notre spécialité</p>
<p style="text-align:left;margin:0 0 14px;{FONT}font-size:20px;font-weight:700;line-height:1.3;color:#ffffff;">Pourquoi recruter un Jeune professionnel</p>
{''.join(f'<p style="text-align:left;margin:0 0 12px;{FONT}font-size:14.5px;line-height:1.6;color:#e3e1f3;"><strong style="color:#ffffff;">{a}</strong> {b}</p>' for a,b in [
 ('Aucune EIMT à obtenir :','les permis d’Expérience internationale Canada sont dispensés de l’étude d’impact sur le marché du travail (code de dispense C21). Pas d’EIMT, donc pas de délai d’EIMT.'),
 ('Un permis lié à votre entreprise :','le jeune professionnel obtient un permis de travail propre à l’employeur, pour acquérir de l’expérience dans son métier ou son domaine d’études.'),
 ('Workin s’occupe de tout :','recrutement en France, montage complet du dossier, offre d’emploi au Portail des employeurs et suivi jusqu’à l’arrivée.')])}
<p style="text-align:left;margin:4px 0 16px;{FONT}font-size:14.5px;line-height:1.6;color:#ffffff;">La saison 2026 est fermée, mais vos recrutements 2027 se préparent dès maintenant : nous montons chaque dossier pour qu’il soit déposé dès la réouverture des bassins.</p>
{button('Un poste à pourvoir en 2027 ? Écrivez-nous','mailto:eric%40workin-group.com?subject=Recrutement%202027%20-%20Jeune%20professionnel')}
<p style="text-align:left;margin:16px 0 0;{FONT}font-size:11px;line-height:1.5;color:#b9b5dc;">Source : IRCC, « International Experience Canada (IEC) – [R204(d) – C21] », page modifiée le 24-12-2025, consultée le 27-10-2026.</p>
</td></tr></table></td></tr>

<!-- PAR SECTEUR -->
<tr><td class="px" style="text-align:left;padding:30px 26px 0;">
<p style="text-align:left;margin:0 0 12px;{FONT}font-size:11px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:{ROSE};">Par secteur</p>
{secteur('Restauration et hôtellerie','La saison estivale 2027 se prépare maintenant. Un cuisinier ou un employé de salle recruté en France cet automne pourra déposer son profil dès la réouverture des bassins si son dossier est prêt. Et si vos équipes comptent des travailleurs sous EIMT, vérifiez dès aujourd’hui leurs dates d’expiration : dans la région de Montréal, certaines demandes d’EIMT pour des postes à bas salaire ne sont pas traitées jusqu’au 7 janvier 2027.')}
{secteur('Alimentation et commerce de détail','Gérants de rayon, bouchers, boulangers : ces postes se préparent bien à l’avance. Nos dossiers Jeunes professionnels avancent pendant la fermeture du bassin, pour être déposés dès la réouverture. Si vous prévoyez un remplacement ou un nouveau poste en 2027, c’est le moment d’en parler.')}
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
<p style="text-align:left;margin:0;{FONT}font-size:11.5px;line-height:1.55;color:{GRIS};">Cette infolettre fournit une information générale à jour au 27 octobre 2026. Elle ne constitue pas un avis sur votre situation particulière : chaque dossier s’examine au cas par cas.</p>
</td></tr>
</table>
</td></tr></table>
<!--/email_off-->
</body></html>'''
out=pathlib.Path(__file__).parent/'infolettre-2026-10.html'
out.write_text(body,encoding='utf-8'); print(out, len(body))
