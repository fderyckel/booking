# -*- coding: utf-8 -*-
# Copyright (c) 2017, Britlog and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class BookingNotification(Document):
	pass

def trigger_notification(slot):
	"""
		Clear sending_date to trigger email notification
	"""

	# check if a new place is available
	last_available_places = frappe.get_value('Booking Slot', slot.name, 'available_places') or 0

	if int(last_available_places) <= 0 and int(slot.available_places) > 0:
		for notification in slot.get('notifications'):
			if frappe.db.sql("""select COUNT(*) from `tabBooking` where slot = %(slot)s and email_id = %(email)s""",
							{"slot": slot.name, "email": notification.email_id})[0][0] <= 0:
				notification.sending_date = ""

def send_notification_email():
	"""
		Send email to customer who ask to be warned for available places
	"""

	notifications = frappe.db.sql("""select distinct BS.name AS slot, BN.email_id
			from `tabBooking Slot` BS
			inner join `tabBooking Notification` BN on BS.name = BN.parent
			where BS.time_slot > NOW() and BS.available_places > 0 and BN.sending_date is null""", as_dict=True)

	if notifications:
		waiting_list_notification = frappe.db.get_single_value('Booking Settings', 'waiting_list_notification')

		if waiting_list_notification:
			email_template = frappe.get_doc("Email Template", waiting_list_notification)

			for notification in notifications:

				args = frappe.get_doc('Booking Slot', notification.slot).as_dict()
				message = frappe.render_template(email_template.response, args)
				subject = frappe.render_template(email_template.subject, args)

				try:
					frappe.sendmail(
						recipients=notification.email_id,
						message=message,
						subject=subject)
				except Exception as e:
					frappe.log_error(frappe.get_traceback(), 'waiting list notification email failed')

				frappe.db.sql("""
					update `tabBooking Notification` set sending_date = NOW(), counter = IFNULL(counter,0) + 1 
					where parent = %(parent)s and email_id = %(email)s and sending_date is null """,
					{"parent": notification.slot,"email":notification.email_id})

def send_streaming_link():
	"""
		Send streaming link by email
	"""

	notifications = frappe.db.sql("""select distinct BSL.name AS slot, BSN.email_id, BSU.subscription
			from `tabBooking Slot` BSL
			inner join `tabBooking Subscriber` BSU on BSL.name = BSU.parent
			inner join `tabBooking Subscription` BSN on BSU.subscription = BSN.name
			where BSL.time_slot > NOW() and IFNULL(BSL.streaming_link, "") != "" 
			and BSU.cancellation_date is null and BSU.notification_date is null""", as_dict=True)

	if notifications:
		streaming_link_notification = frappe.db.get_single_value('Booking Settings', 'streaming_link_notification')

		if streaming_link_notification:
			email_template = frappe.get_doc("Email Template", streaming_link_notification)

			for notification in notifications:

				args = frappe.get_doc('Booking Slot', notification.slot).as_dict()
				message = frappe.render_template(email_template.response, args)
				subject = frappe.render_template(email_template.subject, args)

				try:
					frappe.sendmail(
						recipients=notification.email_id,
						message=message,
						subject=subject)
				except Exception as e:
					frappe.log_error(frappe.get_traceback(), 'streaming link notification email failed')

				frappe.db.sql("""
					update `tabBooking Subscriber` set notification_date = NOW() 
					where parent = %(parent)s and subscription = %(subscription)s and notification_date is null """,
					{"parent": notification.slot,"subscription":notification.subscription})