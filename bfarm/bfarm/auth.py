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


def on_session_creation(login_manager=None):
	"""Warm boot cache ngay trong request đăng nhập để chặn "loading lâu" ở lần vào đầu.

	Vấn đề: frappe/auth.py dòng 155 gọi `frappe.clear_cache(user=usr)` mỗi lần login
	-> xóa toàn bộ user cache (kể cả `bootinfo:{user}`, xem clear_user_cache trong
	frappe/cache_manager.py). Nên request desk GET `/desk/bfarm-agriculture` đầu tiên
	sau login phải REBUILD toàn bộ boot (thường 1-6s với site 4 app, có trình duyệt
	thấy "Loading" mãi vì vượt timeout).

	Hook on_session_creation chạy bên trong make_session (auth.py:250) — tại đây
	frappe.session.user ĐÃ là user mới (Session.start đã set), và TRƯỚC set_user_info.
	Gọi frappe.sessions.get() để build + hset("bootinfo", user) => desk GET kế tiếp
	được phục vụ từ Redis (frappe/sessions.py:139) => splash hiện gần như tức thì.
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		frappe.local.flags.home_page = "/desk/bfarm-agriculture"

		# Cho phép tắt warm nếu site config có bfarm_warm_boot_on_login = 0
		if not frappe.conf.get("bfarm_warm_boot_on_login", True):
			return

		try:
			import frappe.sessions

			# nếu cache vẫn còn (login lại trong thời gian ngắn) thì hàm này chỉ đọc cache
			frappe.sessions.get()
		except Exception:
			# Warm thất bại KHÔNG được làm hỏng login - lần desk GET sau sẽ tự rebuild
			frappe.log_error(title="Bfarm: Boot warm failed (on login)", message=frappe.get_traceback())