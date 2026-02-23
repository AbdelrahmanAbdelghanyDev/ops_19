# -*- coding: utf-8 -*-
{
    'name': "Ops custom Cost Estimation",


    'author': "centione",
    'website': "http://www.centione.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account','cost_estimation','product','stock','crm'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/sale_order.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    # 'qweb': ['static/src/xml/disable_save.xml'],

}
