# -*- coding: utf-8 -*-
from datetime import date

from odoo import models, fields, api
import re
from odoo import exceptions


class AQuestionnaire(models.Model):
    _inherit = 'a.questionnaire'



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('mobile')
    def constrains_mobile(self):
        if self.mobile:
            # rule = re.compile(r'(^[+0-9]{1,3})*([0-9]{10,11}$)')
            rule = re.compile(r'(^([+]\d{2})?\d{10}$)')
            if not rule.search(self.mobile):
                raise exceptions.ValidationError('Invalid mobile number.')
            if len(self.env['res.partner'].search([('mobile', '=', self.mobile)])) > 1:
                telephone = self.env['a.questionnaire'].search([('respondent_id', '=', self.id),('telephone', '=', self.mobile)])
                if telephone:
                    date_diff = date.today() - telephone.date
                    if date_diff.days < 180:
                        raise exceptions.ValidationError('This Mobile Is Available')
