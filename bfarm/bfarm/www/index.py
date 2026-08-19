import frappe

def get_context(context):
	# Tự động chuyển hướng từ trang gốc / sang trang Desk /app/bfarm-agriculture
	frappe.local.flags.redirect_to = "/app/bfarm-agriculture"
	raise frappe.Redirect

