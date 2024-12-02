# -*- coding: utf-8 -*-
from odoo import http


class Openacademy(http.Controller):
    @http.route('/openacademy/openacademy', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/openacademy/static_list', auth='public')
    def static_list(self, **kw):
        return """
        <html>
            <body>
                <ul>
                    <li>Diana Padilla</li>
                    <li>Jody Caroll</li>
                    <li>Lester Vaughn</li>
                </ul>
            </body>
        </html>
        """

    @http.route('/openacademy/sessions', auth='public', website=True)
    def list_sessions(self, **kw):
        Sessions = http.request.env['openacademy.session'].sudo().search([])
        return http.request.render('openacademy.session_list_template', {
            'sessions': Sessions
        })