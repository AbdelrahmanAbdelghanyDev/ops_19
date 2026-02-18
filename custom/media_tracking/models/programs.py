# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProgramLines(models.Model):
    _name = 'a.program.line'
    _description = 'Program Lines'

    program_id = fields.Many2one(comodel_name="a.programs", string="Program")
    media_channel_id = fields.Many2one(comodel_name="media.channel", string="Channel")
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')
    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')
    date_from_id = fields.Many2one(comodel_name="a.time_from", string="Date From")
    date_to_id = fields.Many2one(comodel_name="a.time_from", string="Date To")
    date_from_seq = fields.Integer(related='date_from_id.seq')
    date_to_seq = fields.Integer(related='date_to_id.seq')

    @api.constrains('period', 'media_channel_id')
    def period_constrains(self):
        for rec in self:
            if rec.period in rec.program_id.program_line_ids.filtered(
                    lambda r: r.media_channel_id == rec.media_channel_id and r.id != rec.id).mapped('period'):
                raise ValidationError('You can not use same run with same channel more than one')


class Programs(models.Model):
    _name = 'a.programs'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "name"
    _description = "Program"

    name = fields.Char('Name',tracking=True,required=True)
    other = fields.Boolean('Other',default=True)
    program_line_ids = fields.One2many(comodel_name="a.program.line",
                                       inverse_name="program_id", string="Program Lines")

    @api.constrains('name')
    def unique_name(self):
        for rec in self:
            programs = self.env['a.programs'].search([('id', '!=', rec.id), ('name', '=', rec.name)])
            if programs:
                raise ValidationError('Program name must be unique')




