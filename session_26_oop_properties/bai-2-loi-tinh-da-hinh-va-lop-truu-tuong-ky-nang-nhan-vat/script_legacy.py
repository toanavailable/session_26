# Lớp cha: Khuôn mẫu Tướng (Nhưng không dùng thư viện ABC)
class Hero:
    def use_ultimate(self):
        # Ném ra lỗi nếu lớp con quên ghi đè hàm này
        raise NotImplementedError("Lớp con bắt buộc phải có chiêu cuối use_ultimate!")

# Lớp con 1: Pháp Sư (Code đúng)
class Mage(Hero):
    def use_ultimate(self):
        print("🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!")

# Lớp con 2: Sát Thủ (Lỗi thiết kế)
class Assassin(Hero):
    # Lập trình viên quên ghi đè use_ultimate(), tự chế ra hàm mới
    def stealth_kill(self):
        print("🗡 Sát Thủ tung chiêu: ÁM SÁT TỪ PHÍA SAU!")

# --- KỊCH BẢN LỖI RUNTIME ---
print("--- LOADING TRẬN ĐẤU ---")
# Việc khởi tạo Sát Thủ diễn ra trót lọt, không hề có cảnh báo nào!
team_heroes = [Mage(), Assassin()]
print("Tải trận đấu thành công! Các tướng đã sẵn sàng...")

print("\n--- GIAO TRANH TỔNG BẮT ĐẦU ---")
# Vòng lặp Đa hình (Polymorphism)
for hero in team_heroes:
    hero.use_ultimate()
