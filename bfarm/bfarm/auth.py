import frappe


def on_login(login_manager):
	"""Ép mọi đăng nhập đưa user thẳng về workspace Bfarm Agriculture.

	Set frappe.local.flags.home_page bằng đường dẫn TUYỆT ĐỐI khiến:
	- auth.py::set_user_info (dòng 211) trả home_page = "/desk/bfarm-agriculture"
	  -> login.js handler 200 (dòng 325) navigate tới URL tuyệt đối, không phụ thuộc
	  vào resolution của URL tương đối ("desk/bfarm-agriculture") nên ổn định trên
	  mọi trình duyệt (sửa tình trạng "đăng nhập OK nhưng không vào được trang").
	- get_home_page() (frappe/website/utils.py:99-100) trả ngay flags,
	  BỎ QUA toàn bộ truy vấn DB của _get_home_page() (duyệt role, portal settings,
	  hooks, load_user default_workspace) trong chính request đăng nhập => giảm lag khi login.
	"""
	if not login_manager or login_manager.user == "Guest":
		return

	frappe.local.flags.home_page = "/desk/bfarm-agriculture"