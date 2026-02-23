# -*- coding: utf-8 -*-

from odoo import models, fields, api

class purchase(models.Model):
    _inherit = 'purchase.order'

    def button_confirm(self):
        res = super(purchase, self).button_confirm()
        for order in self:
            move = self.env['account.move']
            # move_data = {
            #     'date': order.date_order,
            #     'ref': order.name,
            #     'currency_id': order.currency_id.id,
            # }
            journal = self.env['account.journal'].search([('type', '=', 'general'),('company_id', '=', self.company_id.id),('name' , '=', 'Miscellaneous Operations')], limit=1)
            credit_account_id = self.env['account.account'].search([('name', 'ilike', 'Accrued Expenses Trade'),('user_type_id.name', '=', 'Current Liabilities'),('company_id', '=', self.company_id.id)], limit=1)
            debit_account_id = self.env['account.account'].search([('name', 'ilike', 'External FW'),('user_type_id.name', '=', 'Current Assets'),('company_id', '=', self.company_id.id)], limit=1)
            print('credit_account_id', credit_account_id)
            print('debit_account_id', debit_account_id)
            print("company", self.company_id.name)
            print('journal',  journal)
            move_data = {
                'date': order.date_order,
                'ref': order.name,
                'currency_id': order.currency_id.id,
                'journal_id': journal.id,
            }
            # if self.env.company.name == 'AWE Egypt':
            #     move_data['journal_id'] = 11
            # elif self.env.company.name == 'AWE KSA':
            #     move_data['journal_id'] = 19
            # elif self.env.company.name == 'AWE UAE':
            #     move_data['journal_id'] = 28
            move_id = move.create(move_data)

            # debit_account_id = 0
            # if self.env.company.name == 'AWE Egypt':
            #     debit_account_id = 3227
            # elif self.env.company.name == 'AWE KSA':
            #     debit_account_id = 5024
            # elif self.env.company.name == 'AWE UAE':
            #     debit_account_id = 6316
            #
            # credit_account_id = 0
            # if self.env.company.name == 'AWE Egypt':
            #     credit_account_id = 3292
            # elif self.env.company.name == 'AWE KSA':
            #     credit_account_id = 5084
            # elif self.env.company.name == 'AWE UAE':
            #     credit_account_id = 7948

            move_lines = []
            for line in order.order_line:
                move_lines.extend([
                    (0, 0, {'account_id': debit_account_id.id, 'partner_id': order.partner_id.id,
                            'name': order.name,
                            'analytic_account_id': line.account_analytic_id.id,
                            'debit': order.currency_id._convert(line.price_subtotal,
                                                                self.env.company.currency_id,
                                                                self.env.company, order.date_order),
                            'currency_id': order.currency_id.id,
                            'amount_currency': line.price_subtotal,
                            'credit': 0
                            }),
                    (0, 0, {'account_id': credit_account_id.id, 'partner_id': order.partner_id.id,
                            'name': order.name,
                            'currency_id': order.currency_id.id, 'debit': 0,
                            'analytic_account_id': line.account_analytic_id.id,
                            'amount_currency': -1 * line.price_subtotal,
                            'credit': order.currency_id._convert(line.price_subtotal,
                                                                 self.env.company.currency_id,
                                                                 self.env.company, order.date_order),
                            })])
            move_id.line_ids = move_lines
            order.state = 'purchase'
        return res
