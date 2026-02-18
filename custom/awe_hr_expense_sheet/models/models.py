# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class Partner(models.Model):
    _inherit = 'res.partner'

    is_employee = fields.Boolean(string="Employee")



# class HrExpenseSheet(models.Model):
#     _inherit = 'hr.expense.sheet'
#
#     # has_product_in_expense_lines = fields.Boolean(
#     #     string="Has Product in Expense Lines", compute='_compute_has_product_in_expense_lines'
#     # )
#     #
#     # @api.depends('expense_line_ids.product_id')
#     # def _compute_has_product_in_expense_lines(self):
#     #     for sheet in self:
#     #         sheet.has_product_in_expense_lines = any(line.product_id for line in sheet.expense_line_ids)
#     #
#     # @api.onchange('expense_line_ids.product_id')
#     # def _onchange_expense_line_product_id(self):
#     #     for record in self:
#     #         # If the expense line has a product selected
#     #         if record.expense_line_ids:
#     #             for line in record.expense_line_ids:
#     #                 if line.product_id:
#     #                     product_account = line.product_id.product_tmpl_id.product_account_id
#     #
#     #                     journal = self.env['account.journal'].search(
#     #                         [('default_account_id', '=', product_account.id), ('type', '=', 'bank')], limit=1)
#     #
#     #                     if journal:
#     #                         record.bank_journal_id = journal.id
#     #                     else:
#     #                         record.bank_journal_id = False
#     # bank_journal_id = fields.Many2one('account.journal', string='Bank Journal')
#
#
#     partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", required=True,
#                                  domain=[('is_employee', '=', True)])
#     manager_partner_id = fields.Many2one(comodel_name="res.partner", string="Manager",
#                                  domain=[('is_employee', '=', True)])
#
#     employee_id = fields.Many2one('hr.employee', string="Employee", required=False)
#
#     attachments_ids = fields.Many2many('ir.attachment')
#
#     # payment_mode = fields.Selection([
#     #     ("own_accounts", "Employee (to reimburses)"),
#     #     ("company_accounts", "Company")
#     # ],
#     #     states={'done': [('readonly', True)], 'approved': [('readonly', True)], 'reported': [('readonly', True)]},
#     #     string="Paid By")
#     payment_mode = fields.Selection(related='expense_line_ids.payment_mode', default='company_accounts', readonly=True, string="Paid By", tracking=True)
#
#
#     def _default_bank_journal_id(self):
#         return self.env['account.journal'].search(
#             [('name', '=', 'Expenses'), ('company_id', '=', self.env.company.id)], limit=1
#         ).id
#
#     bank_journal_id = fields.Many2one(
#         'account.journal',
#         string='Bank Journal',
#         states={'done': [('readonly', True)], 'post': [('readonly', True)]},
#         check_company=True,
#         domain="[('type', 'in', ['cash', 'bank', 'purchase']), ('company_id', '=', company_id)]",
#         default=_default_bank_journal_id,
#         help="The payment method used when the expense is paid by the company.",
#         readonly=True
#     )
#
#     def action_view_journal_entries(self):
#         self.ensure_one()
#         return {
#             'name': 'Journal Entries',
#             'type': 'ir.actions.act_window',
#             'res_model': 'account.move',
#             'view_mode': 'tree,form',
#             'domain': [('id', 'in', self.account_move_id.ids)],  # Use account_move_id.ids for One2many
#             'context': {'create': False},
#         }
#
#     def action_sheet_move_create(self):
#         res = super().action_sheet_move_create()
#         for move in res.values():
#             move.attachments_ids = self.attachments_ids.ids
#         return res

