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

    // Chuyển hướng sau login nếu người dùng ở trang /app mà chưa vào bfarm-agriculture
    if (frappe.session.user && frappe.session.user !== "Guest") {
        let current_route = frappe.get_route_str();
        if (current_route === "" || current_route === "workspace/home" || current_route === "home" || current_route === "desk") {
            // Chuyển hướng tới workspace bfarm-agriculture
            setTimeout(function() {
                frappe.set_route("bfarm-agriculture");
            }, 100);
        }
    }
});
