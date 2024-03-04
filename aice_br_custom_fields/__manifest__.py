# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Aice BR Custom Fields',
    'version': '1.0.0',
    'category': 'custom_fields',
    'summary': '',
    'description': 'AICE Brazil Custom Fields',
    'live_test_url': '',
    'sequence': '1',
    'website': 'https://codedbytes.vercel.app/',
    'author': 'João Victor',
    'maintainer': '',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['mail','product', 'account', 'report_xlsx', 'web', 'sale', 'base', 'product'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
