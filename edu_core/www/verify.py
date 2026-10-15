import frappe


def get_context(context):
    code = frappe.form_dict.get("code")
    context.code = code
    context.certificate = None

    if code:
        cert = frappe.db.get_value(
            "Certification",
            {"verification_code": code},
            ["name", "certificate_number", "student", "issue_date", "expiry_date", "status"],
            as_dict=True,
        )
        context.certificate = cert

    context.no_cache = 1
