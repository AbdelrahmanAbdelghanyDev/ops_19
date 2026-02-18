from odoo import models, fields, api

class estimation_template_changes(models.Model):

    _inherit='cost.estimation.template'

    template_sales_ids = fields.One2many('sale.order.line','estimation_id')






class sale_order_line_changes(models.Model):

    _inherit='sale.order.line'

    estimation_id = fields.Many2one('cost.estimation.template')






