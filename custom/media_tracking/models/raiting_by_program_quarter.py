# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime


class RatingByProgramQuarter(models.Model):
    _name = 'a.quarter'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Many2one('a.questionnaire', string='Seq')
    data_processing = fields.Many2one('a.data.processing')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    channel_id = fields.Many2one('a.channels', string='Channel')
    media_channel_id = fields.Many2one('media.channel', string='Media Channel')
    programs_id = fields.Many2one('a.programs', string='Program')
    region = fields.Selection(related='name.sec6', string='Region',store=True)
    age_range = fields.Selection(related='name.s3', string='Age Range',store=True)
    sec = fields.Selection(related='name.sec', string='SEC', store=True)
    date = fields.Date(related='name.date', string='Date', store=True)
    gender = fields.Selection(related='name.s4', string='Gender', store=True)
    day_name = fields.Char(related='name.day_name',string='Day', store=True)
    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')

    base = fields.Float('Base (%)', store=True, digits=(16, 4))
    week_end = fields.Float('WE (%)', store=True, digits=(16, 4))
    week_day = fields.Float('WD (%)', store=True, digits=(16, 4))
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')

    duration = fields.Char('Duration', compute='compute_duration', store=True)

    @api.depends('base')
    def compute_duration(self):
        for rec in self:
            if rec.header == '1':
                # rec.duration = '%s AM - %s AM'%(str(datetime.timedelta(hours=rec.time_from)).rsplit(':', 1)[0],str(datetime.timedelta(hours=rec.time_to)).rsplit(':', 1)[0])
                rec.duration = '%s AM - %s AM' % (rec.time_from.name, rec.time_to.name)
            if rec.header == '2':
                # rec.duration = '%s PM - %s PM'%(str(datetime.timedelta(hours=rec.time_from)).rsplit(':', 1)[0],str(datetime.timedelta(hours=rec.time_to)).rsplit(':', 1)[0])
                rec.duration = '%s PM - %s PM' % (rec.time_from.name, rec.time_to.name)

            else:
                pass

    channel_lines = fields.Many2one('a.channel.lines', ondelete='restrict')


class RatingByProgramQuarterTotalSample(models.Model):
    _name = 'a.quarter.total.sample'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"

    name = fields.Many2one('a.questionnaire', string='Seq')
    data_processing = fields.Many2one('a.data.processing')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    channel_id = fields.Many2one('a.channels', string='Channel')
    media_channel_id = fields.Many2one('media.channel', string='Media Channel')
    programs_id = fields.Many2one('a.programs', string='Program')
    region = fields.Selection(related='name.sec6', string='Region', store=True)
    age_range = fields.Selection(related='name.s3', string='Age Range', store=True)
    sec = fields.Selection(related='name.sec', string='SEC', store=True)
    date = fields.Date(related='name.date', string='Date', store=True)
    gender = fields.Selection(related='name.s4', string='Gender', store=True)
    day_name = fields.Char(related='name.day_name', string='Day', store=True)
    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')

    base = fields.Float('Base (%)', store=True, digits=(16, 4))
    week_end = fields.Float('WE (%)', store=True, digits=(16, 4))
    week_day = fields.Float('WD (%)', store=True, digits=(16, 4))
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')

    duration = fields.Char('Duration', compute='compute_duration', store=True)

    @api.depends('base')
    def compute_duration(self):
        for rec in self:
            if rec.header == '1':
                # rec.duration = '%s AM - %s AM'%(str(datetime.timedelta(hours=rec.time_from)).rsplit(':', 1)[0],str(datetime.timedelta(hours=rec.time_to)).rsplit(':', 1)[0])
                rec.duration = '%s AM - %s AM' % (rec.time_from.name, rec.time_to.name)
            if rec.header == '2':
                # rec.duration = '%s PM - %s PM'%(str(datetime.timedelta(hours=rec.time_from)).rsplit(':', 1)[0],str(datetime.timedelta(hours=rec.time_to)).rsplit(':', 1)[0])
                rec.duration = '%s PM - %s PM' % (rec.time_from.name, rec.time_to.name)

            else:
                pass

    channel_lines = fields.Many2one('a.channel.lines', ondelete='restrict')
