# -*- coding: utf-8 -*-
# from odoo import http


# class CitProjectSaleName(http.Controller):
#     @http.route('/cit_project_sale_name/cit_project_sale_name', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cit_project_sale_name/cit_project_sale_name/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cit_project_sale_name.listing', {
#             'root': '/cit_project_sale_name/cit_project_sale_name',
#             'objects': http.request.env['cit_project_sale_name.cit_project_sale_name'].search([]),
#         })

#     @http.route('/cit_project_sale_name/cit_project_sale_name/objects/<model("cit_project_sale_name.cit_project_sale_name"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cit_project_sale_name.object', {
#             'object': obj
#         })
