{
    'name': 'OPS Purchase Customization',
    'version': '1.0',
    'category': 'Purchase',
    'summary': 'Customize purchase order template based on company settings',
    'description': '''
        This module customizes the purchase order template to replace "Shipping Address" 
        and "Contact" with "Client" based on company ops_emirate setting.
    ''',
    'depends': ['purchase','base','purchase_stock'],
    'data': [
        'views/res_company_views.xml',
        'views/purchase_order_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}