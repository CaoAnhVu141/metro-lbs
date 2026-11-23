# dev-v1: Phần nền dữ liệu và mô hình hoá (Khối 1–3)

Notebook `notebooks/dev-v1.ipynb` là phần nền của đề tài *Ứng dụng Local Beam Search trong thiết kế tối ưu mạng lưới trạm Metro TP.HCM giai đoạn mở rộng*. Notebook này đọc và làm sạch dữ liệu, sinh tập vị trí ứng viên, tính trước ma trận khoảng cách và định nghĩa toàn bộ hàm mô hình (trạng thái, hàm mục tiêu, ràng buộc, hàng xóm). Notebook `notebooks/metro_lbs.ipynb` (Khối 4, thuật toán) nạp lại các hàm này bằng `%run ./dev-v1.ipynb`.

## 1. Cấu trúc thư mục

```text
metro-lbs/
├── data/
│   ├── wards.csv          # 168 phường/xã/đặc khu: tên, dân số 2025, toạ độ
│   └── stations.csv       # 148 dòng trạm metro: tên, tuyến, trạng thái, toạ độ
├── docs/
│   ├── links.txt          # link nguồn dữ liệu và danh sách tuyến metro
│   └── NIEN GIAM TP 2025_...pdf   # Niên giám Thống kê TP.HCM 2025
├── figures/
│   ├── hien_trang.png     # bản đồ hiện trạng dân số và trạm metro
│   └── ung_vien.png       # tập ứng viên giữ lại / bị loại
├── notebooks/
│   ├── dev-v1.ipynb       # Khối 1–3 (tài liệu này)
│   └── metro_lbs.ipynb    # Khối 4: Local Beam Search, Stochastic LBS
├── report/                # báo cáo
├── results/               # CSV kết quả thực nghiệm
├── tools/
│   ├── auto_get_coordinates_stations.py   # geocode toạ độ trạm
│   └── auto_get_coordinates_wards.py      # geocode toạ độ phường/xã
├── README.md
└── requirements.txt
```

## 2. Cài đặt và chạy

```bash
pip install -r requirements.txt     # pandas, numpy, matplotlib, jupyter, geopy
cd notebooks
jupyter notebook dev-v1.ipynb       # chạy Kernel > Restart & Run All
```

Notebook dùng đường dẫn tương đối (`../data`, `../figures`, `../results`), nên **phải mở từ thư mục `notebooks/`**. Chạy hết mất khoảng 10–30 giây và sinh lại `figures/hien_trang.png`, `figures/ung_vien.png`.

## 3. Nguồn dữ liệu

### 3.1. Dân số phường/xã (`data/wards.csv`)

| Mục | Nội dung |
|---|---|
| Nguồn | **Niên giám Thống kê Thành phố Hồ Chí Minh 2025**, Thống kê TP. Hồ Chí Minh, NXB Tổng hợp TP.HCM (bản lưu: `docs/NIEN GIAM TP 2025_...pdf`) |
| Link gốc | https://thongkehochiminh.nso.gov.vn/uploads/NIEN%20GIAM%20TP%202025_20261016104855_16a485877d7a4c18b4c8d457120e6e12.pdf |
| Biểu sử dụng | Chương Dân số và Lao động, **Biểu 9: "Dân số trung bình năm 2025 phân theo đơn vị hành chính cấp xã"** (Average population in 2025 by commune), **trang 81–87** |
| Chỉ tiêu | Dân số trung bình năm 2025, số liệu **sơ bộ**, đơn vị: người |
| Mốc hành chính | Địa giới mới sau sáp nhập TP.HCM, Bình Dương và Bà Rịa – Vũng Tàu (từ 01/07/2025): **168 đơn vị cấp xã** (113 phường, 54 xã, 1 đặc khu). Không còn cấp quận nên cột `quan` để trống |
| Tổng dân số | 13.803.797 người (khớp dòng "TỔNG SỐ" của Biểu 9) |
| Toạ độ | Không có trong niên giám. Lấy tự động bằng `tools/auto_get_coordinates_wards.py` (geopy + Nominatim/OpenStreetMap), là điểm đại diện của phường/xã chứ không phải tâm hình học |

Đã đối chiếu: cột `dan_so` của cả 168 dòng trong `wards.csv` khớp từng số với Biểu 9.

### 3.2. Danh sách trạm metro (`data/stations.csv`)

| Mục | Nội dung |
|---|---|
| Nguồn | Trang thông tin Metro TP.HCM: https://mrt.com.vn/tphcm/ |
| Danh sách tuyến | `docs/links.txt` |
| Toạ độ | Lấy tự động bằng `tools/auto_get_coordinates_stations.py` (geopy + Nominatim/OpenStreetMap) theo tên ga |
| Trạng thái | `dang_hoat_dong`, `dang_xay`, `quy_hoach`. Mô hình coi `dang_hoat_dong` và `dang_xay` là **trạm đã có**; `quy_hoach` để riêng, dùng khi so sánh với quy hoạch thực |

