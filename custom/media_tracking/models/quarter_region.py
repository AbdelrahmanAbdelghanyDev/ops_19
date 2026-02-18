# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QuarterRegion(models.Model):
    _inherit = 'a.quarter'

    base_cairo = fields.Float('Cairo Base (%)', store=True, digits=(16, 4))
    week_end_cairo = fields.Float('Cairo WE (%)', store=True, digits=(16, 4))
    week_day_cairo = fields.Float('Cairo WD (%)', store=True, digits=(16, 4))

    base_alex = fields.Float('Alex Base (%)', store=True, digits=(16, 4))
    week_end_alex = fields.Float('Alex WE (%)', store=True, digits=(16, 4))
    week_day_alex = fields.Float('Alex WD (%)', store=True, digits=(16, 4))

    base_delta = fields.Float('Delta Base (%)', store=True, digits=(16, 4))
    week_end_delta = fields.Float('Delta WE (%)', store=True, digits=(16, 4))
    week_day_delta = fields.Float('Delta WD (%)', store=True, digits=(16, 4))

    base_ue = fields.Float('UE Base (%)', store=True, digits=(16, 4))
    week_end_ue = fields.Float('UE WE (%)', store=True, digits=(16, 4))
    week_day_ue = fields.Float('UE WD (%)', store=True, digits=(16, 4))

    base_c_r = fields.Float('Cannal & Red Sea Base (%)', store=True, digits=(16, 4))
    week_end_c_r = fields.Float('Cannal & Red Sea WE (%)', store=True, digits=(16, 4))
    week_day_c_r = fields.Float('Cannal & Red Sea WD (%)', store=True, digits=(16, 4))


class QuarterRegionTotalSample(models.Model):
    _inherit = 'a.quarter.total.sample'

    base_cairo = fields.Float('Cairo Base (%)', store=True, digits=(16, 4))
    week_end_cairo = fields.Float('Cairo WE (%)', store=True, digits=(16, 4))
    week_day_cairo = fields.Float('Cairo WD (%)', store=True, digits=(16, 4))

    base_alex = fields.Float('Alex Base (%)', store=True, digits=(16, 4))
    week_end_alex = fields.Float('Alex WE (%)', store=True, digits=(16, 4))
    week_day_alex = fields.Float('Alex WD (%)', store=True, digits=(16, 4))

    base_delta = fields.Float('Delta Base (%)', store=True, digits=(16, 4))
    week_end_delta = fields.Float('Delta WE (%)', store=True, digits=(16, 4))
    week_day_delta = fields.Float('Delta WD (%)', store=True, digits=(16, 4))

    base_ue = fields.Float('UE Base (%)', store=True, digits=(16, 4))
    week_end_ue = fields.Float('UE WE (%)', store=True, digits=(16, 4))
    week_day_ue = fields.Float('UE WD (%)', store=True, digits=(16, 4))

    base_c_r = fields.Float('Cannal & Red Sea Base (%)', store=True, digits=(16, 4))
    week_end_c_r = fields.Float('Cannal & Red Sea WE (%)', store=True, digits=(16, 4))
    week_day_c_r = fields.Float('Cannal & Red Sea WD (%)', store=True, digits=(16, 4))
