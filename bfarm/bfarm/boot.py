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
		
		# Ghi đè logo ứng dụng hệ thống sang logo Bfarm
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"
		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			for app in bootinfo.app_data:
				app["app_logo_url"] = "/assets/bfarm/images/logo.png"
				if "logo" in app:
					app["logo"] = "/assets/bfarm/images/logo.png"

