# EduAfrica : authentification des applications (Flutter, Next.js)

## Choix
OAuth 2.0, flux « code d'autorisation + PKCE », fourni par Frappe.
Aucun secret n'est stocké dans l'application cliente.
Les clés API (`token clé:secret`) restent réservées aux intégrations serveur à serveur.

## Points d'accès (base : `https://<site>/api/method/`)
| Rôle | Chemin |
|---|---|
| Autorisation (dans un navigateur) | `frappe.integrations.oauth2.authorize` |
| Échange code → jeton, et renouvellement | `frappe.integrations.oauth2.get_token` |
| Révocation | `frappe.integrations.oauth2.revoke_token` |
| Identité de l'utilisateur | `frappe.integrations.oauth2.openid_profile` |

## Déroulé
1. Le client génère un `code_verifier` aléatoire et son `code_challenge` (S256).
2. Il ouvre `authorize` avec : `client_id`, `response_type=code`, `scope=openid all`,
   `redirect_uri`, `state`, `code_challenge`, `code_challenge_method=S256`.
3. L'utilisateur se connecte et accepte. Frappe redirige vers `redirect_uri?code=…&state=…`.
4. Le client vérifie `state`, puis envoie en POST à `get_token` :
   `grant_type=authorization_code`, `code`, `client_id`, `redirect_uri`, `code_verifier`.
5. Il appelle l'API avec `Authorization: Bearer <access_token>`.
6. Renouvellement : POST `get_token` avec `grant_type=refresh_token`, `refresh_token`, `client_id`.
7. Déconnexion : POST `revoke_token` avec `token`.

## Règles
- HTTPS obligatoire hors développement. `OAUTHLIB_INSECURE_TRANSPORT` n'existe que dans `compose.dev.yaml`.
- Un « OAuth Client » par application (mobile, web), chacun avec sa propre `redirect_uri`.
- Mobile : jetons dans le stockage sécurisé du téléphone (Keychain / Keystore).
- Toute route de l'API vérifie les permissions de l'utilisateur du jeton (voir `docs/API.md`).
- Flux validé de bout en bout par un test automatisé en développement (étape 11).
