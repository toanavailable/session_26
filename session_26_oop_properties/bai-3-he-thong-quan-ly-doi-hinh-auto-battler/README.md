# Bài 3 - Phân tích: Hệ thống quản lý đội hình Auto-Battler (Rikkei RPG)

## Đề bài

Studio Rikkei RPG xây dựng chế độ chơi Auto-Battler (Cờ tự động). Lập trình viên thực tập trước đó viết code quản lý quân cờ (Champions) bằng một class duy nhất và nhồi nhét hàng tá lệnh `if-else` để phân biệt kỹ năng, chỉ số của từng hệ / tộc; khi thêm tướng mới hệ thống liên tục xung đột dữ liệu và crash. Nhiệm vụ: đập đi xây lại module quản lý đội hình bằng **OOP nâng cao** để dễ mở rộng hàng trăm tướng về sau.

**Kiến thức áp dụng:** Abstract Base Classes (`Champion` làm khuôn mẫu, ngăn khởi tạo tướng "không có hệ tộc"); Inheritance & `super()` (`Warrior`, `Mage` kế thừa `Champion`); Polymorphism (`calculate_skill_damage()` khác nhau nhưng cùng tên hàm); Operator Overloading (`+` cộng dồn sức mạnh đội hình, `>` / `<` so sánh quân cờ).

### Thiết kế lớp

| Lớp | Thuộc tính | Phương thức |
|---|---|---|
| `Champion(ABC)` | `champion_id`, `name`, `base_hp`, `base_atk` | `@abstractmethod calculate_skill_damage()`; `get_combat_power()` = Máu + (Sát thương kỹ năng × 1.5); `__add__`, `__gt__` |
| `Warrior` | + `shield_bonus` (giáp cộng thêm) | Sát thương kỹ năng = `base_atk × 2 + shield_bonus` |
| `Mage` | + `ability_power` (hệ số phép thuật, VD 1.5, 2.0) | Sát thương kỹ năng = `base_atk × ability_power` |

### Menu

```
===== RIKKEI RPG - AUTO-BATTLER MANAGER =====
1. Hiển thị bể tướng hiện có
2. Thêm quân cờ mới
3. So sánh 2 quân cờ
4. Tính tổng chiến lực Đội Hình Ra Sân
5. Thoát chương trình
==================================================
Chọn chức năng (1-5):
```

| Chức năng | Yêu cầu |
|---|---|
| 1. Hiển thị bể tướng | `champion_pool` khởi tạo sẵn ít nhất 3 tướng (2 Warrior, 1 Mage); bảng phân biệt rõ hệ và chỉ số riêng |
| 2. Thêm quân cờ mới | Chọn hệ (1 - Warrior, 2 - Mage), nhập thông tin chung và thuộc tính riêng |
| 3. So sánh 2 quân cờ | Tìm trong bể tướng, dùng `if champion1 > champion2:` (nạp chồng toán tử) |
| 4. Tổng chiến lực đội hình | Nhập mã cách nhau bằng dấu phẩy, cộng dồn bằng toán tử `+` (nạp chồng toán tử) |
| 5. Thoát | "Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!" |

### Edge cases

| Bẫy | Xử lý |
|---|---|
| Bẫy 1 - Khởi tạo lớp trừu tượng | `Champion(...)` → `TypeError` nhờ ABC |
| Bẫy 2 - Chỉ số âm hoặc bằng 0 | `base_hp` / `base_atk` <= 0 → tự gán mặc định 100 (kèm thông báo) |
| Bẫy 3 - Mã tướng không tồn tại | "Mã tướng [Mã] không hợp lệ, bỏ qua!" và chạy tiếp, không crash |
| Bẫy 4 - Trùng mã tướng | Từ chối thêm mới và báo lỗi |

## (1) Phân tích và thiết kế giải pháp

### Sơ đồ cấu trúc

```
                Champion (ABC)
   champion_id, name, base_hp, base_atk
   @abstractmethod calculate_skill_damage()
   get_combat_power(), __add__, __radd__, __gt__
                 /            \
          Warrior              Mage
     + shield_bonus        + ability_power
     skill = atk*2+shield  skill = atk*ability_power
```

`Warrior` và `Mage` **IS-A** `Champion`: tái sử dụng khởi tạo chung qua `super().__init__(...)`, chỉ bổ sung thuộc tính riêng và công thức kỹ năng riêng.

### Phân tích đa hình

