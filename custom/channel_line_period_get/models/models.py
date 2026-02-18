# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ChannelLines(models.Model):
    _inherit = 'a.channel.lines'

    @api.depends('program', 'time_from', 'time_to', 'channels_id')
    def get_period(self):
        for rec in self:
            rec.period = False
            if rec.program and rec.time_from and rec.time_to and rec.channels_id:
                program_line = self.env['a.program.line'].search([('program_id', '=', rec.program.id),
                                                                  ('date_from_seq', '<=', rec.time_from.seq),
                                                                  ('date_to_seq', '>=', rec.time_to.seq),
                                                                  ('media_channel_id', '=',
                                                                   rec.channels_id.channel_id.id)], limit=1)
                if program_line:
                    rec.period = program_line.period
                else:
                    rec.period = False
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run', compute='get_period', required=True)


