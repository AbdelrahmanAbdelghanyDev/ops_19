# -*- coding: utf-8 -*-
{
    'name': "Cost Estimation Reports",

    'summary': """
      
      """,

    'description': """
    
    """,

    'author': "Digizilla",
    'website': "http://www.digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'CRM',
    'version': '11',

    # any module necessary for this one to work correctly
    'depends': ['base', 'cost_estimation'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/cost_estimation_report.xml',
        'views/cost_estimation_product_report.xml',
        'views/cost_estimation_type_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
