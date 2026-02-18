# -*- coding: utf-8 -*-

from odoo import models, fields, api


class N4(models.Model):
    _name = 'a.n4'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "n4"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
