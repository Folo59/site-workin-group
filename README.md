# workin-group.com

Site vitrine de Workin Group, en HTML statique (sans WordPress ni Elementor).
Hébergé sur Cloudflare Pages : chaque modification poussée sur la branche `main` est mise en ligne automatiquement.

- Pages : un dossier par adresse (`/contact/` → `contact/index.html`)
- Styles et scripts communs : `assets/`
- Images et PDF : `wp-content/uploads/` (mêmes adresses que l'ancien WordPress, pour ne rien perdre en référencement)
- Formulaire de contact : `functions/api/contact.js` (envoi par email à loic@workin-group.com via Resend)
- Redirections des anciennes adresses : `_redirects`
- Flux RSS des actualités (pour Zapier) : `feed.xml`
