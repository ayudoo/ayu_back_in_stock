from odoo import api, models, fields


class Website(models.Model):
    _inherit = "website"

    back_in_stock_active = fields.Boolean(
        string="Activate Back in Stock Customer Registrations",
        readonly=False,
        default=False,
    )

    pending_back_in_stock_ids = fields.One2many(
        "ayu_back_in_stock.notification",
        "website_id",
        domain=[("state", "=", "pending")],
        string="Pending Back in Stock Notifications",
    )

    back_in_stock_reply_to = fields.Char(
        string="Back-In-Stock Reply To",
        translate=False,
    )

    @api.model
    def send_back_in_stock_notification_mails(self):
        for website in self.search([]):
            for product in website.pending_back_in_stock_ids.product_id:
                product._send_back_in_stock_notification_mails(website)
