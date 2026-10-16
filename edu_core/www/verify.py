import frappe

from edu_core.certificates import lookup_certificate, normalize_code


def get_context(context):
    context.no_cache = 1
    context.code = ""
    context.searched = False
    context.certificate = None

    raw = str(frappe.form_dict.get("code") or "").strip()
    if not raw:
        return

    context.searched = True
    code = normalize_code(raw)
    if not code:
        return

    context.code = code
    context.certificate = lookup_certificate(code)
