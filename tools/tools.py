from langchain_core.tools import tool

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1450000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2800000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1200000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1350000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1100000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1600000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1300000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3200000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1300000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1100000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650000, "class": "economy"},
    ],
}


HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1800000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1200000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3500000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1500000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2800000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1400000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180000, "area": "Quận 1", "rating": 4.6},
    ],
}

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: Thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: Thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    def format_price(price: int) -> str:
        return f"{price:,.0f}đ".replace(",", ".")

    flights = FLIGHTS_DB.get((origin, destination))
    direction = f"{origin} → {destination}"

    if not flights:
        # Thử tìm chiều ngược lại
        flights = FLIGHTS_DB.get((destination, origin))
        if flights:
            direction = f"{destination} → {origin}"

    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    lines = [f"✈️ Chuyến bay {direction}:\n"]
    for i, f in enumerate(flights, 1):
        lines.append(
            f"  {i}. {f['airline']} | {f['departure']} → {f['arrival']} "
            f"| Hạng {f['class']} | Giá: {format_price(f['price'])}"
        )
    return "\n".join(lines)

@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.

    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VND), mặc định không giới hạn

    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """

    # TODO: Sinh viên tự triển khai
    # - Tra cứu HOTELS_DB[city]
    # - Lọc theo max_price_per_night
    # - Sắp xếp theo rating giảm dần
    # - Format đẹp. Nếu không có kết quả -> "Không tìm thấy khách sạn tại X
    #   với giá dưới Y/đêm. Hãy thử tăng ngân sách."

    def format_price(price: int) -> str:
        return f"{price:,.0f}đ".replace(",", ".")

    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy thông tin khách sạn tại {city}."

    filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    if not filtered:
        return f"Không có khách sạn tại {city} với giá dưới {format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."

    # Sắp xếp theo rating giảm dần
    filtered.sort(key=lambda h: h["rating"], reverse=True)

    lines = [f"🏨 Khách sạn tại {city} (giá dưới {format_price(max_price_per_night)}/đêm):\n"]
    for i, h in enumerate(filtered, 1):
        stars_str = "⭐" * h["stars"]
        lines.append(
            f"  {i}. {h['name']} {stars_str} | Khu vực: {h['area']} "
            f"| Giá: {format_price(h['price_per_night'])}/đêm | Rating: {h['rating']}/5"
        )
    return "\n".join(lines)
    
@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.

    Tham số:
    - total_budget: tổng ngân sách ban đầu (VND)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')

    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """

    def format_price(price: float) -> str:
        return f"{price:,.0f}đ".replace(",", ".")

    # Parse chuỗi expenses thành list [(tên, số_tiền)]
    items = []
    for part in expenses.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            return f"❌ Lỗi định dạng: '{part}' không hợp lệ. Dùng định dạng 'tên:số_tiền' (VD: 'vé_máy_bay:890000')."
        name, _, amount_str = part.partition(":")
        try:
            amount = float(amount_str.strip())
        except ValueError:
            return f"❌ Lỗi: '{amount_str.strip()}' không phải số hợp lệ cho khoản '{name.strip()}'."
        items.append((name.strip().replace("_", " ").title(), int(amount)))

    if not items:
        return "❌ Không có khoản chi nào được cung cấp."

    total_expense = sum(amount for _, amount in items)
    remaining = total_budget - total_expense

    lines = ["💰 Bảng chi phí:\n"]
    for name, amount in items:
        lines.append(f"  - {name}: {format_price(amount)}")
    lines.append(f"  {'─' * 40}")
    lines.append(f"  📊 Tổng chi  : {format_price(total_expense)}")
    lines.append(f"  💵 Ngân sách : {format_price(total_budget)}")

    if remaining >= 0:
        lines.append(f"  ✅ Còn lại   : {format_price(remaining)}")
    else:
        lines.append(f"  ⚠️  Còn lại   : -{format_price(abs(remaining))}")
        lines.append(f"\n  🚨 Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh.")

    return "\n".join(lines)
