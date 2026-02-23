# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'

    team_id = fields.Many2one(track_visibility='onchange')
    fully_invoiced = fields.Boolean(default=False)

    def create_invoice_new(self):
        for order in self:
            order.fully_invoiced = True
            inv_obj = self.env['account.move']
            ir_property_obj = self.env['ir.property']
            lines = []

            for line in order.order_line:
                account_id = False
                if line.product_id.id:
                    account_id = order.fiscal_position_id.map_account(
                        line.product_id.property_account_income_id or line.product_id.categ_id.property_account_income_categ_id).id
                if not account_id:
                    inc_acc = ir_property_obj.get('property_account_income_categ_id', 'product.category')
                    account_id = order.fiscal_position_id.map_account(inc_acc).id if inc_acc else False
                if not account_id:
                    raise UserError(
                        _(
                            'There is no income account defined for this product: "%s". You may have to install a chart of account from Accounting app, settings menu.') %
                        (self.product_id.name,))
                taxes = line.product_id.taxes_id.filtered(
                    lambda r: not order.company_id or r.company_id == order.company_id)
                if order.fiscal_position_id and taxes:
                    tax_ids = order.fiscal_position_id.map_tax(taxes).ids
                else:
                    tax_ids = taxes.ids

                lines.append((0, 0, {
                    'name': line.name,
                    'ref': order.name,
                    'account_id': account_id,
                    'price_unit': line.price_unit,
                    'quantity': line.product_uom_qty,
                    'discount': line.discount,
                    'product_uom_id': line.product_id.uom_id.id,
                    'product_id': line.product_id.id,
                    'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                    'tax_ids': [(6, 0, tax_ids)],
                    'analytic_account_id': order.analytic_account_id.id or False,
                })),

            invoice = inv_obj.create({
                # 'name': order.client_order_ref or order.name,
                # 'invoice_origin': order.client_order_ref or order.name,
                'move_type': 'out_invoice',
                # 'reference': False,
                # 'account_id': order.partner_id.property_account_receivable_id.id,
                'partner_id': order.partner_invoice_id.id,
                'partner_shipping_id': order.partner_shipping_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                # 'payment_term_id': order.payment_term_id.id,
                'fiscal_position_id': order.fiscal_position_id.id or order.partner_id.property_account_position_id.id,
                'team_id': order.team_id.id,
                'user_id': order.user_id.id,
                # 'comment': order.note,
                'invoice_line_ids': lines,
            })

            order.order_line.invoice_lines = [(4, l) for l in invoice.invoice_line_ids.ids]
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'ref': order},
                                           subtype_id=self.env.ref('mail.mt_note').id)
            line.qty_invoiced = line.qty_invoiced + line.product_uom_qty
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'views': [[self.env.ref('account.view_move_form').id, 'form']],
            'target': 'current',
            'res_id': invoice.id,
        }


class AccMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        result = super(AccMove, self).action_post()
        if result and result.journal_id:
            records = self.search([('name', 'ilike', result.journal_id.code + '/')]).filtered(
                lambda l: l.name.startswith(result.journal_id.code))
            inv_count = str(len(records.ids))
            seq = "0" * (4 - len(inv_count)) + inv_count
            result.name = "%s/%04d/%02d/%s" % (self.journal_id.code, self.date.year, self.date.month, seq)
        return result
