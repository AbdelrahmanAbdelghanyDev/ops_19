from odoo import models, fields, api, _


class AddLine(models.Model):
    _name = 'a.add.line'
    _description = 'Add Line Wizard'

    name = fields.Many2one('a.questionnaire')
    channel_id = fields.Many2one('a.channels')
    program_id = fields.Many2one('a.programs')
    questionnaire_date = fields.Date('Date')
    channel_lines = fields.One2many('a.add.line.channel.lines','add_line_id')

    @api.onchange('program_id','channel_id')
    def onchange_program(self):
        self.channel_lines = False
        if self.channel_id:
            channel = self.env['a.channels'].search(['&',('id','=',self.channel_id.id),'|','&',
                               ('date_from', '<=', self.questionnaire_date),('date_to', '>=', self.questionnaire_date),'&',
                               ('date_from', '=', False),('date_to', '=', False)])
            if channel:
                for rec in channel.channel_lines:
                    if self.program_id:
                        if rec.program.id == self.program_id.id:
                            self.channel_lines.create({'header': rec.header,
                                                       'time_from': rec.time_from.id,
                                                       'time_to':rec.time_to.id,
                                                       'period':rec.period,
                                                       'add_line_id':self.id,
                                                       'readonly_field': True,
                                                       'checked': False,
                                                       })
        if not self.program_id:
            self.channel_id = False


    def add_line(self):
        lines = []
        channels = []
        for record in self.channel_lines:
            if record.checked:
                lines.append([0, 0,{'header':record.header,
                                    'time_from':record.time_from.id,
                                    'time_to':record.time_to.id,
                                    'period':record.period,
                                    'channel_id':self.channel_id.id,
                                    'programs_id':self.program_id.id,
                                    }])
                if not record.readonly_field and self.channel_id.other:
                    channels.append([0, 0, {'header': record.header,
                                            'time_from': record.time_from.id,
                                            'time_to': record.time_to.id,
                                            'period': record.period,
                                            'program': self.program_id.id,
                                            }])
        self.channel_id.sudo().write({'channel_lines': channels})
        self.name.sudo().write({'q3': lines})
    def add_new_line(self):
        self.add_line()
        return {
            'name': 'Add Line',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'a.add.line',
            'target': 'new',
            'context': {
                'default_name': self.name.id,
                'default_questionnaire_date': self.questionnaire_date,
            },
            'type': 'ir.actions.act_window',
        }


class AddLineChannel(models.Model):
    _name = 'a.add.line.channel.lines'
    _description = 'Add Line Channel Wizard'

    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')
    time_from = fields.Many2one('a.time_from',string='Time From',tracking=True)
    time_to = fields.Many2one('a.time_from',string='Time To',tracking=True)
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')
    checked = fields.Boolean('Checked',default=True)
    readonly_field = fields.Boolean('Readonly')
    add_line_id = fields.Many2one('a.add.line')
