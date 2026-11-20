# Metro LBS

Ứng dụng **Local Beam Search** trong thiết kế tối ưu mạng lưới trạm Metro TP.HCM giai đoạn mở rộng.

Đồ án môn Trí tuệ nhân tạo — HCMUTE.

## 1. Giới thiệu

Dự án xây dựng mô hình chọn vị trí đặt các trạm Metro mới tại TP.HCM sao cho phục vụ được nhiều dân số nhất với chi phí hợp lý, sau đó giải bằng Local Beam Search và các biến thể.

Kết quả được so sánh giữa các thuật toán, giữa các giá trị beam width `k`, và với quy hoạch Metro thực tế của TP.HCM.

## 2. Công nghệ

- Python 3 trên Jupyter Notebook
- `pandas` — xử lý dữ liệu
- `numpy` — tính toán, sinh số ngẫu nhiên
- `matplotlib` — đồ thị và bản đồ

## 3. Cấu trúc thư mục

```
metro-lbs/
├── notebooks/        # Notebook chính, chia theo 6 khối chức năng
├── data/
│   ├── raw/          # Dữ liệu gốc, không chỉnh sửa
│   └── processed/    # Dữ liệu đã chuẩn hoá
├── results/          # Kết quả thực nghiệm dạng CSV
├── figures/          # Đồ thị và bản đồ xuất ra
├── report/           # Báo cáo
├── requirements.txt
└── README.md
```

## 4. Cài đặt và chạy

```bash
# 1. Tạo môi trường ảo
python3 -m venv .venv

# 2. Kích hoạt môi trường ảo
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# 3. Cài thư viện
pip install -r requirements.txt

# 4. Chạy Jupyter Notebook
jupyter notebook
```

> **Lưu ý:** Trên một số hệ thống Linux, dùng `python3` thay vì `python`.
> Nếu muốn dùng lệnh `python` trực tiếp: `sudo apt install python-is-python3`

## 5. Phân chia công việc

| Thành viên | Khối code phụ trách | Chương báo cáo |
|---|---|---|
| Thành viên 1 | Khối 1. Dữ liệu<br>Khối 2. Tập ứng viên<br>Khối 3. Mô hình hoá bài toán | Chương 1, Chương 3, Chương 5 (cùng viết) |
| Thành viên 2 | Khối 4. Thuật toán<br>Khối 5. Thực nghiệm<br>Khối 6. Trình bày kết quả | Chương 2, Chương 4, Chương 5 (cùng viết) |

Thành viên 1 làm phần nền (dữ liệu và mô hình), Thành viên 2 làm phần chạy và phân tích. Mỗi người viết chương báo cáo gắn với phần code của mình.

Tổng cộng 30 chức năng, mỗi người 15.

## 6. Danh sách chức năng

### Khối 1. Dữ liệu — Thành viên 1

Chuẩn bị toàn bộ dữ liệu đầu vào. Đầu ra là các DataFrame sạch, dùng chung cho cả nhóm.

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Đọc bảng phường | Tên, quận, dân số, vĩ độ, kinh độ vào DataFrame |
| 2 | Đọc danh sách trạm Metro hiện có | Các trạm đã có hoặc đang xây, kèm toạ độ |
| 3 | Chuẩn hoá và kiểm tra dữ liệu | Chuẩn hoá tên cột, kiểu dữ liệu, tên phường; xử lý giá trị thiếu và dòng trùng |
| 4 | Tính khoảng cách địa lý | Hàm Haversine, đơn vị km |
| 5 | Vẽ bản đồ hiện trạng | Phân bố dân số theo phường và vị trí các trạm hiện có |

### Khối 2. Tập ứng viên — Thành viên 1

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Sinh tập vị trí ứng viên | Từ tâm các phường hoặc từ lưới điểm phủ khu vực |
| 2 | Lọc ứng viên không hợp lệ | Loại ứng viên quá gần trạm đã có hoặc ngoài vùng xét |
| 3 | Tính trước ma trận khoảng cách | Giữa ứng viên và các phường, để hàm mục tiêu chạy nhanh |

### Khối 3. Mô hình hoá bài toán — Thành viên 1

Khối trung tâm. Khối 4 dùng trực tiếp các hàm ở đây nên cần chốt sớm.

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Tạo trạng thái ngẫu nhiên hợp lệ | Chọn ngẫu nhiên một tập trạm mới thoả ràng buộc cơ bản |
| 2 | Tính dân số được phục vụ | Tổng dân số các phường trong bán kính phục vụ của ít nhất một trạm |
| 3 | Tính chi phí xây dựng và chiều dài tuyến | Theo số trạm và tổng chiều dài tuyến nối các trạm |
| 4 | Kiểm tra ràng buộc và tính hình phạt | Khoảng cách tối thiểu, số trạm tối đa, ngân sách |
| 5 | Hàm mục tiêu tổng hợp | Kết hợp dân số, chi phí, hình phạt theo bộ trọng số |
| 6 | Sinh toàn bộ hàng xóm | Mọi trạng thái kề: thay, thêm hoặc bớt một trạm |
| 7 | Sinh một hàng xóm ngẫu nhiên | Dùng cho stochastic local beam search |

