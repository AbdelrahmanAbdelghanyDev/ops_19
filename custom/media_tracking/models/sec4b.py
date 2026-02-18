# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SEC4B(models.Model):
    _name = 'a.sec4b'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Sec4b"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
    score = fields.Integer('Score')