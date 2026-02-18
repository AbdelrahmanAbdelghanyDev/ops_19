# -*- coding: utf-8 -*-
# from odoo import http


# class CostEstimationInterface(http.Controller):
#     @http.route('/cost_estimation_interface/cost_estimation_interface/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cost_estimation_interface/cost_estimation_interface/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cost_estimation_interface.listing', {
#             'root': '/cost_estimation_interface/cost_estimation_interface',
#             'objects': http.request.env['cost_estimation_interface.cost_estimation_interface'].search([]),
#         })

#     @http.route('/cost_estimation_interface/cost_estimation_interface/objects/<model("cost_estimation_interface.cost_estimation_interface"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cost_estimation_interface.object', {
#             'object': obj
#         })
