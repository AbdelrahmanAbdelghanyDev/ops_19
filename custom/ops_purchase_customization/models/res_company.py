# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    ops_emirate = fields.Boolean(
        string='OPS Emirate',
        default=False,
        help='Enable OPS Emirate features for this company'
    )