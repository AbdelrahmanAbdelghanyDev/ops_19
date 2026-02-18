# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Gender(models.Model):
    _name = 'gender.data'

    name = fields.Char()


class Region(models.Model):
    _name = 'region.data'

    name = fields.Char()


class Age(models.Model):
    _name = 'age.data'
    _order = "name asc"
    name = fields.Char()


class SEC(models.Model):
    _name = 'sec.data'

    name = fields.Char()
