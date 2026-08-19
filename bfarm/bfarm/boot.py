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
		
		# Ghi đè logo và tên ứng dụng hệ thống sang Bfarm
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"
		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			for app in bootinfo.app_data:
				app["app_logo_url"] = "/assets/bfarm/images/logo.png"
				if app.get("app_name") in ["erpnext", "frappe", "bfarm"]:
					app["app_title"] = "Bfarm"
				if "logo" in app:
					app["logo"] = "/assets/bfarm/images/logo.png"

def update_website_context(context):
	"""
	Hook chạy cho ngữ cảnh website (bao gồm trang /login).
	Ép logo, favicon và tên ứng dụng về Bfarm.
	"""
	logo_path = "/assets/bfarm/images/logo.png"
	context["logo"] = logo_path
	context["app_logo"] = logo_path
	context["favicon"] = logo_path
	context["splash_image"] = logo_path
	context["app_name"] = "Bfarm"


