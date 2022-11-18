from odoo import models, fields, _
from odoo.exceptions import ValidationError

class otherdetails(models.TransientModel):
    _name = "other.details"

    parent_name = fields.Char(string="Parent Name")
    parent_age = fields.Char(string="Parent Age")
    parent_mo = fields.Char(string="Parent Mo")
    parent_gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Parent Gender")



    def btn_submit(self):
        for rec in self:
            if not rec.parent_name:
                raise ValidationError(_("Please enter the details"))


    def btn_cancel(self):
        return