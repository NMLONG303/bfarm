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
			doc.content = data.get("content")
			doc.links = []
			for link in data.get("links", []):
				doc.append("links", link)
			doc.sequence_id = data.get("sequence_id", 0)
			doc.icon = data.get("icon", "agriculture")
			doc.title = data.get("title")
			doc.restrict_to_domain = data.get("restrict_to_domain")
			doc.save(ignore_permissions=True)
			frappe.db.commit()
