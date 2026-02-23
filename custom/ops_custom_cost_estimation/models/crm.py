from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError




class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_estimation(self):

        approved_cost_estimation = self.env['cost.estimation'].search(
            [('opportunity.id', '=', self.id), ('state', '=', 'approved')])
        multiple_cost_estimate = self.env['ir.config_parameter'].sudo().get_param('multiple_cost_estimate') or False
        quantity = 0
        if approved_cost_estimation and not multiple_cost_estimate:
            raise ValidationError(
                _("You can't create multiple cost estimation for this opportunity due to your setting restrictions"))
        else:
            if (not self.product_line) and (not self.pdt_line) and (not self.pdt_line_ql):
                raise ValidationError(_(
                    "You can't create cost estimation without product lines"))
            else:
                if self.pdt_line:
                    self.product_line = False
                    result_qn = []
                    for line_qn in self.pdt_line:
                        values_qn = {'product_id': line_qn.product_id.id,
                                     'fw_country': line_qn.fw_city_country,
                                     'data_capture': line_qn.data_capture,
                                     'fw_city': line_qn.fw_country,
                                     'quantity_qn': line_qn.product_uom_qty}
                        result_qn.append((0, 0, values_qn))
                    self.product_line = result_qn
                if self.pdt_line_ql:
                    self.product_line = False
                    result_ql = []
                    for line_ql in self.pdt_line_ql:
                        values_ql = {'product_id': line_ql.product_id.id,
                                     'fw_country': line_ql.fw_city_country,
                                     'data_capture': line_ql.data_capture,
                                     'fw_city': line_ql.fw_country,
                                     'sec': line_ql.sec,
                                     'mp_of_respondants': line_ql.no_of_respondants,
                                     'gender': line_ql.gender,
                                     'age': line_ql.age,
                                     'quantity': line_ql.no_of_units_attendees}
                        result_ql.append((0, 0, values_ql))
                    self.product_line = result_ql
                cost_estimation_line = []
                time_estimation_line = []
                for rec in self.product_line:
                    if (not rec.product_id.cost_ok) and (rec.product_id.cost_estimation or
                                                         rec.product_id.time_estimation_ids):
                        if self.research_type_name == 'QN':
                            quantity = rec.quantity_qn
                        if self.research_type_name == 'QL':
                            quantity = rec.quantity
                        for product in rec.product_id.cost_estimation:
                            if not product.cost_item_type:
                                cost_item_type = 'material'
                            else:

                                cost_item_type = product.cost_item_type
                            values = {'salable_product': rec.id,
                                      'sp_desc': rec.description,
                                      'sp_quant': quantity,
                                      'cost_item': product.product_id.id,
                                      'cost_item_description': product.description,
                                      'cost_item_unit_cost': 1.0,
                                      'cost_item_cost_currency': 0.0,
                                      'cost_item_quant_sp': product.qty,
                                      'cost_item_uom_id': product.uom.id,
                                      'cost_item_type': cost_item_type,
                                      'cost_item_cost_sp': 1.0,
                                      'taxes': False,
                                      'fx': 1.0,
                                      'total_cost_item_quantity': 1.0,
                                      'budgetary_position': product.budgetary_position.id,
                                      'total_cost_item_cost': 1.0}
                            cost_estimation_line.append((0, 0, values))

                        for product in rec.product_id.time_estimation_ids:
                            if not product.cost_item_type:
                                cost_item_type = 'overhead'
                            else:
                                cost_item_type = product.cost_item_type
                            values = {'salable_product': rec.id,
                                      'sp_desc': rec.description,
                                      'sp_quant': quantity,
                                      'cost_item': product.product_id.id,
                                      'cost_item_description': product.description,
                                      'cost_item_unit_cost': 1.0,
                                      'cost_item_cost_currency': 0.0,
                                      'cost_item_quant_sp': product.product_id.standard_price,
                                      'cost_item_uom_id': product.uom.id,
                                      'cost_item_type': cost_item_type,
                                      'cost_item_cost_sp': 1.0,
                                      'taxes': False,
                                      'fx': 1.0,
                                      'total_cost_item_quantity': 1.0,
                                      'budgetary_position': product.budgetary_position.id,
                                      'total_cost_item_cost': 1.0}
                            time_estimation_line.append((0, 0, values))
                    else:
                        if self.research_type_name == 'QN':
                            quantity = rec.quantity_qn
                        if self.research_type_name == 'QL':
                            quantity = rec.quantity
                        values = {'salable_product': rec.id,
                                  'sp_desc': rec.description,
                                  'sp_quant': quantity,
                                  'cost_item': False,
                                  'cost_item_description': False,
                                  'cost_item_unit_cost': 1.0,
                                  'cost_item_cost_currency': 1.0,
                                  'cost_item_type': 'material',
                                  'budgetary_position': rec.product_id.budgetary_position.id,
                                  'cost_item_quant_sp': 1.0,
                                  'cost_item_cost_sp': 1.0,
                                  'taxes': False,
                                  'fx': 1.0,
                                  'total_cost_item_quantity': 1.0,
                                  'total_cost_item_cost': 1.0}
                        cost_estimation_line.append((0, 0, values))
                        time_estimation_line.append((0, 0, values))
                action = self.env.ref("cost_estimation.cost_estimation_form_action").read()[0]

                action['context'] = {
                    'default_customer': self.partner_id.id,
                    'default_research_type': self.research_type_id.id,
                    'default_opportunity': self.id,
                    'default_price_list': self.partner_id.property_product_pricelist.id,
                    'default_objective': self.objective,
                    'default_methodology': self.methodology,
                    'default_criteria_usage': self.criteria_usage,
                    'default_sample_size_text': self.sample_size_text,
                    'default_sample_struct_per_reg': self.sample_struct_per_reg,
                    'default_sample_struct_per_sec': self.sample_struct_per_sec,
                    'default_sample_struct_per_age': self.sample_struct_per_age,
                    'default_sample_struct_per_gen': self.sample_struct_per_gen,
                    'default_sample_struct_per_bra': self.sample_struct_per_bra,
                    'default_length_of_interview': self.length_of_interview_sel,
                    'default_details': self.details,
                    'default_sp_desc': self.description,
                    'default_translation': self.translation,
                    'default_other_translation': self.other_translation,
                    'default_no_of_client_attendees': self.no_of_client_attendees,
                    'default_no_of_units_attendees': self.no_of_units_attendees,
                    'default_client_attendence_region_ids': self.client_attendence_region_ids.ids,
                    'default_viewing_facility': self.viewing_facility,
                    'default_transcript': self.transcript,
                    'default_transcript_lang': self.transcript_lang,
                    'default_ex_transcript': self.ex_transcript,
                    'default_printing_material': self.printing_material,
                    'default_details_ql': self.details_ql,
                    'default_cost_estimation_line': cost_estimation_line,
                    'default_time_estimation_ids': time_estimation_line,
                    'default_seq': 'New',
                }

                return action
