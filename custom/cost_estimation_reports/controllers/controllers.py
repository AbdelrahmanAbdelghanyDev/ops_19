# -*- coding: utf-8 -*-
# from odoo import http


# class CostEstimationReports(http.Controller):
#     @http.route('/cost_estimation_reports/cost_estimation_reports/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cost_estimation_reports/cost_estimation_reports/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cost_estimation_reports.listing', {
#             'root': '/cost_estimation_reports/cost_estimation_reports',
#             'objects': http.request.env['cost_estimation_reports.cost_estimation_reports'].search([]),
#         })

#     @http.route('/cost_estimation_reports/cost_estimation_reports/objects/<model("cost_estimation_reports.cost_estimation_reports"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cost_estimation_reports.object', {
#             'object': obj
#         })
