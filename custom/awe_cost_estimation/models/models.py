# -*- coding: utf-8 -*-

from odoo import models, fields, api

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


class ProductCategoryInherit(models.Model):
    _inherit = 'product.category'

    company_id = fields.Many2one('res.company')


class CustomCRMLead(models.Model):
    _inherit = 'crm.lead'

    # @api.multi
    # def _get_domain_research(self):
    #
    #     return [('company_id', '=', self.env.user.company_id.id), ('name', 'in', ['QL', 'QN'])]

    executive_team_id = fields.Many2one('executive.team')
    revenue_team_id = fields.Many2one('revenue.team')
    project_objective = fields.Many2one('project.objective')
    working_country = fields.Many2one(
        'res.country', string="Filed Work Country")
    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )
    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    transcript_lang = fields.Char(
        string='Transcript Language'
    )
    length_of_interview = fields.Char('Length of Interview')
    length_of_interview_sel = fields.Selection(
        [('15', '15'), ('15-30', '15-30'), ('30-45', '40-45'), ('45-60', '45-60'), ('60', '60+')],
        string='Length of Interview in Minutes'
    )

    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    dp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    reporting = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    presentation = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])
    project_type = fields.Selection([
        ('0', 'Adhoc'),
        ('1', 'Tracker'),
        ('2', 'Desk Research'),
        ('3', 'syndicated')
    ])
    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology', compute='_compute_methodology', readonly=False)
    methodology_desc = fields.Char('Methodology Desc')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Float('Sample Size', compute='_compute_sample_size', readonly=True)
    sample_struct_per_reg = fields.Char('Sample Structure per Region')
    sample_struct_per_sec = fields.Char('Sample Structure per SEC')
    sample_struct_per_age = fields.Char('Sample Structure per Age')
    sample_struct_per_gen = fields.Char('Sample Structure per Gender')
    sample_struct_per_bra = fields.Char('Sample Structure per Brand')
    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')
    client_attendence_region_ids = fields.Many2many(
        'res.country.state', relation="awe_lead_country_rel",
        string='Client Attendance Region'
    )
    # research_type_id = fields.Many2one('product.category', required=True, domain=_get_domain_research)
    research_type_name = fields.Char(
        'Reaseach Type Name',
        related="research_type_id.name",
        readonly=True,
    )
    research_type_company = fields.Many2one('res.company', related="research_type_id.company_id", readonly=True, )

    details = fields.Text("Other Details:")
    details_ql = fields.Text("Other Details:")
    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI')])

    project_objective = fields.Many2one('project.objective')
    restore_done = fields.Boolean(string="restore done", default=False)

    # @api.multi
    def restore_ql(self):
        records = self.env['crm.lead'].search([])
        for record in records:
            for line in record.pdt_line:
                if line.pdt_crm_research_id == 'QL':
                    print("hhahahahahahhahhah", line.pdt_crm_2, line.pdt_crm)
                    line.pdt_crm_2 = line.pdt_crm

            record.restore_done = True

    @api.onchange('pdt_line', 'product_line')
    # @api.multi
    def _compute_sample_size(self):
        total = 0.0

        for record in self:

            for rec in record.pdt_line:
                total += rec.product_uom_qty
            for rec_qn in record.product_line:
                quantity = 0.0
                if record.research_type_name == 'QN':
                    quantity = rec_qn.quantity_qn
                if record.research_type_name == 'QL':
                    quantity = rec_qn.quantity
                total += quantity
            record.sample_size_text = total

    @api.onchange('product_line')
    # @api.multi
    def _compute_methodology(self):
        for rec in self:
            if rec.product_line and rec.product_line[0].product_id:
                rec.methodology = rec.product_line[0].product_id.name or ""
            if rec.pdt_line:
                rec.methodology = rec.pdt_line[0].product_id.name
        # if self.product_line and not self.pdt_line:
        #     for record in self:
        #         if record.cost_estimation_number > 0 and record.product_line:
        #             record.methodology = record.product_line[0].product_id.name
        #         else:
        #             if record.product_line:
        #                 record.methodology = record.product_line[0].product_id.name
        # if self.pdt_line:
        #     for record in self:
        #         record.methodology = record.pdt_line[0].product_id.name

    @api.onchange('research_type_id')
    def onchange_research_id(self):
        obj = self.research_type_id
        while True:
            if not obj.parent_id:
                self.research_type_name = obj.name
                return {'research_type_name': obj.name}
            else:
                # print()
                obj = obj.parent_id

    def new_cost_estimation(self):
        vals = {'partner_id': self.partner_id.id,
                'client_attendence_region_ids': [(6, 0, self.client_attendence_region_ids.ids)],
                'viewing_facility': self.viewing_facility,
                'transcript': self.transcript,
                'no_of_client_attendees': self.no_of_client_attendees,
                'translation': self.translation,
                'ex_transcript': self.ex_transcript,
                'printing_material': self.printing_material,
                'transcript_lang': self.transcript_lang,
                'other_translation': self.other_translation,
                'no_of_units_attendees': self.no_of_units_attendees,
                'user_id': self.user_id.id,
                'parent_opportunity': self.id,
                'pricelist_id': self.partner_id.property_product_pricelist and self.partner_id.property_product_pricelist.id or False,
                'research_type': self.research_type,
                'approach': self.approach,
                'methodology': self.methodology,
                'number_of_legs': self.number_of_legs,
                'sample_size': self.sample_size,
                'age': self.age,
                'gender': self.gender,
                'sec': self.sec,
                'region': self.region,
                'usership': self.usership,
                'moub': self.moub,
                'length_of_interview': self.length_of_interview,
                'dp': self.dp,
                'reporting': self.reporting,
                'presentation': self.presentation,
                'client_attendance': self.client_attendance,
                'details': self.details,
                'estimation_type': self.research_type_id.id,
                }
        estimation = self.env['opportunity.cost.estimation'].create(vals)
        product = self.env['crm.product_line']
        for i in self.pdt_line:
            product_value = {
                'pdt_cost_estimation': estimation.id,
                'product_id': i.product_id.id,
                'name': i.name,
                'product_uom_qty': i.product_uom_qty,
                'uom_id': i.uom_id.id,
                'category': i.category.id,
                'fw_country': i.fw_country.id,
                'project_objective': i.project_objective.id,
                'research_type': i.research_type,
                'data_capture': i.data_capture,
                'gender': i.gender,
                'sec': i.sec,
                'age': i.age,
                'number_of_legs': i.number_of_legs,
                'client_attendance': i.client_attendance,
            }

            product.create(product_value)

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'opportunity.cost.estimation',
            'target': 'current',
            'res_id': estimation.id,
            'views': [(self.env.ref(
                'custom_opportunity_cost_estimation_v11.opportunity_cost_estimation_form').id,
                       'form')],
        }

    # @api.multi
    def allocate_salesman(self, user_ids=None, team_id=False, executive_team_id=False, revenue_team_id=False):
        """ Assign salesmen and salesteam to a batch of leads.  If there are more
            leads than salesmen, these salesmen will be assigned in round-robin.
            E.g.: 4 salesmen (S1, S2, S3, S4) for 6 leads (L1, L2, ... L6).  They
            will be assigned as followed: L1 - S1, L2 - S2, L3 - S3, L4 - S4,
            L5 - S1, L6 - S2.

            :param list ids: leads/opportunities ids to process
            :param list user_ids: salesmen to assign
            :param int team_id: salesteam to assign
            :return bool
        """
        index = 0
        for lead in self:
            value = {}
            if team_id:
                value['team_id'] = team_id
            if executive_team_id:
                value['executive_team_id'] = executive_team_id
            if revenue_team_id:
                value['revenue_team_id'] = revenue_team_id
            if user_ids:
                value['user_id'] = user_ids[index]
                # Cycle through user_ids
                index = (index + 1) % len(user_ids)
            if value:
                lead.write(value)
        return True


