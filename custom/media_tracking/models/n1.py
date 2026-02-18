# -*- coding: utf-8 -*-

from odoo import models, fields, api


class N1(models.Model):
    _name = 'a.n1'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "N1"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
