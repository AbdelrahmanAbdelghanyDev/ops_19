# -*- coding: utf-8 -*-
# from odoo import http


# class ChannelLinePeriodGet(http.Controller):
#     @http.route('/channel_line_period_get/channel_line_period_get/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/channel_line_period_get/channel_line_period_get/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('channel_line_period_get.listing', {
#             'root': '/channel_line_period_get/channel_line_period_get',
#             'objects': http.request.env['channel_line_period_get.channel_line_period_get'].search([]),
#         })

#     @http.route('/channel_line_period_get/channel_line_period_get/objects/<model("channel_line_period_get.channel_line_period_get"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('channel_line_period_get.object', {
#             'object': obj
#         })
