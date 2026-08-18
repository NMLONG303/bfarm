frappe.ready(function() {
    // Customization for Desk Navbar
    let customize_navbar = function() {
        let brand = $(".navbar-brand");
        if (brand.length) {
            // Đổi logo text trên thanh điều hướng Desk
            brand.html('<span class="bfarm-logo-text" style="font-weight: 700; color: #2e7d32; font-size: 16px; letter-spacing: 0.5px; display: flex; align-items: center; gap: 8px;"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" style="width: 20px; height: 20px;"><path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 14c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg> Bfarm Agriculture</span>');
        }
    };

    $(document).on("toolbar_setup", function() {
        customize_navbar();
    });

    // Đảm bảo navbar được chỉnh sửa ngay khi load trang
    setTimeout(customize_navbar, 300);
    setTimeout(customize_navbar, 1000);

    // Chuyển hướng sau login nếu người dùng ở trang chủ mặc định của Desk
    if (frappe.session.user && frappe.session.user !== "Guest") {
        let current_route = frappe.get_route_str();
        console.log("[Bfarm Debug] Current route: ", current_route);
        
        let should_redirect = !current_route || 
            current_route.toLowerCase() === "workspaces/home" || 
            current_route.toLowerCase() === "home" || 
            current_route.toLowerCase() === "desk" ||
            current_route.toLowerCase() === "workspaces";
            
        if (should_redirect) {
            console.log("[Bfarm Debug] Redirecting to bfarm-agriculture...");
            setTimeout(function() {
                frappe.set_route("bfarm-agriculture");
            }, 200);
        }
    }

    // ==========================================
    // Custom Geolocation Map Zoom (Override)
    // ==========================================
    let override_geolocation_map = function() {
        // Ghi đè cấu hình map mặc định của Frappe
        if (frappe.utils && frappe.utils.map_defaults) {
            let tiles = frappe.utils.map_defaults.tiles;
            if (tiles.default_tile && tiles.default_tile.options) {
                tiles.default_tile.options.maxZoom = 23;
                tiles.default_tile.options.maxNativeZoom = 19;
            }
            if (tiles.satellite_tile && tiles.satellite_tile.options) {
                tiles.satellite_tile.options.maxZoom = 23;
                tiles.satellite_tile.options.maxNativeZoom = 19;
            }
            if (tiles.labels_tail && tiles.labels_tail.options) {
                tiles.labels_tail.options.maxZoom = 23;
                tiles.labels_tail.options.maxNativeZoom = 19;
            }
            if (tiles.terrain_lines_tail && tiles.terrain_lines_tail.options) {
                tiles.terrain_lines_tail.options.maxZoom = 23;
                tiles.terrain_lines_tail.options.maxNativeZoom = 19;
            }
        }

        // Ghi đè class ControlGeolocation
        if (frappe.ui.form.ControlGeolocation && !frappe.ui.form.ControlGeolocation.prototype._bfarm_overridden) {
            frappe.ui.form.ControlGeolocation.prototype._bfarm_overridden = true;
            
            // Ghi đè hàm bind_leaflet_map
            frappe.ui.form.ControlGeolocation.prototype.bind_leaflet_map = function() {
                // Khởi tạo map với maxZoom là 23
                this.map = L.map(this.map_id, {
                    maxZoom: 23
                });
                
                this.map.setView(frappe.utils.map_defaults.center, frappe.utils.map_defaults.zoom);

                this.streetLayer = L.tileLayer(
                    frappe.utils.map_defaults.tiles.default_tile.url,
                    frappe.utils.map_defaults.tiles.default_tile.options
                );
                this.satelliteLayer = L.tileLayer(
                    frappe.utils.map_defaults.tiles.satellite_tile.url,
                    frappe.utils.map_defaults.tiles.satellite_tile.options
                );
                this.labelsLayer = L.tileLayer(
                    frappe.utils.map_defaults.tiles.labels_tail.url,
                    frappe.utils.map_defaults.tiles.labels_tail.options
                );
                this.terrainLayer = L.tileLayer(
                    frappe.utils.map_defaults.tiles.terrain_lines_tail.url,
                    frappe.utils.map_defaults.tiles.terrain_lines_tail.options
                );

                this.streetLayer.addTo(this.map);

                this.editableLayers = new L.FeatureGroup();
                console.log("[Bfarm Geolocation Override] Leaflet map initialized with maxZoom: 23, maxNativeZoom: 19");
            };
        }
    };

    // Theo dõi sự kiện thay đổi trang để áp dụng override
    $(document).on("page-change", function() {
        override_geolocation_map();
    });
    
    // Áp dụng ngay khi ready
    override_geolocation_map();
});
