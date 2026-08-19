import frappe
import os
import json

def sync_workspaces():
	workspace_path = frappe.get_app_path("bfarm", "workspace", "bfarm_agriculture", "bfarm_agriculture.json")
	if os.path.exists(workspace_path):
		with open(workspace_path, "r", encoding="utf-8") as f:
			data = json.load(f)
		
		name = data.get("name") or "Bfarm Agriculture"
		
		# Kiểm tra và tạo Module Def nếu chưa tồn tại
		if not frappe.db.exists("Module Def", "Bfarm"):
			frappe.get_doc({
				"doctype": "Module Def",
				"module_name": "Bfarm",
				"app_name": "bfarm",
				"package": "Bfarm"
			}).insert(ignore_permissions=True)
			frappe.db.commit()

		# Kiểm tra xem Workspace đã tồn tại chưa
		if not frappe.db.exists("Workspace", name):
			doc = frappe.get_doc(data)
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
		else:
			doc = frappe.get_doc("Workspace", name)
			# Cập nhật nội dung JSON
			doc.app = data.get("app") or "bfarm"
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
