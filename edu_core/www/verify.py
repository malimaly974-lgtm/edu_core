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


def get_context(context):
    context.no_cache = 1
    context.code = ""
    context.searched = False
    context.certificate = None

    raw = str(frappe.form_dict.get("code") or "").strip().upper()
    if not raw:
        return

    context.searched = True
    if not CODE_PATTERN.match(raw):
        return

    context.code = raw
    cert = frappe.db.get_value(
        "Certification",
        {"verification_code": raw},
        ["name", "student", "certification_type", "establishment",
         "issue_date", "expiry_date", "status"],
        as_dict=True,
    )
    if not cert:
        return

    state = "valid"
    if cert.status == "Revoked":
        state = "revoked"
    elif cert.status == "Expired" or (
        cert.expiry_date and getdate(cert.expiry_date) < getdate(nowdate())
    ):
        state = "expired"

    cert.label, cert.color = STATES[state]
    cert.holder_name = frappe.db.get_value("Student", cert.student, "student_name")
    cert.type_title = frappe.db.get_value("Certification Type", cert.certification_type, "title")
    cert.issuer_name = frappe.db.get_value("Establishment", cert.establishment, "establishment_name")
    context.certificate = cert
