# -*- coding: utf-8 -*-

from odoo import models, fields, api

class new_awe_edits(models.Model):

    _inherit = 'sale.order'

    work_country_id = fields.Many2one('res.country', 'Work Country')


# class new_project_task(models.Model):
#     _inherit = 'project.task'


    
