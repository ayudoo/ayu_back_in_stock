from odoo import fields, models
from ast import literal_eval


class Partner(models.Model):
    _inherit = "res.partner"

    back_in_stock_ids = fields.One2many(
        "ayu_back_in_stock.notification",
        "partner_id",
        string="Back in Stock Notifications",
    )

    def _compute_back_in_stock_count(self):
        for record in self:
            record.back_in_stock_count = len(
                record.back_in_stock_ids.filtered(lambda x: x.state == "pending")
            )

    back_in_stock_count = fields.Integer(compute=_compute_back_in_stock_count)

    def action_pending_back_in_stock(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ayu_back_in_stock.action_notification"
        )
        action["context"] = literal_eval(action.get("context"))
        if self and len(self) == 1:
            action["context"] = action["context"].update(
                {
                    "search_default_partner_id": self.id,
                }
            )
        return action
