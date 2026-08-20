import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	- Chỉ giữ lại 2 ứng dụng trên màn hình Desktop: Bfarm và Framework (ẩn ERPNext icon).
	- Đặt route cho icon Bfarm mở trực tiếp ERPNext Workspace (/desk/bfarm-agriculture).
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"

		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			# 1. Ẩn ứng dụng ERPNext khỏi màn hình Desktop (chỉ giữ Bfarm và Framework)
			bootinfo.app_data = [
				app for app in bootinfo.app_data if app.get("app_name") != "erpnext"
			]

			# 2. Đặt cấu hình icon Bfarm mở trực tiếp ERPNext Agriculture Workspace
			for app in bootinfo.app_data:
				if app.get("app_name") == "bfarm":
					app["app_title"] = "Bfarm"
					app["app_logo_url"] = "/assets/bfarm/images/logo.png"
					app["logo"] = "/assets/bfarm/images/logo.png"
					app["app_route"] = "/desk/bfarm-agriculture"

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