class CustomSaleOrder(models.Model):
    _inherit = 'sale.order'
    executive_team_id = fields.Many2one('executive.team')
    revenue_team_id = fields.Many2one('revenue.team', track_visibility='onchange')

    margin = fields.Float(compute='_compute_margin')
    margin_percentage = fields.Char(compute='_compute_margin')
    contribution_profit = fields.Float(related='margin', store=True)
    contribution_margin = fields.Char(related='margin_percentage', store=True)

    travel_expenses = fields.Float()
    margin_after_travel = fields.Float(compute='_compute_margin')
    margin_percentage_after = fields.Char(compute='_compute_margin')
    third_party_cost = fields.Float(string="Third Party Cost", track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=False)
    budget_total = fields.Float(compute='_compute_budget_total')
    budget_currency = fields.Many2one('res.currency', string="Budget Currency", readonly=False,
                                      related='opportunity_cost_estimation.currency_id')

    # @api.one
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

    # @api.one
    @api.depends('budget_total', 'amount_untaxed', 'travel_expenses')
    def _compute_margin(self):
        for rec in self:
            if rec.budget_total >= 0:
                rec.margin = rec.amount_untaxed - rec.budget_total - rec.third_party_cost
                if rec.amount_untaxed == 0:
                    rec.margin_percentage = '-Inf %'
                else:
                    rec.margin_percentage = str(
                        round(rec.margin / rec.amount_untaxed * 100.0, 2)) + ' %'
                    rec.margin_percentage_x = '-Inf %'
                rec.margin_after_travel = rec.amount_untaxed - \
                                          rec.budget_total - rec.travel_expenses - rec.third_party_cost
                rec.margin_after_travel_x = 0

                if rec.amount_untaxed == 0:
                    rec.margin_percentage_after = '-Inf %'
                else:
                    rec.margin_percentage_after = str(
                        round(rec.margin_after_travel / rec.amount_untaxed * 100.0, 2)) + ' %'
                    rec.margin_percentage_after_x = '-Inf %'
                    #################################################################################################

            if rec.budget_total_x > 0 and rec.budget_total == 0:
                rec.margin_x = rec.amount_untaxed - rec.budget_total_x - rec.third_party_cost

                if rec.amount_untaxed == 0:
                    rec.margin_percentage_x = '-Inf %'
                else:
                    rec.margin_percentage_x = str(
                        round(rec.margin_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                    rec.margin_percentage = '-Inf %'

                rec.margin_after_travel_x = rec.amount_untaxed - \
                                            rec.budget_total_x - rec.travel_expenses - rec.third_party_cost
                rec.margin_after_travel = 0
                if rec.amount_untaxed == 0:
                    rec.margin_percentage_after_x = '-Inf %'
                else:
                    rec.margin_percentage_after_x = str(
                        round(rec.margin_after_travel_x / rec.amount_untaxed * 100.0, 2)) + ' %'
                    rec.margin_percentage_after = '-Inf %'
            # self.write({'total_budget_custom': self.margin_after_travel})
            # print('xxxxxxxxxxxxxxxxxx', self.total_budget_custom, self.cp_after_travel_custom)

    # @api.onchange('opportunity_cost_estimation')
    # def _onchange_opportunity(self):
    #     print (self.opportunity_cost_estimation)
    #     self.budget_total = self.opportunity_total_cost_2 * self.pricelist_id.currency_id.rate

    # @api.depends('opportunity_total_cost_2','pricelist_id')
    # def budget_cost(self):
    #
    #     self.budget_total=self.opportunity_total_cost_2*self.pricelist_id.currency_id.rate


class CustomLeadtoOpportunity(models.TransientModel):
    _inherit = 'crm.lead2opportunity.partner'
    executive_team_id = fields.Many2one('executive.team')
    revenue_team_id = fields.Many2one('revenue.team')

    # @api.multi
    def _convert_opportunity(self, vals):
        self.ensure_one()

        res = False

        leads = self.env['crm.lead'].browse(vals.get('lead_ids'))
        for lead in leads:
            self_def_user = self.with_context(default_user_id=self.user_id.id)
            partner_id = self_def_user._create_partner(
                lead.id,
                self.action,
                vals.get('partner_id') or lead.partner_id.id
            )
            res = lead.convert_opportunity(partner_id, [], False)
        user_ids = vals.get('user_ids')

        leads_to_allocate = leads
        if self._context.get('no_force_assignation'):
            leads_to_allocate = leads_to_allocate.filtered(
                lambda lead: not lead.user_id)

        if user_ids:
            leads_to_allocate.allocate_salesman(
                user_ids,
                team_id=(vals.get('team_id')),
                executive_team_id=(
                    vals.get('executive_team_id')),
                revenue_team_id=(vals.get('revenue_team_id')),
            )

        return res

    # @api.multi
    def action_apply(self):
        """ Convert lead to opportunity or merge lead and opportunity and open
            the freshly created opportunity view.
        """
        self.ensure_one()
        values = {
            'team_id': self.team_id.id,
            'executive_team_id': self.executive_team_id.id,
            'revenue_team_id': self.revenue_team_id.id,
        }

        if self.partner_id:
            values['partner_id'] = self.partner_id.id

        if self.name == 'merge':
            leads = self.opportunity_ids.merge_opportunity()
            if leads.type == "lead":
                values.update(
                    {'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
                self.with_context(
                    active_ids=leads.ids)._convert_opportunity(values)
            elif not self._context.get('no_force_assignation') or not leads.user_id:
                values['user_id'] = self.user_id.id
                leads.write(values)
        else:
            leads = self.env['crm.lead'].browse(
                self._context.get('active_ids', []))
            values.update(
                {'lead_ids': leads.ids, 'user_ids': [self.user_id.id]})
            self._convert_opportunity(values)

        return leads[0].redirect_opportunity_view()


# class ProjectObjective(models.Model):
#     _name = 'project.objective'
#
#     name = fields.Char()


class CustomSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    no_of_waves = fields.Integer(default=1)  # Based on customer request.
    no_of_units = fields.Float(default=1)  # Based on customer request.
    # Based on customer request.
    price_subtotal_new = fields.Float(compute='_amount_subtotal_new')
    margin = fields.Float(compute='_compute_margin')
    margin_percentage = fields.Char(compute='_compute_margin')

    # @api.one
    @api.depends('product_id')
    def _compute_margin(self):
        for rec in self:
            rec.margin = \
                rec.product_id.lst_price - rec.product_id.standard_price
            if rec.product_id.standard_price == 0:
                rec.margin_percentage = 'Inf'
            else:
                rec.margin_percentage = str(
                    1.0 * (rec.margin / rec.product_id.standard_price) * 100.0)

    @api.depends('no_of_units', 'product_uom_qty', 'price_unit')
    def _amount_subtotal_new(self):
        for i in self:
            i.price_subtotal_new = \
                i.no_of_units * i.product_uom_qty * i.price_unit

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'no_of_waves', 'price_subtotal_new',
                 'no_of_units')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(
                price * line.no_of_units * line.no_of_waves,
                line.order_id.currency_id,
                line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id
            )
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': line.price_subtotal_new * line.no_of_waves,
            })


class LeadProductLine(models.Model):
    _inherit = 'crm.product_line'

    breif = fields.Char()
    fw_country = fields.Many2one('res.country.state')
    project_objective = fields.Many2one('project.objective')
    research_type = fields.Selection([('ql', 'QL'),
                                      ('qn', 'QN')])
    data_capture = fields.Selection([('capi', 'CAPI'),
                                     ('papi', 'PAPI'), ('cati', 'CATI'), ('online', 'Online')])
    # sample_size = fields.Many2one('sample.size')
    sample_size = fields.Char('SS')
    number_of_legs = fields.Integer()
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('both', 'Both')])
    sec = fields.Selection(SEC)
    # fw_country = fields.Many2one('res.country', ' Country')
    fw_city_country = fields.Many2one('res.country', ' Country')
    age = fields.Char('Age')
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])
    no_of_respondants = fields.Integer('No of Respondants')
    no_of_attendees = fields.Integer('No of attendees')
    no_of_units_attendees = fields.Char('Number of Units')

    name = fields.Char(compute='_compute_name', string="Description")
    pdt_crm_research_id = fields.Char(related='pdt_crm.research_type_id.name')
    pdt_crm_2_research_id = fields.Char(related='pdt_crm_2.research_type_id.name', default='QL')

    # @api.onchange('pdt_line')
    # def get_domain_ids(self):
    #     print (':::get_domain_ids ::::')
    # print({
    #     'domain': {
    #         'product_id': [
    #             ('categ_id', '=', self._context['product_category_id'])
    #         ]
    #     }
    # })
    #     try:
    #         return {
    #             'domain': {
    #                 'product_id': [
    #                     ('categ_id', '=', self._context['product_category_id'])
    #                 ]
    #             }
    #         }
    #     except Exception:
    #         return []

    # @api.multi
    @api.depends('product_id', 'fw_country', 'sec')
    def _compute_name(self):
        for record in self:
            record.name = ''
            if record.product_id:
                record.name += record.product_id.name + ', '
            if record.fw_country:
                record.name += record.fw_country.name + ', '
            if record.sec:
                record.name += record.sec

    # @api.onchange('product_id')
    # def product_domain(self):
    #     print(self._context)
    #     # products = self.env['product.product'].search([
    #     #     ('categ_id', '=', self._context['product_category_id']),
    #     #     # ('categ_id.parent_id', '=', self._context['product_category_id'])
    #     # ])
    #     products_2 = self.env['product.product'].search([
    #         # ('categ_id', '=', self._context['product_category_id']),
    #         ('categ_id.parent_id', '=', self._context['product_category_id']),
    #         ('purchase_ok', '=', True)
    #     ])
    #     # lst = products.ids
    #     # lst.append(products_2.ids)
    #     # print(products)
    #     return {'domain': {'product_id': [('id', 'in', products_2.ids)], }}


