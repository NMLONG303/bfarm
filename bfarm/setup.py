import frappe
import os
import json

def sync_workspaces():
	workspace_path = frappe.get_app_path("bfarm", "workspace", "bfarm_agriculture", "bfarm_agriculture.json")
	if os.path.exists(workspace_path):
		with open(workspace_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		
		name = data.get("name") or "Bfarm Agriculture"
		
		# Tạo Number Card "Completed Tasks" nếu chưa có
		if not frappe.db.exists("Number Card", "Completed Tasks"):
			card_path = frappe.get_app_path("bfarm", "number_card", "completed_tasks", "completed_tasks.json")
			if os.path.exists(card_path):
				with open(card_path, "r", encoding="utf-8") as f:
					card_data = json.load(f)
				frappe.get_doc(card_data).insert(ignore_permissions=True)
				frappe.db.commit()

		# Ghi đè trực tiếp logo.png lên các tệp logo gốc của ERPNext và Frappe
		try:
			import shutil
			src_logo = frappe.get_app_path("bfarm", "assets", "logo.png")
			if os.path.exists(src_logo):
				erpnext_img_dir = frappe.get_app_path("erpnext", "public", "images")
				if os.path.exists(erpnext_img_dir):
					shutil.copyfile(src_logo, os.path.join(erpnext_img_dir, "erpnext-logo.png"))
					shutil.copyfile(src_logo, os.path.join(erpnext_img_dir, "erpnext-logo-blue.png"))
					shutil.copyfile(src_logo, os.path.join(erpnext_img_dir, "erpnext-logo.svg"))
				frappe_img_dir = frappe.get_app_path("frappe", "public", "images")
				if os.path.exists(frappe_img_dir):
					shutil.copyfile(src_logo, os.path.join(frappe_img_dir, "frappe-framework-logo.svg"))
					shutil.copyfile(src_logo, os.path.join(frappe_img_dir, "frappe-framework-logo.png"))
					shutil.copyfile(src_logo, os.path.join(frappe_img_dir, "frappe-logo.png"))
			
			# Ghi đè trực tiếp template login.html tiếng Việt
			src_login = frappe.get_app_path("bfarm", "www", "login.html")
			dest_login = frappe.get_app_path("frappe", "www", "login.html")
			if os.path.exists(src_login) and os.path.exists(os.path.dirname(dest_login)):
				shutil.copyfile(src_login, dest_login)
		except Exception:
			pass

		# Đổi thương hiệu ứng dụng hệ thống sang Bfarm và dùng logo mới
		try:
			frappe.db.set_single_value("Website Settings", "app_name", "Bfarm")
			frappe.db.set_single_value("Website Settings", "app_logo", "/assets/bfarm/images/logo.png")
			frappe.db.set_single_value("Website Settings", "favicon", "/assets/bfarm/images/logo.png")
			frappe.db.set_single_value("Website Settings", "splash_image", "/assets/bfarm/images/logo.png")
			frappe.db.set_single_value("Website Settings", "banner_html", '<img src="/assets/bfarm/images/logo.png" style="height: 28px;"> Bfarm')
			frappe.db.set_single_value("Website Settings", "language", "vi")
			frappe.db.set_single_value("System Settings", "app_name", "Bfarm")
			frappe.db.set_single_value("System Settings", "language", "vi")
			frappe.db.set_single_value("Navbar Settings", "app_logo", "/assets/bfarm/images/logo.png")
			frappe.db.commit()
		except Exception:
			pass

		# Xóa các bản copy cá nhân tùy chỉnh (User Workspace) nếu người dùng từng Edit khiến Workspace bị khóa/cũ
		try:
			frappe.db.sql("""DELETE FROM `tabWorkspace` WHERE (title = %s OR label = %s OR name LIKE %s) AND (public = 0 OR (for_user IS NOT NULL AND for_user != ''))""", ("Bfarm Agriculture", "Bfarm Agriculture", "%Bfarm Agriculture%"))
			frappe.db.sql("""DELETE FROM `tabUser Settings` WHERE `data` LIKE %s""", ("%Bfarm Agriculture%",))
			frappe.db.commit()
		except Exception:
			pass

		# Kiểm tra xem Workspace đã tồn tại chưa
		if not frappe.db.exists("Workspace", name):
			doc = frappe.get_doc(data)
			doc.app = data.get("app") or "erpnext"
			doc.public = 1
			doc.for_user = ""
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
		else:
			doc = frappe.get_doc("Workspace", name)
			doc.app = data.get("app") or "erpnext"
			doc.public = 1
			doc.for_user = ""
			doc.is_hidden = 0
			doc.content = data.get("content")
			doc.charts = []
			for chart in data.get("charts", []):
				doc.append("charts", chart)
			doc.number_cards = []
			for card in data.get("number_cards", []):
				doc.append("number_cards", card)
			doc.links = []
			for link in data.get("links", []):
				doc.append("links", link)
			doc.sequence_id = data.get("sequence_id", -100.0)
			doc.icon = data.get("icon", "agriculture")
			doc.title = data.get("title")
			doc.restrict_to_domain = data.get("restrict_to_domain")
			doc.sidebar_items = []
			for sb in data.get("sidebar_items", []):
				doc.append("sidebar_items", sb)
			doc.save(ignore_permissions=True)
			frappe.db.commit()

		# Ẩn Workspace Home mặc định của ERPNext để Bfarm Agriculture ghi đè thay thế làm Home chính
		if frappe.db.exists("Workspace", "Home"):
			frappe.db.set_value("Workspace", "Home", "is_hidden", 1)
			frappe.db.commit()

		# Xóa cache server để áp dụng ngay
		frappe.clear_cache()

