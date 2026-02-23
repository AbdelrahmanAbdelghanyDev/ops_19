# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CostEstimationAccounting(models.Model):
    _inherit = 'cost.estimation'

    budget_date_from = fields.Date(string="Budget Date From", default=fields.Datetime.now(),track_visibility='onchange')
    budget_date_to = fields.Date(string="To", default=fields.Datetime.now(),track_visibility='onchange')
    budget = fields.Many2one('crossovered.budget',string='Budget',readonly='1')

class CostEstimationLineAccounting(models.Model):
    _inherit = 'cost.estimation.line'

    budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')

    @api.onchange('cost_item')
    def onchange_cost_item_budget(self):
        if self.cost_item.budgetary_position:
            self.budgetary_position = self.cost_item.budgetary_position.id

class ProductCostEstimation(models.Model):
    _inherit = "cost.estimation.products"

    budgetary_position = fields.Many2one('account.budget.post',related='product_id.budgetary_position', string='Budgetary Position')