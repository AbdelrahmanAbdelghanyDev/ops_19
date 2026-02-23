# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CostEstimationQuotation(models.Model):
    _inherit = 'sale.order'
    budget = fields.Many2one('crossovered.budget',string="Budget", readonly=True)

    def action_confirm(self):
        res = super(CostEstimationQuotation, self).action_confirm()
        if self.cost_estimation_ref:
            if not self.analytic_account_id:
                client_order_ref = self.client_order_ref
                customer_name = self.partner_id.name or ''

                analytic_account_name = self.name

                analytic_account = self.env['account.analytic.account'].create({
                    'name': analytic_account_name,
                    'code': client_order_ref or '',
                    'partner_id': self.partner_id.id,
                    'company_id': self.company_id.id,
                })
                self.analytic_account_id = analytic_account.id

            budget_line_list = []
            line_list = []
            for rec in self.cost_estimation_ref.cost_estimation_line:
                if rec.budgetary_position.id not in line_list and (rec.budgetary_position.id != False):
                    line_list.append(rec.budgetary_position.id)

            for item in line_list:
                total_budgetary_list = []
                for line in self.cost_estimation_ref.cost_estimation_line:
                    if item == line.budgetary_position.id:
                        total_budgetary_list.append(line.total_cost_item_cost)

                budget_line_list.append((0, 0, {'general_budget_id': item,
                                                'analytic_account_id': self.analytic_account_id.id,
                                                'date_from': self.cost_estimation_ref.budget_date_from,
                                                'date_to': self.cost_estimation_ref.budget_date_to,
                                                'planned_amount': sum(total_budgetary_list)}))
            if line_list != []:
                budget = self.env['crossovered.budget'].search([]).create(
                    {'name': "%s - %s" % (self.name, self.cost_estimation_ref.seq),
                     'date_from': self.cost_estimation_ref.budget_date_from,
                     'date_to': self.cost_estimation_ref.budget_date_to,
                     'user_id': self.user_id.id,
                     'cost_estimation_id': self.cost_estimation_ref.id,
                     'crossovered_budget_line': budget_line_list})
                self.budget = budget.id
                self.cost_estimation_ref.budget = self.budget
            else:
                pass
        return res
