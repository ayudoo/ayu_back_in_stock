import werkzeug
from odoo.addons.website_sale_stock.controllers.main import WebsiteSale
from odoo import http
from odoo.http import request


class WebsiteSaleBackInStock(WebsiteSale):
    @http.route(
        ['/back-in-stock/registration-form/<model("product.product"):product>'],
        type="http",
        auth="public",
        website=True,
    )
    def back_in_stock_product(self, product, **kwargs):
        email = ""

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
    )
    def back_in_stock_notify_me(self, email, product_id, **kwargs):
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
