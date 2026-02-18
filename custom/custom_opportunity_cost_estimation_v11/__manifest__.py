# -*- coding: utf-8 -*-
{
    'name': "custom_opportunity_cost_estimation_v11",

    'summary': """
         Adding Cost estimation to the sales module.
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Digizilla_M.Rizk",
    'website': "http://digizilla.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
        'crm',
        'sale',
        'sale_management',
        'sale_crm',
        'product',
        'project',
        'hr_timesheet',
        'account_accountant',
        'account',
        'custom_project',
        'sector',
    ],


    # always loaded
    'data': [
        'security/user_groups.xml',
        'data/data.xml',
        'views/cost_estimate_views.xml',
        'views/project.xml',
        'views/sales.xml',
        'views/task.xml',
        'views/templates.xml',
        'views/estimation_template_changes_view.xml',
        'views/quotation_estimation_inherit.xml',
        'views/budget_unit_invisible_inherit.xml',
        'security/user_groups.xml',
        'views/invoice_form_inherit.xml',
        'security/ir.model.access.csv',
    ],

    "assets": {
        "web.assets_backend": [
            # 'static/src/xml/widget.xml',
            # 'static/src/js/widget.js',
     ],
    },


    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