Các tuyến và cách mã hoá trong cột `tuyen`:

| # | Tuyến (theo `docs/links.txt`) | `tuyen` | `trang_thai` | Số trạm |
|---|---|---|---|---|
| 1 | Tuyến số 1: Bến Thành – Suối Tiên | `1` | `dang_hoat_dong` | 14 |
| 2 | Tuyến số 2: Bến Thành – Tham Lương | `2` | `dang_xay` | 11 |
| 3 | Tuyến Bến Thành – Thủ Thiêm | `2` | `dang_xay` | 6 |
| 4 | Tuyến Bến Thành – Cần Giờ | `CG` | `dang_xay` | 8 |
| 5 | Tuyến Thủ Thiêm – Long Thành | `LT` | `quy_hoach` | 14 |
| 6 | Tuyến số 1 kéo dài: Suối Tiên – Thành phố mới Bình Dương | `1` | `quy_hoach` | 19 |
| 7 | Tuyến số 2 đoạn Thủ Dầu Một – TP.HCM: Thủ Dầu Một – Tao Đàn | `2` | `quy_hoach` | 24 |
| 8 | Tuyến số 6 (giai đoạn 1): Sân bay Tân Sơn Nhất – Phú Hữu | `6` | `quy_hoach` | 22 |
| 9 | Tuyến số 4: Đông Thạnh – Hiệp Phước | `4` | `quy_hoach` | 30 |
| | **Tổng** | | | **148** |

Tuyến Bến Thành – Thủ Thiêm (Hàm Nghi → Thủ Thiêm) đang được ghi chung mã `2` với tuyến số 2. Các ga trung chuyển (ví dụ Bến Thành, Tao Đàn, An Phú, Thủ Thiêm) xuất hiện ở nhiều tuyến.

## 4. Tiền xử lý dữ liệu (Khối 1)

**Phường/xã:** chuẩn hoá tên cột và chuẩn hoá Unicode NFC cho tên; chuyển `dan_so`, `lat`, `lon` sang số; kiểm tra thiếu, trùng `(ten, quan)` và toạ độ ngoài khung (vĩ độ 10,3–11,5; kinh độ 106,3–107,6, đã nới rộng để chứa Bình Dương và Vũng Tàu).

- Thiếu: 0. Trùng: 0.
- Loại 1 dòng ngoài khung: **Đặc khu Côn Đảo** (8,69; 106,61), vì nằm ngoài đất liền và không liên quan tới mạng metro.
- Còn **167** phường/xã, tổng dân số **13.793.648** người.

**Trạm:** chuẩn hoá tương tự; loại 2 dòng trùng `(ten, tuyen)` (An Phú tuyến 1 và Tao Đàn tuyến 2, giữ bản ghi đã có/đang xây). Còn **146** trạm: **39** trạm đã có (14 đang hoạt động, 25 đang xây) và **107** trạm quy hoạch.

**Hàm khoảng cách:** `haversine` (km, bán kính Trái Đất 6.371 km) và `distance_matrix` (vector hoá). Kiểm tra: Bến Thành – Suối Tiên ≈ 17,56 km theo đường chim bay.

## 5. Tập ứng viên (Khối 2)

- Nguồn ứng viên: tâm 167 phường/xã và lưới đều bước `GRID_STEP_KM` = 1 km phủ khung toạ độ (15.128 điểm), tổng 15.295.
- Lọc: bỏ ứng viên cách trạm đã có dưới `D_MIN_KM`, và bỏ ứng viên cách phường gần nhất quá `R_SERVICE_KM`. Còn **568** ứng viên (149 tâm phường, 419 điểm lưới). Cột `id` của ứng viên là phần tử của trạng thái.
- Ma trận tính trước: `D_CW` (ứng viên–phường, 568×167), `D_CC` (ứng viên–ứng viên, 568×568), `D_CS` (ứng viên–trạm đã có, 568×39), `D_SW` (trạm đã có–phường).
- Hiện trạng: trạm đã có phục vụ 18/167 phường, **1.241.783 người (9,00%)** dân số.

## 6. Mô hình hoá (Khối 3)

Bài toán: chọn tập trạm mới S ⊆ C, |S| ≤ K_max, để cực đại

```text
f(S) = w_pop · Pop(S)/Pop_tổng − w_cost · Cost(S)/BUDGET − w_pen · Penalty(S)
```

