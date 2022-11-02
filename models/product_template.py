from ast import literal_eval
from odoo import fields, models
from odoo.addons.website.models import ir_http


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _default_back_in_stock_notification_type_id(self):
        notification_type_id = int(self.env['ir.config_parameter'].sudo().get_param(
            'ayu_back_in_stock.default_notification_type_id'
        ))
        return self.env['ayu_back_in_stock.notification_type'].search([
            ('id', "=", notification_type_id)
        ], limit=1).id

    back_in_stock_notification_type_id = fields.Many2one(
        "ayu_back_in_stock.notification_type",
        string="Back in Stock Notification Type",
        default=_default_back_in_stock_notification_type_id,
    )

    def _compute_back_in_stock_count(self):
        for record in self:
            record.back_in_stock_count = sum([
                len(p.back_in_stock_ids.filtered(lambda x: x.state == "pending"))
                for p in record.product_variant_ids
            ])

    back_in_stock_count = fields.Integer(compute=_compute_back_in_stock_count)

    def action_product_tmpl_pending_back_in_stock(self):
        action = self.env["ir.actions.actions"]._for_xml_id(
            "ayu_back_in_stock.action_notification"
        )
        action['context'] = literal_eval(action.get('context'))
        if self and len(self) == 1:
            action['context'] = action['context'].update({
                'search_default_product_template_id': self.ids[0],
            })
        return action

    def _get_combination_info(self, *args, **kwargs):
        info = super()._get_combination_info(*args, **kwargs)
        website = ir_http.get_request_website()
        if website:
            info["back_in_stock_notify_me"] = self._get_back_in_stock_notify_me(
                website
            )

        return info

    def _get_back_in_stock_notify_me(self, website):
        if self.back_in_stock_notification_type_id:
            return website.back_in_stock_active

        return False
