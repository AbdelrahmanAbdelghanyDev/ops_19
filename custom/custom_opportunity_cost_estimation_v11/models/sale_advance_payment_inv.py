from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    tag_ids = fields.Many2many('account.account.tag', string="Tags", relation="awe_acc_move_tag_rel")
    executive_team_id = fields.Many2one('executive.team', string="Executive Team")
    revenue_team_id = fields.Many2one('revenue.team', string="Revenue Team")


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    # @api.multi
    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        inv_update = self.env[res.get('res_model')].search([('id', '=', res.get('res_id'))])
        sale = self.env['sale.order'].search([('name', '=', inv_update.ref)])
        if sale:
            inv_update.write({
                'tag_ids': [(6, 0, sale.tag_ids.ids)],
                'executive_team_id': sale.executive_team_id.id,
                'revenue_team_id': sale.revenue_team_id.id
            })
        return res
