"""Rikkei RPG - Auto-Battler Manager: quản lý quân cờ bằng OOP nâng cao.

Sơ đồ lớp:
    Champion (ABC)            champion_id, name, base_hp, base_atk
      |  @abstractmethod calculate_skill_damage()
      |  get_combat_power() = HP + skill_damage * 1.5
      |  __add__ / __radd__ (cộng chiến lực), __gt__ (so sánh)
      |-- Warrior             + shield_bonus;  skill = base_atk * 2 + shield_bonus
      |-- Mage                + ability_power; skill = base_atk * ability_power
"""

from abc import ABC, abstractmethod

DEFAULT_STAT = 100          # Bẫy 2: HP / ATK <= 0 thì gán mặc định 100
POWER_MULTIPLIER = 1.5
TABLE_LINE = "-" * 96
MENU_LINE = "=" * 50


class Champion(ABC):
    """Lớp trừu tượng: khuôn mẫu chung của mọi quân cờ (không tạo object trực tiếp)."""

    role = "Champion"

    def __init__(self, champion_id, name, base_hp, base_atk):
        """Khởi tạo thông tin chung; chỉ số <= 0 được gán mặc định 100."""
        self.champion_id = champion_id
        self.name = name
        self.base_hp = base_hp if base_hp > 0 else DEFAULT_STAT
        self.base_atk = base_atk if base_atk > 0 else DEFAULT_STAT

    @abstractmethod
    def calculate_skill_damage(self):
        """Sát thương kỹ năng (float) - mỗi hệ tự định nghĩa (đa hình)."""

    @abstractmethod
    def special_stat(self):
        """Chuỗi mô tả chỉ số riêng của hệ (để hiển thị)."""

    def get_combat_power(self):
        """Chiến lực = Máu + (Sát thương kỹ năng * 1.5)."""
        return self.base_hp + self.calculate_skill_damage() * POWER_MULTIPLIER

    def __add__(self, other):
        """Champion + Champion / số -> tổng chiến lực (số)."""
        if isinstance(other, Champion):
            return self.get_combat_power() + other.get_combat_power()
        if isinstance(other, (int, float)):
            return self.get_combat_power() + other
        return NotImplemented

    def __radd__(self, other):
        """số + Champion (cần cho sum() vì sum bắt đầu cộng từ 0)."""
        return self.__add__(other)

    def __gt__(self, other):
        """So sánh chiến lực giữa 2 quân cờ bằng toán tử >."""
        if not isinstance(other, Champion):
            return NotImplemented
        return self.get_combat_power() > other.get_combat_power()

    def __str__(self):
        """Chuỗi ngắn gọn: mã - tên."""
        return f"{self.champion_id} - {self.name}"


class Warrior(Champion):
    """Chiến binh: sát thương kỹ năng = base_atk * 2 + shield_bonus."""

    role = "Warrior"

    def __init__(self, champion_id, name, base_hp, base_atk, shield_bonus):
        """Dùng super() để tái sử dụng khởi tạo của Champion."""
        super().__init__(champion_id, name, base_hp, base_atk)
        self.shield_bonus = shield_bonus

    def calculate_skill_damage(self):
        """Sát thương kỹ năng của Warrior."""
        return float(self.base_atk * 2 + self.shield_bonus)

    def special_stat(self):
        """Hiển thị giáp."""
        return f"Armor: {self.shield_bonus}"


class Mage(Champion):
    """Pháp sư: sát thương kỹ năng = base_atk * ability_power."""

    role = "Mage"

    def __init__(self, champion_id, name, base_hp, base_atk, ability_power):
        """Dùng super() để tái sử dụng khởi tạo của Champion."""
        super().__init__(champion_id, name, base_hp, base_atk)
        self.ability_power = ability_power

    def calculate_skill_damage(self):
        """Sát thương kỹ năng của Mage."""
        return float(self.base_atk * self.ability_power)

    def special_stat(self):
        """Hiển thị hệ số phép thuật."""
        return f"Ability: x{self.ability_power}"


# =====================================================================
# HÀM GIAO DIỆN
# =====================================================================
def find_champion(champion_pool, champion_id):
    """Tìm quân cờ theo mã (đã chuẩn hóa), trả về object hoặc None."""
    for champion in champion_pool:
        if champion.champion_id == champion_id:
            return champion
    return None


def input_number(prompt, cast=int):
    """Nhập số (try-except); nhập chữ thì báo lỗi và nhập lại."""
    while True:
        text = input(prompt).strip()
        try:
            return cast(text)
        except ValueError:
            print("Giá trị phải là số, vui lòng nhập lại!")


def format_power(value):
    """Định dạng chiến lực: bỏ phần thập phân .0."""
    return f"{value:g}" if value == int(value) else f"{value:.1f}"