class OpportunityCostEstimation(models.Model):
    _inherit = 'opportunity.cost.estimation'

    length_of_interview = fields.Char()
    dp = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    reporting = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    presentation = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    viewing_facility = fields.Selection([('yes', 'Yes'), ('no', 'No')])
    client_attendance = fields.Selection([('yes', 'Yes'),
                                          ('no', 'No')])

    details = fields.Text()
    transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Transcript'
    )

    objective = fields.Char('Objective')
    methodology = fields.Char('Methodology')
    criteria_usage = fields.Text('Criteria / Usage')
    sample_size_text = fields.Char('Sample Size')
    sample_struct_per_reg = fields.Char('Sample Structure per Region')
    sample_struct_per_sec = fields.Char('Sample Structure per SEC')
    sample_struct_per_age = fields.Char('Sample Structure per Age')
    sample_struct_per_gen = fields.Char('Sample Structure per Gender')
    sample_struct_per_bra = fields.Char('Sample Structure per Brand')
    no_of_client_attendees = fields.Char('Number of Clients to Attend')
    no_of_units_attendees = fields.Char('Number of Units Client will Attend')
    client_attendence_region_ids = fields.Many2many(
        'res.country.state', relation="awe_cost_country_rel",
        string='Client Attendance Region'
    )
    cpi = fields.Float(compute='_compute_cpi')

    # quotations_ids = fields.One2many(
    #     'sale.order', 'opportunity_cost_estimation')

    quotation_id = fields.Many2many('sale.order', relation="awe_cost_quotation_rel", )
    ex_transcript = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Extended Transcript'
    )
    printing_material = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string='Printing Material'
    )
    transcript_lang = fields.Char(
        string='Transcript Language'
    )
    length_of_interview = fields.Char('Length of Interview')
    translation = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Simultaneous Translation"
    )
    other_translation = fields.Char(
        string="Other Translation"
    )
    research_type_name = fields.Char(
        'Reaseach Type Name',
        related="estimation_type.name",
        readonly=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        readonly=False,
    )

    @api.depends('order_line')
    def _compute_cpi(self):
        for record in self:
            sum_qty = 0
            sum_total_cost = 0
            sum_SS = 0
            for line in record.order_line:
                sum_qty += line.product_uom_qty
                sum_total_cost += line.price_subtotal
            for line2 in record.pdt_line_view:
                sum_SS += line2.product_uom_qty

            if sum_SS:
                record.cpi = sum_total_cost / sum_SS

    @api.model
    def change_prefix(self):
        seq_id = self.env.ref(
            'custom_opportunity_cost_estimation_v11.seq_cost_estimation').id
        self.env['ir.sequence'].browse(seq_id).prefix = 'BUD/'


