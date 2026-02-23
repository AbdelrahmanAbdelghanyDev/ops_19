# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

from odoo.addons.account.models.account_bank_statement import AccountBankStatementLine as StatementLine


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'


    # overwrite from main function of button post to bypass validation error to allow post of adding line in statement lines
    def button_post(self):
        ''' Move the bank statements from 'draft' to 'posted'. '''
        # if any(statement.state != 'open' for statement in self):
            # raise UserError(_("Only new statements can be posted."))

        self._check_cash_balance_end_real_same_as_computed()

        for statement in self:
            if not statement.name:
                statement._set_next_sequence()

        self.write({'state': 'posted'})
        lines_of_moves_to_post = self.line_ids.filtered(lambda line: line.move_id.state != 'posted')
        if lines_of_moves_to_post:
            lines_of_moves_to_post.move_id._post(soft=False)

class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'


    # function used to bypass validation error ro allow statment post and reconicle in processing statement
    # overwrite from main function in odoo
    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        counterpart_account_ids = []

        for vals in vals_list:
            statement = self.env['account.bank.statement'].browse(vals['statement_id'])
            if statement.state != 'open' and self._context.get('check_move_validity', True):
                # raise UserError(_("You can only create statement line in open bank statements."))
                pass

            # Force the move_type to avoid inconsistency with residual 'default_move_type' inside the context.
            vals['move_type'] = 'entry'

            journal = statement.journal_id
            # Ensure the journal is the same as the statement one.
            vals['journal_id'] = journal.id
            vals['currency_id'] = (journal.currency_id or journal.company_id.currency_id).id
            if 'date' not in vals:
                vals['date'] = statement.date

            # Avoid having the same foreign_currency_id as currency_id.
            journal_currency = journal.currency_id or journal.company_id.currency_id
            if vals.get('foreign_currency_id') == journal_currency.id:
                vals['foreign_currency_id'] = None
                vals['amount_currency'] = 0.0

            # Hack to force different account instead of the suspense account.
            counterpart_account_ids.append(vals.pop('counterpart_account_id', None))

        st_lines = super(StatementLine,self).create(vals_list)

        for i, st_line in enumerate(st_lines):
            counterpart_account_id = counterpart_account_ids[i]

            to_write = {'statement_line_id': st_line.id}
            if 'line_ids' not in vals_list[i]:
                to_write['line_ids'] = [(0, 0, line_vals) for line_vals in st_line._prepare_move_line_default_vals(
                    counterpart_account_id=counterpart_account_id)]

            st_line.move_id.write(to_write)

        return st_lines

