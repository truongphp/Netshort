import json
import base64
from datetime import datetime

# ==============================================================================
# KHỐI 1: CƠ SỞ DỮ LIỆU TRUNG TÂM (Tương đương biến appState trong file HTML)
# ==============================================================================
app_state = {
    "room": "NHOM6-CHITIEU",
    "pin": "1234",
    "members": ["Trường", "Thành viên 2", "Thành viên 3", "Thành viên 4", "Thành viên 5", "Thành viên 6"],
    "expenses": [
        {
            "id": 1,
            "date": "2026-10-22",
            "title": "Liên hoan nhóm buổi đầu",
            "amount": 600000,
            # paid_map lưu số tiền từng người (từ 0 đến 5) đã đóng cho khoản chi này
            "paid_map": {0: 100000, 1: 100000, 2: 100000, 3: 0, 4: 0, 5: 0}
        },
        {
            "id": 2,
            "date": "2026-10-22",
            "title": "Tiền sân cầu lông + Nước",
            "amount": 300000,
            "paid_map": {0: 50000, 1: 50000, 2: 0, 3: 50000, 4: 0, 5: 0}
        }
    ]
}

is_admin_mode = True  # True = Quản Quỹ (Người Nhập), False = Chế Độ Xem


# ==============================================================================
# KHỐI 2: CÁC HÀM TIỆN ÍCH & HIỂN THỊ BẢNG THỐNG KÊ + BIỂU ĐỒ (RENDER ENGINE)
# ==============================================================================
def format_vnd(so_tien):
    """Định dạng số thành tiền VNĐ (VD: 600000 -> 600,000 đ)"""
    return f"{int(round(so_tien)):,} đ"


def ve_thanh_bieu_do(phan_tram, do_dai=15):
    """Vẽ thanh biểu đồ trực quan [████████░░░░░░░] giống hệt chart-bar trên web"""
    so_o_day = int((phan_tram / 100) * do_dai)
    so_o_trong = do_dai - so_o_day
    thanh = "█" * so_o_day + "░" * so_o_trong
    mau = "\033[92m" if phan_tram >= 100 else ("\033[93m" if phan_tram >= 50 else "\033[91m")
    return f"{mau}[{thanh}] {phan_tram}%\033[0m"


def hien_thi_toan_bo():
    """Tương đương hàm renderAll() trong file HTML của bạn"""
    tong_da_chi = 0
    tong_da_thu = 0
    can_dong = [0, 0, 0, 0, 0, 0]
    da_dong = [0, 0, 0, 0, 0, 0]

    # Tính toán số liệu cho cả nhóm và từng người
    for exp in app_state["expenses"]:
        chia_6 = exp["amount"] / 6
        tong_da_chi += exp["amount"]
        for m in range(6):
            can_dong[m] += chia_6
            tien_dong = exp["paid_map"].get(m, 0)
            da_dong[m] += tien_dong
            tong_da_thu += tien_dong

    # 1. Thanh trạng thái đám mây & quyền hạn
    quyen_str = "\033[93m🔑 Quản Quỹ (Người Nhập)\033[0m" if is_admin_mode else "\033[96m👀 Chế Độ Xem\033[0m"
    print("\n" + "=" * 72)
    print(f"☁️  PHÒNG: \033[95m{app_state['room']}\033[0m | Chế độ: {quyen_str}")
    print("=" * 72)

    # 2. Bốn ô tổng quan (Summary Grid)
    print(f"📌 Tổng khoản chi : {len(app_state['expenses'])} mục")
    print(f"💸 Tổng tiền chi  : \033[96m{format_vnd(tong_da_chi)}\033[0m")
    print(f"⚖️  Mỗi người (÷6) : \033[93m{format_vnd(tong_da_chi / 6)}\033[0m")
    print(f"💰 Đã thu về quỹ  : \033[92m{format_vnd(tong_da_thu)}\033[0m")
    print("-" * 72)

    # 3. Bảng kê chi tiêu chi tiết
    print("\033[96m📋 BẢNG KÊ CHI TIÊU CHI TIẾT:\033[0m")
    if not app_state["expenses"]:
        print("   (Chưa có khoản chi nào)")
    for idx, exp in enumerate(app_state["expenses"]):
        chia_6 = round(exp["amount"] / 6)
        print(f" #{idx + 1} [{exp['date']}] {exp['title']} | Tổng: \033[93m{format_vnd(exp['amount'])}\033[0m (÷6: {format_vnd(chia_6)})")
        
        # Hiển thị chip trạng thái đóng tiền của 6 người
        chips = []
        for m_idx, m_name in enumerate(app_state["members"]):
            p_val = exp["paid_map"].get(m_idx, 0)
            if p_val >= chia_6 and chia_6 > 0:
                chips.append(f"\033[92m✓ {m_name}\033[0m")
            elif p_val > 0:
                chips.append(f"\033[93m~ {m_name}({format_vnd(p_val)})\033[0m")
            else:
                chips.append(f"\033[90m○ {m_name}\033[0m")
        print("    └─ Trạng thái: " + " | ".join(chips))

    print("-" * 72)

    # 4. Bảng thống kê 6 thành viên & Biểu đồ
    print("\033[96m📊 THỐNG KÊ TỔNG HỢP 6 THÀNH VIÊN & BIỂU ĐỒ TIẾN ĐỘ:\033[0m")
    for m_idx, m_name in enumerate(app_state["members"]):
        need = round(can_dong[m_idx])
        paid = round(da_dong[m_idx])
        diff = paid - need
        pct = min(100, round((paid / need) * 100)) if need > 0 else 100

        if diff == 0:
            trang_thai = "\033[92mĐã đóng đủ ✓\033[0m"
        elif diff < 0:
            trang_thai = f"\033[91mThiếu {format_vnd(abs(diff))}\033[0m"
        else:
            trang_thai = f"\033[96mDư +{format_vnd(diff)}\033[0m"

        bieu_do = ve_thanh_bieu_do(pct)
        print(f" {m_idx + 1}. {m_name:<13} | Đã đóng: {format_vnd(paid):<11} | {bieu_do} | {trang_thai}")
    print("=" * 72)


