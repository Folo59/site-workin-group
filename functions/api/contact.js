// Cloudflare Pages Function : reçoit le « Formulaire entreprises » et l'envoie par email.
// Envoi via Resend (resend.com). Variable secrète à définir dans Cloudflare Pages
// > Settings > Variables and Secrets :
//   RESEND_API_KEY   (clé API Resend)
// Variables facultatives :
//   CONTACT_TO       (destinataire, par défaut loic@workin-group.com)
//   CONTACT_FROM     (expéditeur, par défaut onboarding@resend.dev tant que le domaine n'est pas vérifié)
//   CONTACT_COPY     (copie lue chaque matin pour créer la fiche dans Marvin, par défaut spyckerelleloic@gmail.com ;
//                     ne part qu'une fois le domaine workin-group.com vérifié dans Resend)

const LABELS = {
  entreprise: 'Entreprise',
  nom: 'Nom et prénom',
  fonction: 'Fonction',
  ville: "Ville de l'entreprise",
  email: 'Courriel',
  telephone: 'Téléphone',
  poste: 'Poste à pourvoir',
  nombre_postes: 'Nombre de postes',
  entree_en_poste: 'Entrée en poste souhaitée',
  service: 'Service envisagé',
  besoin: 'Besoin',
};

const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export async function onRequestPost({ request, env }) {
  const data = await request.formData();
  if (data.get('site_web')) return Response.json({ ok: true }); // robot : champ piège rempli
  const email = String(data.get('email') || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !data.get('consentement')) {
    return Response.json({ ok: false, error: 'invalid' }, { status: 400 });
  }
  if (!env.RESEND_API_KEY) {
    return Response.json({ ok: false, error: 'not_configured' }, { status: 503 });
  }

  const get = (k) => String(data.get(k) || '').slice(0, 5000).trim();
  const rows = Object.entries(LABELS)
    .filter(([k]) => get(k))
    .map(([k, label]) => `<tr><td style="padding:6px 12px 6px 0;color:#6b6890;vertical-align:top;white-space:nowrap">${label}</td><td style="padding:6px 0;color:#29245c">${esc(get(k)).replace(/\n/g, '<br>')}</td></tr>`)
    .join('');
  const text = Object.entries(LABELS).filter(([k]) => get(k)).map(([k, l]) => `${l} : ${get(k)}`).join('\n');
  const subject = `Nouvelle demande entreprise : ${get('entreprise') || get('nom')}${get('poste') ? ' · ' + get('poste') : ''}`;

  const send = (to) => fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: `Site Workin Group <${env.CONTACT_FROM || 'onboarding@resend.dev'}>`,
      to: [to],
      reply_to: email,
      subject: subject.slice(0, 180),
      html: `<div style="font-family:Arial,sans-serif;font-size:14px"><p style="color:#ea346f;font-weight:bold">Demande reçue via le formulaire de workin-group.com</p><table>${rows}</table><p style="color:#6b6890;font-size:12px">Répondez directement à ce mail pour écrire au prospect.</p></div>`,
      text: 'Demande reçue via le formulaire de workin-group.com\n\n' + text,
    }),
  });
  const r = await send(env.CONTACT_TO || 'loic@workin-group.com');
  // copie pour l'automatisme Marvin : sans effet tant que le domaine n'est pas vérifié
  try { await send(env.CONTACT_COPY || 'spyckerelleloic@gmail.com'); } catch (e) {}
  if (!r.ok) return Response.json({ ok: false, error: 'send_failed', status: r.status }, { status: 502 });
  return Response.json({ ok: true });
}
