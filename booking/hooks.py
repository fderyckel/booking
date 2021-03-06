# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "booking"
app_title = "Booking"
app_publisher = "Britlog"
app_description = "App for managing class booking"
app_icon = "octicon octicon-calendar"
app_color = "#FFB973"
app_email = "info@britlog.com"
app_license = "GNU General Public License"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/booking/css/booking.css"
# app_include_js = "/assets/booking/js/booking.js"

# include js, css files in header of web template
# web_include_css = "/assets/booking/css/booking.css"
# web_include_js = "/assets/booking/js/booking.js"
web_include_css = "/assets/booking/css/website.css"
# web_include_js = "/assets/booking/js/shopping_cart.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "booking.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "booking.install.before_install"
# after_install = "booking.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "booking.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
# doc_events = {
#      "Customer": {
#          "on_update": "booking.booking.doctype.booking_slot.booking_slot.update_remaining_classes"
#      }
# }

doc_events = {
     "Payment Request": {
         "on_change": "booking.booking.doctype.booking.booking.update_payment_status"
     },
	"Sales Order": {
		"before_insert": "booking.booking.doctype.booking_subscription.booking_subscription.set_delivery_date",
		"after_insert": "booking.booking.doctype.booking_subscription.booking_subscription.create_subscription"
	}
}

doctype_js = {
    # "Customer": ["booking/custom_scripts/customer.js"]
	# "Item": ["booking/custom_scripts/item.js"]
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	"all": [
		"booking.booking.doctype.booking_notification.booking_notification.send_notification_email"
	],
	"daily": [
		"booking.booking.doctype.booking_subscription.booking_subscription.update_subscriptions",
		"booking.booking.doctype.booking_subscription.booking_subscription.make_delivery_note_shopping_cart",
		"booking.booking.doctype.booking.booking.convert_sales_order"
	],
	"hourly": [
		"booking.booking.doctype.booking_notification.booking_notification.send_streaming_link"
	]
}
# scheduler_events = {
# 	"all": [
# 		"booking.tasks.all"
# 	],
# 	"daily": [
# 		"booking.tasks.daily"
# 	],
# 	"hourly": [
# 		"booking.tasks.hourly"
# 	],
# 	"weekly": [
# 		"booking.tasks.weekly"
# 	]
# 	"monthly": [
# 		"booking.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "booking.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "booking.event.get_events"
# }

