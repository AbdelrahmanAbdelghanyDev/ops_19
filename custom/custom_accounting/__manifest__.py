# -*- coding: utf-8 -*-
{
    'name': "custom_accounting",

    'summary': """
        Cash in and out report with currency""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla_E",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'account_reports', 'account_accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/custom_account_report.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # 'qweb': ['static/src/xml/disable_save.xml'],

}
