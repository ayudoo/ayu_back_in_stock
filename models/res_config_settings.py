from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("back_in_stock_notification_type_id")
    def compute_back_in_stock_ir_cron_id(self):
        self.auto_send_back_in_stock_ir_cron_id = self.env.ref(
            "ayu_back_in_stock.ir_cron_send_back_in_stock_notifications"
        )

    back_in_stock_notification_type_id = fields.Many2one(
        "ayu_back_in_stock.notification_type",
        string="Default Notification Type",
        config_parameter="ayu_back_in_stock.default_notification_type_id",
    )

    auto_send_back_in_stock_ir_cron_id = fields.Many2one(
        "ir.cron",
        compute=compute_back_in_stock_ir_cron_id,
        string="Auto Send Back in Stock Notifications",
    )

    auto_send_back_in_stock_active = fields.Boolean(
        string="Activate Auto Send Back in Stock Notifications",
        readonly=False,
        related="auto_send_back_in_stock_ir_cron_id.active",
    )
    auto_send_back_in_stock_interval_number = fields.Integer(
        string="Auto Send Back in Stock Interval Number",
        default=1,
        help="Auto Send Back in Stock Repeat every x.",
        related="auto_send_back_in_stock_ir_cron_id.interval_number",
        readonly=False,
    )
    auto_send_back_in_stock_interval_type = fields.Selection(
        string="Auto Send Back in Stock Interval Unit",
        default="days",
        related="auto_send_back_in_stock_ir_cron_id.interval_type",
        readonly=False,
    )
    auto_send_back_in_stock_nextcall = fields.Datetime(
        string="Auto Send Back in Stock Next Execution Date",
        related="auto_send_back_in_stock_ir_cron_id.nextcall",
        readonly=False,
    )

    website_back_in_stock_active = fields.Boolean(
        string="Activate Back in Stock Customer Registrations",
        readonly=False,
        related="website_id.back_in_stock_active",
    )

    website_back_in_stock_reply_to = fields.Char(
        string="Back-In-Stock Reply To",
        readonly=False,
        related="website_id.back_in_stock_reply_to",
    )

    def action_update_notification_type_on_products(self):
        type_id = self.back_in_stock_notification_type_id.id or False
        self.env["product.template"].with_context(active_test=False).search([]).write(
            {"back_in_stock_notification_type_id": type_id}
        )

    def action_send_back_in_stock_notification_mails_now(self):
        self.env["website"].send_back_in_stock_notification_mails()
