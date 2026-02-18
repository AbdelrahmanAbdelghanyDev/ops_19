# -*- coding: utf-8 -*-

from odoo import models, fields, api


class N3(models.Model):
    _name = 'a.n3'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "n3"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
    other = fields.Boolean('Other', default=False)