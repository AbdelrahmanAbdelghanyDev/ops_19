# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class InvoiceTaf(models.Model):
    _inherit = "account.move"
    amount_to_text = fields.Text(
        store=True,
        compute='_amount_to_words'
    )
    amount_to_text_arabic = fields.Text(
        store=True,
        compute='_amount_to_words'
    )

    @api.depends('amount_total')
    def _amount_to_words(self):
        for rec in self:
            if rec.partner_id:
                # print '1',re.match(r'\W*(\w[^,. !?"]*)', self.text_amount_ar)
                # print '2',re.match(r'\W*(\w[^,. !?"]*)', self.text_amount_ar).groups()[0]
                rec.amount_to_text = num2words(rec.amount_total, to='currency',
                                               lang='en',
                                               )
                rec.amount_to_text_arabic = num2words(rec.amount_total, to='currency',
                                                      lang='ar',
                                                      )