`calculate_skill_damage()` có cùng tên ở mọi lớp nhưng mỗi hệ một công thức. `get_combat_power()`, bảng hiển thị, so sánh, tính tổng đội hình đều chỉ gọi `champion.calculate_skill_damage()` mà **không cần biết** quân cờ là hệ gì → không có `if-else` theo hệ tộc. Khi Studio thêm hệ mới (VD `Assassin`, `Ranger`) chỉ cần viết lớp con mới override `calculate_skill_damage()` (và `special_stat()`); toàn bộ menu, so sánh, tính tổng **giữ nguyên không phải sửa** (nguyên tắc Open/Closed). ABC còn bảo đảm lớp mới không thể quên cài đặt công thức.

### Phân tích nạp chồng toán tử `__add__`

`sum(team)` thực hiện `0 + c1 + c2 + ...`. Bước đầu là **số nguyên 0 cộng với object**: Python gọi `int.__add__(0, c1)` → `NotImplemented`, rồi thử `c1.__radd__(0)`. Vì vậy class cài đặt:

- `__add__(self, other)`: nếu `other` là `Champion` → cộng 2 chiến lực; nếu là số → cộng chiến lực với số đó (tổng đang cộng dồn); kiểu khác → `NotImplemented`.
- `__radd__(self, other)` = `__add__`: xử lý trường hợp số đứng trước (`0 + champion`, `tổng + champion`).

Kết quả của phép `+` là **số** (tổng chiến lực), không làm thay đổi bất kỳ quân cờ nào.

Kiểm tra trực tiếp:

```
>>> c = Champion('C01', 'Test', 100, 100)
TypeError: Can't instantiate abstract class Champion without an implementation for abstract methods 'calculate_skill_damage', 'special_stat'
>>> Đa hình: cùng gọi calculate_skill_damage(), mỗi hệ một công thức
  Warrior: 750.0
  Mage: 750.0
>>> w + m = 4250.0 | w + 100 = 2425.0 | sum([w, m]) = 4250.0
>>> Nếu chỉ có __add__ mà không có __radd__, sum() bắt đầu bằng 0 + w:
TypeError: unsupported operand type(s) for +: 'int' and 'WarriorNoRadd'
>>> w > 'abc':
TypeError: '>' not supported between instances of 'Warrior' and 'str'
```

## (2) Triển khai code

File: [`main.py`](main.py)

```python
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
```

## Kết quả chạy thử

Kịch bản: xem bể tướng → thêm WAR03 → thêm `mag02` (HP âm, ATK nhập chữ) → trùng `war01` → hệ sai → so sánh WAR01 / MAG01, WAR02 / MAG02 → mã không tồn tại → tổng đội hình WAR01, MAG01, WAR02 → đội có mã sai → xem lại → menu sai → thoát. Khung menu lặp lại được ẩn.

