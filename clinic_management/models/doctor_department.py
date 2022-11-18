# -*- coding: utf-8 -*-

from odoo import api, fields, models
import datetime


class ClinicDoctorsDepartment(models.Model):
    _name = "doctor.department"
    _rec_name = "doctor_department"

    doctor_department = fields.Char(string="Department")
    doctor_ids = fields.One2many("doctor.details", 'depart_id', string="Doctors")
