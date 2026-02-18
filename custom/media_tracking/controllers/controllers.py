# -*- coding: utf-8 -*-
# from odoo import http


# class MediaTracking(http.Controller):
#     @http.route('/media_tracking/media_tracking/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/media_tracking/media_tracking/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('media_tracking.listing', {
#             'root': '/media_tracking/media_tracking',
#             'objects': http.request.env['media_tracking.media_tracking'].search([]),
#         })

#     @http.route('/media_tracking/media_tracking/objects/<model("media_tracking.media_tracking"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('media_tracking.object', {
#             'object': obj
#         })
