# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from lxml import etree

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


################################################ QL ######################################
class CRMProductLine(models.Model):
    _name = 'cost.product.line'
    _rec_name = 'product_id'

    description = fields.Text(string="Description", compute='_compute_description')
    product_id = fields.Many2one('product.product', string='Methodology')
    custom_company_id = fields.Integer(compute='_run',
                                                   default=lambda self: self.env['res.company']._company_default_get(
                                                       'sale.order').id)

    def _run(self):
        for rec in self:
            rec.custom_company_id = rec.env['res.company']._company_default_get('sale.order').id

    fw_country = fields.Many2one('res.country')
    fw_city = fields.Many2one('res.country.state')
    sec = fields.Selection(SEC, string='SEC')
    quantity = fields.Float(string='No of Units')

    quantity_qn = fields.Float(string='ss', default=1)
    mp_of_respondants = fields.Float(string='No of Respondants')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')])
    age = fields.Char('Age')
    idx = fields.Many2one('crm.lead')
    unit_of_measure = fields.Many2one('uom.uom', string='UoM', readonly=True)
    # quantity = fields.Float(string='ss')
    # data_capture = fields.Selection([('capi', 'CAPI'),
    #                                  ('papi', 'PAPI'), ('cati', 'CATI'), ('online', 'Online')])

    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI'),
                                     ('cati', 'CATI'),
                                     ('online', 'Online')])
    research_type_id_crm = fields.Many2one(related='idx.research_type_id')
    research_type_id_crm_name = fields.Char(related='research_type_id_crm.name')

    @api.onchange('product_id')
    def _compute_description(self):
        for rec in self:
            product = rec.product_id.name or ''
            fw_city = rec.fw_city.name or ''
            sec = rec.sec or ''

            description = ''  # ✅ ALWAYS assign

            if rec.idx and rec.idx.research_type_name == 'QN':
                description = f'{product},{fw_city}'
            elif rec.idx and rec.idx.research_type_name == 'QL':
                description = f'{product},{fw_city},{sec}'

            rec.description = description
            rec.unit_of_measure = rec.product_id.uom_id.id if rec.product_id else False


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'
    research_type_id = fields.Many2one('product.category', required=True,
                                       domain="[('company_id', '=', company_id), ('name', 'in', ['QL', 'QN'])]")

    product_line = fields.One2many('cost.product.line', 'idx')


# class CostEstimation(models.Model):
#     _inherit = 'cost.estimation'


class QuotationC(models.Model):
    _inherit = 'sale.order'

    cost_estimation_ref = fields.Many2one('cost.estimation', string='Cost Estimation Ref')
    total_cost = fields.Float('Cost / Waves')
    total_margin = fields.Float('Total Margin', digits=(12, 4), )
    margin_percent = fields.Float('Margin Percent', digits=(12, 4), )
    budget_currency_x = fields.Many2one('res.currency', string="Budget Currency", readonly=True, store=True)
    budget_total_x = fields.Float(compute='_compute_budget_total_x', string="Cost (budget currency)")
    margin_x = fields.Float(compute='_compute_margin_x', store=True)
    margin_percentage_x = fields.Char(compute='_compute_margin_x', store=True)
    margin_after_travel_x = fields.Float(compute='_compute_margin_x', store=True)
    margin_percentage_after_x = fields.Char(compute='_compute_margin_x', store=True)
    contribution_profit_x = fields.Float(related='margin_x', store=True)
    contribution_margin_x = fields.Char(related='margin_percentage_x', store=True)
    travel_expenses = fields.Float('Travel Expense')
    travel_expenses = fields.Float()
    third_party_cost = fields.Float(string="Third Party Cost", track_visibility='onchange')
    budget_total = fields.Float(compute='_compute_budget_total')
    budget_currency = fields.Many2one('res.currency', string="Budget Currency", readonly=False,
                                      related='opportunity_cost_estimation.currency_id')

    @api.depends('opportunity_total_cost', 'budget_currency', )
    def _compute_budget_total(self):

        for rec in self:
            budget_rates = rec.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.budget_currency.id)], limit=1)
            print("the budget rate", budget_rates)
            company_rates = rec.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.pricelist_id.currency_id.id)],
                limit=1)
            print("the company rate", company_rates)

            if rec.pricelist_id.currency_id.rate:
                if not budget_rates:
                    the_budget_rate = 1

                else:
                    the_budget_rate = budget_rates.rate

                if not company_rates:
                    the_company_rate = 1

                else:
                    the_company_rate = company_rates.rate

                first_ex = rec.opportunity_total_cost / the_budget_rate
                print("first_ex", first_ex)
                print("66666666666666666666666", rec.opportunity_total_cost)
                my_budget_total = first_ex * the_company_rate

                rec.update({'budget_total': my_budget_total})

            else:
                rec.update({'budget_total': 0})
            # self.write({'cp_after_travel_custom': self.budget_total})

    @api.constrains('cost_estimation_ref')
    def const_est(self):
        for rec in self:
            print('rec', rec)
            if rec.cost_estimation_ref:
                rec.budget_currency_x = rec.cost_estimation_ref.price_list.currency_id

    # @api.one
    # @api.constrains('budget_total_x', 'amount_untaxed', 'travel_expenses', 'third_party_cost')
    @api.depends('budget_total_x', 'amount_untaxed', 'travel_expenses', 'third_party_cost')
    def _compute_margin_x(self):
        for rec in self:
            rec.margin_x = rec.amount_untaxed - (
                rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.third_party_cost
            if rec.amount_untaxed == 0:
                rec.margin_percentage_x = '-Inf %'
            else:
                rec.margin_percentage_x = str(
                    round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'

            rec.margin_after_travel_x = rec.amount_untaxed - \
                                        (
                                            rec.budget_total_x if rec.budget_total_x else rec.budget_total) - rec.travel_expenses - rec.third_party_cost
            if rec.amount_untaxed == 0:
                rec.margin_percentage_after_x = '-Inf %'
            else:
                rec.margin_percentage_after_x = str(
                    round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'
            print("YYYY", rec.amount_untaxed, rec.budget_total, rec.travel_expenses, rec.third_party_cost)

    # @api.one
    @api.depends('total_cost', 'budget_currency_x', )
    def _compute_budget_total_x(self):
        for rec in self:
            budget_rates = rec.env['res.currency.rate'].search(
                [('company_id', '=', rec.company_id.id), ('currency_id', '=', rec.pricelist_id.currency_id.id)],
                limit=1)

            rec.budget_total_x = budget_rates.rate * rec.total_cost

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):

        res = super(QuotationC, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        eview = etree.fromstring(res['arch'])
        quotation = self.env['ir.config_parameter'].sudo().get_param('quotation_restriction') or False
        if quotation and view_type:
            for node in eview.xpath("//tree"):
                node.set('create', "false")
            for node in eview.xpath("//form"):
                node.set('create', "false")
        else:
            for node in eview.xpath("//form"):
                node.set('create', "true")
            for node in eview.xpath("//tree"):
                node.set('create', "true")
        res['arch'] = etree.tostring(eview)
        return res

    def action_confirm(self):
        res = super(QuotationC, self).action_confirm()
        if self.cost_estimation_ref:
            sale_order = self.env['sale.order'].search(
                [('cost_estimation_ref', '=', self.cost_estimation_ref.id), ('state', '=', 'sale')])
            if len(sale_order) > 1:
                raise ValidationError(_("There is a sale order for this cost estimation"))
            else:
                self.cost_estimation_ref.sale_order = self.id
        return res