def show_pool(champion_pool):
    """Chức năng 1: bảng bể tướng (đa hình: special_stat, get_combat_power)."""
    print("--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---")
    if not champion_pool:
        print("Bể tướng đang trống.")
        return
    print(f"{'Mã':<6}| {'Tên tướng':<17}| {'Hệ':<8}| {'HP':<6}| {'ATK':<5}| "
          f"{'Chỉ số riêng':<16}| Chiến lực")
    print(TABLE_LINE)
    for champion in champion_pool:
        print(f"{champion.champion_id:<6}| {champion.name:<17}| {champion.role:<8}| "
              f"{champion.base_hp:<6}| {champion.base_atk:<5}| "
              f"{champion.special_stat():<16}| "
              f"{format_power(champion.get_combat_power())}")
    print(TABLE_LINE)


def add_champion(champion_pool):
    """Chức năng 2: tạo Warrior / Mage mới."""
    role = input("Chọn hệ (1 - Warrior, 2 - Mage): ").strip()
    if role not in ("1", "2"):
        print("Hệ không hợp lệ!")
        return
    role_name = "WARRIOR" if role == "1" else "MAGE"
    print(f"--- TẠO TƯỚNG {role_name} ---")
    champion_id = input("Nhập mã tướng: ").strip().upper()
    if not champion_id:
        print("Mã tướng không được để trống!")
        return
    if find_champion(champion_pool, champion_id) is not None:
        print(f"Mã tướng {champion_id} đã tồn tại trong bể tướng!")
        return
    name = " ".join(input("Nhập tên tướng: ").split())
    base_hp = input_number("Nhập HP: ")
    base_atk = input_number("Nhập ATK: ")
    for label, value in (("HP", base_hp), ("ATK", base_atk)):
        if value <= 0:
            print(f"{label} <= 0 không hợp lệ, tự động gán mặc định {DEFAULT_STAT}.")
    if role == "1":
        champion = Warrior(champion_id, name, base_hp, base_atk,
                           input_number("Nhập Armor: "))
    else:
        champion = Mage(champion_id, name, base_hp, base_atk,
                        input_number("Nhập Ability Power (VD: 1.5): ", float))
    champion_pool.append(champion)
    print(f"\nThêm tướng {champion.role} thành công!")
    print(f"Mã: {champion.champion_id} | Tên: {champion.name} | Chiến lực: "
          f"{format_power(champion.get_combat_power())}")


def compare_champions(champion_pool):
    """Chức năng 3: so sánh 2 quân cờ bằng toán tử > (gọi __gt__)."""
    print("--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---")
    first_id = input("Nhập mã tướng thứ nhất: ").strip().upper()
    second_id = input("Nhập mã tướng thứ hai: ").strip().upper()
    first = find_champion(champion_pool, first_id)
    second = find_champion(champion_pool, second_id)
    for champion_id, champion in ((first_id, first), (second_id, second)):
        if champion is None:
            print(f"Mã tướng {champion_id} không hợp lệ, bỏ qua!")
    if first is None or second is None:
        return
    print("Thông tin so sánh:")
    for champion in (first, second):
        print(f"{champion} | Hệ: {champion.role} | Chiến lực: "
              f"{format_power(champion.get_combat_power())}")
    if first > second:
        print(f"Kết quả: {first} mạnh hơn {second}.")
    elif second > first:
        print(f"Kết quả: {second} mạnh hơn {first}.")
    else:
        print("Kết quả: Hai quân cờ có chiến lực ngang nhau.")


def team_power(champion_pool):
    """Chức năng 4: cộng dồn chiến lực đội hình bằng toán tử +."""
    print("--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---")
    raw_ids = input("Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: ")
    team = []
    for champion_id in (item.strip().upper() for item in raw_ids.split(",")):
        if not champion_id:
            continue
        champion = find_champion(champion_pool, champion_id)
        if champion is None:
            print(f"Mã tướng {champion_id} không hợp lệ, bỏ qua!")
            continue
        team.append(champion)
    if not team:
        print("Đội hình không có quân cờ hợp lệ nào.")
        return
    print("Danh sách đội hình:")
    for index, champion in enumerate(team, start=1):
        print(f"{index}. {champion} | Chiến lực: "
              f"{format_power(champion.get_combat_power())}")
    total = sum(team)                      # 0 + c1 -> __radd__, rồi + c2 ...
    print(f"Tổng chiến lực đội hình: {format_power(total)}")


def display_menu():
    """In menu chính."""
    print("\n===== RIKKEI RPG - AUTO-BATTLER MANAGER =====")
    print("1. Hiển thị bể tướng hiện có")
    print("2. Thêm quân cờ mới")
    print("3. So sánh 2 quân cờ")
    print("4. Tính tổng chiến lực Đội Hình Ra Sân")
    print("5. Thoát chương trình")
    print(MENU_LINE)


def main():
    """Khởi tạo bể tướng mẫu và chạy vòng lặp menu."""
    champion_pool = [
        Warrior("WAR01", "Rikkei Knight", 1200, 300, 150),
        Warrior("WAR02", "Steel Guardian", 1500, 250, 200),
        Mage("MAG01", "Rikkei Wizard", 800, 500, 1.5),
    ]
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-5): ").strip()
        if choice == "1":
            show_pool(champion_pool)
        elif choice == "2":
            add_champion(champion_pool)
        elif choice == "3":
            compare_champions(champion_pool)
        elif choice == "4":
            team_power(champion_pool)
        elif choice == "5":
            print("Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-5!")


if __name__ == "__main__":
    main()
