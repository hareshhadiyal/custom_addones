# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ClinicOPD(models.Model):
    _name = "opd.details"

    opd_id = fields.Char(default="New", readonly=True)
    patient_number = fields.Char(default="New")
    patient_id = fields.Many2one("patient.details", string="Patient Name")
    patient_address = fields.Char(string="Address 1")
    patient_dob = fields.Date(string='Date Of Birth')
    patient_age = fields.Integer(string='Age', compute="compute_age", store=True, readonly=True)
    department_id = fields.Many2one("doctor.department", string="Department")
    app_date = fields.Date(string="Date")
    doctor_id = fields.Many2one("doctor.details", string="Doctor"
                                , domain="[('depart_id', '=', department_id)]")  # Domain in field
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                              string="Status", readonly=True, index=True, default='draft', required=True)
    medicine = fields.Many2many("opd.medicine", string="Medicine")
    total = fields.Float(string="Total", compute="compute_total")
    untaxed_amount = fields.Integer(string='Untaxed Amount', compute='compute_total')
    taxes_amount = fields.Float(string='Taxes Amount', compute='compute_total')

    # ------------------------------ Compute Age ---------------------------------

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

    # ----------------------------Domain using function--------------------------

    # @api.onchange("department_id")
    # def onchange_department(self):
    #     for rec in self:
    #         return {'domain': {'doctor_id': [('depart_id.id', '=', rec.department_id.id)]}}

    # -------------------------access value of patient object---------------------------

    @api.onchange("patient_id")
    def _onchange_patient_name(self):
        for rec in self:
            rec.patient_address = self.patient_id.patient_address
            rec.patient_number = self.patient_id.patient_number
            rec.patient_dob = self.patient_id.patient_dob
            rec.patient_age = self.patient_id.patient_age

    # ----------------------------------- compute Method ----------------------------------

    @api.depends('medicine')
    def compute_total(self):
        for rec in self:
            untaxed_amount = taxes_amount = 0
            total = 0
            for line in rec.medicine:
                if line.medicine_name:
                    untaxed_amount += line.amount
                    taxes_amount += line.tax_price
            rec.update({
                'untaxed_amount': untaxed_amount,
                'taxes_amount': taxes_amount,
                'total': untaxed_amount + taxes_amount
            })

    # -------------------------------statusbar button condition----------------------------------

    @api.model
    def create(self, vals):
        vals['opd_id'] = self.env['ir.sequence'].next_by_code('opd.details')
        return super(ClinicOPD, self).create(vals)

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        return True

    def action_cancel(self):
        self.write({'state': 'cancel'})
        return True

    def action_done(self):
        vals = self.write({'state': 'done'})
        return True

    def action_reset(self):
        self.write({'state': 'draft'})
        return True

    def action_email(self):
        email_template = self.env.ref("clinic_management.opd_template_email").id
        template = self.env["mail.template"].browse(email_template)
        template.send_mail(self.id, force_send=True)


class ClinicOPDMedicine(models.Model):
    _name = "opd.medicine"

    medicine_name = fields.Char(string="Medicine")
    medicine_use = fields.Char(string="How to Use")
    quantity = fields.Integer(string="Quantity")
    price = fields.Float(string="Price")
    amount = fields.Float(string="Amount",  compute="compute_quantity")
    tax_id = fields.Many2many('account.tax', string='Taxes', context={'active_test': False})
    tax_price = fields.Float(string="Tax Price", compute="compute_tax_price")

    @api.depends('tax_id', 'price', 'quantity')
    def compute_tax_price(self):
        for rec in self:
            total_amt = 0
            if rec.tax_id:
                for line in rec.tax_id:
                    total_amt = total_amt + ((rec.amount*line.amount)/100)
            rec.tax_price = total_amt

    @api.depends('quantity', 'price')
    def compute_quantity(self):
        for rec in self:
            rec.amount = rec.price * rec.quantity
