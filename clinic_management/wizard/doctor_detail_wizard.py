# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ClinicDoctorsWizard(models.Model):
    _name = "doctor.wizard"

    doctor_name_id = fields.Many2one("doctor.details", string="Doctor Name", required=True)
    app_date = fields.Date(string='Date')
    doctor_department_id = fields.Many2one("doctor.department", string="Department")

    # -------------------Domain ------------------------------------

    # @api.onchange("doctor_department_id")
    # def onchange_department(self):
    #     for rec in self:
    #         return {'domain': {'doctor_name_id': [('depart_id.id', '=', rec.doctor_department_id.id)]}}

# -----------------create opd in threw patient form using wizard----------------------

    @api.onchange('patient_id')
    def create_opd_action(self):
        active_id = self._context.get('active_id')

        vals = {
            'patient_id': active_id,
            'doctor_id': self.doctor_name_id.id,
            'department_id': self.doctor_department_id.id,
            'app_date': self.app_date
        }
        new_opd_id = self.env['opd.details'].create(vals)

# ------------------open direct opd created form view----------------------

        action = {
            'name': "Opd 1 Count",
            'view_mode': 'form',
            'res_model': 'opd.details',
            'res_id': new_opd_id.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return action

# ------------------check all opd of selected doctor------------------

    def all_opd(self):
        action = self.env.ref('clinic_management.opd_details_action').read()[0]     # or other method is below
        # action = self.env['ir.actions.actions']._for_xml_id('clinic_manage.opd_details_action')
        action['domain'] = [('doctor_id', '=', self.doctor_name_id.id)]
        print('-------------------------------', action['domain'])
        return action
