# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QuarterAge(models.Model):
    _inherit = 'a.quarter'

    base_2 = fields.Float('15 - 19 Base (%)', store=True, digits=(16, 4))
    week_end_2 = fields.Float('15 - 19 WE (%)', store=True, digits=(16, 4))
    week_day_2 = fields.Float('15 - 19 WD (%)', store=True, digits=(16, 4))

    base_3 = fields.Float('20 - 24 Base (%)', store=True, digits=(16, 4))
    week_end_3 = fields.Float('20 - 24 WE (%)', store=True, digits=(16, 4))
    week_day_3 = fields.Float('20 - 24 WD (%)', store=True, digits=(16, 4))

    base_4 = fields.Float('25 - 29 Base (%)', store=True, digits=(16, 4))
    week_end_4 = fields.Float('25 - 29 WE (%)', store=True, digits=(16, 4))
    week_day_4 = fields.Float('25 - 29 WD (%)', store=True, digits=(16, 4))

    base_5 = fields.Float('30 - 34 Base (%)', store=True, digits=(16, 4))
    week_end_5 = fields.Float('30 - 34 WE (%)', store=True, digits=(16, 4))
    week_day_5 = fields.Float('30 - 34 WD (%)', store=True, digits=(16, 4))

    base_6 = fields.Float('35 - 39 Base (%)', store=True, digits=(16, 4))
    week_end_6 = fields.Float('35 - 39 WE (%)', store=True, digits=(16, 4))
    week_day_6 = fields.Float('35 - 39 WD (%)', store=True, digits=(16, 4))

    base_7 = fields.Float('40 - 44 Base (%)', store=True, digits=(16, 4))
    week_end_7 = fields.Float('40 - 44 WE (%)', store=True, digits=(16, 4))
    week_day_7 = fields.Float('40 - 44 WD (%)', store=True, digits=(16, 4))

    base_8 = fields.Float('45 - 49 Base (%)', store=True, digits=(16, 4))
    week_end_8 = fields.Float('45 - 49 WE (%)', store=True, digits=(16, 4))
    week_day_8 = fields.Float('45 - 49 WD (%)', store=True, digits=(16, 4))

    base_9 = fields.Float('50 - 59 Base (%)', store=True, digits=(16, 4))
    week_end_9 = fields.Float('50 - 59 WE (%)', store=True, digits=(16, 4))
    week_day_9 = fields.Float('50 - 59 WD (%)', store=True, digits=(16, 4))

    base_10 = fields.Float('More Than 59  Base (%)', store=True, digits=(16, 4))
    week_end_10 = fields.Float('More Than 59 WE (%)', store=True, digits=(16, 4))
    week_day_10 = fields.Float('More Than 59 WD (%)', store=True, digits=(16, 4))


class QuarterAgeTotalSample(models.Model):
    _inherit = 'a.quarter.total.sample'

    base_2 = fields.Float('15 - 19 Base (%)', store=True, digits=(16, 4))
    week_end_2 = fields.Float('15 - 19 WE (%)', store=True, digits=(16, 4))
    week_day_2 = fields.Float('15 - 19 WD (%)', store=True, digits=(16, 4))

    base_3 = fields.Float('20 - 24 Base (%)', store=True, digits=(16, 4))
    week_end_3 = fields.Float('20 - 24 WE (%)', store=True, digits=(16, 4))
    week_day_3 = fields.Float('20 - 24 WD (%)', store=True, digits=(16, 4))

    base_4 = fields.Float('25 - 29 Base (%)', store=True, digits=(16, 4))
    week_end_4 = fields.Float('25 - 29 WE (%)', store=True, digits=(16, 4))
    week_day_4 = fields.Float('25 - 29 WD (%)', store=True, digits=(16, 4))

    base_5 = fields.Float('30 - 34 Base (%)', store=True, digits=(16, 4))
    week_end_5 = fields.Float('30 - 34 WE (%)', store=True, digits=(16, 4))
    week_day_5 = fields.Float('30 - 34 WD (%)', store=True, digits=(16, 4))

    base_6 = fields.Float('35 - 39 Base (%)', store=True, digits=(16, 4))
    week_end_6 = fields.Float('35 - 39 WE (%)', store=True, digits=(16, 4))
    week_day_6 = fields.Float('35 - 39 WD (%)', store=True, digits=(16, 4))

    base_7 = fields.Float('40 - 44 Base (%)', store=True, digits=(16, 4))
    week_end_7 = fields.Float('40 - 44 WE (%)', store=True, digits=(16, 4))
    week_day_7 = fields.Float('40 - 44 WD (%)', store=True, digits=(16, 4))

    base_8 = fields.Float('45 - 49 Base (%)', store=True, digits=(16, 4))
    week_end_8 = fields.Float('45 - 49 WE (%)', store=True, digits=(16, 4))
    week_day_8 = fields.Float('45 - 49 WD (%)', store=True, digits=(16, 4))

    base_9 = fields.Float('50 - 59 Base (%)', store=True, digits=(16, 4))
    week_end_9 = fields.Float('50 - 59 WE (%)', store=True, digits=(16, 4))
    week_day_9 = fields.Float('50 - 59 WD (%)', store=True, digits=(16, 4))

    base_10 = fields.Float('More Than 59  Base (%)', store=True, digits=(16, 4))
    week_end_10 = fields.Float('More Than 59 WE (%)', store=True, digits=(16, 4))
    week_day_10 = fields.Float('More Than 59 WD (%)', store=True, digits=(16, 4))
