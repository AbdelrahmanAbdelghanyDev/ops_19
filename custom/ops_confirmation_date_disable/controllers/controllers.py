# -*- coding: utf-8 -*-
# from odoo import http


# class OpsConfirmationDateDisable(http.Controller):
#     @http.route('/ops_confirmation_date_disable/ops_confirmation_date_disable/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ops_confirmation_date_disable/ops_confirmation_date_disable/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ops_confirmation_date_disable.listing', {
#             'root': '/ops_confirmation_date_disable/ops_confirmation_date_disable',
#             'objects': http.request.env['ops_confirmation_date_disable.ops_confirmation_date_disable'].search([]),
#         })

#     @http.route('/ops_confirmation_date_disable/ops_confirmation_date_disable/objects/<model("ops_confirmation_date_disable.ops_confirmation_date_disable"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ops_confirmation_date_disable.object', {
#             'object': obj
#         })
