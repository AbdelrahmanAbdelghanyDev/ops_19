# -*- coding: utf-8 -*-

from odoo import models, fields, api


class RatingByProgramFull(models.Model):
    _name = 'a.full'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "media_channel_id"

    # channel_id = fields.Many2one('a.channels', string='Channel')
    media_channel_id = fields.Many2one('media.channel', string='Channel')
    programs_id = fields.Many2one('a.programs', string='Program')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    avg_rate = fields.Float('Avg Rating(%)')
    total_rate = fields.Float('Total Rating(%)')
    reach = fields.Float(string="Reach", required=False, default=0.0)
    header_from = fields.Selection(string="Day/Night", selection=[('1', 'AM'), ('2', 'PM')])
    header_to = fields.Selection(string="Day/Night", selection=[('1', 'AM'), ('2', 'PM')])
    base = fields.Float(string="Base")
    base_male = fields.Float(string="Base Male")
    base_female = fields.Float(string="Base Female")
    base_cairo = fields.Float(string="Base Cairo")
    base_alex = fields.Float(string="Base Alex")
    base_delta = fields.Float(string="Base Delta")
    base_ue = fields.Float(string="Base UE")
    base_canal_red_sea = fields.Float(string="Base Canal And Red Sea")
    base_2 = fields.Float(string="Base 15 - 19")
    base_3 = fields.Float(string="Base 20 - 24")
    base_4 = fields.Float(string="Base 25 - 29")
    base_5 = fields.Float(string="Base 30 - 34")
    base_6 = fields.Float(string="Base 35 - 39")
    base_7 = fields.Float(string="Base 40 - 44")
    base_8 = fields.Float(string="Base 45 - 49")
    base_9 = fields.Float(string="Base 50 - 59")
    base_10 = fields.Float(string="Base More Than 59")
    base_a = fields.Float(string="Base A")
    base_b = fields.Float(string="Base B")
    base_c1 = fields.Float(string="Base C1")
    base_c2 = fields.Float(string="Base C2")
    base_de = fields.Float(string="Base DE")


class RatingByProgramFullTotalSample(models.Model):
    _name = 'a.full.total.sample'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "media_channel_id"

    # channel_id = fields.Many2one('a.channels', string='Channel')
    media_channel_id = fields.Many2one('media.channel', string='Channel')
    programs_id = fields.Many2one('a.programs', string='Program')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    avg_rate = fields.Float('Avg Rating(%)')
    total_rate = fields.Float('Total Rating(%)')
    reach = fields.Float(string="Reach", required=False, default=0.0)
    header_from = fields.Selection(string="Day/Night", selection=[('1', 'AM'), ('2', 'PM')])
    header_to = fields.Selection(string="Day/Night", selection=[('1', 'AM'), ('2', 'PM')])
    base = fields.Float(string="Base")
    base_male = fields.Float(string="Base Male")
    base_female = fields.Float(string="Base Female")
    base_cairo = fields.Float(string="Base Cairo")
    base_alex = fields.Float(string="Base Alex")
    base_delta = fields.Float(string="Base Delta")
    base_ue = fields.Float(string="Base UE")
    base_canal_red_sea = fields.Float(string="Base Canal And Red Sea")
    base_2 = fields.Float(string="Base 15 - 19")
    base_3 = fields.Float(string="Base 20 - 24")
    base_4 = fields.Float(string="Base 25 - 29")
    base_5 = fields.Float(string="Base 30 - 34")
    base_6 = fields.Float(string="Base 35 - 39")
    base_7 = fields.Float(string="Base 40 - 44")
    base_8 = fields.Float(string="Base 45 - 49")
    base_9 = fields.Float(string="Base 50 - 59")
    base_10 = fields.Float(string="Base More Than 59")
    base_a = fields.Float(string="Base A")
    base_b = fields.Float(string="Base B")
    base_c1 = fields.Float(string="Base C1")
    base_c2 = fields.Float(string="Base C2")
    base_de = fields.Float(string="Base DE")