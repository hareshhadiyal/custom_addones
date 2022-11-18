from odoo import models, fields, api


class HotelPayment(models.Model):
    _name = "payment.payment"

    customer_id = fields.Text(string="ID")
    payment = fields.Selection([('A', 'Cash'), ('B', 'UPI'), ('C', 'Card')], string='payment')
    acc_details = fields.Text(string="Acc Details")
    payment_id = fields.Many2one('booking.booking',string='paymentid')