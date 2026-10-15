import frappe

# Rôles "staff" : jamais restreints par ce filtre
STAFF_ROLES = {"System Manager", "Establishment Manager", "Academics User"}


def _is_student_only(user):
    roles = set(frappe.get_roles(user))
    return "Student" in roles and not (roles & STAFF_ROLES)


def certification_query(user=None):
    """Filtre SQL des listes : un étudiant ne voit que ses certificats."""
    user = user or frappe.session.user
    if not _is_student_only(user):
        return ""
    return (
        "`tabCertification`.`student` in "
        f"(select `name` from `tabStudent` where `user` = {frappe.db.escape(user)})"
    )


def certification_has_permission(doc, ptype=None, user=None, **kwargs):
    """Réponse explicite (True/False). Les droits par rôle restent contrôlés séparément par Frappe."""
    user = user or frappe.session.user
    if not _is_student_only(user):
        return True
    student = doc.get("student")
    if not student:
        return False
    return frappe.db.get_value("Student", student, "user") == user
