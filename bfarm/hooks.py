from . import __version__ as app_version

app_name = "bfarm"
app_title = "Bfarm"
app_publisher = "Beeyond"
app_description = "Bfarm Agriculture Customization"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "contact@beeyond.com"
app_license = "MIT"
app_logo_url = "/assets/bfarm/images/logo.png"
favicon = "/assets/bfarm/images/logo.png"
app_home = "/desk/bfarm-agriculture"

# Khai báo bfarm trên apps screen để Frappe Server định tuyến đăng nhập thẳng về /desk/bfarm-agriculture
add_to_apps_screen = [
	{
		"name": "bfarm",
		"logo": "/assets/bfarm/images/logo.png",
		"title": "Bfarm",
		"route": "/desk/bfarm-agriculture",
		"sequence_id": 1,
	}
]

website_context = {
	"favicon": "/assets/bfarm/images/logo.png",
	"splash_image": "/assets/bfarm/images/logo.png",
	"logo": "/assets/bfarm/images/logo.png"
}

required_apps = ["erpnext", "agriculture"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/bfarm/css/bfarm.css"
app_include_js = "/assets/bfarm/js/bfarm.js"

# include js, css files in website & login page
web_include_css = "/assets/bfarm/css/bfarm.css"
web_include_js = "/assets/bfarm/js/bfarm.js"
update_website_context = "bfarm.bfarm.boot.update_website_context"

# Home Pages
# ----------

# application home page
home_page = "/desk/bfarm-agriculture"

# website user home page (by Role)
# => get_home_page() trả "desk/bfarm-agriculture" cho tất cả người dùng hệ thống,
# khiến sau đăng nhập (auth.py set_user_info -> login.js data.home_page) đi thẳng
# về workspace Bfarm Agriculture.
role_home_page = {
	"System Manager": "/desk/bfarm-agriculture",
	"Administrator": "/desk/bfarm-agriculture",
	"Agriculture User": "/desk/bfarm-agriculture",
	"All": "/desk/bfarm-agriculture"
}

# Session Boot Hook
boot_session = "bfarm.bfarm.boot.boot_session"

# Authentication - chạy SAU khi xác thực, TRƯỚC khi set_user_info
# => đặt flags.home_page tuyệt đối để post-login redirect ổn định + giảm lag (xem bfarm/auth.py)
on_login = [
	"bfarm.bfarm.auth.on_login"
]

# Session được tạo xong (make_session) - frappe.session.user đã set
# => warm boot cache ngay trong POST login để desk GET đầu tiên sau login không rebuild (xem bfarm/auth.py)
on_session_creation = [
	"bfarm.bfarm.auth.on_session_creation"
]

# Installation
# ------------
after_migrate = "bfarm.bfarm.setup.sync_workspaces"

# Domains
# -------
domains = {
	"Agriculture": "agriculture",
}
