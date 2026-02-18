# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TimeTo(models.Model):
    _name = 'a.time_to'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Time To"

    name = fields.Char('Time to',required=True,tracking=True)