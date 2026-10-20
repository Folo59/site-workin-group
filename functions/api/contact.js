// Cloudflare Pages Function : reçoit le « Formulaire entreprises » et l'envoie par email
// depuis la messagerie Microsoft 365 de Workin Group (API Microsoft Graph), sans service tiers.
// Variables à définir dans Cloudflare Pages > Settings > Variables and Secrets :
//   MS_TENANT_ID      (ID de l'annuaire Microsoft Entra)
//   MS_CLIENT_ID      (ID de l'application « Site workin-group.com »)
//   MS_CLIENT_SECRET  (secret de cette application) — type Secret
// Facultatif :
//   CONTACT_MAILBOX   (boîte qui envoie et reçoit, par défaut loic@workin-group.com)

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

async function graphToken(env) {
  const r = await fetch(`https://login.microsoftonline.com/${env.MS_TENANT_ID}/oauth2/v2.0/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id: env.MS_CLIENT_ID,
      client_secret: env.MS_CLIENT_SECRET,
      scope: 'https://graph.microsoft.com/.default',
      grant_type: 'client_credentials',
    }),
  });
  if (!r.ok) throw new Error('token ' + r.status);
  return (await r.json()).access_token;
}

export async function onRequestPost({ request, env }) {
  const data = await request.formData();
  if (data.get('site_web')) return Response.json({ ok: true }); // robot : champ piège rempli
  const email = String(data.get('email') || '').trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || !data.get('consentement')) {
    return Response.json({ ok: false, error: 'invalid' }, { status: 400 });
  }
  if (!env.MS_TENANT_ID || !env.MS_CLIENT_ID || !env.MS_CLIENT_SECRET) {
    return Response.json({ ok: false, error: 'not_configured' }, { status: 503 });
  }

  const get = (k) => String(data.get(k) || '').slice(0, 5000).trim();
  const rows = Object.entries(LABELS)
    .filter(([k]) => get(k))
    .map(([k, label]) => `<tr><td style="padding:6px 12px 6px 0;color:#6b6890;vertical-align:top;white-space:nowrap">${label}</td><td style="padding:6px 0;color:#29245c">${esc(get(k)).replace(/\n/g, '<br>')}</td></tr>`)
    .join('');
  const subject = `Nouvelle demande entreprise : ${get('entreprise') || get('nom')}${get('poste') ? ' · ' + get('poste') : ''}`;
  const mailbox = env.CONTACT_MAILBOX || 'loic@workin-group.com';

  try {
    const token = await graphToken(env);
    const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(mailbox)}/sendMail`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: {
          subject: subject.slice(0, 180),
          body: {
            contentType: 'HTML',
            content: `<div style="font-family:Arial,sans-serif;font-size:14px"><p style="color:#ea346f;font-weight:bold">Demande reçue via le formulaire de workin-group.com</p><table>${rows}</table><p style="color:#6b6890;font-size:12px">Répondez directement à ce mail pour écrire au prospect.</p></div>`,
          },
          toRecipients: [{ emailAddress: { address: mailbox } }],
          replyTo: [{ emailAddress: { address: email, name: get('nom') || email } }],
        },
        saveToSentItems: false,
      }),
    });
    if (!r.ok) return Response.json({ ok: false, error: 'send_failed', status: r.status }, { status: 502 });
  } catch (e) {
    return Response.json({ ok: false, error: 'send_failed' }, { status: 502 });
  }
  return Response.json({ ok: true });
}