class ResearchType(models.Model):
    _name = 'research.type'

    name = fields.Char(string='Research Type')


class DataCapture(models.Model):
    _name = 'data.capture'

    name = fields.Char(string='Data Capture')


class CustomAccountInvoice(models.Model):
    _inherit = 'account.move'

    custom_description = fields.Char()
    custom_quantity = fields.Integer(compute='_compute_custom_quantity')
    custom_unit_price = fields.Float(compute='_compute_unit_price')

    @api.depends('invoice_line_ids')
    def _compute_custom_quantity(self):
        for record in self:
            total = 0
            for line in record.invoice_line_ids:
                total += line.quantity

            record.custom_quantity = total

    @api.depends('invoice_line_ids')
    def _compute_unit_price(self):
        for record in self:
            total = 0
            for line in record.invoice_line_ids:
                total += line.price_unit

            record.custom_unit_price = total


class CustomPdtLine(models.Model):
    _inherit = 'crm.product_line'

    research_type_id = fields.Char(
        # 'product.category',
        required=False,
        # related='pdt_crm.research_type_id.name',
        # default=lambda self: self.pdt_crm.research_type_id.name,
        # compute='compute_category',
        # store=True

    )

    # @api.model
    # def test(self):
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     return True
    # @api.onchange

    # @api.one
    # @api.onchange('research_type_id')
    # def compute_category(self):
    #     print('::: compute_category :::')
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     print('::: out :::')
    #     return True

    # @api.one
    # @api.onchange('product_id')
    # def get_domain_ids(self):
    #     print (':::get_domain_ids ::::')
    #     # try:
    #     #     return {
    #     #         'domain': {
    #     #             'product_id': [
    #     #                 ('categ_id', '=', self._context['product_category_id']),
    #     #                 ('sale_ok', '=', True)
    #     #             ]
    #     #         }
    #     #     }
    #     # except Exception:
    #     #     print('IAm Excepted')
    #     #     return {}
    #     # print('::: compute_category :::')
    #     catg = self.pdt_crm.research_type_id.id
    #     self.write({'research_type_id': catg})
    #     return True


class SaleOrder(models.Model):
    """Add several date fields to Sales Orders, computed or user-entered"""
    _inherit = 'sale.order'

    commitment_date = fields.Datetime('Order Dates', copy=False, store=True,
                                      states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
                                      help="Date by which the products are sure to be delivered. This is "
                                           "a date that you can promise to the customer, based on the "
                                           "Product Lead Times.")

    date_order = fields.Datetime(string='Confirming Date', required=True, readonly=True, index=True,
                                 states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, copy=False,
                                 default=fields.Datetime.now)
