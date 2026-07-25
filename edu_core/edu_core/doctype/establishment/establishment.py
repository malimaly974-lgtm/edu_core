# Copyright (c) 2026, malyma and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Establishment(Document):
    def before_insert(self):
        if frappe.db.count("Establishment") > 0:
            frappe.throw("Un seul Establishment est autorisé par site.")	