# ==============================================================================
# KHỐI 3: CÁC HÀM NGHIỆP VỤ QUẢN QUỸ (THÊM, ĐÁNH DẤU ĐÓNG TIỀN, XÓA, ĐỔI TÊN)
# ==============================================================================
def them_khoan_chi():
    """Tương đương hàm addExpense() trong file HTML"""
    if not is_admin_mode:
        print("\033[91m✖ Bạn đang ở Chế Độ Xem! Hãy mở khóa Quản Quỹ trước.\033[0m")
        return

    ten_muc = input("👉 Nhập tên khoản chi (VD: Ăn lẩu, Trà sữa...): ").strip()
    so_tien = int(input("👉 Nhập tổng số tiền đã chi (VNĐ): "))

    if not ten_muc or so_tien <= 0:
        print("\033[91m✖ Tên khoản chi hoặc số tiền không hợp lệ!\033[0m")
        return

    chia_6 = round(so_tien / 6)
    print(f"\033[96m💡 Tự động chia 6: {format_vnd(chia_6)} / người\033[0m")

    khoan_moi = {
        "id": len(app_state["expenses"]) + 1,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "title": ten_muc,
        "amount": so_tien,
        "paid_map": {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    }
    app_state["expenses"].append(khoan_moi)
    print("\033[92m✔ Đã lưu khoản chi mới thành công!\033[0m")


def danh_dau_dong_tien():
    """Tương đương hàm toggleMemberPaid() trong file HTML"""
    if not is_admin_mode:
        print("\033[91m✖ Chỉ Quản Quỹ mới được đánh dấu đóng tiền!\033[0m")
        return

    stt_muc = int(input("👉 Nhập STT khoản chi (VD: 1, 2...): ")) - 1
    if stt_muc < 0 or stt_muc >= len(app_state["expenses"]):
        print("\033[91m✖ Không tìm thấy khoản chi này!\033[0m")
        return

    exp = app_state["expenses"][stt_muc]
    chia_6 = round(exp["amount"] / 6)

    print(f"Đang chọn mục: \033[93m{exp['title']}\033[0m (Mỗi người cần đóng: {format_vnd(chia_6)})")
    for i, name in enumerate(app_state["members"]):
        print(f"  [{i + 1}] {name} (Đã đóng: {format_vnd(exp['paid_map'][i])})")

    stt_tv = int(input("👉 Chọn số thứ tự thành viên (1-6): ")) - 1
    if stt_tv < 0 or stt_tv >= 6:
        print("\033[91m✖ Thành viên không hợp lệ!\033[0m")
        return

    hien_tai = exp["paid_map"][stt_tv]
    if hien_tai == 0:
        exp["paid_map"][stt_tv] = chia_6
        print(f"\033[92m✔ Đã đánh dấu {app_state['members'][stt_tv]} đóng đủ {format_vnd(chia_6)}!\033[0m")
    else:
        tuy_chinh = int(input(f"Nhập số tiền {app_state['members'][stt_tv]} đã đóng (Nhập 0 để hủy): "))
        exp["paid_map"][stt_tv] = max(0, tuy_chinh)
        print("\033[92m✔ Đã cập nhật số tiền!\033[0m")


# 🎯 NHIỆM VỤ 1 CỦA BẠN: Hoàn thiện hàm xóa khoản chi
def xoa_khoan_chi():
    if not is_admin_mode:
        print("\033[91m✖ Chỉ Quản Quỹ mới được xóa!\033[0m")
        return
    # HƯỚNG DẪN CODE:
    # 1. Dùng int(input(...)) hỏi người dùng muốn xóa khoản chi STT mấy.
    # 2. Dùng lệnh app_state["expenses"].pop(stt - 1) để xóa khoản chi đó khỏi danh sách.
    # 3. In thông báo màu xanh lá: Đã xóa thành công!
    print("\033[93m[Chức năng này đang chờ bạn viết code ở Nhiệm Vụ 1!]\033[0m")


# 🎯 NHIỆM VỤ 2 CỦA BẠN: Hoàn thiện hàm đổi tên 6 thành viên
def doi_ten_thanh_vien():
    if not is_admin_mode:
        print("\033[91m✖ Chỉ Quản Quỹ mới được đổi tên thành viên!\033[0m")
        return
    # HƯỚNG DẪN CODE:
    # Dùng vòng lặp: for i in range(6):
    # Hỏi tên mới: ten_moi = input(f"Nhập tên mới cho thành viên {i+1}: ")
    # Nếu ten_moi khác rỗng thì gán: app_state["members"][i] = ten_moi
    print("\033[93m[Chức năng này đang chờ bạn viết code ở Nhiệm Vụ 2!]\033[0m")


# 🎯 NHIỆM VỤ 3 CỦA BẠN: Hoàn thiện hàm đổi tên Phòng & Mã PIN
def cai_dat_phong_pin():
    if not is_admin_mode:
        print("\033[91m✖ Chỉ Quản Quỹ mới được cài đặt phòng!\033[0m")
        return
    # HƯỚNG DẪN CODE:
    # 1. Hỏi tên phòng mới -> gán vào app_state["room"]
    # 2. Hỏi mã PIN mới -> gán vào app_state["pin"]
    print("\033[93m[Chức năng này đang chờ bạn viết code ở Nhiệm Vụ 3!]\033[0m")


def chuyen_che_do_quyen():
    """Tương đương hàm toggleEditMode() kiểm tra mã PIN trong file HTML"""
    global is_admin_mode
    if is_admin_mode:
        is_admin_mode = False
        print("\033[96m👀 Đã chuyển sang: Chế Độ Xem (Khóa chỉnh sửa).\033[0m")
    else:
        nhap_pin = input("🔒 Nhập Mã PIN Quản Quỹ để mở khóa (Mặc định: 1234): ")
        if nhap_pin == app_state["pin"]:
            is_admin_mode = True
            print("\033[92m🔑 Mở khóa thành công! Đang ở chế độ Quản Quỹ.\033[0m")
        else:
            print("\033[91m✖ Sai Mã PIN!\033[0m")


def xuat_ma_chia_se():
    """Tương đương hàm openShareModal() mã hóa Base64 toàn bộ dữ liệu"""
    chuoi_json = json.dumps(app_state, ensure_ascii=False)
    ma_hoa = base64.b64encode(chuoi_json.encode("utf-8")).decode("utf-8")
    print("\n\033[92m🔗 LINK ĐỒNG BỘ DỮ LIỆU CỦA NHÓM 6 NGƯỜI:\033[0m")
    print(f"https://quynhom6.app/?room={app_state['room']}&view=1#data={ma_hoa[:45]}...")


# ==============================================================================
# KHỐI 4: VÒNG LẶP ĐIỀU KHIỂN TRUNG TÂM (MAIN CONTROLLER)
# ==============================================================================
def chay_ung_dung():
    while True:
        hien_thi_toan_bo()
        print("🎛️  MENU ĐIỀU KHIỂN: [1] Thêm khoản chi | [2] Đánh dấu đóng tiền | [3] Xóa khoản chi")
        print("                    [4] Đổi tên 6 người | [5] Cài đặt Phòng/PIN  | [6] Đổi Chế độ Xem/Sửa")
        print("                    [7] Xuất Link đồng bộ | [0] Thoát chương trình")
        
        chon = input("\n👉 Nhập lựa chọn của bạn (0-7): ").strip()
        if chon == "1":
            them_khoan_chi()
        elif chon == "2":
            danh_dau_dong_tien()
        elif chon == "3":
            xoa_khoan_chi()
        elif chon == "4":
            doi_ten_thanh_vien()
        elif chon == "5":
            cai_dat_phong_pin()
        elif chon == "6":
            chuyen_che_do_quyen()
        elif chon == "7":
            xuat_ma_chia_se()
        elif chon == "0":
            print("\033[93m👋 Đã lưu dữ liệu quỹ nhóm. Hẹn gặp lại!\033[0m")
            break
        else:
            print("\033[91m✖ Lựa chọn không hợp lệ!\033[0m")

# Khởi chạy toàn bộ hệ thống
chay_ung_dung()