```
Chọn chức năng (1-5): 1
--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---
Mã    | Tên tướng        | Hệ      | HP    | ATK  | Chỉ số riêng    | Chiến lực
------------------------------------------------------------------------------------------------
WAR01 | Rikkei Knight    | Warrior | 1200  | 300  | Armor: 150      | 2325
WAR02 | Steel Guardian   | Warrior | 1500  | 250  | Armor: 200      | 2550
MAG01 | Rikkei Wizard    | Mage    | 800   | 500  | Ability: x1.5   | 1925
------------------------------------------------------------------------------------------------

Chọn chức năng (1-5): 2
Chọn hệ (1 - Warrior, 2 - Mage): 1
--- TẠO TƯỚNG WARRIOR ---
Nhập mã tướng: WAR03
Nhập tên tướng: Dragon Slayer
Nhập HP: 1300
Nhập ATK: 350
Nhập Armor: 180

Thêm tướng Warrior thành công!
Mã: WAR03 | Tên: Dragon Slayer | Chiến lực: 2620

Chọn chức năng (1-5): 2
Chọn hệ (1 - Warrior, 2 - Mage): 2
--- TẠO TƯỚNG MAGE ---
Nhập mã tướng: mag02
Nhập tên tướng: Frost Witch
Nhập HP: -50
Nhập ATK: ba trăm
Giá trị phải là số, vui lòng nhập lại!
Nhập ATK: 400
HP <= 0 không hợp lệ, tự động gán mặc định 100.
Nhập Ability Power (VD: 1.5): 2.0

Thêm tướng Mage thành công!
Mã: MAG02 | Tên: Frost Witch | Chiến lực: 1300

Chọn chức năng (1-5): 2
Chọn hệ (1 - Warrior, 2 - Mage): 1
--- TẠO TƯỚNG WARRIOR ---
Nhập mã tướng: war01
Mã tướng WAR01 đã tồn tại trong bể tướng!

Chọn chức năng (1-5): 2
Chọn hệ (1 - Warrior, 2 - Mage): 3
Hệ không hợp lệ!

Chọn chức năng (1-5): 3
--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---
Nhập mã tướng thứ nhất: WAR01
Nhập mã tướng thứ hai: MAG01
Thông tin so sánh:
WAR01 - Rikkei Knight | Hệ: Warrior | Chiến lực: 2325
MAG01 - Rikkei Wizard | Hệ: Mage | Chiến lực: 1925
Kết quả: WAR01 - Rikkei Knight mạnh hơn MAG01 - Rikkei Wizard.

Chọn chức năng (1-5): 3
--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---
Nhập mã tướng thứ nhất: WAR02
Nhập mã tướng thứ hai: MAG02
Thông tin so sánh:
WAR02 - Steel Guardian | Hệ: Warrior | Chiến lực: 2550
MAG02 - Frost Witch | Hệ: Mage | Chiến lực: 1300
Kết quả: WAR02 - Steel Guardian mạnh hơn MAG02 - Frost Witch.

Chọn chức năng (1-5): 3
--- SO SÁNH SỨC MẠNH 2 QUÂN CỜ ---
Nhập mã tướng thứ nhất: WAR01
Nhập mã tướng thứ hai: XX99
Mã tướng XX99 không hợp lệ, bỏ qua!

Chọn chức năng (1-5): 4
--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---
Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: WAR01, MAG01, WAR02
Danh sách đội hình:
1. WAR01 - Rikkei Knight | Chiến lực: 2325
2. MAG01 - Rikkei Wizard | Chiến lực: 1925
3. WAR02 - Steel Guardian | Chiến lực: 2550
Tổng chiến lực đội hình: 6800

Chọn chức năng (1-5): 4
--- TÍNH TỔNG CHIẾN LỰC ĐỘI HÌNH RA SÂN ---
Nhập danh sách mã tướng, cách nhau bằng dấu phẩy: war03, abc, mag02
Mã tướng ABC không hợp lệ, bỏ qua!
Danh sách đội hình:
1. WAR03 - Dragon Slayer | Chiến lực: 2620
2. MAG02 - Frost Witch | Chiến lực: 1300
Tổng chiến lực đội hình: 3920

Chọn chức năng (1-5): 1
--- DANH SÁCH QUÂN CỜ TRONG BỂ TƯỚNG ---
Mã    | Tên tướng        | Hệ      | HP    | ATK  | Chỉ số riêng    | Chiến lực
------------------------------------------------------------------------------------------------
WAR01 | Rikkei Knight    | Warrior | 1200  | 300  | Armor: 150      | 2325
WAR02 | Steel Guardian   | Warrior | 1500  | 250  | Armor: 200      | 2550
MAG01 | Rikkei Wizard    | Mage    | 800   | 500  | Ability: x1.5   | 1925
WAR03 | Dragon Slayer    | Warrior | 1300  | 350  | Armor: 180      | 2620
MAG02 | Frost Witch      | Mage    | 100   | 400  | Ability: x2.0   | 1300
------------------------------------------------------------------------------------------------

Chọn chức năng (1-5): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1-5!

Cảm ơn bạn đã sử dụng Rikkei RPG - Auto-Battler Manager!
```

## Ghi chú

- Đề nêu công thức **Chiến lực = Máu + (Sát thương kỹ năng × 1.5)** nhưng các con số mẫu (1650, 1950, 1800, 1830) không khớp với công thức này (VD WAR01: 1200 + (300×2 + 150) × 1.5 = 2325). Chương trình tuân theo công thức đã nêu nên chiến lực khác số mẫu.
- Dữ liệu mẫu ghi "Mana: 250" cho Mage, còn thiết kế lớp dùng `ability_power` (hệ số, VD 1.5); chương trình dùng `ability_power = 1.5` cho MAG01.
- Mã tướng được chuẩn hóa `strip().upper()`; tướng mới có chỉ số <= 0 được gán 100 và có thông báo cho người dùng.

## Cách chạy

```bash
python main.py
```
