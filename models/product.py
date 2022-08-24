from ast import literal_eval
from odoo import fields, models
from odoo.tools import float_compare


class Product(models.Model):
    _inherit = "product.product"

    back_in_stock_ids = fields.One2many(
        "ayu_back_in_stock.notification",
        "product_id",
        string="Back in Stock Notifications",
    )

    def _compute_back_in_stock_count(self):
        for record in self:
            record.back_in_stock_count = len(
                record.back_in_stock_ids.filtered(lambda x: x.state == "pending")
            )

    back_in_stock_count = fields.Integer(compute=_compute_back_in_stock_count)

    def action_product_tmpl_pending_back_in_stock(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ayu_back_in_stock.action_notification"
        )
        action["context"] = literal_eval(action.get("context"))
        if self and len(self) == 1:
            action["context"].update(
                {
                    "search_default_product_id": self.ids[0],
                }
            )
        return action

    def _send_back_in_stock_notification_mails(self, website):
        self = self.with_context(
            website_id=website.id,
            warehouse=website._get_warehouse_available(),
        )

        if (
            float_compare(
                self.virtual_available, 0, precision_rounding=self.uom_id.rounding
            )
            <= 0
        ):
            return

        notification_type = self.product_tmpl_id.back_in_stock_notification_type_id

        limit = notification_type.get_limit_to_notify(self.virtual_available)

        pending_notification = self.env["ayu_back_in_stock.notification"].search(
            [
                ("website_id", "=", website.id),
                ("product_id", "=", self.id),
                ("state", "=", "pending"),
            ],
            limit=limit,
        )

        for notification in pending_notification:
            notification.send_back_in_stock_mail()
