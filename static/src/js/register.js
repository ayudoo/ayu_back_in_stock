odoo.define('back_in_stock.register', function(require) {
  'use strict';

  var publicWidget = require('web.public.widget');
  var core = require('web.core');
  var _t = core._t;
  var timeout;

  publicWidget.registry.BackInStockRegister = publicWidget.Widget.extend({
    selector: '.oe_website_sale #product_details',
    events: {
      'click .js_back_in_stock_notify_me': '_onClick',
    },

    init: function() {
      this._super.apply(this, arguments);
      this._loading = false;

      // this._openRegisterModal = _.debounce(this._openRegisterModal.bind(this), 500);
    },

    start: function() {
      return this._super.apply(this, arguments);
    },

    _setLoading: function(loading, $link) {
      this._loading = loading;
      if (loading) {
        if ($link && $link.length) {
          $link.find('.fa-envelope-o').addClass("fa-spinner fa-spin");
        } else {
          this.$('.fa-envelope-o').addClass("fa-spinner fa-spin");
        }
      } else {
        this.$('.fa-envelope-o').removeClass("fa-spinner fa-spin");
      }
    },

    _thankYou: function() {
      this.$(".availability_messages .js_back_in_stock_notify_me").replaceWith(
        "<div>" + _t("Thank You for your registration!") + "<div>"
      );
    },

    _openRegisterModal: function(productId) {
      var url = "/back-in-stock/registration-form/" + productId;
      self._modalRPC = $.get(url, {
        type: 'modal',
      }).then((data) => {
          this._setLoading(false);
          this.$("#ayu_back_in_in_stock_registration_modal").remove();
          this.$el.append(data)
          var $modal = this.$("#ayu_back_in_in_stock_registration_modal");

          if ($modal.length) {
            $modal.modal('show');

            $modal.on('click', 'button#btn_submit', (event) => {
              var $button = $(event.target);
              $button.html("<span class='fa fa-spinner fa-spin'/>");
              event.preventDefault();

              var email = $(event.target).closest('form').find('input[name="email"]').val();
              var productId = $(event.target).closest('form').find('input[name="product_id"]').val();
              email = email.trim();

              this._rpc({
                route: "/back-in-stock/notify-me",
                params: {
                  'email': email,
                  'product_id': productId,
                }
              }).then((data) => {
                this._thankYou();
                $modal.modal('hide');
                setTimeout(function() {
                  $modal.remove();
                }, 1000);
              })
            });
          }
        },
        (error) => {
          this._setLoading(false);
          console.log(error);
        }
      );
    },

    _onClick: function(ev) {
      var $link = $(ev.target).closest(".js_back_in_stock_notify_me");
      var productId = $link.data('productId');
      ev.preventDefault();
      if (this._loading) {
        return;
      }
      if (!productId) {
        return
      }
      this._setLoading(true, $link);
      this._openRegisterModal(productId);
    },
  });

  return publicWidget.registry.BackInStockRegister;
});
