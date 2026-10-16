import frappe
from frappe.rate_limiter import rate_limit

from edu_core.certificates import lookup_certificate

DEFAULT_PAGE = 20
MAX_PAGE = 100


def _to_int(value, default):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@frappe.whitelist(allow_guest=True, methods=["GET"])
@rate_limit(limit=20, seconds=60)
def verify_certificate(code=None):
    """Vérification publique. Réponse identique pour un code inconnu ou mal formé."""
    cert = lookup_certificate(code)
    if not cert:
        return {"found": False, "valid": False}
    return {
        "found": True,
        "valid": cert.state == "valid",
        "status": cert.state,
        "holder": cert.holder_name,
        "certification": cert.type_title,
        "issued_by": cert.issuer_name,
        "number": cert.name,
        "issue_date": str(cert.issue_date) if cert.issue_date else None,
        "expiry_date": str(cert.expiry_date) if cert.expiry_date else None,
    }


@frappe.whitelist(methods=["GET"])
def list_certifications(start=0, limit=DEFAULT_PAGE):
    """Certificats visibles par l'utilisateur connecté (permissions Frappe appliquées)."""
    start = max(_to_int(start, 0), 0)
    limit = min(max(_to_int(limit, DEFAULT_PAGE), 1), MAX_PAGE)
    return frappe.get_list(
        "Certification",
        fields=["name", "certification_type", "issue_date", "expiry_date", "status"],
        order_by="issue_date desc, name desc",
        limit_start=start,
        limit_page_length=limit,
    )


@frappe.whitelist(methods=["GET"])
def my_student_profile():
    """Fiche de l'étudiant lié au compte connecté. Ne retourne jamais celle d'un autre."""
    student = frappe.db.get_value(
        "Student",
        {"user": frappe.session.user},
        ["name", "student_name", "custom_campus"],
        as_dict=True,
    )
    if not student:
        return {"linked": False}
    return {
        "linked": True,
        "student": student.name,
        "full_name": student.student_name,
        "campus": student.custom_campus,
    }
