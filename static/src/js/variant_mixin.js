/*
Forked From Odoo, contributions go there.

Unfortunataly, there is no way of extending or modifying the QWEB template here,
(Note: it is not registered in the manifest). So, we need to override
website_sale_stock.VariantMixin completely just to use another template.
*/
odoo.define('ayu_back_in_stock.VariantMixin', function(require) {
  'use strict';

  var VariantMixin = require('sale.VariantMixin');
  var publicWidget = require('web.public.widget');
  var ajax = require('web.ajax');
  var core = require('web.core');
  var QWeb = core.qweb;
  var xml_load = ajax.loadXML(
    '/ayu_back_in_stock/static/src/xml/product_availability.xml',
    QWeb
  );

  VariantMixin._onChangeCombinationStock = function(ev, $parent, combination) {
    var product_id = 0;
    // needed for list view of variants
    if ($parent.find('input.product_id:checked').length) {
      product_id = $parent.find('input.product_id:checked').val();
    } else {
      product_id = $parent.find('.product_id').val();
    }
    var isMainProduct = combination.product_id &&
      ($parent.is('.js_main_product') || $parent.is('.main_product')) &&
      combination.product_id === parseInt(product_id);

    if (!this.isWebsite || !isMainProduct) {
      return;
    }
    var qty = $parent.find('input[name="add_qty"]').val();

    $parent.find('#add_to_cart').removeClass('out_of_stock');
    $parent.find('#buy_now').removeClass('out_of_stock');
    if (combination.product_type === 'product' && _.contains(['always', 'threshold'], combination.inventory_availability)) {
      combination.virtual_available -= parseInt(combination.cart_qty);
      if (combination.virtual_available < 0) {
        combination.virtual_available = 0;
      }
      // Handle case when manually write in input
      if (qty > combination.virtual_available) {
        var $input_add_qty = $parent.find('input[name="add_qty"]');
        qty = combination.virtual_available || 1;
        $input_add_qty.val(qty);
      }
      if (qty > combination.virtual_available ||
        combination.virtual_available < 1 || qty < 1) {
        $parent.find('#add_to_cart').addClass('disabled out_of_stock');
        $parent.find('#buy_now').addClass('disabled out_of_stock');
      }
    }

    xml_load.then(function() {
      $('.oe_website_sale')
        .find('.availability_message_' + combination.product_template)
        .remove();

      var $message = $(QWeb.render(
        'website_sale_stock.product_availability',
        combination
      ));
      $('div.availability_messages').html($message);
    });
  };

  return VariantMixin;

});
