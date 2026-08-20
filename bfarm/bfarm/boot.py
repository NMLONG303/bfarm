import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	- Hợp nhất toàn bộ Workspaces và Modules của ERPNext vào ứng dụng Bfarm,
	  để thanh điều hướng bên trái (sidebar/rail) hiển thị đầy đủ tất cả các tính năng
	  Nông nghiệp + ERPNext (Kế toán, Kho bãi, Mua hàng, Bán hàng, Nhân sự, Dự án...).
	- Ẩn icon ERPNext riêng biệt khỏi màn hình Desktop (chỉ giữ lại 2 icon: Bfarm và Framework).
	- Đặt route cho icon Bfarm mở trực tiếp /desk/bfarm-agriculture.
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"

		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			# Tìm thông tin app erpnext và bfarm trong bootinfo.app_data
			erpnext_app = next((a for a in bootinfo.app_data if a.get("app_name") == "erpnext"), None)

			erpnext_workspaces = []
			erpnext_modules = []
			if erpnext_app:
				erpnext_workspaces = erpnext_app.get("workspaces") or []
				erpnext_modules = erpnext_app.get("modules") or []

			# 1. Ẩn icon ERPNext riêng biệt khỏi màn hình Desktop (chỉ hiển thị 2 icon: Bfarm và Framework)
			bootinfo.app_data = [
				app for app in bootinfo.app_data if app.get("app_name") != "erpnext"
			]

			# 2. Cấu hình ứng dụng Bfarm: Hợp nhất workspaces của ERPNext vào Bfarm
			for app in bootinfo.app_data:
				if app.get("app_name") == "bfarm":
					app["app_title"] = "Bfarm"
					app["app_logo_url"] = "/assets/bfarm/images/logo.png"
					app["logo"] = "/assets/bfarm/images/logo.png"
					app["app_route"] = "/desk/bfarm-agriculture"

					# Hợp nhất workspaces của ERPNext vào Bfarm (đặt Bfarm Agriculture lên đầu)
					existing_ws = app.get("workspaces") or []
					combined_ws = ["Bfarm Agriculture"]
					for ws in list(existing_ws) + list(erpnext_workspaces):
						if ws and ws not in combined_ws:
							combined_ws.append(ws)
					app["workspaces"] = combined_ws

					# Hợp nhất modules của ERPNext vào Bfarm
					existing_mod = app.get("modules") or []
					combined_mod = list(existing_mod)
					for mod in erpnext_modules:
						if mod and mod not in combined_mod:
							combined_mod.append(mod)
					app["modules"] = combined_mod

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
