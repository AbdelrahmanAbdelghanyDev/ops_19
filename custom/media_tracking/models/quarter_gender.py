# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class QuarterGender(models.Model):
    _inherit = 'a.quarter'

    base_male = fields.Float('Male Base (%)', store=True, digits=(16, 4))
    week_end_male = fields.Float('Male WE (%)', store=True, digits=(16, 4))
    week_day_male = fields.Float('Male WD (%)', store=True, digits=(16, 4))

    base_female = fields.Float('Female Base (%)', store=True, digits=(16, 4))
    week_end_female = fields.Float('Female WE (%)', store=True, digits=(16, 4))
    week_day_female = fields.Float('Female WD (%)', store=True, digits=(16, 4))


class QuarterGenderTotalSample(models.Model):
    _inherit = 'a.quarter.total.sample'

    base_male = fields.Float('Male Base (%)', store=True, digits=(16, 4))
    week_end_male = fields.Float('Male WE (%)', store=True, digits=(16, 4))
    week_day_male = fields.Float('Male WD (%)', store=True, digits=(16, 4))

    base_female = fields.Float('Female Base (%)', store=True, digits=(16, 4))
    week_end_female = fields.Float('Female WE (%)', store=True, digits=(16, 4))
    week_day_female = fields.Float('Female WD (%)', store=True, digits=(16, 4))
