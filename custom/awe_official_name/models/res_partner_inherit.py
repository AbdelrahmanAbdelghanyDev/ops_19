from odoo import models, fields, api


class AweResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    _rec_name = 'official_name'

    official_name = fields.Char(string='Official Name')
    cr_numb = fields.Char(string="CR Number", required=False)
