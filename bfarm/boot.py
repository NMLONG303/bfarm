import frappe

def boot_session(bootinfo):
	"""
	Hook chạy mỗi khi khởi tạo phiên làm việc (session boot).
	Ép home_page, app_logo và bảo đảm Workspace "Bfarm Agriculture" luôn có mặt trong bootinfo.workspaces.pages.
	"""
	if frappe.session.user and frappe.session.user != "Guest":
		bootinfo.home_page = "/desk/bfarm-agriculture"
		bootinfo.app_logo_url = "/assets/bfarm/images/logo.png"

		# Xóa cache rác để đảm bảo dữ liệu workspace luôn mới nhất
		try:
			frappe.cache.hdel("home_page", frappe.session.user)
		except Exception:
			pass

		# Đảm bảo Workspace "Bfarm Agriculture" luôn có mặt trong bootinfo.workspaces.pages của mọi user
		if not hasattr(bootinfo, "workspaces") or not bootinfo.workspaces:
			bootinfo.workspaces = frappe._dict(pages=[], has_access=True, has_create_access=True)

		pages = bootinfo.workspaces.get("pages")
		if pages is None:
			pages = []
			bootinfo.workspaces["pages"] = pages

		has_bfarm = False
		for p in pages:
			p_name = p.get("name") if isinstance(p, dict) else getattr(p, "name", None)
			if p_name in ("Bfarm Agriculture", "bfarm-agriculture"):
				has_bfarm = True
				break

		if not has_bfarm:
			if frappe.db.exists("Workspace", "Bfarm Agriculture"):
				try:
					doc = frappe.get_doc("Workspace", "Bfarm Agriculture")
					doc_dict = doc.as_dict()
					doc_dict["label"] = doc_dict.get("title") or doc_dict.get("name")
					pages.insert(0, doc_dict)
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
