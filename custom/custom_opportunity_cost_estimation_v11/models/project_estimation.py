from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class CustomTaskEstimationLine(models.Model):
    _name = 'custom.task.estimation.line'

    # Define required fields
    name = fields.Text(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', copy=False, index=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=(16,2), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', digits=(16, 2))
    price_subtotal = fields.Float(string='Subtotal')
    price_tax = fields.Float(string='Tax')
    price_total = fields.Float(string='Total')
    discount = fields.Float(string='Discount (%)', digits=(16, 2), default=0.0)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    create_uid = fields.Many2one('res.users', readonly=True)
    create_date = fields.Datetime(readonly=True)
    write_uid = fields.Many2one('res.users', readonly=True)
    write_date = fields.Datetime(readonly=True)

    product_no_variant_attribute_value_ids = fields.Many2many('product.template.attribute.value',
                                                              relation="awe_task_line_product_rel",
                                                              string="Extra Values", ondelete='restrict')

    opportunity_cost_estimation = fields.Many2many(
        'opportunity.cost.estimation', relation="awe_task_line_opportunity_rel",
        store=True,
        domain="[('parent_opportunity.id', '=', parent_opportunity), ('state','=','done')]"
    )
    invoice_lines = fields.Many2many('account.move.line', 'awe_task_line_invoice_rel', 'order_line_id2',
                                     'invoice_line_id2', string='Invoice Lines', copy=False)

    task_id = fields.Many2one('project.task')
    task_name = fields.Char(string="Tasks")
    combined = fields.Boolean(string="Combined Line")
    exceed_limit = fields.Boolean()
    is_used = fields.Boolean(default=False)
    total_actual_qty = fields.Float()
    total_actual_total = fields.Float()
    project_id = fields.Many2one('project.project')
    parent_cost = fields.Many2one('opportunity.cost.estimation', string='parent_cost')
    actual_qty = fields.Float(default=0)
    actual_unit_price = fields.Float(default=0)

    to_WH = fields.Boolean()
    done_to_WH = fields.Boolean()
    done_to_acct = fields.Boolean()
    done_to_expense = fields.Boolean(string="Done Exp")

    # @api.multi
    def show_details(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'list',
            'view_mode': 'list',
            'res_model': 'custom.task.estimation.line',
            'target': 'new',
            'views': [(self.env.ref(
                'custom_opportunity_cost_estimation_v11.custom_task_estimation_line_tree').id,
                       'tree')],
            "domain": [["project_id", "=", self.project_id.id],
                       ["parent_cost", "=", self.parent_cost.id],
                       ["product_id", "=", self.product_id.id]],
        }

    # @api.multi
    def to_expense(self):
        for i in self:
            if i.done_to_expense:
                return
            try:
                analytic_account = i.project_id.sale_line_id.order_id.analytic_account_id.id
            except Exception:
                pass

            vals = {
                'name': i.project_id.name + " / " + i.product_id.name,
                'product_id': i.product_id.id,
                'unit_amount': i.actual_unit_price,
                'quantity': i.actual_qty,
                'analytic_account_id': analytic_account or False,
            }
            self.env['hr.expense'].create(vals)
            i.done_to_expense = True

    # @api.multi
    def to_accountant(self):
        for i in self:
            project = self.env['project.project'].search(
                [('id', '=', i.project_id.id)])
            analytic_account = self.env['account.analytic.account'].browse(
                project.analytic_account_id.id)
            if not i.done_to_acct:
                i.done_to_acct = True
                a = self.env['product.product'].browse(
                    i.product_id.id).categ_id.id
                b = self.env['product.category'].browse(
                    a).property_account_expense_categ_id.id
                c = self.env['account.account'].browse(b).id
                vals = {
                    'product_id': i.product_id.id,
                    'product_uom_id': self.env['product.product'].browse(
                        i.product_id.id).uom_id.id,
                    'unit_amount': i.actual_qty,
                    'account_id': analytic_account.id,
                    'amount': i.actual_total * - 1.0,
                    'project_id': 0,
                    'general_account_id': c,
                }
                # print vals
                # print i.product_id.name
                self.env['account.analytic.line'].create(vals)

    # @api.multi
    # def bulk_verify(self):
    #     products = []
    #     for i in self:
    #         if not i.done_to_WH:
    #             _logger.error("product name:")
    #             _logger.error(i.name)
    #             products.append((0, 0, {'product_id': i.product_id.id,
    #                                     'product_uom': i.product_uom.id,
    #                                     'name': i.name,
    #                                     'product_uom_qty': i.actual_qty,
    #                                     }))
    #             i.done_to_WH = True
    #
    #     tmp_task_name = str(self[0].name)
    #     origin_name = str(self[0].project_id.name) + '/' + str(self[0].name)
    #     for i in self:
    #         if i.name != tmp_task_name:
    #             origin_name = str(self[0].project_id.name)
    #             break
    #
    #     vals = {
    #         'picking_type_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_operation").id,
    #         'location_id': self.env.ref("stock.stock_location_stock").id,
    #         'location_dest_id': self.env.ref(
    #             "custom_opportunity_cost_estimation_v11.custom_warehouse_location").id,
    #         'move_lines': products,
    #         'origin': origin_name,
    #         'name': origin_name,
    #     }
    #     _logger.error("stock name:")
    #     _logger.error(origin_name)
    #     self.env['stock.picking'].create(vals)

    @api.model
    def unlink(self):
        res = super(CustomTaskEstimationLine, self).unlink()

        return res

    @api.model
    def create(self, vals):
        res = super(CustomTaskEstimationLine, self).create(vals)
        project_id = self.env['project.project'].browse(vals['project_id'])
        for line in project_id.tasks_estimations_ids_report:
            if line.product_id.id == vals['product_id'] and line.parent_cost.id == vals['parent_cost']:
                line.task_id = False
                line.task_name = \
                    str(line.task_id.name) + \
                    str(self.env['project.task'].browse(vals['task_id']).name)
                line.combined = True
                line.actual_qty = line.actual_qty + vals['actual_qty']
                line.actual_unit_price = vals['actual_unit_price']
                line.is_used = True
                if (line.product_uom_qty < line.actual_qty) or (line.price_unit < line.actual_unit_price):
                    line.exceed_limit = True

                tmp_line = self.env['custom.task.estimation.line'].search(
                    [
                        ('project_id', '=', project_id.id),
                        ('parent_cost', '=', line.parent_cost.id),
                        ('product_id', '=', line.product_id.id),
                    ]
                )
                total_qty = 0
                total_cost = 0
                for i in tmp_line:
                    total_qty += i.actual_qty
                    total_cost += i.actual_total

                line.total_actual_qty = total_qty
                line.total_actual_total = total_cost

                return res

        if (vals['product_uom_qty'] < vals['actual_qty']) or (vals['price_unit'] < vals['actual_unit_price']):
            if (vals['parent_cost']):
                vals['exceed_limit'] = True

        vals['is_used'] = True
        vals['total_actual_qty'] = vals['actual_qty']
        vals['total_actual_total'] = vals['actual_qty'] * \
                                     vals['actual_unit_price']
        self.env['custom.task.estimation.line'].create(vals)
        return res

    @api.onchange('parent_cost')
    def get_domain(self):
        print('######################## get_domain #######################')
        # self.get_domain_2()
        try:
            print('######################## i am trying #######################')
            if self.parent_cost.id is False:
                cost_estimation = \
                    self.env['opportunity.cost.estimation'].search(
                        [('id', '=', self._context['parent_cost_id'])])
            else:
                cost_estimation = self.parent_cost

            cost_estimation_products = []
            for line in cost_estimation.order_line:
                cost_estimation_products.append(line.product_id.id)

            parent_cost_domain = []
            if self.project_id.id:
                a = self.project_id.estimation_ids.search(
                    [('project_id', '=', self.project_id.id)])
                for i in a:
                    parent_cost_domain.append(i.parent_cost.id)
            else:
                parent_cost_domain = []
                a = self.project_id.estimation_ids.search(
                    [('project_id', '=', self.project_id.id)])
                for i in a:
                    parent_cost_domain.append(i.parent_cost.id)
            print({
                'domain': {
                    'product_id': [('id', '=', cost_estimation_products)],
                }
            })
            return {
                'domain': {
                    'product_id': [('id', '=', cost_estimation_products)],
                }
            }

        except Exception:
            print('######################## i am excepted #######################')
            parent_cost_domain = []
            if self.project_id.id:
                a = self.project_id.estimation_ids.search(
                    [('project_id', '=', self.project_id.id)])
                for i in a:
                    parent_cost_domain.append(i.parent_cost.id)
            else:
                parent_cost_domain = []

                a = self.project_id.estimation_ids.search(
                    [('project_id', '=', self.project_id.id)])
                for i in a:
                    parent_cost_domain.append(i.parent_cost.id)
            print({'domain': {'product_id': [], }})
            return {'domain': {'product_id': [], }}

    @api.onchange('project_id')
    def get_domain_2(self):
        print('##################### get_domain_2 ##########################')
        parent_cost_domain = []
        print(self._context['default_project_id'])
        a = self.env['project.project'].search(
            [('id', '=', self._context['default_project_id'])])
        print(a)
        for i in a:
            print(i.estimation_ids)
            for j in i.estimation_ids:
                print(j)
                parent_cost_domain.append(j.parent_cost.id)
        print('###############################################')
        print({'domain': {'parent_cost': [('id', '=', parent_cost_domain)], }})
        return {'domain': {'parent_cost': [('id', '=', parent_cost_domain)], }}

    # @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        a = self.get_domain()
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [
            ('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        # Getting the estimated qty of the product from the CE if exists.
        vals['product_uom_qty'] = 0.0
        if self.parent_cost.id:
            cost_estimation = self.parent_cost
            for i in cost_estimation.order_line:
                if i.product_id == self.product_id:
                    vals['product_uom_qty'] = i.product_uom_qty

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        domain['product_id'] = a['domain']['product_id']
        result = {'domain': domain}

        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
                return result

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale

        vals['name'] = name
        self._compute_tax_id()
        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = \
                self.env['account.tax']._fix_tax_included_price_company(
                    self._get_display_price(product),
                    product.taxes_id, self.tax_ids,
                    self.company_id
                )

        # Getting the estimated price_unit of the product from the CE if exists
        vals['price_unit'] = 0
        if self.parent_cost.id:
            cost_estimation = self.parent_cost
            for i in cost_estimation.order_line:
                if i.product_id == self.product_id:
                    vals['price_unit'] = i.price_unit

        self.update(vals)

        return result


class CustomProjectEstimationLine(models.Model):
    _name = 'custom.project.estimation.line'

    name = fields.Text(string='Description', required=True)
    order_id = fields.Many2one('sale.order', required=False, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', digits=(16,2), required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')
    price_unit = fields.Float(string='Unit Price', digits=(16, 2))
    price_subtotal = fields.Float(string='Subtotal')
    price_tax = fields.Float(string='Tax')
    price_total = fields.Float(string='Total')
    discount = fields.Float(string='Discount (%)', digits=(16, 2), default=0.0)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency')
    tax_ids = fields.Many2many('account.tax', string='Taxes')
    create_uid = fields.Many2one('res.users', readonly=True)
    create_date = fields.Datetime(readonly=True)
    write_uid = fields.Many2one('res.users', readonly=True)
    write_date = fields.Datetime(readonly=True)
    project_id = fields.Many2one('project.project')
    parent_cost = fields.Many2one('opportunity.cost.estimation', string='parent_cost')

    def get_domain(self):
        try:
            if not self.parent_cost.id:
                cost_estimation = \
                    self.env['opportunity.cost.estimation'].search(
                        [('id', '=', self._context['parent_cost_id'])])
            else:
                cost_estimation = self.parent_cost

            cost_estimation_products = []
            for i in cost_estimation.order_line:
                cost_estimation_products.append(i.product_id.id)

            return {
                'domain': {
                    'product_id': [('id', '=', cost_estimation_products)]
                }
            }

        except Exception:
            return {'domain': {'product_id': []}}

    # @api.multi
    @api.onchange('product_id')
    def product_id_change(self):

        a = self.get_domain()
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [
            ('category_id', '=', self.product_id.uom_id.category_id.id)]}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = 1.0

        vals['product_uom_qty'] = 1.0
        if self.parent_cost.id:
            cost_estimation = self.parent_cost
            for i in cost_estimation.order_line:
                if i.product_id == self.product_id:
                    vals['product_uom_qty'] = i.product_uom_qty

        product = self.product_id.with_context(
            lang=self.order_id.partner_id.lang,
            partner=self.order_id.partner_id.id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        domain['product_id'] = a['domain']['product_id']
        result = {'domain': domain}
        title = False
        message = False
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s") % product.name
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
                return result

        name = product.name_get()[0][1]
        if product.description_sale:
            name += '\n' + product.description_sale
        vals['name'] = name

        self._compute_tax_id()
        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = \
                self.env['account.tax']._fix_tax_included_price_company(
                    self._get_display_price(product), product.taxes_id,
                    self.tax_ids,
                    self.company_id
                )

        vals['price_unit'] = 0
        if self.parent_cost.id:
            cost_estimation = self.parent_cost
            for i in cost_estimation.order_line:
                if i.product_id == self.product_id:
                    vals['price_unit'] = i.price_unit

        self.update(vals)

        return result
