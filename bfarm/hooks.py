from . import __version__ as app_version

app_name = "bfarm"
app_title = "Bfarm"
app_publisher = "Beeyond"
app_description = "Bfarm Agriculture Customization"
app_icon = "octicon octicon-file-directory"
app_color = "green"
app_email = "contact@beeyond.com"
app_license = "MIT"

required_apps = ["erpnext", "agriculture"]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/bfarm/css/bfarm.css"
app_include_js = "/assets/bfarm/js/bfarm.js"

# Home Pages
# ----------

# application home page
home_page = "app/bfarm-agriculture"

# website user home page (by Role)
role_home_page = {
	"System Manager": "app/bfarm-agriculture",
	"Administrator": "app/bfarm-agriculture",
	"Agriculture User": "app/bfarm-agriculture",
	"All": "app/bfarm-agriculture"
}

# Domains
# -------
domains = {
	"Agriculture": "agriculture",
}
