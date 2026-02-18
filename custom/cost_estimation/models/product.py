# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCanBeCost(models.Model):
    _inherit = "product.template"

    cost_ok = fields.Boolean(string='Can be Cost Item')
    cost_estimation = fields.One2many('cost.estimation.products', 'idx')
    cost_item_type = fields.Selection([('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead')],
                                      string="CI Type")
    budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')


class ProductCostEstimation(models.Model):
    _name = "cost.estimation.products"

    product_id = fields.Many2one('product.template', string='Product')
    description = fields.Text('Description')
    qty = fields.Float('Quantity')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    cost_item_type = fields.Selection(related='product_id.cost_item_type', string="CI Type")
    idx = fields.Many2one('product.template')

    @api.onchange('product_id')
    def _onch_proj(self):
        self.uom = self.product_id.uom_id.id
