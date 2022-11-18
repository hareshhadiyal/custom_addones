# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ClinicDoctors(models.Model):
    _name = "doctor.details"
    _rec_name = "doctor_name"

    user_id = fields.Many2one('res.users', string="User Id")
    doctor_number = fields.Char(default="New", readonly=True)
    doctor_name = fields.Char(string="Doctor Name", required=True)
    doctor_address = fields.Char(string="Address 1")
    doctor_dob = fields.Date(string='Date Of Birth')
    doctor_age = fields.Integer(string='Age', compute="compute_age", store=True, readonly=True)
    total_opd_visit = fields.Integer(compute="total_opd_visit_count")
    depart_id = fields.Many2one("doctor.department")

# ----------------------------------- count total opd ------------------------------------ #

    @api.depends("doctor_name")
    def total_opd_visit_count(self):
        for rec in self:
            total_opd_visit = self.env['opd.details'].search_count([("doctor_id", "=", rec.id)])
            rec.total_opd_visit = total_opd_visit

# ------------------------------ open tree view with specific condition --------------------------- #

    def total_count_visit(self):
        return {
            'name': "Opd Visit Count",
            'view_mode': 'tree,form',
            'domain': [('doctor_id', '=', self.id)],
            'res_model': 'opd.details',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }

# -------------------------count age------------------------------ #

    @api.depends('doctor_dob')
    def compute_age(self):
        today_date = datetime.date.today()
        for rec in self:
            if rec.doctor_dob:
                rec.doctor_age = today_date.year - rec.doctor_dob.year
                if rec.doctor_age < 0:
                    rec.doctor_age = 0
            else:
                rec.doctor_age = 0

    @api.model
    def create(self, vals):
        vals['doctor_number'] = self.env['ir.sequence'].next_by_code('doctor.details')
        return super(ClinicDoctors, self).create(vals)

    def create_doctor(self):
        for rec in self:
            vals = {
                'name': rec.doctor_name,
                'login': rec.doctor_name,
                'in_group_14': True,
            }

            user_id = self.env['res.users'].create(vals)
            rec.user_id = user_id
