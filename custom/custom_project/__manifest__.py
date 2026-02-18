# -*- coding: utf-8 -*-
{
    'name': "CustomProject",
    'summary': "Customization for Project Module Reports",
    'description': "Customization for Project Module Reports",
    'author': "Digizilla",
    'website': "http://www.digizilla.net",
    'category': 'Project',
    'version': '0.1',
    'depends': ['base', 'project', 'hr_timesheet', 'crm', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        'views/templates.xml',
        'reports.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}
