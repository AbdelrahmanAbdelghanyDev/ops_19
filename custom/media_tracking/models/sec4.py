# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SEC4(models.Model):
    _name = 'a.sec4'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Sec4"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
    score = fields.Integer('Score')