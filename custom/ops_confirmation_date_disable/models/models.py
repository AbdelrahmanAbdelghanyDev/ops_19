# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def _prepare_confirmation_values(self):
        return {
            'state': 'sale',
            'date_order': self.date_order,
            # 'date_order': '2022-08-17 00:00:00'
        }
