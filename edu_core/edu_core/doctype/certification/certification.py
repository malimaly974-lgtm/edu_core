import frappe
import secrets
from frappe.model.document import Document
from frappe.utils import add_months, getdate


class Certification(Document):
    def before_insert(self):
        if not self.verification_code:
            self.verification_code = secrets.token_hex(8).upper()
        self.certificate_number = self.name

    def validate(self):
        if self.certification_type:
            validity = frappe.db.get_value(
                "Certification Type", self.certification_type, "validity_months"
            )
            if validity and self.issue_date:
                self.expiry_date = add_months(getdate(self.issue_date), validity)
