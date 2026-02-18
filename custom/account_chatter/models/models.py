# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountingMove(models.Model):
    _name = 'account.move'
    _inherit = ['account.move', 'mail.thread', 'mail.activity.mixin']
    name = fields.Char(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    state = fields.Selection(track_visibility='onchange')
    # because message is not undersandable, we should do it in another way
    # line_id = fields.One2many(track_visibility='onchange')
    to_check = fields.Boolean(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    amount = fields.Float(track_visibility='onchange')
    date = fields.Date(track_visibility='onchange')
    narration = fields.Text(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    balance = fields.Float(track_visibility='onchange')

    def button_cancel(self):
        for rec in self:
            rec.message_post(body='<ul>Status: Posted &rArr; Unposted</ul>')
        return super(AccountingMove, self).button_cancel()

class Accounting(models.Model):
    _inherit = 'account.move.line'

    def write(self, vals):
        if vals:
            message = ""

            for _key, _value in vals.items():
                if _key == 'account_id':
                    old_value = self.account_id.name
                    old_name = 'Account'
                    last_value = self.env['account.account'].search([('id', '=', _value)]).name
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'debit':
                    old_value = self.debit
                    old_name = 'Debit'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'credit':
                    old_value = self.credit
                    old_name = 'Credit'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)

                elif _key == 'currency_id':
                    old_value = self.currency_id.name
                    old_name = 'Currency'
                    last_value = self.env['res.currency'].search([('id', '=', _value)]).name
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)
                elif _key == 'amount_currency':
                    old_value = self.amount_currency
                    old_name = 'Amount Currency'
                    last_value = _value
                    message += '<li>%s: %s &rArr; %s</li><br/>' % (old_name, old_value, last_value)
                else:
                    pass
            if message:
                self.move_id.message_post(body=message)
        res = super(Accounting, self).write(vals)
        return res