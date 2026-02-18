{
    'name': "Cost Estimation",

    'summary': """
    General Cost Estimation Module""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'crm',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'new_awe_edits', 'custom_opportunity_cost_estimation_v11', 'account_budget', 'crm',
                'cost_estimation_interface', 'awe_cost_estimation','report_xlsx'],

    # always loaded
    'data': [
        # 'data/data.xml',
        'security/ir.model.access.csv',
        'views/settings.xml',
        'views/crm.xml',
        'views/cost_estimation.xml',
        'views/product.xml',
        'views/quotation.xml',
        'views/cost_estimation_report.xml',

        # 'views/templates.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
# -*- coding: utf-8 -*-
