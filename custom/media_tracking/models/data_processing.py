# -*- coding: utf-8 -*-

from odoo import models, fields, api

_dayOfWeekName = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']


class DataProcessing(models.Model):
    _name = 'a.data.processing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Many2one('a.questionnaire', string='Seq', ondelete='restrict')
    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    respondent_id = fields.Many2one(related='name.respondent_id', store=True, ondelete='restrict')
    channel_id = fields.Many2one('a.channels', string='Channel', ondelete='restrict')
    media_channel_id = fields.Many2one('media.channel', string='Media Channel', related='channel_id.channel_id',
                                       store=True)
    stage_id = fields.Selection(related='name.stage_id', store=True)
    programs_id = fields.Many2one('a.programs', string='Program', ondelete='restrict', required=True)
    age_range = fields.Selection(related='name.s3', string='Age Range', store=True)
    sec = fields.Selection(related='name.sec', string='SEC', store=True)
    region = fields.Selection(related='name.sec6', string='Region', store=True)
    gender = fields.Selection(related='name.s4', string='Gender', store=True)
    date = fields.Date(related='name.call_date', string='Date', store=True)
    day_name = fields.Char(related='name.day_name', string='Day', store=True)
    week_end = fields.Boolean('Week End')
    week_day = fields.Boolean('Week Day')
    time = fields.Char('')
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')

    channel_lines = fields.Many2one('a.channel.lines', ondelete='restrict')

    @api.depends('date')
    def _get_month(self):
        for rec in self:
            rec.month = rec.date.month

    month = fields.Integer(compute='_get_month', store=True)

    # @api.onchange('header','time_from','time_to','channel_id','programs_id')
    # def programs_domain(self):
    #     programs = self.env['a.channel.lines'].search([('date_from','<=',self.name.date),
    #     ('date_to','>=',self.name.date),
    #                                                    ('time_from','=',self.time_from.id),('time_to','=',self.time_to.id),
    #                                                    ('header','=',self.header),('channels_id','=',self.channel_id.id)])
    #     channels_domain = self.env['a.channels'].search(
    #         ['|',('other','=',True),'&',('date_from', '<=', self.date),('date_to', '>=', self.date)])
    # self.period = programs.period
    # self.programs_id = programs.program.id
    # return {'domain': {'programs_id': ['|',('other','=',True),('id', 'in', programs.mapped('program').ids)],
    # 'channel_id':[('id','in',channels_domain.ids)]}}
    @api.model
    def create(self, vals):
        res = super(DataProcessing, self).create(vals)

        if res.day_name in _dayOfWeekName:
            res.week_day = True
            res.week_end = False
        else:
            res.week_day = False
            res.week_end = True
        res.time = "%s - %s" % (res.time_from.name, res.time_to.name)

        channel_lines = self.env['a.channel.lines'].search(
            [
             ('time_from', '=', res.time_from.id), ('time_to', '=', res.time_to.id), ('period', '=', res.period),
             ('header', '=', res.header), ('program', '=', res.programs_id.id),
                ('channels_id', '=', res.channel_id.id)])

        if channel_lines:
            res.channel_lines = channel_lines.id
        return res

