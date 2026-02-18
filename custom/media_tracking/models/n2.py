# -*- coding: utf-8 -*-

from odoo import models, fields, api


class N2(models.Model):
    _name = 'a.n2'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "n2"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
    other = fields.Boolean('Other',default=False)
    show_n3 = fields.Boolean('Show N3',default=False)
    report_n3 = fields.Boolean('Report N3',default=False)