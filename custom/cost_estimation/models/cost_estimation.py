# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from io import BytesIO
import xlsxwriter

SEC = [
    ('A', 'A'),
    ('AB', 'AB'),
    ('BC1', 'BC1'),
    ('C1', 'C1'),
    ('C2', 'C2'),
    ('C1C2', 'C1C2'),
    ('C2D', 'C2D'),
    ('D', 'D'),
    ('E', 'E'),
    ('DE', 'DE'),
]
from lxml import etree


class CostEst(models.Model):
    _name = 'cost.estimation'
    _rec_name = 'seq'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    seq = fields.Char(readonly=True, string="CE No.",copy=False)
    state = fields.Selection([('draft', 'Draft'),
                              ('first_approval', 'Waiting 1st Approval'),
                              ('second_approval', 'Waiting 2nd Approval'),
                              ('approved', 'Approved'),
                              ('rejected', 'Rejected'),
                              ('cancelled', 'Cancelled')], string="State", default='draft', track_visibility='onchange')
    customer = fields.Many2one('res.partner', string="Customer", readonly=True, store=True)
    opportunity = fields.Many2one('crm.lead', string="Source Document", readonly=True, store=True)
    sales_team = fields.Many2one("crm.team", string="Sales Team", related='opportunity.team_id',
                                 track_visibility='onchange', readonly=True)
    sales_person = fields.Many2one("res.users", string="Sales Person", related='opportunity.user_id',
                                   track_visibility='onchange', readonly=True)

    price_list = fields.Many2one('product.pricelist', string="PriceList", track_visibility='onchange')
    estimate_date = fields.Datetime(readonly=True, default=fields.Datetime.now(), string="Estimation Date", store=True,
                                    track_visibility='onchange')

    t_margin = fields.Float(string='Total Margin', store=True, compute='_compute_total', digits=(12, 4),
                            track_visibility='onchange')
    t_margin_percentage = fields.Float(string='Margin Percent', store=True, compute='_compute_total', digits=(12, 4),
                                       track_visibility='onchange')
    fx = fields.Float('Fx Rate', default=1.0, store=True, digits=(12, 4), track_visibility='onchange')

    cost_estimation_line = fields.One2many('cost.estimation.line', 'idx_cost' , copy=1)
    products_line = fields.One2many('products.line', 'idx_cost',copy=1)

    total_material_cost = fields.Float('Total Materials Cost', store=True, compute="_compute_total",
                                       track_visibility='onchange')
    total_labour_cost = fields.Float('Total labour Cost', store=True, compute="_compute_total",
                                     track_visibility='onchange')
    total_overhead_cost = fields.Float('Total Overhead Cost', store=True, compute="_compute_total",
                                       track_visibility='onchange')
    total_cost = fields.Float('Cost / Waves', store=True, compute="_compute_total", track_visibility='onchange')
    total_unit_price = fields.Float('Total Selling Price', store=True, compute="_compute_product_line_total",
                                    track_visibility='onchange')
    quotations_count = fields.Integer()
    notes = fields.Text('Notes', track_visibility='onchange')
    total_product_line_tax = fields.Float('Taxes', compute='_compute_product_line_total', track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', related='price_list.currency_id', readonly=True)
    company_id = fields.Many2one('res.company', required=True, ondelete='cascade',
                                 default=lambda self: self.env.user.company_id)

    sale_order = fields.Many2one('sale.order', readonly=True, string='Sale Order')

    accounting_installed = fields.Boolean()

    research_type = fields.Many2one('product.category', string='Research Type', store=True, readonly=True)
    research_type_name = fields.Char(related='research_type.name')
    approach = fields.Selection([('capi', 'CAPI'), ('papi', 'PAPI')])

    waves = fields.Float(string='Waves', default=1)
    cost_of_waves = fields.Float(string='Cost of Waves', compute='_compute_cost_of_waves')

    cpi_x = fields.Float(string='CPI')
    third_party_cost = fields.Float(string="Third Party Cost")
    travel_expenses = fields.Float('Travel Expense')
    hide_create_quotation = fields.Boolean(compute='_check_sale_order_state', default=False, readonly=False)
    @api.depends('sale_order.state')
    def _check_sale_order_state(self):
        for rec in self:
            if rec.sale_order and (rec.sale_order.state != 'draft'):
                rec.hide_create_quotation = True
            else:
                pass

    @api.onchange('cost_of_waves')
    def _set_cpi(self):
        list_products_line = []
        quantity = 0
        for rec in self.opportunity.product_line:
            if self.research_type_name == 'QL':
                quantity = rec.quantity
            if self.research_type_name == 'QN':
                quantity = rec.quantity_qn
            list_products_line.append(quantity)
        if list_products_line and (sum(list_products_line) > 0):
            self.cpi_x = self.cost_of_waves / sum(list_products_line)
        else:
            pass

    @api.depends('waves')
    def _compute_cost_of_waves(self):
        self.cost_of_waves = self.waves * self.total_cost

    # methodology = fields.Char('Methodology')
    # number_of_legs = fields.Integer()
    # sample_size = fields.Float()
    # age = fields.Integer()
    # gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('both', 'Both')], string="Gender")
    # sec = fields.Char()
    # region = fields.Char()
    # usership = fields.Char()
    # moub = fields.Char()
    ################ QN ####################
    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Char('Sample Size')
    sample_struct_per_reg = fields.Char('Sample Structure per Region')
    sample_struct_per_sec = fields.Char('Sample Structure per SEC')
    sample_struct_per_age = fields.Char('Sample Structure per Age')
    sample_struct_per_gen = fields.Char('Sample Structure per Gender')
    sample_struct_per_bra = fields.Char('Sample Structure per Brand')
    length_of_interview = fields.Selection(
        [('15', '15'), ('15-30', '15-30'), ('30-45', '40-45'), ('45-60', '45-60'), ('60', '60+')],
        string='Length of Interview in Minutes'
    )
    details = fields.Text("Other Details:")

    ############## QL ##########################

    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')
    client_attendence_region_ids = fields.Many2many(
        'res.country.state',
        string='Client Attendance Region'
    )
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])

    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )

    transcript_lang = fields.Char(
        string='Transcript Language'
    )
    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    details_ql = fields.Text("Other Details:")

    @api.onchange('price_list')
    def onch_pricelist(self):
        self.fx = self.price_list.currency_id.rate
    markup = fields.Float(string="Markup")

    @api.depends('products_line.subtotal', 'products_line.subtotal_taxed', 'products_line.taxes',
                 'total_cost', 'markup')
    def _compute_product_line_total(self):
        for rec in self:
            # prices_list = []
            product_line_tax_list = []
            for rec_product_line in rec.products_line:
                # prices_list.append(rec_product_line.subtotal)
                if rec_product_line.taxes:
                    product_line_tax_list.append(rec_product_line.subtotal_taxed)
            rec.total_product_line_tax = sum(product_line_tax_list)
            # rec.total_unit_price = sum(prices_list) + rec.total_product_line_tax
            rec.total_unit_price = rec.total_cost + (rec.total_cost * (rec.markup / 100))

    @api.depends('cost_estimation_line.total_cost_item_cost', 'total_unit_price', 'total_cost', 'third_party_cost',
                 'travel_expenses')
    def _compute_total(self):
        for rec in self:
            # rec = self
            material_list = []
            labour_list = []
            overhead_list = []

            for line in rec.cost_estimation_line:
                if line.cost_item_type == 'material':
                    material_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'labour':
                    labour_list.append(line.total_cost_item_cost)
                if line.cost_item_type == 'overhead':
                    overhead_list.append(line.total_cost_item_cost)

            rec.total_material_cost = sum(material_list)
            rec.total_labour_cost = sum(labour_list)
            rec.total_overhead_cost = sum(overhead_list)
            rec.total_cost = rec.total_material_cost + rec.total_labour_cost + rec.total_overhead_cost + rec.third_party_cost + rec.travel_expenses

        if rec.total_unit_price:
            rec.t_margin = rec.total_unit_price - rec.total_cost
            rec.t_margin_percentage = (rec.t_margin / rec.total_unit_price) * 100

    @api.model
    def create(self, vals):
        if vals.get('seq', 'New') == 'New':
            # vals['seq'] = self.env['ir.sequence'].next_by_code('cost.estimation') or 'New'
            vals['seq'] = self.env['ir.sequence'].sudo().next_by_code('cost.estimation') or 'New'
        print("AAAA", vals)
        result = super(CostEst, self).create(vals)

        return result

    def button_compute(self):
        line_list = []
        for rec in self.cost_estimation_line:
            if rec.salable_product.id not in line_list:
                line_list.append(rec.salable_product.id)
        products_list = []
        for li in line_list:
            unit_cost_list = []
            descp_list = []
            for line in self.cost_estimation_line:
                if line.salable_product.id == li:
                    unit_cost_list.append(line.cost_item_cost_sp)
                    if line.cost_item_description:
                        descp_list.append(line.cost_item_description)
            t = ""
            if descp_list:
                for desc in descp_list:
                    t = t + '- ' + desc + '\n'

            if self.env['cost.product.line'].search([('id', '=', li)]).quantity > 0:
                quantity_line = self.env['cost.product.line'].search([('id', '=', li)]).quantity
            else:
                quantity_line = self.env['cost.product.line'].search([('id', '=', li)]).quantity_qn
            products_list.append((0, 0, {'idx_cost': self.id, 'cost_item_description': t, 'salable_product': li,
                                         'unit_cost': sum(unit_cost_list) / quantity_line}))

        self.products_line = False
        self.products_line = products_list

    def create_quotation(self):
        quotation = self.env['sale.order']
        quotation_description_product = self.env['ir.config_parameter'].sudo().get_param(
            'quotation_description_product') or False

        product_list = []
        for line in self.products_line:
            if quotation_description_product == 'sp':
                description = line.sp_desc
            else:
                description = line.cost_item_description
            print('line.taxes', line.taxes.ids)
            product_list.append((0, 0, {'product_id': line.salable_product.product_id.id,
                                        'name': description,
                                        'product_uom_qty': line.sp_quant,
                                        'price_unit': line.unit_price,
                                        'estim_line': line.id}))
        if not self.customer:
            raise ValidationError(_("Set Customer field value!"))
        quotation.create({'partner_id': self.customer.id,
                          'cost_estimation_ref': self.id,
                          'total_margin': self.t_margin,
                          'margin_percent': self.t_margin_percentage,
                          'total_cost': self.total_material_cost,
                          'wave_cost': self.total_cost,
                          'user_id': self.sales_person.id,
                          'team_id': self.sales_team.id,
                          'pricelist_id': self.customer.property_product_pricelist.id,
                          'opportunity_id': self.opportunity.id,
                          'work_country_id': self.opportunity.work_country_id.id,
                          'project_objective': self.opportunity.project_objective.id,
                          'parent_opportunity': self.opportunity.id,
                          'revenue_team_id': self.opportunity.revenue_bu.id,
                          'third_party_cost': self.third_party_cost,
                          'travel_expenses': self.travel_expenses,
                          'order_line': product_list})
        self.quotations_count = len(self.env['sale.order'].search([('cost_estimation_ref', '=', self.id)]))
        return {
            'name': _('Quotation'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'domain': [('id', '=',
                        self.env['sale.order'].search([('cost_estimation_ref', '=', self.id)], order='name desc',
                                                      limit=1).id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
        }

    def action_view_quotation(self):
        return {
            'name': _('Quotations'),
            'domain': [('cost_estimation_ref', '=', self.id)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    def submit(self):
        self.state = 'first_approval'
        self.accounting_installed = self.env['cost.estimation'].search([('accounting_installed', '=', True)],
                                                                       limit=1).accounting_installed

    def approve_1(self):
        self.state = 'second_approval'

    def approve_2(self):
        one_approved_cost_est = self.env['ir.config_parameter'].sudo().get_param('one_approved_cost_est') or False
        multiple_ce = self.search([('opportunity', '=', self.opportunity.id), ('state', '=', 'approved')])
        if one_approved_cost_est and (len(multiple_ce) >= 1):
            raise ValidationError(_("You can't Approve Multiple cost estimation "))
        else:
            cost_estimations = self.env['cost.estimation'].search(
                [('opportunity.id', '=', self.opportunity.id), ('state', 'not in', ['approved', 'rejected'])])
            cancel_non_conf_ce = self.env['ir.config_parameter'].sudo().get_param('cancel_non_conf_ce') or False

            if cancel_non_conf_ce:
                for rec in cost_estimations:
                    rec.state = 'cancelled'
            self.state = 'approved'

    def reject_1(self):
        self.state = 'rejected'

    def reject_2(self):
        self.state = 'rejected'

    def cancel(self):
        self.state = 'cancelled'

    def set_draft(self):
        self.state = 'draft'


class ProductsLine(models.Model):
    _name = 'products.line'

    salable_product = fields.Many2one('cost.product.line', string='Methodology', store=True, readonly=True)
    sp_desc = fields.Text(string="Description", related='salable_product.description', readonly=True)
    cost_item_description = fields.Text('CI Description', store=True, readonly=True)
    sp_quant = fields.Float(compute='_compute_quant', string='SS', default=1.0)
    sp_quant_ql = fields.Float(related='sp_quant', string='No of Units')
    taxes = fields.Many2many('account.tax', string='Taxes', domain=[('type_tax_use', '=', 'sale')])
    # taxes = fields.Many2many('account.tax', string='Taxes', default=lambda self: self.salable_product.product_id.taxes_id.ids, domain=[('type_tax_use', '=', 'sale')])
    unit_of_measure = fields.Many2one('uom.uom', string='UoM', related='salable_product.unit_of_measure', readonly=True)
    unit_cost = fields.Float(string="Unit Cost", store=True, readonly=True)
    total_cost = fields.Float(string="Total Cost", compute='_product_line_calculations', store=True)
    margin = fields.Float(string="Markup")
    subtotal = fields.Float(string="Subtotal", compute='_product_line_calculations')
    subtotal_taxed = fields.Float(string="Subtotal Taxed", compute="_product_line_calculations")
    unit_price = fields.Float(string="Unit Price", compute='_product_line_calculations')
    idx_cost = fields.Many2one('cost.estimation')

    fw_city = fields.Many2one('res.country.state', 'FW City', related='salable_product.fw_city')
    sec = fields.Selection(SEC, related='salable_product.sec', string='SEC')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')], related='salable_product.gender')
    age = fields.Char('Age', related='salable_product.age')

    @api.constrains('salable_product')
    def onch_sal(self):
        self.taxes = self.salable_product.product_id.taxes_id.ids

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            elif rec.salable_product.idx.research_type_name == 'QL':
                rec.sp_quant = rec.salable_product.quantity
            else:
                rec.sp_quant = 1.0

    @api.depends('unit_cost', 'sp_quant', 'margin', 'taxes')
    def _product_line_calculations(self):
        for rec in self:
            rec.subtotal_taxed = 0
            rec.total_cost = (rec.unit_cost * rec.sp_quant)
            rec.subtotal = rec.total_cost + (rec.total_cost * rec.margin / 100)
            rec.unit_price = rec.unit_cost + (rec.unit_cost * rec.margin / 100)
            tax_list = []
            if rec.taxes:
                for tax in rec.taxes:
                    tax_list.append(tax.amount)
                rec.subtotal_taxed = rec.subtotal * (sum(tax_list) / 100)


class CostEstimationLine(models.Model):
    _name = 'cost.estimation.line'

    salable_product = fields.Many2one('cost.product.line', string='Salable Product',
                                      domain=lambda self: self._domain_product_id())
    sp_desc = fields.Text(string="SP Description", related='salable_product.description', readonly=True)
    sp_quant = fields.Float(string="SP Qty", related='salable_product.quantity_qn')
    cost_item = fields.Many2one('product.template', string="Cost Item")
    product_rate=fields.Float(string='Product Rate' ,related='cost_item.standard_price')
    cost_item_description = fields.Text('CI Description')
    cost_item_type = fields.Selection([('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead')],
                                      string="CI Type", required=True, default='material')
    cost_item_quant_sp = fields.Float(string="CI Qty/SP", default='1')
    cost_item_cost_currency = fields.Float(string="CI Unit Cost(Currency)", default='1')
    fx = fields.Float('Fx Rate', related='idx_cost.fx', store=True, digits=(12, 4), readonly=True)
    taxes = fields.Many2many('account.tax', string='Taxes', default=False, domain=[('type_tax_use', '=', 'purchase')])
    cost_item_unit_cost = fields.Float(string="CI Unit Cost", compute='_calculations')
    cost_item_cost_sp = fields.Float(string="CI Cost/SP", compute='_calculations')
    total_cost_item_quantity = fields.Float(string='Total CI Qty', compute='_calculations')
    total_cost_item_cost = fields.Float(string='CI Total Cost', compute='_calculations')
    cost_item_uom_id = fields.Many2one('uom.uom', string='CI Unit of Measure', related='cost_item.uom_id',
                                       readonly=True)

    idx_cost = fields.Many2one('cost.estimation')

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            if rec.salable_product.idx.research_type_name == 'QL':
                rec.sp_quant = rec.salable_product.quantity

    @api.depends('cost_item_cost_currency', 'taxes', 'fx', 'cost_item_quant_sp', 'sp_quant')
    def _calculations(self):
        for rec in self:
            taxes_list = []
            for tax in rec.taxes:
                taxes_list.append(tax.amount)
            if rec.fx > 0:
                rec.cost_item_unit_cost = (rec.cost_item_cost_currency / rec.fx) + (
                        (rec.cost_item_cost_currency / rec.fx) * (sum(taxes_list) / 100))
            else:
                rec.cost_item_unit_cost = rec.cost_item_cost_currency + (
                        rec.cost_item_cost_currency * (sum(taxes_list) / 100))

            rec.cost_item_cost_sp = rec.cost_item_unit_cost * rec.cost_item_quant_sp
            rec.total_cost_item_quantity = rec.cost_item_quant_sp * rec.sp_quant
            # rec.total_cost_item_cost = rec.cost_item_cost_sp * rec.sp_quant
            rec.total_cost_item_cost = rec.cost_item_unit_cost * rec.cost_item_quant_sp

    @api.onchange('salable_product')
    def onchange_salable_product(self):
        domain = {'salable_product': [('id', 'in', self.idx_cost.opportunity.product_line.ids)]}
        return {'domain': domain}

    @api.onchange('cost_item')
    def onchange_cost_item(self):
        # self.cost_item_description = self.cost_item.description_picking
        self.cost_item_uom_id = self.cost_item.uom_id.id
        self.cost_item_type = self.cost_item.cost_item_type

    def _domain_product_id(self):
        if self.env.context.get('active_id'):
            opportunity = self.env['crm.lead'].search(
                [('id', '=', self.env.context.get('active_id'))])

            return "[('id', 'in', %s)]" % opportunity.product_line.ids

    @api.model
    def create(self, vals):
        if 'cost_item' in vals and not vals.get('cost_item_quant_sp'):
            product = self.env['product.template'].browse(vals['cost_item'])
            vals['cost_item_quant_sp'] = product.standard_price
        return super(CostEstimationLine, self).create(vals)

    class CostEstimationXlsx(models.AbstractModel):
        _name = 'report.cost_estimation.report_cost_estimation_xlsx'
        _inherit = 'report.report_xlsx.abstract'

        def safe_value(self, val):
            """Helper to safely convert any field to printable string or number"""
            if val is None:
                return ''
            if hasattr(val, 'name'):
                return val.name
            return val if isinstance(val, (int, float, str)) else str(val)

        def generate_xlsx_report(self, workbook, data, objs):
            for obj in objs:
                sheet = workbook.add_worksheet("Cost Estimation")
                bold = workbook.add_format({'bold': True})
                row = 0

                # Header Section
                sheet.write(row, 0, "Header Information", bold)
                row += 2

                headers = [
                    ("Customer", obj.customer),
                    ("Opportunity", obj.opportunity),
                    ("Sales Team", obj.sales_team),
                    ("Sales Person", obj.sales_person),
                    ("Price List", obj.price_list),
                    ("Fix Rate", obj.fx),
                    ("Estimation Date", obj.estimate_date),
                    ("Budget Date From", obj.budget_date_from),
                    ("Budget", obj.budget),
                    ("Company", obj.company_id),
                    ("Sale Order", obj.sale_order),
                    ("Total Margin", obj.t_margin),
                    ("Margin Percent", obj.t_margin_percentage),
                    ("Research Type", obj.research_type),
                    ("Waves", obj.waves),
                    ("Cost of Waves", obj.cost_of_waves),
                    ("CPI", obj.cpi_x),
                    ("Third Party Cost", obj.third_party_cost),
                    ("Travel Expense", obj.travel_expenses),
                    ("Markup", obj.markup),
                ]

                for h, v in headers:
                    sheet.write(row, 0, h)
                    sheet.write(row, 1, self.safe_value(v))
                    row += 1

                # Table Title
                row += 1
                sheet.write(row, 0, "Cost Items", bold)
                row += 1

                # Table headers
                table_headers = [
                    "Salable Product", "SP Description", "Sp Qty", "Cost Item", "Product Rate",
                    "CI Description", "CI Type", "CI Qty/Sp", "CI Unit Cost",
                    "CI Cost/SP", "CI Total Cost", "Budgetary Position"
                ]
                for col, h in enumerate(table_headers):
                    sheet.write(row, col, h, bold)
                row += 1

                # Table data
                for line in obj.cost_estimation_line:
                    sheet.write(row, 0, self.safe_value(line.salable_product))
                    sheet.write(row, 1, self.safe_value(line.sp_desc))
                    sheet.write(row, 2, line.sp_quant or 0)
                    sheet.write(row, 3, self.safe_value(line.cost_item))
                    sheet.write(row, 4, line.product_rate or 0)
                    sheet.write(row, 5, self.safe_value(line.cost_item_description))
                    sheet.write(row, 6, self.safe_value(line.cost_item_type))
                    sheet.write(row, 7, line.cost_item_quant_sp or 0)
                    sheet.write(row, 8, line.cost_item_unit_cost or 0)
                    sheet.write(row, 9, line.cost_item_cost_sp or 0)
                    sheet.write(row, 10, line.total_cost_item_cost or 0)
                    sheet.write(row, 11, self.safe_value(line.budgetary_position))
                    row += 1

                # Summary
                row += 1
                sheet.write(row, 0, "Summary", bold)
                row += 1
                sheet.write(row, 0, "Total Materials Cost")
                sheet.write(row, 1, obj.total_material_cost or 0)

                sheet.write(row, 4, "Gross Margin Value")
                sheet.write(row, 5, obj.gross_margin_value or 0)
                row += 1

                sheet.write(row, 0, "Total Labour Cost")
                sheet.write(row, 1, obj.total_labour_cost or 0)

                sheet.write(row, 4, "Gross Margin Percentage %")
                sheet.write(row, 5, obj.gross_margin_percentage or 0)
                row += 1

                sheet.write(row, 0, "Cost / Waves")
                sheet.write(row, 1, obj.total_cost or 0)

                sheet.write(row, 4, "Operating Profit")
                sheet.write(row, 5, obj.operating_profit or 0)
                row += 1

                sheet.write(row, 0, "Total Selling Price")
                sheet.write(row, 1, obj.total_unit_price or 0)

                sheet.write(row, 4, "Operating Profit Percentage %")
                sheet.write(row, 5, obj.operating_profit_percentage or 0)
                row += 1

                sheet.write(row, 4, "CPI")
                sheet.write(row, 5, obj.cpi or 0)
