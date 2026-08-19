import frappe

def get_context(context):
	# Tự động chuyển hướng từ trang gốc / sang trang Desk /desk/bfarm-agriculture
	frappe.local.flags.redirect_to = "/desk/bfarm-agriculture"
	raise frappe.Redirect
