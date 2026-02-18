# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
import logging
from odoo.exceptions import UserError


class AddRevenueCRMLead(models.Model):
    _inherit = 'crm.lead'

    revenue_bu = fields.Many2one('revenue.team', string="Revenue BU", required=True)


class RevenueTeams(models.Model):
    _name = 'revenue.team'
    _inherit = 'crm.team'

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    favorite_user_ids = fields.Many2many(
        'res.users', 'revenue_team_favorite_user_rel', 'revenue_team_id', 'user_id',
        default=_get_default_favorite_user_ids,
        string='Members')


class CustomProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project']

    mon = fields.Date(string='Month of Completion ', required=True)
    internl_pro_name = fields.Char(string='Internal Project Name')


class ProjectTask(models.Model):
    _inherit = 'project.task'

    img_name = fields.Char(string="Alternative text",
                           required=True, translate=True)

    task_id = fields.Many2one(
        'project.task', string='Task', ondelete='set null', index=True)

    team_id = fields.Many2one('project.task.teams', 'Team')

    original_image = fields.Binary(string='Original image')

    medium_image = fields.Binary(
        string='Medium image', compute='_resize_image', store=True)

    small_image = fields.Binary(
        string='Small image', compute='_resize_image', store=True)

    date_start_splited = fields.Date(
        string='Start Date2', compute='_split_date', store=True)

    date_end_splited = fields.Date(
        string='End Date2', compute='_split_date', store=True)

    time_start = fields.Char(
        string='Start Time', compute='_split_date', store=True)

    time_end = fields.Char(
        string='End Time', compute='_split_date', store=True)

    traveling_time = fields.Datetime('Target(month of completion)', required=True,
                                     track_visibility='onchange')  # 'Traveling Time'

    date_start = fields.Datetime(string='Starting Date',
                                 default=fields.Datetime.now,
                                 index=True, copy=False)

    today_date = fields.Date(
        'Today',
        readonly=True,
        default=lambda self: fields.Datetime.now()
    )
    today_flag = fields.Boolean('Today Flag',
                                default=False,
                                compute='_split_date',
                                store=True
                                )
    executive_person = fields.Many2one('executive.team', string="Executive Person")
    Revenue_bu = fields.Many2one('revenue.team', string="Revenue BU", track_visibility='onchange')
    Sales_bu = fields.Many2one('crm.team', string="Sales BU", track_visibility='onchange')
    date_end1 = fields.Datetime(string='Ending Date', index=True, copy=False)

    user_check = fields.Boolean(compute="_check_group")

    @api.depends('name')
    def _check_group(self):
        groups_list = []
        self.user_check = False
        for rec in self.env.user.groups_id:
            groups_list.append(rec.name)
        if "Finance Team" not in groups_list:
            print('eee', self.active)
            return False
        else:
            print('bbb', self)
            self.user_check = True

    @api.constrains('active')
    def onch_active(self):
        groups_list = []
        for rec in self.env.user.groups_id:
            groups_list.append(rec.name)
        for line in self:
            if "Finance Team" not in groups_list and (line.active == False):
                raise UserError(_('You have no Access to Archive task'))

    @api.depends('date_end1')
    def _set_date_end(self):
        if self.date_end1:
            self.date_end = self.date_end1

    @api.depends('date_start', 'date_end1')
    def _split_date(self):
        for rec in self:
            if rec.date_start:
                rec.date_start_splited = rec.date_start.strftime('%Y-%m-%d')
                rec.time_start = rec.date_start.strftime('%H:%M:%S')
            if rec.date_end1:
                rec.date_end_splited = rec.date_end1.strftime('%Y-%m-%d')
                rec.time_end = rec.date_end1.strftime('%H:%M:%S')
            if rec.date_start_splited and rec.date_end_splited:
                if rec.date_start_splited < rec.today_date and rec.date_end_splited > rec.today_date:
                    rec.today_flag = True

    @api.depends('original_image')
    def _resize_image(self):
        for rec in self:
            original_image = rec.with_context({}).original_image
            if original_image:
                data = tools.image_get_resized_images(original_image)
                rec.medium_image = data['image_medium']
                rec.small_image = data['image_small']
            else:
                rec.medium_image = ""
                rec.small_image = ""


class ExecutiveTeams(models.Model):
    _name = 'executive.team'
    _inherit = 'crm.team'

    def _get_default_favorite_user_ids(self):
        return [(6, 0, [self.env.uid])]

    favorite_user_ids = fields.Many2many(
        'res.users', 'executive_team_favorite_user_rel', 'executive_team_id', 'user_id',
        default=_get_default_favorite_user_ids,
        string='Members')


class Teams(models.Model):
    _name = 'project.task.teams'
    _inherit = ['mail.thread']

    name = fields.Char("Team Name", required=True, track_visibility='always')

    member_ids = fields.One2many(
        'team.members',
        'team_id',
        string='Related Member',
        track_visibility='always'
    )


class TeamMembers(models.Model):
    _name = 'team.members'

    name = fields.Char("Member Name", required=True)
    team_id = fields.Many2one('project.task.teams', 'Team Member')


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    traveling_time = fields.Datetime('Target(month of completion)', readonly=True)

    def _select(self):
        return super(ReportProjectTaskUser, self)._select() + """,
            traveling_time as traveling_time"""

    def _group_by(self):
        return super(ReportProjectTaskUser, self)._group_by() + """,
            traveling_time"""
