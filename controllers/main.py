import werkzeug
from odoo import http
from odoo.addons.http_routing.models.ir_http import unslug
from odoo.addons.website_sale_stock.controllers.main import WebsiteSale
from odoo.exceptions import UserError
from odoo.http import request


class WebsiteSaleBackInStock(WebsiteSale):
    @http.route(
        ['/back-in-stock/registration-form/<int:product_id>'],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def back_in_stock_product(self, product_id, **kwargs):
        email = ""
        product = request.env["product.product"].browse(product_id)
        is_website_restricted_editor = request.env['res.users'].has_group(
            'website.group_website_restricted_editor'
        )

        if not (
            product.exists()
            and (is_website_restricted_editor or product.sudo().website_published)
        ):
            raise werkzeug.exceptions.NotFound("Product ID not found")

        if not request.website.is_public_user():
            is_registered = self._is_back_in_stock_registered(product)

            if is_registered:
                return request.env["ir.ui.view"]._render_template(
                    "ayu_back_in_stock.back_in_stock_already_registered",
                    {
                        "product": product,
                    },
                )

            if request.env.user.email:
                email = request.env.user.email

        notification_type = product.product_tmpl_id.back_in_stock_notification_type_id

        if not notification_type:
            return ""

        return request.env["ir.ui.view"]._render_template(
            "ayu_back_in_stock.back_in_stock_registration_form",
            {
                "pop_up_content": notification_type.pop_up_content,
                "notification_type": notification_type,
                "product": product,
                "email": email,
            },
        )

    def _is_back_in_stock_registered(self, product, email=None):
        if email is None and not request.website.is_public_user():
            email = request.env.user.partner_id.email

        if not email:
            return

        return (
            request.env["ayu_back_in_stock.notification"]
            .sudo()
            .search(
                [
                    ("product_id", "=", product.id),
                    ("email", "=", email),
                    ("state", "=", "pending"),
                ],
                limit=1,
            )
        )

    @http.route(
        ["/back-in-stock/notify-me"],
        type="json",
        auth="public",
        methods=["POST"],
        website=True,
        sitemap=False,
    )
    def back_in_stock_notify_me(self, email, product_id, **kwargs):
        if not email:
            raise UserError("Invalid Email")

        product_id = int(product_id)
        product = request.env["product.product"].browse(product_id)

        if not product.exists():
            raise werkzeug.exceptions.NotFound("Product ID not found")

        is_registered = self._is_back_in_stock_registered(product, email)
        if is_registered:
            return {
                "Message": "Already Registered",
            }

        Notification = request.env["ayu_back_in_stock.notification"].sudo()
        values = self._get_back_in_stock_notification_data(email, product, **kwargs)
        notification = Notification.create(values)
        notification.send_registration_confirmation_mail()

        return {
            "Message": "Registered Successfully",
        }

    def _get_back_in_stock_notification_data(self, email, product, **kwargs):
        lang_id = request.env["res.lang"]._lang_get_id(request.context["lang"])

        values = {
            "email": email,
            "lang_id": lang_id,
            "product_id": product.id,
            "website_id": request.website.id,
            "user_id": request.website.salesperson_id
            and request.website.salesperson_id.id,
        }
        if not request.website.is_public_user():
            values["partner_id"] = request.env.user.partner_id.id

        return values

        values = {
            "email": email,
            "lang_id": lang_id,
            "product_id": product.id,
            "website_id": request.website.id,
            "user_id": request.website.salesperson_id
            and request.website.salesperson_id.id,
        }
        if not request.website.is_public_user():
            values["partner_id"] = request.env.user.partner_id.id

        return values
