# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
from datetime import datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class HiddenField(models.Model):
    _inherit = 'account.move'

    cor = fields.Char(hidden_field=True)  # cost or revenue


class CustomProjectTask(models.Model):
    _inherit = 'project.task'

    is_cost_button_clicked = fields.Boolean(hidden_field=True, default=False)
    # is_revenue_button_clicked = fields.Boolean(hidden_field=True, default=False)
    revenue = fields.Float(string='Sales Value', readonly=True)
    original_currency_id = fields.Many2one('res.currency', readonly=True)
    converted_revenue = fields.Float(string='Sales(Base Currency)', readonly=False, store=True)
    tag_id = fields.Many2one('crm.tag', 'Tag')
    order_date = fields.Datetime(string="Order Date", readonly=False)
    cost_date = fields.Date(string="Cost Date")

    # @api.multi
    def post_journals(self):
        if self.is_cost_button_clicked:
            return

        if not self.cost_date:
            message = 'Can\'t Create Journal Entry!\n' + 'Please insert Cost Date.'
            raise exceptions.ValidationError(message)
            return

        project_cost_accounts = self.env['cost.accounts']
        journal_entry_item = self.env['account.move.line']
        journal_entry = self.env['account.move']

        # journal_entry_item_found indicates if an item with an original account
        # and project analytic_account_id is found or not
        # journal_entry_item_project is the variable holding reference to the list of found journal_entry_items
        # with one of the original accounts and project_analytic_account_id
        # journal_entry_id holds reference to the newly created journal_entry to hold the items

        # in order for this function to work there should be a journal entry with lines that include
        # 1)the analytic account of the project
        # and 2)the account the same as one of the original accounts in the Cost/Wip Accounts

        # 1st it searches for journal with the name Project Closure and the same company as the currently selected company
        # then it searches for entry items with one of the original accounts and project analytic account
        # if any of the items was already created from the button

        journal_entry_item_found = False
        original_accounts = project_cost_accounts.search([])

        journal_entry_id = self.env['account.move']
        journal_entry_item1 = self.env['account.move.line']
        journal_entry_item2 = self.env['account.move.line']

        if not original_accounts:
            message = 'Can\'t Create Journal Entry!\n' + 'Please Create Cost / WIP accounts.'
            raise exceptions.ValidationError(message)
            return
        current_company_id = self.env.user.company_id.id
        journal = self.env['account.journal'].search(
            [('name', '=', 'Project Closure'), ('company_id', '=', current_company_id)])

        for o_account in original_accounts:
            journal_entry_item_project = journal_entry_item.search(
                [('account_id', '=', o_account.original_acc_id.id),  # original_accounts[i].original_acc_id.id),
                 ('analytic_account_id', '=', self.project_id.analytic_account_id.id),
                 ('move_id.date', '<=', self.cost_date),
                 ('move_id.state', '=', 'posted')])
            # print("journal_entry_item_project : ",journal_entry_item_project)
            # ('date_maturity','>=', self.date_deadline), ('date_maturity','<=', self.cost_date)
            for item_project in journal_entry_item_project:
                if item_project.move_id.cor == '(cost)' or item_project.move_id.cor == '(revenue)':
                    continue
                if journal_entry_item_found is False:
                    journal_entry_item_found = True
                    journal_entry_id = journal_entry.create({
                        'date': self.cost_date,  # fields.Date.today(),
                        'journal_id': journal.id,  # journal_entry_item_project[j].journal_id.id,#3
                        'ref': self.project_id.name,
                        'name': self.env['ir.sequence'].search(
                            [('name', '=', 'Project Closure'), ('company_id', '=', current_company_id)]).next_by_id(),
                        # 'name': 'Project Completion ' + self.project_id.analytic_account_id.display_name,
                        'cor': '(cost)',
                    })
                # if the account was credit make it debit and vice versa
                if item_project.debit != 0:
                    item1 = 'credit'
                    item2 = 'debit'
                    amount = item_project.debit
                    amount_currency = item_project.amount_currency
                    currency_id = item_project.currency_id.id
                elif item_project.credit != 0:
                    item1 = 'debit'
                    item2 = 'credit'
                    amount = item_project.credit
                    amount_currency = item_project.amount_currency
                    currency_id = item_project.currency_id.id

                data_1 = {
                    'account_id': o_account.original_acc_id.id,
                    'analytic_account_id': self.project_id.analytic_account_id.id,
                    'move_id': journal_entry_id.id,
                    # 'item1': amount,
                    'amount_currency': amount_currency if item1 == 'debit' else -amount_currency,
                    'debit': amount_currency if item1 == 'debit' else 0,
                    'credit': 0 if item1 == 'debit' else amount_currency,
                    'currency_id': currency_id,
                }
                data_2 = {
                    'account_id': o_account.corresponding_acc_id.id,
                    'analytic_account_id': self.project_id.analytic_account_id.id,
                    'move_id': journal_entry_id.id,
                    # item2: amount,
                    'amount_currency': amount_currency if item2 == 'debit' else -amount_currency,
                    'credit': amount_currency if item1 == 'debit' else 0,
                    'debit': 0 if item1 == 'debit' else amount_currency,
                    'currency_id': currency_id,
                }
                journal_entry_item1 = journal_entry_item.with_context(check_move_validity=False).create(data_1)
                journal_entry_item2 = journal_entry_item.with_context(check_move_validity=False).create(data_2)
        if journal_entry_item_found is False:
            message = 'Can\'t Create Journal Entry!\n' + \
                      'No Journal Entry line found with the Analytical Account of the Project' + \
                      ' and One of the Cost / WIP Original Accounts.'
            raise exceptions.ValidationError(message)

        if journal_entry_id and journal_entry_item1 and journal_entry_item2:
            self.is_cost_button_clicked = True

    def get_converted_revenue(self, amount_convert):
        self.original_currency_id = self.sale_line_id.currency_id.id
        # print(self.original_currency_id)
        order_rate = self.env['res.currency.rate'].search(
            [('company_id', '=', self.company_id.id), ('currency_id', '=', self.original_currency_id.id),
             ('name', '<=', self.sale_line_id.order_id.date_order)], limit=1)

        if not order_rate:
            order_rate = self.env['res.currency.rate'].search(
                [('company_id', '=', self.company_id.id), ('currency_id', '=', self.original_currency_id.id)], limit=1)
        if not order_rate:
            _logger.info("No Currency rates found.")
            the_order_rate = 1
        else:
            _logger.info("Amount will be converted on following rates : ", order_rate.rate)
            the_order_rate = order_rate.rate
        my_revenue_total = amount_convert / the_order_rate
        return my_revenue_total

    @api.model
    def get_old_converted_revenue(self):
        proj_tasks = self.env['project.task'].search([])
        for task in proj_tasks:
            task.update({'converted_revenue': task.get_converted_revenue(task.revenue)})
