import frappe

def get_context(context):
	# Tự động chuyển hướng từ trang gốc / sang trang Desk /desk/home
	frappe.local.flags.redirect_to = "/desk/home"
	raise frappe.Redirect
