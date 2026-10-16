# EduAfrica : API REST

URL de base : `https://<site>/api/method/edu_core.api.<fonction>`

| Fonction | Accès | Verbe | Description |
|---|---|---|---|
| `verify_certificate?code=<code>` | Public | GET | Vérifie un certificat. Limité à 20 requêtes/min/IP (HTTP 429 au-delà). |
| `list_certifications?start=0&limit=20` | Connecté | GET | Certificats visibles par l'utilisateur (limit max 100). |
| `my_student_profile` | Connecté | GET | Fiche de l'étudiant lié au compte connecté. |

## Authentification
En-tête `Authorization: token <api_key>:<api_secret>`.
Les clés se génèrent sur la fiche de l'utilisateur (section API Access).

## Exemples
```bash
curl "https://<site>/api/method/edu_core.api.verify_certificate?code=0123456789ABCDEF"

curl -H "Authorization: token <api_key>:<api_secret>" \
  "https://<site>/api/method/edu_core.api.list_certifications?limit=10"
```

## Règles
- Un code inconnu et un code mal formé renvoient la même réponse (`found: false`).
- Toute nouvelle fonction exposée doit être justifiée, testée avec un jeton limité, et utiliser les permissions Frappe (`get_list`, `has_permission`).
