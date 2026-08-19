import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	Ép route mặc định của Desk về "bfarm-agriculture".
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		if hasattr(bootinfo, "user") and bootinfo.user:
			bootinfo.user.default_route = "bfarm-agriculture"
		bootinfo.default_route = "bfarm-agriculture"