class HrExpense(models.Model):
    _inherit = 'hr.expense'

    payment_mode = fields.Selection([
        ("own_account", "Employee (to reimburse)"),
        ("company_account", "Company")
    ], default='company_account', tracking=True,
        states={'done': [('readonly', True)], 'approved': [('readonly', True)], 'reported': [('readonly', True)]},
        string="Paid By")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    employee_id = fields.Many2one('hr.employee', string="Employee", required=False)


    def _get_account_move_line_values(self):
        move_line_values_by_expense = {}
        for expense in self:
            move_line_name = expense.partner_id.name + ': ' + expense.name.split('\n')[0][:64]
            account_src = expense._get_expense_account_source()
            account_dst = expense._get_expense_account_destination()
            account_date = expense.date or expense.sheet_id.accounting_date or fields.Date.context_today(expense)

            company_currency = expense.company_id.currency_id

            move_line_values = []
            unit_amount = expense.unit_amount or expense.total_amount
            quantity = expense.quantity if expense.unit_amount else 1
            taxes = expense.tax_ids.with_context(round=True).compute_all(unit_amount, expense.currency_id,quantity,expense.product_id)
            total_amount = 0.0
            total_amount_currency = 0.0
            partner_id = expense.partner_id.id

            # source move line
            balance = expense.currency_id._convert(taxes['total_excluded'], company_currency, expense.company_id, account_date)
            amount_currency = taxes['total_excluded']
            move_line_src = {
                'name': move_line_name,
                'quantity': expense.quantity or 1,
                'debit': balance if balance > 0 else 0,
                'credit': -balance if balance < 0 else 0,
                'amount_currency': amount_currency,
                'account_id': account_src.id,
                'product_id': expense.product_id.id,
                'product_uom_id': expense.product_uom_id.id,
                'analytic_account_id': expense.analytic_account_id.id,
                'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)],
                'expense_id': expense.id,
                'partner_id': partner_id,
                'tax_ids': [(6, 0, expense.tax_ids.ids)],
                'tax_tag_ids': [(6, 0, taxes['base_tags'])],
                'currency_id': expense.currency_id.id,
            }
            move_line_values.append(move_line_src)
            total_amount -= balance
            total_amount_currency -= move_line_src['amount_currency']

            # taxes move lines
            for tax in taxes['taxes']:
                balance = expense.currency_id._convert(tax['amount'], company_currency, expense.company_id, account_date)
                amount_currency = tax['amount']

                if tax['tax_repartition_line_id']:
                    rep_ln = self.env['account.tax.repartition.line'].browse(tax['tax_repartition_line_id'])
                    base_amount = self.env['account.move']._get_base_amount_to_display(tax['base'], rep_ln)
                    base_amount = expense.currency_id._convert(base_amount, company_currency, expense.company_id, account_date)
                else:
                    base_amount = None

                move_line_tax_values = {
                    'name': tax['name'],
                    'quantity': 1,
                    'debit': balance if balance > 0 else 0,
                    'credit': -balance if balance < 0 else 0,
                    'amount_currency': amount_currency,
                    'account_id': tax['account_id'] or move_line_src['account_id'],
                    'tax_repartition_line_id': tax['tax_repartition_line_id'],
                    'tax_tag_ids': tax['tag_ids'],
                    'tax_base_amount': base_amount,
                    'expense_id': expense.id,
                    'partner_id': partner_id,
                    'currency_id': expense.currency_id.id,
                    'analytic_account_id': expense.analytic_account_id.id if tax['analytic'] else False,
                    'analytic_tag_ids': [(6, 0, expense.analytic_tag_ids.ids)] if tax['analytic'] else False,
                }
                total_amount -= balance
                total_amount_currency -= move_line_tax_values['amount_currency']
                move_line_values.append(move_line_tax_values)

            # destination move line
            move_line_dst = {
                'name': move_line_name,
                'debit': total_amount > 0 and total_amount,
                'credit': total_amount < 0 and -total_amount,
                'account_id': account_dst,
                'date_maturity': account_date,
                'amount_currency': total_amount_currency,
                'currency_id': expense.currency_id.id,
                'expense_id': expense.id,
                'partner_id': partner_id,
                'exclude_from_invoice_tab': True,
            }
            move_line_values.append(move_line_dst)

            move_line_values_by_expense[expense.id] = move_line_values
        return move_line_values_by_expense

    def action_move_create(self):
        '''
        main function that is called when trying to create the accounting entries related to an expense
        '''
        move_group_by_sheet = self._get_account_move_by_sheet()

        move_line_values_by_expense = self._get_account_move_line_values()

        for expense in self:
            # get the account move of the related sheet
            move = move_group_by_sheet[expense.sheet_id.id]

            # get move line values
            move_line_values = move_line_values_by_expense.get(expense.id)

            # link move lines to move, and move to expense sheet
            move.write({'line_ids': [(0, 0, line) for line in move_line_values]})
            expense.sheet_id.write({'account_move_id': move.id})

        # post the moves
        # for move in move_group_by_sheet.values():
        #     move._post()

        return move_group_by_sheet


