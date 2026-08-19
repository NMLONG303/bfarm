# Quy tắc và Hướng dẫn Tùy biến Dự án Bfarm (rule.md)

Tài liệu này cung cấp phân tích chi tiết về cấu trúc hệ thống, các module, chức năng và đặt ra các quy tắc phát triển (customization rules) để phục vụ cho việc vận hành và nâng cấp dự án **Bfarm** sau này.

---

## 1. Tổng quan Kiến trúc Hệ thống

Hệ thống Bfarm bao gồm hai thành phần chính kết nối qua giao thức HTTPS:
1. **BfarmMobileApp (Frontend di động)**: Viết bằng Kotlin (Jetpack Compose), kết nối trực tiếp với backend qua REST API sử dụng Session Authentication (Cookie-based).
2. **BfarmWeb/Frappe (Backend & Quản trị)**: Chạy trên nền tảng **Frappe Framework** cùng **ERPNext** và các ứng dụng tùy biến. Đây là nơi quản lý dữ liệu, cung cấp REST API và giao diện quản trị (Desk).

---

## 2. Cấu trúc Dự án Web & Backend (`BfarmWeb/frappe/beeyond`)

Thư mục root của backend là một **Frappe Bench** (tên thư mục: `beeyond`). Cấu trúc thư mục chi tiết như sau:

```
beeyond/
├── apps/                               # Thư mục chứa mã nguồn các ứng dụng (git repos)
│   ├── frappe/                         # Core Framework (không được sửa đổi trực tiếp)
│   ├── erpnext/                        # Core ERP (Task, Project, Item... không sửa trực tiếp)
│   ├── agriculture/                    # App cung cấp các Doctype nông nghiệp cơ bản của Frappe
│   └── bfarm/                          # App tùy biến chính của dự án Bfarm (Nơi viết toàn bộ code custom)
├── sites/                              # Thư mục chứa dữ liệu cấu hình và tệp tải lên của các site
│   ├── common_site_config.json         # Cấu hình chung của Bench (ports, redis, gunicorn)
│   └── bfarm/                          # Thư mục site chính: cấu hình riêng, cơ sở dữ liệu và file uploads
├── env/                                # Môi trường ảo Python (Virtualenv) chứa các thư viện phụ thuộc
└── logs/                               # Log hoạt động của các tiến trình (worker, web, schedule)
```

---

## 3. Các Ứng dụng Tùy biến và Chức năng Chính

### 3.1. Ứng dụng `agriculture` (Nghiệp vụ Nông nghiệp)
App này đóng vai trò cung cấp các kiểu dữ liệu (DocTypes) chuyên ngành nông nghiệp:
*   **Các Doctype cốt lõi**: `Crop`, `Crop Cycle`, `Fertilizer`, `Disease`, `Weather`, `Soil Texture`.
*   **Phân tích & Chỉ số**: `Soil Analysis`, `Water Analysis`, `Plant Analysis`, `Agriculture Analysis Criteria` (chứa hơn 90 chỉ số đo lường đất/nước/khí hậu mặc định).
*   **Cơ chế xác thực (`agriculture/agriculture/auth.py`)**: Gắn vào hook `on_login` để kiểm tra vai trò của người dùng. Chỉ cho phép các tài khoản có vai trò `Agriculture User` hoặc `Agriculture Manager` (ngoại trừ `Administrator` và `System Manager`) được đăng nhập vào hệ thống nhằm bảo mật API.
*   **Cấp quyền tự động (`setup.py`)**: Tự động thêm quyền truy cập `Location` cho các vai trò nông nghiệp sau khi cài đặt.

### 3.2. Ứng dụng `bfarm` (Tùy biến Giao diện & Trải nghiệm Bfarm)
Đây là ứng dụng chứa các mã nguồn tùy chỉnh riêng của dự án Bfarm, đóng vai trò ghi đè (override) và mở rộng tính năng của hệ thống mà không can thiệp vào mã nguồn gốc:
*   **hooks.py**: Khai báo nạp các tệp CSS và JS tùy biến vào Desk:
    ```python
    app_include_css = "/assets/bfarm/css/bfarm.css"
    app_include_js = "/assets/bfarm/js/bfarm.js"
    ```
    Đồng thời đăng ký trang chủ mặc định qua `role_home_page` dẫn tới workspace `bfarm-agriculture`.
