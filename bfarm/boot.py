import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	- ERPNext giữ nguyên là ứng dụng chính cùng toàn bộ các Workspaces gốc (Kế toán, Kho, Mua/Bán, HR, Dự án, Bfarm Agriculture...).
	- Ẩn ứng dụng bfarm phụ khỏi màn hình Desktop.
	- Đổi tên ứng dụng ERPNext trên Desktop thành "Bfarm" và đổi biểu tượng logo thành logo Bfarm.
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"

		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			# 1. Ẩn app 'bfarm' phụ khỏi màn hình Desktop (chỉ giữ lại ERPNext và Framework)
			bootinfo.app_data = [
				app for app in bootinfo.app_data if app.get("app_name") != "bfarm"
			]

			# 2. Đổi tên ứng dụng chính ERPNext thành "Bfarm" và cập nhật logo Bfarm (giữ nguyên 100% Workspaces gốc của ERPNext)
			for app in bootinfo.app_data:
				if app.get("app_name") == "erpnext":
					app["app_title"] = "Bfarm"
					app["app_logo_url"] = "/assets/bfarm/images/logo.png"
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
