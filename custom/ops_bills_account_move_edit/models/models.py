# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from odoo import models, fields, api


class AWEAccountMove(models.Model):
    _inherit = 'account.move'

    awe_due_date = fields.Date(
        string='Due Date',readonly=True)

    @api.onchange('invoice_payment_term_id')
    def onchange_method(self):
        for rec in self:
            for wiz in rec.invoice_payment_term_id:
                for line in wiz.line_ids:
                    if line.value == 'balance':
                        date_1 = datetime.strptime(str(self.invoice_date), '%Y-%m-%d') + timedelta(days=line.days)
                        rec.awe_due_date = date_1
                    # rec.awe_due_date = line.days

    @api.onchange('date')
    def onchange_to_bill_date(self):
        self.invoice_date = self.date
