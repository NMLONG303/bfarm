import frappe


def on_login(login_manager):
	"""Ép mọi đăng nhập đưa user thẳng về workspace Bfarm Agriculture (/desk/bfarm-agriculture).

	Set frappe.local.flags.home_page bằng đường dẫn TUYỆT ĐỐI khiến:
	- auth.py::set_user_info trả home_page = "/desk/bfarm-agriculture"
	  -> login.js handler 200 navigate tới URL tuyệt đối /desk/bfarm-agriculture.
	- get_home_page() trả ngay flags, BỎ QUA toàn bộ truy vấn DB của _get_home_page()
	  trong chính request đăng nhập => giúp đăng nhập mượt mà không bị treo.
	"""
	if not login_manager or login_manager.user == "Guest":
		return

	frappe.local.flags.home_page = "/desk/bfarm-agriculture"


def on_session_creation(login_manager=None):
	"""Hook chạy khi session được khởi tạo trong POST login."""
	if frappe.session.user and frappe.session.user != "Guest":
		frappe.local.flags.home_page = "/desk/bfarm-agriculture"