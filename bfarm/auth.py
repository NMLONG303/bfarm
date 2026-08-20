import frappe


def on_login(login_manager):
	"""Ép mọi đăng nhập đưa user thẳng về workspace Bfarm Agriculture (/desk/bfarm-agriculture)."""
	if not login_manager or login_manager.user == "Guest":
		return

	frappe.local.flags.home_page = "/desk/bfarm-agriculture"


def on_session_creation(login_manager=None):
	"""Hook chạy khi session được khởi tạo trong POST login."""
	if frappe.session.user and frappe.session.user != "Guest":
		frappe.local.flags.home_page = "/desk/bfarm-agriculture"
