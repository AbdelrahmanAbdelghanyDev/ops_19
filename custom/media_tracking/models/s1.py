# -*- coding: utf-8 -*-

from odoo import models, fields, api


class S1(models.Model):
    _name = 'a.s1'
    _inherit = ['mail.thread']
    _rec_name = "name"
    _description = "S1"

    name = fields.Char(string="Name", required=True, copy=False,tracking=True)
    continue_questionnaire = fields.Boolean('Continue Questionnaire',default=False)