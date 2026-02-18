# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
from dateutil import relativedelta
from datetime import datetime


class SaleOrderLineAged(models.Model):
    _inherit = 'sale.order.line'

    is_revenue_button_clicked = fields.Boolean(string='Recognized', readonly=True)
    task_status = fields.Many2one('project.task.type', string='Task Status', readonly=True)


class ProjectTaskAged(models.Model):
    _inherit = 'project.task'

    is_revenue_button_clicked = fields.Boolean(hidden_field=True, default=False)

    @api.constrains('stage_id')
    def const_stage_id(self):
        self.sale_line_id.task_status = self.stage_id.id

    @api.constrains('is_revenue_button_clicked')
    def const_recognized(self):
        for rec in self:
            rec.sale_line_id.is_revenue_button_clicked = rec.is_revenue_button_clicked

    def old_aged(self):
        tasks = self.search([])
        for line in tasks:
            if line.sale_line_id:
                line.sale_line_id.task_status = line.stage_id.id
                line.sale_line_id.is_revenue_button_clicked = line.is_revenue_button_clicked

    def close_revenue(self):
        if self.is_revenue_button_clicked:
            return
        project_revenue_accounts = self.env['revenue_accounts']
        journal_entry_item = self.env['account.move.line']
        journal_entry = self.env['account.move']
        p_r_accounts = project_revenue_accounts.search(
            [('tag', '=', self.tag_id.id), ('company_id', '=', self.company_id.id)])

        current_company_id = self.env.user.company_id.id
        journal = self.env['account.journal'].search(
            [('name', '=', 'Project Closure'), ('company_id', '=', current_company_id)])

        if not p_r_accounts:
            if self.tag_id.name:
                message = (
                        'Can\'t Create Journal Entry!\n' + 'Please Create Revenue account with the tag: ' + self.tag_id.name)
            else:
                message = ('Can\'t Create Journal Entry!\n' + 'No tag found ')
            raise exceptions.ValidationError(message)
            return

        current_company_id = self.env.company.id
        journal = self.env['account.journal'].search(
            [('name', '=', 'Project Closure'), ('company_id', '=', current_company_id)])

        if p_r_accounts:
            journal_entry_id = journal_entry.create({
                'date': self.date_deadline,  # fields.Date.today(),
                'journal_id': journal.id,
                'ref': self.project_id.name,
                # 'name': 'Project Completion ' + self.project_id.analytic_account_id.display_name,
                'name': self.env['ir.sequence'].search(
                    [('name', '=', 'Project Closure'), ('company_id', '=', current_company_id)]).next_by_id(),
                'cor': '(revenue)'
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.accrued_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                'move_id': journal_entry_id.id,
                'debit': self.converted_revenue,
                'amount_currency': self.revenue,
                'currency_id': self.original_currency_id.id,
            })
            journal_entry_item.with_context(check_move_validity=False).create({
                'account_id': p_r_accounts.revenue_acc_id.id,
                'analytic_account_id': self.project_id.analytic_account_id.id,
                'move_id': journal_entry_id.id,
                'credit': self.converted_revenue,
                'amount_currency': -self.revenue,
                'currency_id': self.original_currency_id.id,
            })
            self.is_revenue_button_clicked = True

            self.env['account.move'].search([('invoice_origin', '=', self.sale_line_id.order_id.name)]).write({
                'is_revenue_button_clicked': self.is_revenue_button_clicked,
                'task_state': self.stage_id.id})


class InvoiceLineAged(models.Model):
    _inherit = 'account.move.line'

    is_revenue_button_clicked = fields.Boolean(string='Recognized', readonly=True,
                                               related='sale_line_ids.is_revenue_button_clicked')
    task_status = fields.Many2one('project.task.type', string='Task Status', readonly=True,
                                  related='sale_line_ids.task_status')
    price_unit = fields.Float(string='Unit Price', digits=(12, 2))


class InvoiceAged(models.Model):
    _inherit = 'account.move'

    # open_date = fields.Datetime('Invoice Open Date',readonly=True)
    invoice_open_days = fields.Integer('Days of invoice in Open state', default=0, readonly=True)

    def count_days_open_invoice(self):
        invoices = self.sudo().search([('invoice_date', '!=', False), ('state', '!=', 'paid')])
        for rec in invoices:
            date_invoice = datetime.strptime(rec.date_invoice, '%Y-%m-%d')
            date_now = datetime.strptime(fields.Datetime.now(), '%Y-%m-%d %H:%M:%S')
            diff = relativedelta.relativedelta(date_now, date_invoice).days
            rec.invoice_open_days = diff


class CostAccounts(models.Model):
    _name = 'cost.accounts'

    description = fields.Text('Description')
    original_acc_id = fields.Many2one('account.account', 'Original Account', required=True)
    corresponding_acc_id = fields.Many2one('account.account', 'Corresponding Account', required=True)


class RevenueAccounts(models.Model):
    _name = 'revenue_accounts'

    description = fields.Text('Description')
    revenue_acc_id = fields.Many2one('account.account', 'Revenue Account', required=True)
    accrued_acc_id = fields.Many2one('account.account', 'Accrued Account', required=True)
    company_id = fields.Many2one('res.company', 'Company')
    tag = fields.Many2one('crm.tag', 'Tag', required=True)
