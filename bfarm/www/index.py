import frappe


def get_context(context):
	"""Xử lý route gốc (/):
	- Nếu đã đăng nhập → redirect đến /desk/bfarm-agriculture
	- Nếu chưa đăng nhập (Guest) → redirect đến /login
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = "/desk/bfarm-agriculture"
	else:
		frappe.local.flags.redirect_location = "/login"
	raise frappe.Redirect
