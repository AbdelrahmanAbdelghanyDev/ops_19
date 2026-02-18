# -*- coding: utf-8 -*-
{
    'name': "AWE Media Tracking",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla",
    'website': "https://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'contacts', 'web'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/n1.xml',
        'data/n4.xml',
        'views/views.xml',
        'views/channels.xml',
        'views/programs.xml',
        'wizard/add_line.xml',
        'views/questionnaire.xml',
        'views/s1.xml',
        'views/n2.xml',
        'views/n3.xml',
        'views/sec4.xml',
        'views/sec4b.xml',
        'views/sec4c.xml',
        'views/data_process.xml',
        'views/raiting_by_program_quarter.xml',
        'views/raiting_by_program_full.xml',
        'views/time_from.xml',
        'views/time_to.xml',
        'views/raiting_by_program_full.xml',
        'views/n1_internet_report.xml',
        'views/n2_internet_report.xml',
        'views/n3_internet_report.xml',
        'views/n4_internet_report.xml',
        'views/reach_report.xml',
        # 'views/quarter_region.xml',
        # 'views/quarter_age.xml',
        # 'views/quarter_sec.xml',
        'report/gender_report.xml',
        'report/gender_template.xml',
        'wizard/report_quarter.xml',
        'wizard/report_internet.xml',
        'views/template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'media_tracking/static/src/js/required.js',
            'media_tracking/static/src/js/web_widget_timepicker.js',
        ],
    },
}
