# Copyright 2022 <mj@ayudoo.bg>
# License LGPLv3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

{
    "author": "Michael Jurke, Ayudoo EOOD",
    "name": "Back in Stock",
    "version": "0.1",
    "summary": "Back in Stock Notifications",
    "description": """
        Let your customers receive customizable notififations for products back in stock
    """,
    "license": "LGPL-3",
    "category": "Sales/Sales",
    "support": "support@ayudoo.bg",
    "application": True,
    "installable": True,
    "depends": [
        "base",
        "contacts",
        "website_sale_stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/mail_data.xml",
        "data/notification_type_data.xml",
        "data/ir_cron.xml",
        "views/notification_view.xml",
        "views/notification_type_view.xml",
        "views/partner_view.xml",
        "views/product_view.xml",
        "views/res_config_settings_view.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "ayu_back_in_stock/static/src/scss/frontend.scss",
            "ayu_back_in_stock/static/src/js/variant_mixin.js",
            "ayu_back_in_stock/static/src/js/register.js",

            "ayu_back_in_stock/static/src/xml/product_availability.xml",
        ],
    },
    "demo": [],
}
