# Copyright 2022 <mj@ayudoo.bg>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    'author': "Michael Jurke, Ayudoo EOOD",
    'name': "Back in Stock",
    'summary': """
        Let your customers receive customizable notififations for products back in stock
        """,
    'description': """
        Let your customers receive customizable notififations for products back in stock
    """,
    'license': 'LGPL-3',
    'category': 'Sales/Sales',

    'version': '0.1',

    "depends": [
        "base",
        "contacts",
        "website_sale_stock",
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data.xml',
        'data/notification_type_data.xml',
        'data/ir_cron.xml',
        'views/notification_view.xml',
        'views/notification_type_view.xml',
        'views/partner_view.xml',
        'views/product_view.xml',
        'views/res_config_settings_view.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
    'application': True,
    'installable': True,
    'demo': [
    ],
}
