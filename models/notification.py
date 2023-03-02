import logging
from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.addons.website.models import ir_http
from odoo.exceptions import UserError
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class Notification(models.Model):
    _inherit = ["mail.thread"]
    _name = "ayu_back_in_stock.notification"
    _description = "Back in Stock Notification"
    _order = "sequence, id"
    _rec_name = "email"

    sequence = fields.Integer("Sequence")

    state = fields.Selection(
        [
            ("pending", "Pending"),
            ("notified", "Notified"),
            ("cancel", "Cancelled"),
        ],
        default="pending",
        required=True,
    )

    notification_type_id = fields.Many2one(
        "ayu_back_in_stock.notification_type",
        string="Type",
        related="product_template_id.back_in_stock_notification_type_id",
        readonly=True,
    )

    website_id = fields.Many2one("website", required=True)

    def _active_languages(self):
        return self.env["res.lang"].search([]).ids

    def _default_language(self):
        lang_code = self.env["ir.default"].get("res.partner", "lang")
        def_lang_id = self.env["res.lang"]._lang_get_id(lang_code)
        return def_lang_id or self._active_languages()[0]

    lang_id = fields.Many2one(
        "res.lang", string="Language", default=_default_language, required=True
    )

    user_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        index=True,
        default=lambda self: self.env.user,
        domain=lambda self: [
            ("groups_id", "in", self.env.ref("sales_team.group_sale_salesman").id)
        ],
    )

    email = fields.Char("Email", translate=False, required=True, index=True)

    partner_id = fields.Many2one("res.partner", string="Contact", index=True)

    product_id = fields.Many2one(
        "product.product", string="Product", required=True, index=True
    )

    product_template_id = fields.Many2one(
        "product.template",
        string="Product Template",
        related="product_id.product_tmpl_id",
    )

    sent_date = fields.Datetime("Sent on", readonly=True)

    @api.depends("email", "partner_id")
    def _compute_email_formatted(self):
        for record in self:
            if record.partner_id and record.partner_id.name:
                email = tools.formataddr((record.partner_id.name, record.email))
            else:
                email = record.email

            record.email_formatted = email

    email_formatted = fields.Char(
        "Formatted Email",
        compute=_compute_email_formatted,
        help='Format email address "Name <email@domain>"',
    )

    @api.depends("product_id")
    def _product_display_name(self):
        for record in self:
            if not record.product_id:
                record.product_name = ""
                continue

            record.product_name = record.product_id.with_context(
                display_default_code=False
            ).display_name

    product_name = fields.Char(
        "Product Name",
        compute=_product_display_name,
    )

    email = fields.Char("Email", translate=False, required=True, index=True)

    @api.depends("website_id", "product_id")
    def _compute_website_available(self):
        for record in self:
            if not record.product_id:
                record.website_available = 0
                continue

            product = record.product_id

            if record.website_id:
                product = product.with_context(
                    website_id=record.website_id.id,
                    warehouse=record.website_id._get_warehouse_available(),
                )

            record.website_available = product.virtual_available

    website_available = fields.Float(
        "Website Quantity",
        compute=_compute_website_available,
        digits="Product Unit of Measure",
    )

    @api.model
    def create(self, vals):
        email = vals.get("email", None)
        partner_id = vals.get("partner_id", None)
        website = ir_http.get_request_website()

        if email:
            # enforce user contact when created from website context
            if website and not website.is_public_user():
                vals["partner_id"] = self.env.user.partner_id.id

            elif not partner_id:
                partners = self.env["res.partner"].search([("email", "=", email)])
                if partners:
                    vals["partner_id"] = partners[0].id

        return super().create(vals)

    def _notify_get_reply_to(self, **kwargs):
        res = super()._notify_get_reply_to(**kwargs)
        if self.website_id.back_in_stock_reply_to:
            res = {
                res_id: self.website_id.back_in_stock_reply_to
                for res_id in res.keys()
            }
        return res

    def send_registration_confirmation_mail(self):
        if self.env.su:
            self = self.with_user(SUPERUSER_ID)

        template_id = self.notification_type_id.registration_template_id.id
        if template_id:
            self.with_context(force_send=True).message_post_with_template(
                template_id,
                composition_mode="comment",
            )

    def send_back_in_stock_mail(self, raise_exception=True):
        if (
            float_compare(
                self.website_available,
                0,
                precision_rounding=self.product_id.uom_id.rounding,
            )
            <= 0
        ):
            msg = (
                "You want to send a back in stock notification."
                + " But product #{} is currently not available!".format(
                    self.product_id.id
                )
            )
            if raise_exception:
                raise UserError(msg)
            else:
                _logger.warning(msg)
                return

        if self.env.su:
            self = self.with_user(SUPERUSER_ID)

        template_id = self.notification_type_id.back_in_stock_template_id.id
        if template_id:
            self.with_context(force_send=True).message_post_with_template(
                template_id,
                composition_mode="comment",
            )
            self.write({"state": "notified"})

    def action_reset_to_pending(self):
        self.write({"state": "pending"})

    def action_cancel(self):
        self.write({"state": "cancel"})
