# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QuarterSEC(models.Model):
    _inherit = 'a.quarter'

    base_A = fields.Float('A Base (%)', store=True, digits=(16, 4))
    week_end_A = fields.Float('A WE (%)', store=True, digits=(16, 4))
    week_day_A = fields.Float('A WD (%)', store=True, digits=(16, 4))

    base_B = fields.Float('B Base (%)', store=True, digits=(16, 4))
    week_end_B = fields.Float('B WE (%)', store=True, digits=(16, 4))
    week_day_B = fields.Float('B WD (%)', store=True, digits=(16, 4))

    base_C1 = fields.Float('C1 Base (%)', store=True, digits=(16, 4))
    week_end_C1 = fields.Float('C1 WE (%)', store=True, digits=(16, 4))
    week_day_C1 = fields.Float('C1 WD (%)', store=True, digits=(16, 4))

    base_C2 = fields.Float('C2 Base (%)', store=True, digits=(16, 4))
    week_end_C2 = fields.Float('C2 WE (%)', store=True, digits=(16, 4))
    week_day_C2 = fields.Float('C2 WD (%)', store=True, digits=(16, 4))

    base_DE = fields.Float('DE Base (%)', store=True, digits=(16, 4))
    week_end_DE = fields.Float('DE WE (%)', store=True, digits=(16, 4))
    week_day_DE = fields.Float('DE WD (%)', store=True, digits=(16, 4))


class QuarterSECTotalSample(models.Model):
    _inherit = 'a.quarter.total.sample'

    base_A = fields.Float('A Base (%)', store=True, digits=(16, 4))
    week_end_A = fields.Float('A WE (%)', store=True, digits=(16, 4))
    week_day_A = fields.Float('A WD (%)', store=True, digits=(16, 4))

    base_B = fields.Float('B Base (%)', store=True, digits=(16, 4))
    week_end_B = fields.Float('B WE (%)', store=True, digits=(16, 4))
    week_day_B = fields.Float('B WD (%)', store=True, digits=(16, 4))

    base_C1 = fields.Float('C1 Base (%)', store=True, digits=(16, 4))
    week_end_C1 = fields.Float('C1 WE (%)', store=True, digits=(16, 4))
    week_day_C1 = fields.Float('C1 WD (%)', store=True, digits=(16, 4))

    base_C2 = fields.Float('C2 Base (%)', store=True, digits=(16, 4))
    week_end_C2 = fields.Float('C2 WE (%)', store=True, digits=(16, 4))
    week_day_C2 = fields.Float('C2 WD (%)', store=True, digits=(16, 4))

    base_DE = fields.Float('DE Base (%)', store=True, digits=(16, 4))
    week_end_DE = fields.Float('DE WE (%)', store=True, digits=(16, 4))
    week_day_DE = fields.Float('DE WD (%)', store=True, digits=(16, 4))
