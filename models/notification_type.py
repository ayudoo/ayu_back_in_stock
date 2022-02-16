import math
from odoo import fields, models


class NotificationType(models.Model):
    _name = "ayu_back_in_stock.notification_type"
    _description = "Back in Stock Notification Type"

    active = fields.Boolean(
        default=True,
        help="If the active field is set to false, it will allow you to hide"
        + " it without removing it.",
    )

    name = fields.Char(translate=True, required=True)

    on_back_in_stock = fields.Selection(
        [
            ("notify_all", "Notify All Waiting Users"),
            ("notify_fixed", "Notify Fixed Amount of Waiting Users"),
            ("notify_multiple", "Notify Multiple of Stock Amount"),
        ],
        string="On Back in Stock",
        default="notify_all",
        help="Your products might be sold quickly. To avoid frustration of waiting"
        + " users, you can customize the maximum number of users to be notified when"
        + " the scheduler runs.",
        required=True,
    )

    fixed_count = fields.Integer("Fixed", default=10)

    multiple_count = fields.Integer(
        "Multiple of Stock",
        default=5,
        help="Notifies as many users as the available amount multiplied with this"
        + " value, rounded up to full integers.",
    )

    registration_template_id = fields.Many2one(
        "mail.template",
        string="Registration Email",
        domain="[('model', '=', 'ayu_back_in_stock.notification')]",
        help="Email sent to the customer after having registered for back in stock.",
        required=True,
    )

    back_in_stock_template_id = fields.Many2one(
        "mail.template",
        string="Back in Stock Email",
        domain="[('model', '=', 'ayu_back_in_stock.notification')]",
        help="Email sent to the customer when the product is back in stock.",
        required=True,
    )

    pop_up_content = fields.Html(
        "Pop-Up Content",
        translate=True,
        required=True,
    )

    product_template_ids = fields.One2many(
        "product.template",
        "back_in_stock_notification_type_id",
        string="Products",
    )

    def get_limit_to_notify(self, available):
        if self.on_back_in_stock == "notify_all":
            return False
        if self.on_back_in_stock == "notify_fixed":
            return self.fixed_count
        if self.on_back_in_stock == "notify_multiple":
            return math.ceil(self.multiple_count * available)
