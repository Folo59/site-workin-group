// Cloudflare Pages Function : reçoit le formulaire « Formulaire entreprises »
// et l'envoie dans HubSpot (API Forms, sans clé secrète).
// Variables à définir dans Cloudflare Pages > Settings > Environment variables :
//   HUBSPOT_PORTAL_ID  (ID du compte HubSpot)
//   HUBSPOT_FORM_GUID  (ID du formulaire HubSpot qui reçoit les demandes)

const FIELDS = {
  entreprise: 'company',
  nom: 'firstname',
  fonction: 'jobtitle',
  ville: 'city',
  email: 'email',
  telephone: 'phone',
  poste: 'poste_a_pourvoir',
  nombre_postes: 'nombre_de_postes',
  entree_en_poste: 'entree_en_poste_souhaitee',
  service: 'service_envisage',
  besoin: 'message',
};

export async function onRequestPost({ request, env }) {
  const data = await request.formData();
  if (data.get('site_web')) return Response.json({ ok: true }); // robot (champ piège rempli)
  if (!data.get('email') || !data.get('consentement')) {
    return Response.json({ ok: false, error: 'missing' }, { status: 400 });
  }
  if (!env.HUBSPOT_PORTAL_ID || !env.HUBSPOT_FORM_GUID) {
    return Response.json({ ok: false, error: 'not_configured' }, { status: 503 });
  }
  const fields = Object.entries(FIELDS)
    .filter(([k]) => data.get(k))
    .map(([k, name]) => ({ objectTypeId: '0-1', name, value: String(data.get(k)).slice(0, 5000) }));
  const body = {
    fields,
    context: {
      pageUri: request.headers.get('referer') || 'https://workin-group.com/contact/',
      pageName: 'Contact entreprises',
      ipAddress: request.headers.get('cf-connecting-ip') || undefined,
    },
    legalConsentOptions: {
      consent: { consentToProcess: true, text: "J'accepte que Workin Group utilise ces informations pour traiter ma demande." },
    },
  };
  const url = `https://api.hsforms.com/submissions/v3/integration/submit/${env.HUBSPOT_PORTAL_ID}/${env.HUBSPOT_FORM_GUID}`;
  const r = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  if (!r.ok) return Response.json({ ok: false, error: 'hubspot', status: r.status }, { status: 502 });
  return Response.json({ ok: true });
}
