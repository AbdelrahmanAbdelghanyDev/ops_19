# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class EstimationMethodology(models.Model):
    _name = 'estimation.methodology'
    _rec_name = 'name'
    _description = 'Estimation Methodology'

    name = fields.Char(string='Name', required=1)
    type = fields.Char(string='Type')

class CostEstimation(models.Model):
    _inherit = 'cost.estimation'

    time_estimation_ids = fields.One2many(comodel_name="time.estimation.line", copy=True,
                                          inverse_name="idx_time")

    same_methodology_count = fields.Integer(compute='get_same_methodology_count')
    methodology_id = fields.Many2one(comodel_name="estimation.methodology", string="Methodology Type")

    def get_same_methodology_estimation(self):
        self.ensure_one()
        if self.id:
            return {
                "type": "ir.actions.act_window",
                "name": "Same Methodology Estimation",
                "view_mode": "tree",
                "res_model": "cost.estimation",
                "domain": [('methodology_id', '=', self.methodology_id.id), ('id', '!=', self.id)],
                "context": "{'create': False,'tree_view_ref':'time_cost_estimation.similar_estimation_tree'}",
                # 'view_id': self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                # 'views': [(self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                #            'tree')],
            }
        else:
            return {
                "type": "ir.actions.act_window",
                "name": "Same Methodology Estimation",
                "view_mode": "tree",
                "res_model": "cost.estimation",
                "domain": [('methodology_id', '=', self.methodology_id.id)],
                "context": "{'create': False,'tree_view_ref':'time_cost_estimation.similar_estimation_tree'}",
                # 'view_id': self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                # 'views': [(self.env.ref(
                #     'time_cost_estimation.similar_estimation_tree').id,
                #            'tree')],
            }

    @api.depends('methodology_id')
    def get_same_methodology_count(self):
        for rec in self:
            if rec.id:
                rec.same_methodology_count = self.env['cost.estimation'].search_count([('methodology_id',
                                                                                        '=', rec.methodology_id.id),
                                                                                       ('id', '!=', rec.id)])
            else:
                rec.same_methodology_count = self.env['cost.estimation'].search_count([('methodology_id',
                                                                                        '=', rec.methodology_id.id)])

    gross_margin_value = fields.Float(string="Gross Margin Value", compute='get_estimation_margins')
    gross_margin_percentage = fields.Float(string="Gross Margin Percentage %", compute='get_estimation_margins')
    operating_profit = fields.Float(string="Operating Profit", compute='get_estimation_margins')
    operating_profit_percentage = fields.Float(string="Operating Profit Percentage %", compute='get_estimation_margins')
    cpi = fields.Float(string="CPI", compute='get_estimation_margins')


    @api.depends('total_unit_price', 'total_material_cost', 'total_cost', 'opportunity.sample_size')
    def get_estimation_margins(self):
        for rec in self:
            rec.gross_margin_value = rec.total_unit_price - rec.total_material_cost
            rec.gross_margin_percentage = (rec.gross_margin_value / rec.total_unit_price) \
                if rec.total_unit_price != 0 else 0
            rec.operating_profit = rec.total_unit_price - rec.total_cost
            rec.operating_profit_percentage = (rec.operating_profit / rec.total_unit_price) \
                if rec.total_unit_price != 0 else 0
            rec.cpi = rec.total_unit_price / rec.opportunity.sample_size if rec.opportunity.sample_size != 0 else 0

    @api.depends('cost_estimation_line.total_cost_item_cost',
                 'time_estimation_ids.total_cost_item_cost',
                 'total_unit_price', 'total_cost', 'third_party_cost',
                 'travel_expenses')
    def _compute_total(self):
        for rec in self:
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

            for line in rec.time_estimation_ids:
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





class TimeEstimationLine(models.Model):
    _name = 'time.estimation.line'

    salable_product = fields.Many2one('cost.product.line', string='Salable Product',
                                      domain=lambda self: self._domain_product_id())
    sp_desc = fields.Text(string="SP Description", related='salable_product.description', readonly=True)
    sp_quant = fields.Float(string="SP Qty", compute='_compute_quant')
    cost_item = fields.Many2one('product.template', string="Cost Item")
    cost_item_description = fields.Text('CI Description')
    cost_item_type = fields.Selection([('material', 'Material'), ('labour', 'Labour'), ('overhead', 'Overhead')],
                                      string="CI Type", required=True, default='material')
    cost_item_quant_sp = fields.Float(string="CI Qty/SP", default='1')
    cost_item_cost_currency = fields.Float(string="CI Unit Cost(Currency)", default='0')
    fx = fields.Float('Fx Rate', related='idx_time.fx', store=True, digits=(12, 4), readonly=True)
    taxes = fields.Many2many('account.tax', string='Taxes', default=False, domain=[('type_tax_use', '=', 'purchase')])
    cost_item_unit_cost = fields.Float(string="CI Unit Cost", compute='_calculations')
    cost_item_cost_sp = fields.Float(string="CI Cost/SP", compute='_calculations')
    total_cost_item_quantity = fields.Float(string='Total CI Qty', compute='_calculations')
    total_cost_item_cost = fields.Float(string='CI Total Cost', compute='_calculations')
    cost_item_uom_id = fields.Many2one('uom.uom', string='CI Unit of Measure', related='cost_item.uom_id',
                                       readonly=True)

    idx_time = fields.Many2one('cost.estimation')

    budgetary_position = fields.Many2one('account.budget.post', string='Budgetary Position')

    @api.onchange('cost_item')
    def onchange_cost_item_budget(self):
        if self.cost_item.budgetary_position:
            self.budgetary_position = self.cost_item.budgetary_position.id

    @api.depends('salable_product')
    def _compute_quant(self):
        for rec in self:
            rec.sp_quant = 0
            if rec.salable_product.idx.research_type_name == 'QN':
                rec.sp_quant = rec.salable_product.quantity_qn
            if rec.salable_product.idx.research_type_name == 'QL':
                rec.sp_quant = rec.salable_product.quantity
            else:
                rec.sp_quant = 0

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
        domain = {'salable_product': [('id', 'in', self.idx_time.opportunity.product_line.ids)]}
        return {'domain': domain}

    @api.onchange('cost_item')
    def onchange_cost_item(self):
        self.cost_item_description = self.cost_item.description_picking
        self.cost_item_uom_id = self.cost_item.uom_id.id
        self.cost_item_type = self.cost_item.cost_item_type

    def _domain_product_id(self):
        if self.env.context.get('active_id'):
            opportunity = self.env['crm.lead'].search(
                [('id', '=', self.env.context.get('active_id'))])

            return "[('id', 'in', %s)]" % opportunity.product_line.ids


class ProductTemplate(models.Model):
    _inherit = "product.template"

    time_estimation_ids = fields.One2many('product.time.cost.line', 'idt')


class ProductTimeCostLine(models.Model):
    _name = 'product.time.cost.line'
    _description = 'Product Time Cost Line'

    product_id = fields.Many2one('product.template', string='Product')
    description = fields.Text('Description', related='product_id.description_picking')
    qty = fields.Float('Quantity')
    uom = fields.Many2one('uom.uom', string='Unit of Measure')
    cost_item_type = fields.Selection(related='product_id.cost_item_type', string="CI Type")
    idt = fields.Many2one('product.template')
    budgetary_position = fields.Many2one('account.budget.post', related='product_id.budgetary_position',
                                         string='Budgetary Position')

    @api.onchange('product_id')
    def _onch_proj(self):
        self.uom = self.product_id.uom_id.id