### Khối 4. Thuật toán — Thành viên 2

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Local beam search | Mỗi vòng giữ `k` trạng thái tốt nhất trong toàn bộ hàng xóm |
| 2 | Stochastic local beam search | Chọn `k` trạng thái kế tiếp ngẫu nhiên có trọng số theo điểm |
| 3 | Random restart | Chạy lại từ nhiều trạng thái khởi đầu, giữ kết quả tốt nhất |
| 4 | Ghi lịch sử điểm | Điểm tốt nhất và trung bình beam theo từng vòng |
| 5 | Điều kiện dừng | Số vòng tối đa, hoặc nhiều vòng không cải thiện (`patience`) |

### Khối 5. Thực nghiệm — Thành viên 2

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Chạy lặp nhiều seed | Khoảng 20 lần mỗi cấu hình, báo cáo trung bình và độ lệch chuẩn |
| 2 | Quét beam width | `k = 1, 3, 5, 10, 20`; ghi điểm và thời gian chạy |
| 3 | So sánh các thuật toán | Hill climbing, local beam, stochastic beam, random restart (`k = 1` chính là hill climbing) |
| 4 | Phân tích độ nhạy trọng số | Thay đổi trọng số dân số / chi phí |
| 5 | Lưu kết quả ra file | CSV trong `results/` để không phải chạy lại |

### Khối 6. Trình bày kết quả — Thành viên 2

| # | Chức năng | Mô tả |
|---|---|---|
| 1 | Đồ thị hội tụ | Điểm số theo vòng lặp cho từng thuật toán hoặc từng `k` |
| 2 | Đồ thị điểm và thời gian theo `k` | Đánh đổi giữa chất lượng lời giải và thời gian chạy |
| 3 | Bản đồ phương án tốt nhất | Trạm mới đề xuất cùng trạm hiện có trên nền dân số |
| 4 | Bản đồ so sánh với quy hoạch thực | Đặt cạnh quy hoạch Metro TP.HCM |
| 5 | Xuất bảng kết quả | Bảng tổng hợp định dạng sẵn cho báo cáo |

## 7. Giao diện chung

Khối 4, 5, 6 dùng trực tiếp đầu ra của khối 1, 2, 3. Hai người chốt tên hàm, tham số và kiểu trả về ngay từ đầu; sau khi chốt thì không tự ý đổi.

### Quy ước dữ liệu

- **Trạng thái**: tuple các chỉ số ứng viên được chọn, đã sắp xếp
- **Tên cột DataFrame**: `ten`, `dan_so`, `lat`, `lon`
- **Đơn vị khoảng cách**: km
- **Hằng số cần chốt**: bán kính phục vụ, khoảng cách tối thiểu giữa hai trạm, số trạm mới tối đa
- **Chiều điểm số**: điểm càng cao càng tốt (tìm cực đại)

### Chữ ký hàm

| Hàm | Ý nghĩa | Viết / Dùng |
|---|---|---|
| `haversine(lat1, lon1, lat2, lon2) -> float` | Khoảng cách km giữa hai điểm | TV1 / cả hai |
| `random_state(n_stations, rng) -> state` | Trạng thái ngẫu nhiên hợp lệ | TV1 / TV2 |
| `objective(state, weights) -> float` | Điểm số tổng hợp của một trạng thái | TV1 / TV2 |
| `get_neighbors(state) -> list[state]` | Toàn bộ hàng xóm | TV1 / TV2 |
| `random_neighbor(state, rng) -> state` | Một hàng xóm ngẫu nhiên | TV1 / TV2 |
| `local_beam_search(k, max_iters, patience, seed) -> (best_state, best_score, history)` | Thuật toán chính | TV2 / TV2 |

Trong lúc TV1 hoàn thiện khối 3, TV2 có thể dùng một `objective` tạm (trả về số ngẫu nhiên) có cùng chữ ký để viết trước khối 4.

### Quy ước làm việc

- Dùng chung `numpy.random.default_rng(seed)` để kết quả lặp lại được
- Mỗi khối viết trong một phần riêng của notebook, có tiêu đề Markdown ghi rõ khối và người phụ trách
- Dùng chung bảng màu, cỡ chữ và kích thước hình matplotlib cho mọi đồ thị
- Kết quả thực nghiệm lưu CSV vào `results/`, hình lưu vào `figures/`

## 8. Báo cáo

| Chương | Nội dung | Người viết |
|---|---|---|
| 1. Giới thiệu | Thực trạng giao thông TP.HCM, nhu cầu mở rộng Metro, lý do chọn Local Beam Search | TV1 |
| 2. Cơ sở lý thuyết | Tối ưu tổ hợp, local search và các biến thể, Local Beam Search chi tiết | TV2 |
| 3. Mô hình hoá | Biểu diễn trạng thái, hàm mục tiêu, không gian hàng xóm | TV1 |
| 4. Thực nghiệm và kết quả | Dữ liệu thực TP.HCM, so sánh thuật toán, phân tích `k`, so sánh quy hoạch thực | TV2 |
| 5. Kết luận và hướng phát triển | Tổng kết, hạn chế, hướng mở rộng | Cả hai |

Hai người đọc chéo chương của nhau trước khi ghép bản cuối.
