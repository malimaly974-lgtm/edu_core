import re

import frappe
from frappe.utils import getdate, nowdate

# Un code valide = exactement 16 caractères hexadécimaux (voir Certification.before_insert)
CODE_PATTERN = re.compile(r"^[0-9A-F]{16}$")

STATES = {
    "valid": ("Certificat valide", "green"),
    "expired": ("Certificat expiré", "#b00020"),
    "revoked": ("Certificat révoqué", "#b00020"),
}


def normalize_code(raw):
    """Retourne le code en majuscules s'il est bien formé, sinon None."""
    code = str(raw or "").strip().upper()
    return code if CODE_PATTERN.match(code) else None


def _value(doctype, name, fieldname):
    return frappe.db.get_value(doctype, name, fieldname) if name else None


def lookup_certificate(raw_code):
    """Source unique de la logique de vérification (page /verify et API).
    Retourne un frappe._dict, ou None si le code est mal formé ou inconnu."""
    code = normalize_code(raw_code)
    if not code:
        return None

    cert = frappe.db.get_value(
        "Certification",
        {"verification_code": code},
        ["name", "student", "certification_type", "establishment",
         "issue_date", "expiry_date", "status"],
        as_dict=True,
    )
    if not cert:
        return None

    state = "valid"
    if cert.status == "Revoked":
        state = "revoked"
    elif cert.status == "Expired" or (
        cert.expiry_date and getdate(cert.expiry_date) < getdate(nowdate())
    ):
        state = "expired"

    cert.state = state
    cert.label, cert.color = STATES[state]
    cert.holder_name = _value("Student", cert.student, "student_name")
    cert.type_title = _value("Certification Type", cert.certification_type, "title")
    cert.issuer_name = _value("Establishment", cert.establishment, "establishment_name")
    return cert
