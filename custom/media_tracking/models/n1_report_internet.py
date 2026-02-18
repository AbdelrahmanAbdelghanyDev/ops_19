# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InternetReport(models.Model):
    _name = 'a.internet.n1'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "n1"

    # n1 = fields.Selection([
    #     ('1', 'نعم بتفرج ومتابع'),
    #     ('2', 'نعم بتفرج بس مش متابع باستمرار'),
    #     ('3', 'لا,بس بدخل على الانترنت عادي'),
    #     ('4', 'لا أنا مبدخلش على الانترنت'),
    # ])
    n1 = fields.Char(string='N1')
    base = fields.Float('Base', store=True, digits=(16, 4))
    base_percent = fields.Float('Base (%)', store=True, digits=(16, 4))


    ##################### Gender ########################

    base_male = fields.Float('Male Base', store=True, digits=(16, 4))
    base_male_percent = fields.Float('Male (%)', store=True, digits=(16, 4))

    base_female = fields.Float('Female Base', store=True, digits=(16, 4))
    base_female_percent = fields.Float('Female (%)', store=True, digits=(16, 4))

    ##################### Age Range ########################

    base_2 = fields.Float('15 - 19 Base', store=True, digits=(16, 4))
    base_2_percent = fields.Float('15 - 19 (%)', store=True, digits=(16, 4))

    base_3 = fields.Float('20 - 24 Base', store=True, digits=(16, 4))
    base_3_percent = fields.Float('20 - 24 (%)', store=True, digits=(16, 4))

    base_4 = fields.Float('25 - 29 Base', store=True, digits=(16, 4))
    base_4_percent = fields.Float('25 - 29 (%)', store=True, digits=(16, 4))

    base_5 = fields.Float('30 - 34 Base', store=True, digits=(16, 4))
    base_5_percent = fields.Float('30 - 34 (%)', store=True, digits=(16, 4))

    base_6 = fields.Float('35 - 39 Base', store=True, digits=(16, 4))
    base_6_percent = fields.Float('35 - 39 (%)', store=True, digits=(16, 4))

    base_7 = fields.Float('40 - 44 Base', store=True, digits=(16, 4))
    base_7_percent = fields.Float('40 - 44 (%)', store=True, digits=(16, 4))

    base_8 = fields.Float('45 - 49 Base', store=True, digits=(16, 4))
    base_8_percent = fields.Float('45 - 49 (%)', store=True, digits=(16, 4))

    base_9 = fields.Float('50 - 59 Base', store=True, digits=(16, 4))
    base_9_percent = fields.Float('50 - 59 (%)', store=True, digits=(16, 4))

    base_10 = fields.Float('More Than 59  Base', store=True, digits=(16, 4))
    base_10_percent = fields.Float('More Than 59 (%)', store=True, digits=(16, 4))

    ##################### Region ########################

    base_cairo = fields.Float('Cairo Base', store=True, digits=(16, 4))
    base_cairo_percent = fields.Float('Cairo (%)', store=True, digits=(16, 4))

    base_alex = fields.Float('Alex Base', store=True, digits=(16, 4))
    base_alex_percent = fields.Float('Alex (%)', store=True, digits=(16, 4))

    base_delta = fields.Float('Delta Base', store=True, digits=(16, 4))
    base_delta_percent = fields.Float('Delta (%)', store=True, digits=(16, 4))

    base_ue = fields.Float('UE Base', store=True, digits=(16, 4))
    base_ue_percent = fields.Float('UE (%)', store=True, digits=(16, 4))

    base_c_r = fields.Float('Cannal & Red Sea Base', store=True, digits=(16, 4))
    base_c_r_percent = fields.Float('Cannal & Red Sea (%)', store=True, digits=(16, 4))

    ##################### SEC ########################

    base_a = fields.Float('A Base', store=True, digits=(16, 4))
    base_a_percent = fields.Float('A (%)', store=True, digits=(16, 4))

    base_b = fields.Float('B Base', store=True, digits=(16, 4))
    base_b_percent = fields.Float('B (%)', store=True, digits=(16, 4))

    base_c1 = fields.Float('C1 Base', store=True, digits=(16, 4))
    base_c1_percent = fields.Float('C1 (%)', store=True, digits=(16, 4))

    base_c2 = fields.Float('C2 Base', store=True, digits=(16, 4))
    base_c2_percent = fields.Float('C2 (%)', store=True, digits=(16, 4))

    base_de = fields.Float('DE Base', store=True, digits=(16, 4))
    base_de_percent = fields.Float('DE (%)', store=True, digits=(16, 4))