- **Trạng thái:** `tuple` các `id` ứng viên, sắp xếp tăng dần, ví dụ `(3, 17, 42)`.
- **Pop(S):** tổng dân số các phường có tâm nằm trong `R_SERVICE_KM` của ít nhất một trạm (mới hoặc đã có), mỗi phường tính một lần.
- **Cost(S):** `len(S) · COST_PER_STATION + L(S) · COST_PER_KM`, trong đó L(S) là chiều dài cây khung nhỏ nhất (Prim) nối các trạm mới cộng đoạn nối ngắn nhất về mạng hiện có.
- **Penalty(S):** hình phạt mềm, tăng theo mức vi phạm: khoảng cách giữa hai trạm mới < `D_MIN_KM`, trạm mới cách trạm đã có < `D_MIN_KM`, số trạm > `MAX_NEW_STATIONS`, chi phí > `BUDGET`.
- **Hàng xóm:** thay (swap) 1 trạm, thêm (add) 1 trạm, bớt (remove) 1 trạm.

### 6.1. Hằng số

| Hằng số | Giá trị | Ý nghĩa |
|---|---|---|
| `SEED` | 42 | seed mặc định |
| `R_SERVICE_KM` | 1,0 | bán kính phục vụ của một trạm (km) |
| `D_MIN_KM` | 1,0 | khoảng cách tối thiểu giữa hai trạm (km) |
| `MAX_NEW_STATIONS` | 10 | số trạm mới tối đa |
| `GRID_STEP_KM` | 1,0 | bước lưới sinh ứng viên (km) |
| `COST_PER_STATION` | 1,0 | chi phí quy ước cho 1 trạm |
| `COST_PER_KM` | 2,0 | chi phí quy ước cho 1 km tuyến |
| `BUDGET` | 50,0 | ngân sách quy ước |
| `DEFAULT_WEIGHTS` | `{"pop": 1.0, "cost": 0.1, "penalty": 5.0}` | trọng số hàm mục tiêu |

Chi phí và ngân sách là **đơn vị quy ước**, không phải tiền thật.

### 6.2. Giao diện hàm (đã chốt với Khối 4)

```python
haversine(lat1, lon1, lat2, lon2) -> float          # km
distance_matrix(lat_a, lon_a, lat_b, lon_b) -> np.ndarray
make_state(indices) -> tuple
random_state(n_stations, rng) -> tuple              # rng = np.random.default_rng(seed)
served_population(state) -> float
line_length(state) -> float                         # km, MST + đoạn nối mạng hiện có
construction_cost(state) -> float
penalty(state) -> float
is_feasible(state) -> bool
objective(state, weights=DEFAULT_WEIGHTS) -> float  # càng cao càng tốt
objective_breakdown(state, weights=DEFAULT_WEIGHTS) -> dict
get_neighbors(state, allow_add_remove=True) -> list[tuple]
random_neighbor(state, rng, allow_add_remove=True) -> tuple
```

Quy ước: tên hàm dạng snake_case; `n_stations` phải là số nguyên dương; `weights` là dict có đủ ba khoá `pop`, `cost`, `penalty` (không truyền `None`); luôn truyền `rng = np.random.default_rng(seed)`, không dùng `np.random.seed`.

## 7. Kiểm thử

Ô cuối của notebook chạy 6 nhóm kiểm thử: `random_state` lặp lại được theo seed và thoả khoảng cách tối thiểu; thêm trạm không làm giảm dân số phục vụ; trạng thái rỗng chỉ tính trạm đã có; hàng xóm đúng định dạng, không trùng; `random_neighbor` luôn nằm trong `get_neighbors`; leo đồi thử nghiệm tăng điểm và cho lời giải hợp lệ.

Kết quả tham khảo (seed 1, 5 trạm khởi đầu): 3.383 hàng xóm; leo đồi đưa điểm từ −8,23 lên **0,133** với 10 trạm mới, phục vụ 21,1% dân số, tuyến nối 14,5 km, chi phí 39,1/50, không vi phạm ràng buộc.

## 8. Hạn chế dữ liệu đã biết

- **Toạ độ geocode tự động chưa được kiểm tra hết bằng tay.** Một số trạm (chủ yếu là trạm quy hoạch) đang sai vị trí, ví dụ Ngã Sáu Gò Vấp, Nhà thờ Đức Bà và Tân Kỳ Tân Quý trùng một toạ độ; Gò Dầu trùng Thủ Dầu Một; Lotte Mart, Nguyễn Tri Phương, Cầu Chà Và, Phước Thiện và Bình Thắng rơi về phía Vũng Tàu; Bình Khánh (tuyến CG, đang xây) đang lấy nhầm toạ độ ga Bình Khánh ở Thủ Thiêm. Cần sửa tay theo OpenStreetMap trước khi dùng trạm quy hoạch để so sánh.
- Toạ độ phường/xã là điểm đại diện do Nominatim trả về, không phải tâm hình học hay tâm dân cư.
- Mô hình phục vụ là nhị phân theo tâm phường (cả phường được phục vụ hoặc không), trong khi một phường mới có thể rộng hàng chục km² và có tới khoảng 266 nghìn dân.
- Dân số năm 2025 là số liệu sơ bộ của niên giám.
