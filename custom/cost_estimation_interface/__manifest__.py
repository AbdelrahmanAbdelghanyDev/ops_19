# -*- coding: utf-8 -*-
{
    'name': "Cost Estimation Interface",

    'summary': """
        Interface between awe_cost_estimation and cost_estimation""",

    'description': """
        holds the data that makes dependency loop in both modules
    """,

    'author': "Digizilla",
    'website': "http://digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'custom_opportunity_cost_estimation_v11'],

    # always loaded
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
