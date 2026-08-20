import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	Ép home_page, app_logo và đảm bảo Workspace "Bfarm Agriculture" luôn có trong bootinfo.workspaces.pages.
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		bootinfo.home_page = "/desk/bfarm-agriculture"
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"

		# Đảm bảo Workspace "Bfarm Agriculture" luôn có mặt trong bootinfo.workspaces.pages của mọi user
		if hasattr(bootinfo, "workspaces") and isinstance(bootinfo.workspaces, dict) and "pages" in bootinfo.workspaces:
			pages = bootinfo.workspaces.get("pages") or []
			has_bfarm = any(
				page.get("name") == "Bfarm Agriculture" or page.get("title") == "Bfarm Agriculture"
				for page in pages
			)
			if not has_bfarm and frappe.db.exists("Workspace", "Bfarm Agriculture"):
				try:
					ws_doc = frappe.get_doc("Workspace", "Bfarm Agriculture").as_dict()
					ws_doc["label"] = ws_doc.get("title") or ws_doc.get("name")
					bootinfo.workspaces["pages"].insert(0, ws_doc)
				except Exception:
					pass

		if hasattr(bootinfo, "app_data") and bootinfo.app_data:
			for app in bootinfo.app_data:
				app["app_logo_url"] = "/assets/bfarm/images/logo.png"
				if app.get("app_name") == "bfarm":
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
