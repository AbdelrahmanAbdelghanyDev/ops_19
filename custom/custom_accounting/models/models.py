# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

class custom_accounting(models.Model):
    _inherit = 'account.bank.statement'

    name = fields.Char(
        string='Reference',
        states={'open': [('readonly', False)]},
        copy=False, readonly=True
    )
    hide = fields.Boolean()

    def button_in(self):
        if not self.name:
            self.name = self.env['ir.sequence'].get(
                'account.bank.statement.in')
            self.hide = True
        active = self.env['account.bank.statement'].search(
            [('name', '=', self.name)], limit=1).id
        self.create_in_out('in')
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.bank.statement',
            'target': 'main',
            'res_id': active,
        }

    def button_out(self):
        for record in self:
            if not record.name:
                record.name = self.env['ir.sequence'].get(
                    'account.bank.statement.out')
                record.hide = True
            for line in record.line_ids:
                line.amount *= -1
            name = record.name
            active = self.env['account.bank.statement'].search(
                [('name', '=', name)], limit=1).id
            record.create_in_out('out')
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'res_model': 'account.bank.statement',
                'target': 'main',
                'res_id': active,
            }

    def create_in_out(self, type):
        opening_acc = self.env['account.cash.in.out'].autofill()
        total = 0
        vals = {
            'name': self.name,
            'date': self.date,
            'currency_id': self.currency_id.id,
            'rate': self.currency_id.rate,
            'company_id': self.company_id.id,
            'reference': self.name,
        }
        for line in self.line_ids:
            total += line.amount

        if type == 'out':
            total *= -1
            vals['credit'] = total * (1 / vals['rate'])
            vals['debit'] = 0
        else:
            vals['debit'] = total * (1 / vals['rate'])
            vals['credit'] = 0

        vals['amount'] = total

        vals['balance'] = opening_acc.to_balance + \
            vals['debit'] - vals['credit']

        opening_acc.to_balance = vals['balance']

        self.env['account.cash.in.out'].create(vals)


class custom_cash_report(models.Model):
    _name = 'account.cash.in.out'

    name = fields.Char(string="Serial")
    date = fields.Date(string="Date")
    credit = fields.Float(string="Credit", default=0)
    debit = fields.Float(string="Debit", default=0)
    balance = fields.Float(string="Balance", default=0)
    reference = fields.Char(string="Description")
    rate = fields.Float(string="Rate")
    currency_id = fields.Many2one('res.currency', 'Currency')
    amount = fields.Monetary("Amount Currency", currency_field='currency_id')
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env.user.company_id
    )
    to_balance = fields.Float(default=0)

    def autofill(self):
        opening_acc = self.search(
            [('name', '=', 'Opening Balance')])
        if not opening_acc:
            self.search([]).unlink()
            opening = self.env['account.move.line'].search(
                [('account_id.name', '=', 'Opening Income Account')])
            vals = {}
            vals['name'] = "Opening Balance"
            vals['credit'] = opening.credit
            vals['debit'] = opening.debit
            vals['balance'] = vals['debit'] - vals['credit']
            vals['currency_id'] = opening.currency_id.id
            vals['amount'] = opening.amount_currency
            vals['rate'] = opening.currency_id.rate
            vals['reference'] = ''
            vals['company_id'] = opening.company_id.id
            vals['to_balance'] = vals['balance']
            opening_acc = self.env['account.cash.in.out'].create(vals)
        return opening_acc
