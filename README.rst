Back in Stock
=============

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

Notify customers if a product is `Back in Stock`, customize pop-ups and emails for
different types of products.

**This is the Odoo 16 branch**

**Table of contents**

.. contents::
   :local:


Usage
-----

First, review the general settings after install.

In `Settings` -> `Inventory`, in the `Products` sections, you find the `Back in Stock`
group. If you want all your products to allow notifications, set the
``Default Notification Type`` to ``Default Notify Me``, save, and execute the action
``Reset to Default on Products``.

Second, you need to decide whether you want to send the notifications manually or
automatically. To achieve the latter, please select
``Activate Auto Send Back in Stock Notifications`` and save.

Finally, you need to activate the registration for your customers. Navigate to
`Settings` -> `Website`, choose the website in question. In the `Products`
sections of the website activate ``Back in Stock Registration`` and save.


Now, `Temporarily out of stock` products allow for customers to register to be notified
when it's back.

Note, that the ``Notify Me`` is only visible, if a notification type is set.


Customization
^^^^^^^^^^^^^

You may have different types of products, like seasonal products and products, that are
actually not available anymore, but may be back in stock because of rare cases of
returns. You will want to inform your customers about the chances and time period to
have this products back, and for this purpose you can create different
`Notification Types`.

Open the `Inventory` app, and there `Configuration` ->
`Back in Stock Notification Types`. You can create new ones or edit the default. Every
type allows for custom pop-up content and specialized email templates.

Furthermore, you can reduce the max amount of users to be notified on every check
(manually or by the background process). This is useful, when you expect the product to
be sold quickly. Users opening the link to late will find the sold out product again,
presumably an undesirable experience.

In the product form's `Sales` tab, you can choose the notification type in the
``Back In Stock Notification`` select field under ``Out-Of-Stock``.


Overview of pending Notifications
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

On various locations you can check the amount of waiting users and open the
notification details. In the product and contact forms, up in the button box, you see
the amount `Pending` notifications with the envelop icon. To review all notifications,
open `Products` -> `Back in Stock Notifications` in the inventory app.


Bug Tracker
-----------

Bugs are tracked on `GitHub Issues <https://github.com/ayudoo/ayu_back_in_stock>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/ayudoo/ayu_back_in_stock/issues/new**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
-------

Authors
^^^^^^^

* Michael Jurke
* Ayudoo Ltd <support@ayudoo.bg>