*   **bfarm.js (`bfarm/public/js/bfarm.js`)**: Thực hiện các logic ghi đè phía client:
    *   *Điều hướng*: Tự động chuyển hướng từ trang chủ Desk sang workspace `bfarm-agriculture` sau khi đăng nhập.
    *   *Navbar & Brand*: Đổi logo chữ và biểu tượng trên thanh điều hướng Desk thành "Bfarm Agriculture".
    *   *Custom Geolocation Map Zoom*: Ghi đè cấu hình bản đồ mặc định của Frappe:
        *   Tăng độ zoom mặc định ban đầu lên `18` (thay vì `13`) để bản đồ tự động bắt vị trí gần hơn.
        *   Thiết lập `maxZoom: 23` và `maxNativeZoom: 19` cho tất cả tile layers (OSM, Satellite, Terrain, Labels) giúp phóng to sâu mà không bị trắng màn hình.
        *   Ghi đè hàm `bind_leaflet_map` và `fit_and_recenter_map` của `ControlGeolocation` (trong Form View) để giới hạn zoom tự động khi fit bounds ở mức `18` (tránh zoom quá sát vỡ ảnh khi chỉ có 1 marker).
        *   Ghi đè hàm `setup_map` và `render_map_data` của `MapView` (trong List Map View) để mang lại trải nghiệm tương tự trên giao diện danh sách bản đồ.
*   **bfarm.css (`bfarm/public/css/bfarm.css`)**: Tùy biến giao diện Desk, thay đổi màu sắc Navbar, thêm hiệu ứng hover mượt mà cho các card và liên kết trong Workspace.
*   **Bản dịch (`bfarm/translations/vi.csv`)**: Định nghĩa toàn bộ từ điển dịch thuật tiếng Việt cho các thuật ngữ nông nghiệp (ví dụ: chuyển "Crop Cycle" thành "Vụ canh tác", "Task" thành "Công việc chăm sóc"...).

---

## 4. Quy tắc Phát triển và Tùy biến (Customization Rules)

Để đảm bảo dự án có khả năng bảo trì, nâng cấp phiên bản Frappe/ERPNext dễ dàng và không gây xung đột hệ thống, lập trình viên **bắt buộc** tuân thủ các quy tắc sau:

### Quy tắc 1: Không chỉnh sửa mã nguồn core
*   **TUYỆT ĐỐI KHÔNG** sửa đổi trực tiếp bất kỳ tệp tin nào nằm trong thư mục `apps/frappe` hoặc `apps/erpnext`.
*   Hạn chế sửa trực tiếp app `agriculture` vì đây là app nghiệp vụ nền. Mọi mở rộng phải được định cấu hình từ app `bfarm`.

### Quy tắc 2: Thực hiện mọi tùy biến trong app `bfarm`
Mọi thay đổi về hành vi, giao diện, API, logic nghiệp vụ phải được đặt trong ứng dụng tùy biến `bfarm`:
*   *Nếu cần tùy biến CSS/JS*: Thêm code vào `bfarm.css` hoặc `bfarm.js`.
*   *Nếu cần tùy biến Backend*:
    *   Tạo các hàm Python whitelisted (`@frappe.whitelist()`) bên trong `apps/bfarm/bfarm` để làm custom API cho mobile.
    *   Sử dụng cơ chế **Doc Events** hoặc **Override class** trong `hooks.py` của `bfarm` để can thiệp vào vòng đời tài liệu của ERPNext/Frappe.
*   *Nếu cần tạo Doctype mới*: Đăng ký chúng thuộc module `Bfarm`.

### Quy tắc 3: Quy trình áp dụng thay đổi UI bắt buộc
Mỗi khi có sự thay đổi về CSS, JS hoặc cấu hình Workspace trong app `bfarm`, lập trình viên phải chạy các lệnh sau trong thư mục Bench:
1.  **Biên dịch lại Assets**:
    ```bash
    bench build --app bfarm
    ```
    *(Hoặc chạy `bench watch` trong suốt quá trình phát triển để tự động biên dịch)*
2.  **Dọn dẹp Cache hệ thống**:
    ```bash
    bench clear-cache
    ```
3.  **Xóa Cache Trình duyệt**:
    Phía client cần nhấn tổ hợp phím **`Ctrl + F5`** (Windows) hoặc **`Cmd + Shift + R`** (macOS) để cập nhật giao diện tùy biến mới nhất.

### Quy tắc 4: Quản lý bản dịch qua File dịch thuật
*   Không hardcode tiếng Việt vào các tệp JS, HTML hay Python.
*   Luôn bọc chuỗi ký tự bằng hàm dịch thuật: `__("Chuỗi tiếng Anh")` trong JS hoặc `_("Chuỗi tiếng Anh")` trong Python.
*   Khai báo bản dịch tương ứng trong tệp dịch thuật tập trung: [vi.csv](file:///d:/Beeyond/Bfarm/BfarmWeb/frappe/beeyond/apps/bfarm/bfarm/translations/vi.csv).
