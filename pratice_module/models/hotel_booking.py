# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelBooking(models.Model):
    _name = "booking.booking"

    customer_no = fields.Char(default='New')
    customer_name = fields.Char(string='Name')
    gender = fields.Selection([('a', 'Male'), ('b', 'Female')], string="Gender")
    room_no = fields.Text(string="Room No")
    room_type = fields.Selection([('a', 'A'), ('b', 'B'), ('c', 'C')], string='Room Type')
    mobile_num = fields.Integer(string="Mobile Num", required=True)
    email_id = fields.Text(string="Email Id")
    payment_line = fields.One2many('payment.payment', 'payment_id', string='payment_line')
    other_info = fields.Many2many('payment.payment', string='other info:-')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string="state", default='draft')

    def confirm(self):
        self.write({'state': 'done'})

    def cancel(self):
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        vals['customer_no'] = self.env['ir.sequence'].next_by_code('booking.booking')
        return super(HotelBooking, self).create(vals)


