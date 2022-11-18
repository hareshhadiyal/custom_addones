# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ClinicPatients(models.Model):
    _name = "patient.details"
    _rec_name = "patient_name"

    user_id = fields.Many2one('res.users', string="User Id")
    patient_number = fields.Char(default="New", readonly=True)
    patient_name = fields.Char(string="Patient Name", required=True)
    patient_address = fields.Char(string="Address 1")
    patient_dob = fields.Date(string='Date Of Birth')
    patient_age = fields.Integer(string='Age', compute="compute_age", readonly=True, store=True)
    total_opd = fields.Integer(compute="total_opd_count")
    patient_email = fields.Char(string="Patient Mail")

# -------------------------count total opd------------------------------
    @api.depends("patient_name")
    def total_opd_count(self):
        for rec in self:
            total_count = self.env['opd.details'].search_count([("patient_id", "=", rec.id)])
            rec.total_opd = total_count

# ----------------smart button tree view with specific condition using domain---------------------

    def total_count(self):
        return {
                   'name': "Opd Count",
                   'view_mode': 'tree,form',
                   'domain': [('patient_id', '=', self.id)],
                   'res_model': 'opd.details',
                   'type': 'ir.actions.act_window',
                   'target': 'current',
               }
# -------------------------for age count----------------------------------

    @api.depends('patient_dob')
    def compute_age(self):
        today_date = datetime.date.today()
        for rec in self:
            if rec.patient_dob:
                rec.patient_age = today_date.year - rec.patient_dob.year
                if rec.patient_age < 0:
                    rec.patient_age = 0
            else:
                rec.patient_age = 0

# ------------------------------------- for sequence ---------------------------------------- #

    @api.model
    def create(self, vals):
        vals['patient_number'] = self.env['ir.sequence'].next_by_code('patient.details')
        return super(ClinicPatients, self).create(vals)



    def create_patient(self):
        for rec in self:
            vals = {
                'name': rec.patient_name,
                'login': rec.patient_name,
                'in_group_13': True,
            }

            user_id = self.env['res.users'].create(vals)
            rec.user_id = user_id