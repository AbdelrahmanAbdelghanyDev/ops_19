# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TimeFrom(models.Model):
    _name = 'a.time_from'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Time From"

    name = fields.Char('Time From', required=True, tracking=True)
    seq = fields.Integer(string="Sequence", required=True)

    _sql_constraints = [
        ('seq_uniq', 'unique (seq)', 'Sequence Number must be unique !')
    ]

