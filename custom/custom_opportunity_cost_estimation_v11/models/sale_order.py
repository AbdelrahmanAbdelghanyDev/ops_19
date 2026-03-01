from odoo import models, fields, api


class CustomQuotation(models.Model):
    _inherit = 'sale.order'
    parent_opportunity = fields.Many2one(
        'crm.lead', string="parent_opportunity")

    opportunity_cost_estimation = fields.Many2many(
        'opportunity.cost.estimation', relation="awe_sale_order_opportunity_rel",
        store=True,
        domain="[('parent_opportunity.id', '=', parent_opportunity), ('state','=','done')]"
    )
    opportunity_total_cost = fields.Float()
    opportunity_total_cost_2 = fields.Float(
        related='opportunity_total_cost',
        readonly=True
    )

    project_objective = fields.Many2one('project.objective', string="Project Objective",
                                        related='parent_opportunity.project_objective')
    project_type = fields.Selection([
        ('0', 'Adhoc'),
        ('1', 'Tracker'),
        ('2', 'Desk Research'),
        ('3', 'syndicated')
    ], string="Project Type", related='parent_opportunity.project_type')
    sector_id = fields.Many2one('sector', 'Sector', related='parent_opportunity.sector_id')

    # @api.multi
    # @api.depends('parent_opportunity')
    # def _onchange_parent_opportunity(self):
    #     for rec in self:
    #         if rec.parent_opportunity:
    #             rec.project_objective = rec.parent_opportunity.project_objective
    #             rec.project_type = rec.parent_opportunity.project_type
    #             rec.sector_id = rec.partner_id.sector_id

    # @api.multi
    def action_confirm(self):
        res = super(CustomQuotation, self).action_confirm()
        for order in self:
            # order._timesheet_service_generation()
            try:
                # print(order)
                # prints(order.order_line.ids)
                # print(order.tasks_ids)
                order.tasks_ids = self.env['project.task'].search(
                    [('sale_line_id', 'in', order.order_line.ids)])
                # print(order.tasks_ids)
                project_id = order.tasks_ids[0].project_id

                for i in order.opportunity_cost_estimation:
                    for j in i.order_line:
                        project_id.estimation_ids.create({
                            'project_id': project_id.id,
                            'product_id': j.product_id.id,
                            'product_uom': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).uom_id.id,
                            'name': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).name,
                            'price_unit': j.price_unit,
                            'product_uom_qty': j.product_uom_qty,
                            'parent_cost': i.id,
                        })
                        project_id.tasks_estimations_ids_report.create({
                            'project_id': project_id.id,
                            'product_id': j.product_id.id,
                            'product_uom': self.env['product.product'].search(
                                [('id', '=', j.product_id.id)]).uom_id.id,
                            'name': self.env['product.product'].search([
                                ('id', '=', j.product_id.id)]).name,
                            'price_unit': j.price_unit,
                            'product_uom_qty': j.product_uom_qty,
                            'parent_cost': i.id,
                        })
            except Exception:
                continue

        return res

    # #@api.one
    @api.onchange('opportunity_cost_estimation')
    def onchange_opportunity_cost_estimation(self):
        for rec in self:
            tmp_total = 0
            for i in rec.opportunity_cost_estimation:
                tmp_total += i.amount_total

            values = {
                'opportunity_total_cost': tmp_total,
            }
            rec.update(values)

    @api.onchange('opportunity_id')
    def onchange_opportunity_id(self):
        self.parent_opportunity = self.opportunity_id

    @api.model
    def initiate_field(self):
        sales = self.env['sale.order'].search([])
        for i in sales:
            i.parent_opportunity = i.opportunity_id


class CustomSaleOrderLine(models.Model):
    _name = 'custom.sale.order.line'

    # Define all required fields without inheriting from sale.order.line to avoid FK conflicts
    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', copy=False, index=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=(16,2), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', digits=(16, 2))
    price_subtotal = fields.Monetary(compute='_compute_amount', store=True)
    price_tax = fields.Float(compute='_compute_amount', store=True)
    price_total = fields.Monetary(compute='_compute_amount', store=True)
    discount = fields.Float(string='Discount (%)', digits=(16, 2), default=0.0)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='order_id.currency_id')
    order_partner_id = fields.Many2one('res.partner', string='Partner')
    salesman_id = fields.Many2one('res.users', string='Salesman')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    create_uid = fields.Many2one('res.users', readonly=True)
    create_date = fields.Datetime(readonly=True)
    write_uid = fields.Many2one('res.users', readonly=True)
    write_date = fields.Datetime(readonly=True)

    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value',
                                                              relation="awe_custom_line_product_rel",
                                                              string="Extra Values", ondelete='restrict')

    parent_cost = fields.Many2one(
        'opportunity.cost.estimation',
        string='parent_cost'
    )

    no_of_waves = fields.Integer(default=1)  # Based on customer request.
    no_of_units = fields.Float(default=1)  # Based on customer request.
    price_subtotal_new = fields.Float(compute='_amount_subtotal_new')

    # used for estimation line in tasks.
    actual_qty = fields.Float(default=0)
    actual_unit_price = fields.Float(default=0)
    actual_total = fields.Float(compute='_amount_actual_total')
    invoice_lines = fields.Many2many('account.move.line', 'awe_sale_order_line_invoice_rel', 'order_line_id',
                                     'invoice_line_id', string='Invoice Lines', copy=False)

    @api.depends('actual_qty', 'actual_qty')
    def _amount_actual_total(self):
        for i in self:
            i.actual_total = i.actual_qty * i.actual_unit_price

    @api.depends('product_uom_qty', 'price_unit')
    def _amount_subtotal_new(self):
        for i in self:
            i.price_subtotal_new = i.product_uom_qty * i.price_unit

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_ids', 'no_of_waves', 'price_subtotal_new',
                 'no_of_units')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_ids.compute_all(
                price_unit=price * line.no_of_units * line.no_of_waves,
                currency=line.order_id.currency_id,
                quantity=line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': line.price_subtotal_new * line.no_of_waves,
            })
