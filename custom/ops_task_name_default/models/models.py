# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTaskInh(models.Model):
    _inherit = 'project.task'

    @api.onchange('project_id')
    def onchange_method(self):
        if self.project_id:
            self.name = self.project_id.name + ': '
        else:
            self.name = ''
