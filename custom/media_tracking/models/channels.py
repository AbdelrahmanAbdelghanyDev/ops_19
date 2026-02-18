# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MediaChannel(models.Model):
    _name = 'media.channel'
    _rec_name = 'name'
    _description = 'Media Channel'

    name = fields.Char(string='Channel Name', required=True)


class Channels(models.Model):
    _name = 'a.channels'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "channel_id"
    # _rec_name = "ch_name"
    _description = "Channel"

    channel_id = fields.Many2one(comodel_name="media.channel", string="Channel")
    name = fields.Char('Name', tracking=True)
    date_from = fields.Date('Date From', tracking=True)
    date_to = fields.Date('Date To', tracking=True)
    other = fields.Boolean('Other', default=True)
    channel_lines = fields.One2many('a.channel.lines', 'channels_id')
    # channel_name = fields.Selection(string="Channel Name",
    #                                 selection=[('mbc_2', 'MBC 2'), ('mbc_masr', 'MBC Masr'),
    #                                            ('mbc_masr_2', 'MBC Masr 2'),
    #                                            ('mbc_bollywood', 'MBC Bollywood'), ('rotana_cinema', 'Rotana Cinema'),
    #                                            ('al_nahar', 'Al Nahar'),
    #                                            ('al_nahar_drama', 'Al Nahar Drama'), ('mix_hollywood', 'Mix Hollywood'),
    #                                            ('zee_alwan', 'Zee Alwan'), ('zee_aflam', 'Zee Aflam'),
    #                                            ('cbc', 'CBC'), ('cbc_drama', 'CBC Drama'), ('cbc_sofra', 'CBC Sofra'),
    #                                            ('dmc', 'DMC'),
    #                                            ('al_hayat', 'Al Hayat'), ('al_hayat_drama', 'Al Hayat Drama'),
    #                                            ('on_e', 'ON E'),
    #                                            ('on_drama', 'ON Drama'), ('al_kahera_wal_nas', 'Al Kahera Wal Nas'),
    #                                            ('al_kahera_wal_nas_2', 'Al Kahera Wal Nas 2'),
    #                                            ('on_time_sports', 'ON Time Sports'),
    #                                            ('on_time_sports_2', 'ON Time Sports 2'), ('dmc_drama', 'DMC Drama'),
    #                                            ('extra_news', 'Extra News'), ('al_oula', 'Al oula'),
    #                                            ('zamalek_tv', 'Zamalek TV'),
    #                                            ('sada_el_balad', 'Sada El Balad'),
    #                                            ('sada_el_balad_2', 'Sada El Balad + 2 '),
    #                                            ('sada_el_balad_drama', 'Sada El Balad Drama'), ('other', 'Other')
    #                                            ],
    #                                 required=False, default='other')

    # ch_name = fields.Char(string="Channel Name", required=False, compute='_get_ch_name', default='None')

    # @api.depends('channel_name', 'name', 'other')
    # def _get_ch_name(self):
    #     for rec in self:
    #         rec.ch_name = dict(self._fields['channel_name'].selection).get(
    #             rec.channel_name) if not rec.other else rec.name

    @api.model
    def play(self):

        dc = {'MBC Masr 2': 'mbc_masr_2', 'Al Nahar': 'al_nahar', 'Rotana Cinema': 'rotana_cinema',
              'MBC Masr': 'mbc_masr', 'Mix Hollywood': 'mix_hollywood',
              'Al Nahar Drama': 'al_nahar_drama', 'Zee Alwan': 'zee_alwan', 'CBC Drama': 'cbc_drama', 'DMC': 'dmc',
              'Al Hayat Drama': 'al_hayat_drama', 'ON E': 'on_e',
              'Al Hayat': 'al_hayat',
              'ON Drama': 'on_drama', 'Al Kahera Wal Nas': 'al_kahera_wal_nas', 'ON Time Sports': 'on_time_sports',
              'ON Time Sports 2': 'on_time_sports_2', 'CBC': 'cbc',
              'CBC Sofra': 'cbc_sofra', 'DMC Drama': 'dmc_drama', 'Extra News': 'extra_news', 'MBC 2': 'mbc_2',
              'MBC Bollywood': 'mbc_bollywood', 'Al oula': 'al_oula',
              'Zamalek TV': 'zamalek_tv', 'Al Kahera Wal Nas 2': 'al_kahera_wal_nas_2',
              'Sada El Balad Drama': 'sada_el_balad_drama', 'Sada El Balad': 'sada_el_balad',
              'Sada El Balad + 2': 'sada_el_balad_2', 'Zee Aflam': 'zee_aflam', 'El Hayat': 'al_hayat',
              'El Hayat Drama': 'al_hayat_drama', 'ON Time Sport 1': 'on_time_sports',
              'Al kahera Wal Nas': 'al_kahera_wal_nas'}

        for rec in self.env['a.channels'].search([]):
            if rec.name in dc.keys():
                rec.channel_name = dc[rec.name]
            else:
                rec.channel_name = 'other'


class ChannelLines(models.Model):
    _name = 'a.channel.lines'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "program"

    date_from = fields.Date(related='channels_id.date_from', store=True)
    date_to = fields.Date(related='channels_id.date_to', store=True)
    header = fields.Selection([('1', 'AM'), ('2', 'PM')], string='Day/Night')
    time_from = fields.Many2one('a.time_from', string='Time From', tracking=True)
    time_to = fields.Many2one('a.time_from', string='Time To', tracking=True)
    period = fields.Selection([('1', '1st Run'), ('2', '2nd Run'), ('3', '3rd Run'), ('4', '4th Run'),
                               ('5', '5th Run'), ('6', '6th Run'), ('7', '7th Run'), ('8', '8th Run'), ('9', '9th Run'),
                               ('10', '10th Run')], string='Run')
    program = fields.Many2one('a.programs', string='Programs', tracking=True, ondelete='restrict')

    channels_id = fields.Many2one('a.channels', ondelete='restrict')
