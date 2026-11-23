# Bài 4 - Sáng tạo: Hệ thống rèn đúc & quản lý kho vũ khí (RPG Blacksmith System)

## Đề bài

Rikkei Studios làm lại tính năng Lò Rèn (Blacksmith) cho game nhập vai. Phiên bản trước lưu vũ khí bằng Dictionary và một hàm `if/else` dài dằng dặc để tính sát thương cho từng loại vũ khí. Giám đốc kỹ thuật yêu cầu xây lại bằng OOP nâng cao: nhờ **Tính đa hình**, khi hiển thị túi đồ máy chủ chỉ cần duyệt danh sách và gọi `.calculate_total_damage()` mà không quan tâm đó là thanh kiếm sắt bình thường hay một thanh gươm phép thuật. Kho đồ người chơi: `inventory = []`.

### Mô tả cấu trúc Class & Object

| Lớp | Mô tả |
|---|---|
| `Equipment` (lớp trừu tượng) | Kế thừa `ABC`; `@abstractmethod calculate_total_damage(self)` ép mọi loại vũ khí định nghĩa công thức riêng |
| `Weapon` (vũ khí vật lý) | Kế thừa `Equipment`; `name`, `base_damage`, `upgrade_level` (mặc định 0); `calculate_total_damage()` = `base_damage + upgrade_level × 10`; `__gt__` so sánh; `__add__` dung hợp → Weapon mới (tên ghép, cộng cấp) |
| `MagicMixin` | Lớp hỗ trợ (Mixin), không dùng độc lập; `magic_power`; `cast_glow()` in thông báo vũ khí phát sáng |
| `MagicSword` (đa kế thừa) | Kế thừa `(Weapon, MagicMixin)`; `__init__` gọi khởi tạo của các lớp cha theo MRO; `calculate_total_damage()` = `base_damage + upgrade_level × 10 + magic_power` |

### Menu

```
===== LÒ RÈN VŨ KHÍ RIKKEI STUDIOS =====
1. Xem kho vũ khí & Sát thương tổng
2. Rèn Vũ khí Vật lý (Tạo Weapon)
3. Rèn Kiếm Ma Thuật (Tạo MagicSword)
4. Thẩm định vũ khí (So sánh lớn hơn)
5. Dung hợp vũ khí (Cộng dồn cấp độ)
6. Thoát game
=======================================================
Chọn chức năng (1-6):
```

| Chức năng | Yêu cầu |
|---|---|
| 1. Xem kho vũ khí | Tên, cấp cường hóa, sát thương tổng; Duck Typing: chỉ gọi `item.calculate_total_damage()`. Kho trống: "Kho vũ khí hiện đang trống. Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3." |
| 2. Rèn vũ khí vật lý | Nhập thông số, tạo `Weapon`, `.append()` vào `inventory`; giá trị <= 0 → "Giá trị phải lớn hơn 0!" |
| 3. Rèn kiếm ma thuật | Tạo `MagicSword` (VD 120 + 3 × 10 + 80 = 230) |
| 4. Thẩm định | `if inventory[0] > inventory[1]:` → gọi `__gt__`; chưa đủ 2 vũ khí → "Cần ít nhất 2 vũ khí trong kho để thẩm định!" |
| 5. Dung hợp | `new_weapon = inventory[0] + inventory[1]` → `__add__` tạo **Weapon mới** (không phải MagicSword): base cộng dồn, cấp cộng dồn; xóa 2 vũ khí cũ, thêm vũ khí mới |
| 6. Thoát | "Thoát Lò Rèn. Hẹn gặp lại Anh hùng!" |

### Edge cases

| Bẫy | Xử lý |
|---|---|
| Bẫy 1 - Instance của Abstract Class | `Equipment()` bị từ chối nhờ ABC |
| Bẫy 2 - Lỗi Type khi nạp chồng toán tử | `weapon + 10`, `weapon > 'abc'` → `isinstance` kiểm tra, báo "Chỉ có thể dung hợp/so sánh giữa các trang bị!" |
| Bẫy 3 - Khởi tạo đa kế thừa (MRO) | Mọi `__init__` nhận `**kwargs` và gọi `super().__init__(**kwargs)` → `magic_power` không bị thiếu |

## (1) Phân tích thiết kế hệ thống (System Design Document)

Tài liệu này cũng được đặt dưới dạng comment đầu file `main.py`.

**1. Abstract Base Class - vai trò của `Equipment`, `@abstractmethod` ngăn lỗi gì khi thêm lớp `Bow`?**

`Equipment` là **bản hợp đồng** cho mọi loại trang bị: định nghĩa phần dùng chung (so sánh `__gt__` / `__eq__` dựa trên sát thương tổng) và bắt buộc lớp con cài đặt `calculate_total_damage()`. Khi lập trình viên "hậu bối" thêm lớp `Bow` mà quên viết công thức sát thương, `Bow(...)` sẽ báo `TypeError` **ngay lúc tạo vũ khí** (Fail Fast), thay vì tạo thành công rồi crash khi hiển thị kho hoặc thẩm định; đồng thời không ai tạo được một "trang bị chung chung" không có công thức.

**2. Multiple Inheritance & MRO của `MagicSword`; cách viết `__init__` để cả `Weapon` và `MagicMixin` được khởi tạo.**

MRO: `MagicSword → Weapon → Equipment → ABC → MagicMixin → object`. Viết theo kiểu **cooperative inheritance**: mọi `__init__` nhận phần tham số của mình bằng tên và chuyển phần còn lại qua `**kwargs` cho `super().__init__(**kwargs)`. `MagicSword.__init__` chỉ gọi **một lần** `super().__init__(name=..., base_damage=..., upgrade_level=..., magic_power=...)`: `Weapon` lấy `name`, `base_damage`, `upgrade_level` → chuyển tiếp cho `Equipment` → `MagicMixin` lấy `magic_power` → `object`. Nếu `Weapon` không chuyển tiếp `super().__init__(**kwargs)` (hoặc gọi `Weapon.__init__(self, ...)` trực tiếp) thì `MagicMixin.__init__` bị bỏ qua và object thiếu `magic_power` (Bẫy 3, minh họa bên dưới).

**3. Polymorphism ở Chức năng 1.**

Vòng lặp in kho chỉ gọi `item.calculate_total_damage()` và `item.kind` cho mọi phần tử. Với `Weapon` công thức là `base + cấp × 10`; với `MagicSword` là bản override gọi `super().calculate_total_damage()` rồi cộng `magic_power`. Cùng một lời gọi, kết quả theo đúng loại vũ khí, không cần `if isinstance(...)`.

**4. Operator Overloading - pseudocode `__add__` của `Weapon`.**

```
__add__(self, other):          # nhận 2 tham số: self (vế trái), other (vế phải)
    NẾU other KHÔNG phải Weapon:
        raise TypeError("Chỉ có thể dung hợp/so sánh giữa các trang bị!")
    TRẢ VỀ Weapon(
        name          = "Fusion(" + self.name + " + " + other.name + ")",
        base_damage   = self.base_damage + other.base_damage,
        upgrade_level = self.upgrade_level + other.upgrade_level)
    # Kiểu trả về: object Weapon MỚI; self và other không bị thay đổi
```

Kiểm tra trực tiếp các bẫy và trường hợp ngang sức:

```
>>> Trường hợp hai vũ khí ngang sức (Chức năng 4):

--- THẨM ĐỊNH VŨ KHÍ ---
Vũ khí thứ nhất:
Iron Sword | Loại: Weapon | Sát thương: 120

Vũ khí thứ hai:
Bronze Axe | Loại: Weapon | Sát thương: 120

Kết quả: Hai vũ khí có sức mạnh ngang nhau.

>>> Bẫy 1 - Equipment():
TypeError: Can't instantiate abstract class Equipment without an implementation for abstract method 'calculate_total_damage'
>>> Bẫy 2 - weapon + 10:
TypeError: Chỉ có thể dung hợp/so sánh giữa các trang bị!
>>> Bẫy 2 - weapon > 'abc':
TypeError: Chỉ có thể dung hợp/so sánh giữa các trang bị!
>>> Bẫy 3 - MRO của MagicSword: MagicSword -> Weapon -> Equipment -> ABC -> MagicMixin -> object
    Thuộc tính: {'magic_power': 80, 'name': 'Flame Saber', 'base_damage': 120, 'upgrade_level': 3} | Sát thương tổng: 230
>>> Bẫy 3 - phiên bản lỗi: Weapon.__init__ KHÔNG gọi super().__init__(**kwargs)
    Thuộc tính: {'name': 'Broken Saber', 'base_damage': 120, 'upgrade_level': 3}
    AttributeError: 'BadMagicSword' object has no attribute 'magic_power'
```

## (2) Triển khai code

File: [`main.py`](main.py)

```python
"""
====================================================================
TÀI LIỆU THIẾT KẾ HỆ THỐNG - RPG BLACKSMITH SYSTEM (RIKKEI STUDIOS)
====================================================================
Equipment (ABC)              @abstractmethod calculate_total_damage()
   |                         __gt__ / __eq__: so sánh sát thương tổng
   |-- Weapon                name, base_damage, upgrade_level (mặc định 0)
   |      |                  total = base_damage + upgrade_level * 10
   |      |                  __add__: dung hợp -> Weapon MỚI
   |      |
MagicMixin                   magic_power, cast_glow() (Mixin - không độc lập)
   |      |
   +-- MagicSword(Weapon, MagicMixin)
                             total = base_damage + upgrade_level * 10 + magic_power

MRO MagicSword: MagicSword -> Weapon -> Equipment -> ABC -> MagicMixin -> object
Mọi __init__ đều nhận **kwargs và gọi super().__init__(**kwargs) (cooperative
inheritance) nên MagicSword chỉ gọi super() MỘT LẦN là cả Weapon và
MagicMixin đều được khởi tạo đầy đủ.
====================================================================
"""

from abc import ABC, abstractmethod

UPGRADE_DAMAGE = 10
TYPE_ERROR_MESSAGE = "Chỉ có thể dung hợp/so sánh giữa các trang bị!"
MENU_LINE = "=" * 55
TABLE_LINE = "-" * 72


class Equipment(ABC):
    """Trang bị cơ bản (lớp trừu tượng): mọi vũ khí phải có công thức sát thương."""

    def __init__(self, **kwargs):
        """Chuyển tiếp tham số còn lại cho lớp kế tiếp trong MRO."""
        super().__init__(**kwargs)

    @abstractmethod
    def calculate_total_damage(self):
        """Sát thương tổng - mỗi loại vũ khí tự định nghĩa."""

    def __gt__(self, other):
        """Toán tử >: vũ khí nào có sát thương tổng lớn hơn."""
        if not isinstance(other, Equipment):
            raise TypeError(TYPE_ERROR_MESSAGE)
        return self.calculate_total_damage() > other.calculate_total_damage()

    def __eq__(self, other):
        """Toán tử ==: hai trang bị có sát thương tổng bằng nhau."""
        if not isinstance(other, Equipment):
            return NotImplemented
        return self.calculate_total_damage() == other.calculate_total_damage()


class Weapon(Equipment):
    """Vũ khí vật lý."""

    def __init__(self, name, base_damage, upgrade_level=0, **kwargs):
        """Khởi tạo tên, sát thương gốc, cấp cường hóa."""
        super().__init__(**kwargs)
        self.name = name
        self.base_damage = base_damage
        self.upgrade_level = upgrade_level

    @property
    def kind(self):
        """Tên loại vũ khí (chính là tên class)."""
        return type(self).__name__

    def calculate_total_damage(self):
        """Sát thương tổng = base_damage + upgrade_level * 10."""
        return self.base_damage + self.upgrade_level * UPGRADE_DAMAGE

    def __add__(self, other):
        """Dung hợp: trả về Weapon MỚI, cộng sát thương gốc và cấp của cả hai."""
        if not isinstance(other, Weapon):
            raise TypeError(TYPE_ERROR_MESSAGE)
        return Weapon(name=f"Fusion({self.name} + {other.name})",
                      base_damage=self.base_damage + other.base_damage,
                      upgrade_level=self.upgrade_level + other.upgrade_level)


class MagicMixin:
    """Mixin hỗ trợ thuộc tính phép thuật (không dùng độc lập)."""

    def __init__(self, magic_power=0, **kwargs):
        """Khởi tạo sức mạnh phép thuật và chuyển tiếp phần còn lại."""
        super().__init__(**kwargs)
        self.magic_power = magic_power

    def cast_glow(self):
        """Thông báo vũ khí phát sáng."""
        name = getattr(self, "name", "Vũ khí")
        return f"✨ {name} phát sáng với {self.magic_power} sức mạnh phép thuật!"


class MagicSword(Weapon, MagicMixin):
    """Kiếm ma thuật - đa kế thừa Weapon và MagicMixin."""

    def __init__(self, name, base_damage, upgrade_level, magic_power):
        """Một lần super() đi qua toàn bộ MRO: Weapon -> ... -> MagicMixin."""
        super().__init__(name=name, base_damage=base_damage,
                         upgrade_level=upgrade_level, magic_power=magic_power)

    def calculate_total_damage(self):
        """Sát thương tổng = sát thương vật lý (Weapon) + magic_power."""
        return super().calculate_total_damage() + self.magic_power


# =====================================================================
# HÀM GIAO DIỆN
# =====================================================================
def input_positive_int(prompt):
    """Nhập số nguyên > 0; trả về None nếu sai (kèm thông báo)."""
    text = input(prompt).strip()
    try:
        value = int(text)
    except ValueError:
        value = 0
    if value <= 0:
        print("\nGiá trị phải lớn hơn 0!")
        return None
    return value


def describe(weapon):
    """Một dòng mô tả ngắn: tên | loại | sát thương tổng."""
    return (f"{weapon.name} | Loại: {weapon.kind} | Sát thương: "
            f"{weapon.calculate_total_damage()}")


def show_inventory(inventory):
    """Chức năng 1: duyệt kho, Duck Typing gọi calculate_total_damage()."""
    print("\n--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---")
    if not inventory:
        print("Kho vũ khí hiện đang trống.")
        print("Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3.")
        return
    print(f"{'STT':<4}| {'Tên vũ khí':<34}| {'Loại':<11}| {'Cấp':<4}| Sát thương tổng")
    print(TABLE_LINE)
    for index, item in enumerate(inventory, start=1):
        print(f"{index:<4}| {item.name:<34}| {item.kind:<11}| {item.upgrade_level:<4}| "
              f"{item.calculate_total_damage()}")


def forge_weapon(inventory):
    """Chức năng 2: rèn Weapon."""
    print("\n--- RÈN VŨ KHÍ VẬT LÝ ---")
    name = " ".join(input("Nhập tên vũ khí: ").split()).title()
    base_damage = input_positive_int("Nhập sát thương gốc: ")
    if base_damage is None:
        return
    upgrade_level = input_positive_int("Nhập cấp cường hóa: ")
    if upgrade_level is None:
        return
    weapon = Weapon(name, base_damage, upgrade_level)
    inventory.append(weapon)
    print("\n>> Rèn vũ khí vật lý thành công!")
    print(f"Tên vũ khí: {weapon.name}")
    print(f"Loại: {weapon.kind}")
    print(f"Cấp cường hóa: {weapon.upgrade_level}")
    print(f"Sát thương tổng: {weapon.calculate_total_damage()}")


def forge_magic_sword(inventory):
    """Chức năng 3: rèn MagicSword."""
    print("\n--- RÈN KIẾM MA THUẬT ---")
    name = " ".join(input("Nhập tên kiếm ma thuật: ").split()).title()
    values = []
    for prompt in ("Nhập sát thương gốc: ", "Nhập cấp cường hóa: ",
                   "Nhập sức mạnh phép thuật: "):
        value = input_positive_int(prompt)
        if value is None:
            return
        values.append(value)
    sword = MagicSword(name, *values)
    inventory.append(sword)
    print("\n>> Rèn kiếm ma thuật thành công!")
    print(f"Tên vũ khí: {sword.name}")
    print(f"Loại: {sword.kind}")
    print(f"Cấp cường hóa: {sword.upgrade_level}")
    print(f"Sát thương gốc: {sword.base_damage}")
    print(f"Sức mạnh phép thuật: {sword.magic_power}")
    print(f"Sát thương tổng: {sword.calculate_total_damage()}")
    print(sword.cast_glow())


def appraise(inventory):
    """Chức năng 4: so sánh 2 vũ khí đầu kho bằng toán tử > (gọi __gt__)."""
    print("\n--- THẨM ĐỊNH VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để thẩm định!")
        return
    first, second = inventory[0], inventory[1]
    print("Vũ khí thứ nhất:")
    print(describe(first))
    print("\nVũ khí thứ hai:")
    print(describe(second))
    if first > second:
        print(f"\nKết quả: {first.name} mạnh hơn {second.name}.")
    elif second > first:
        print(f"\nKết quả: {second.name} mạnh hơn {first.name}.")
    else:
        print("\nKết quả: Hai vũ khí có sức mạnh ngang nhau.")


def fuse(inventory):
    """Chức năng 5: dung hợp 2 vũ khí đầu kho bằng toán tử + (gọi __add__)."""
    print("\n--- DUNG HỢP VŨ KHÍ ---")
    if len(inventory) < 2:
        print("Cần ít nhất 2 vũ khí trong kho để dung hợp!")
        return
    print("Đang dung hợp 2 vũ khí đầu tiên trong kho...\n")
    first, second = inventory[0], inventory[1]
    for index, item in enumerate((first, second), start=1):
        print(f"Vũ khí {index}: {item.name} | Cấp: {item.upgrade_level} | "
              f"Sát thương gốc: {item.base_damage}")
    new_weapon = first + second
    del inventory[:2]
    inventory.append(new_weapon)
    print("\n>> Dung hợp vũ khí thành công!")
    print(f"Đã xóa khỏi kho: {first.name}")
    print(f"Đã xóa khỏi kho: {second.name}")
    print(f"\nVũ khí mới: {new_weapon.name}")
    print(f"Loại: {new_weapon.kind}")
    print(f"Cấp cường hóa: {new_weapon.upgrade_level}")
    print(f"Sát thương tổng: {new_weapon.calculate_total_damage()}")


def display_menu():
    """In menu chính."""
    print("\n===== LÒ RÈN VŨ KHÍ RIKKEI STUDIOS =====")
    print("1. Xem kho vũ khí & Sát thương tổng")
    print("2. Rèn Vũ khí Vật lý (Tạo Weapon)")
    print("3. Rèn Kiếm Ma Thuật (Tạo MagicSword)")
    print("4. Thẩm định vũ khí (So sánh lớn hơn)")
    print("5. Dung hợp vũ khí (Cộng dồn cấp độ)")
    print("6. Thoát game")
    print(MENU_LINE)


def main():
    """Vòng lặp while điều hướng; kho ban đầu rỗng."""
    inventory = []
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-6): ").strip()
        if choice == "1":
            show_inventory(inventory)
        elif choice == "2":
            forge_weapon(inventory)
        elif choice == "3":
            forge_magic_sword(inventory)
        elif choice == "4":
            appraise(inventory)
        elif choice == "5":
            fuse(inventory)
        elif choice == "6":
            print("Thoát Lò Rèn. Hẹn gặp lại Anh hùng!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-6!")


if __name__ == "__main__":
    main()
```

## Kết quả chạy thử

Kịch bản: xem kho trống → thẩm định / dung hợp khi chưa đủ 2 vũ khí → rèn Weapon (sát thương âm, cấp 0, rồi hợp lệ: 120) → rèn MagicSword (phép âm, rồi hợp lệ: 230) → xem kho → thẩm định → dung hợp (Fusion: cấp 5, 270) → rèn thêm Bronze Axe, Thunder Blade (420) → thẩm định → menu sai → thoát. Khung menu lặp lại được ẩn.

```
Chọn chức năng (1-6): 1

--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---
Kho vũ khí hiện đang trống.
Vui lòng rèn vũ khí bằng Chức năng 2 hoặc Chức năng 3.

Chọn chức năng (1-6): 4

--- THẨM ĐỊNH VŨ KHÍ ---
Cần ít nhất 2 vũ khí trong kho để thẩm định!

Chọn chức năng (1-6): 5

--- DUNG HỢP VŨ KHÍ ---
Cần ít nhất 2 vũ khí trong kho để dung hợp!

Chọn chức năng (1-6): 2

--- RÈN VŨ KHÍ VẬT LÝ ---
Nhập tên vũ khí: iron sword
Nhập sát thương gốc: -100

Giá trị phải lớn hơn 0!

Chọn chức năng (1-6): 2

--- RÈN VŨ KHÍ VẬT LÝ ---
Nhập tên vũ khí: Iron Sword
Nhập sát thương gốc: 100
Nhập cấp cường hóa: 0

Giá trị phải lớn hơn 0!

Chọn chức năng (1-6): 2

--- RÈN VŨ KHÍ VẬT LÝ ---
Nhập tên vũ khí: iron sword
Nhập sát thương gốc: 100
Nhập cấp cường hóa: 2

>> Rèn vũ khí vật lý thành công!
Tên vũ khí: Iron Sword
Loại: Weapon
Cấp cường hóa: 2
Sát thương tổng: 120

Chọn chức năng (1-6): 3

--- RÈN KIẾM MA THUẬT ---
Nhập tên kiếm ma thuật: flame saber
Nhập sát thương gốc: 120
Nhập cấp cường hóa: 3
Nhập sức mạnh phép thuật: -80

Giá trị phải lớn hơn 0!

Chọn chức năng (1-6): 3

--- RÈN KIẾM MA THUẬT ---
Nhập tên kiếm ma thuật: flame saber
Nhập sát thương gốc: 120
Nhập cấp cường hóa: 3
Nhập sức mạnh phép thuật: 80

>> Rèn kiếm ma thuật thành công!
Tên vũ khí: Flame Saber
Loại: MagicSword
Cấp cường hóa: 3
Sát thương gốc: 120
Sức mạnh phép thuật: 80
Sát thương tổng: 230
✨ Flame Saber phát sáng với 80 sức mạnh phép thuật!

Chọn chức năng (1-6): 1

--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---
STT | Tên vũ khí                        | Loại       | Cấp | Sát thương tổng
------------------------------------------------------------------------
1   | Iron Sword                        | Weapon     | 2   | 120
2   | Flame Saber                       | MagicSword | 3   | 230

Chọn chức năng (1-6): 4

--- THẨM ĐỊNH VŨ KHÍ ---
Vũ khí thứ nhất:
Iron Sword | Loại: Weapon | Sát thương: 120

Vũ khí thứ hai:
Flame Saber | Loại: MagicSword | Sát thương: 230

Kết quả: Flame Saber mạnh hơn Iron Sword.

Chọn chức năng (1-6): 5

--- DUNG HỢP VŨ KHÍ ---
Đang dung hợp 2 vũ khí đầu tiên trong kho...

Vũ khí 1: Iron Sword | Cấp: 2 | Sát thương gốc: 100
Vũ khí 2: Flame Saber | Cấp: 3 | Sát thương gốc: 120

>> Dung hợp vũ khí thành công!
Đã xóa khỏi kho: Iron Sword
Đã xóa khỏi kho: Flame Saber

Vũ khí mới: Fusion(Iron Sword + Flame Saber)
Loại: Weapon
Cấp cường hóa: 5
Sát thương tổng: 270

Chọn chức năng (1-6): 1

--- KHO VŨ KHÍ CỦA NGƯỜI CHƠI ---
STT | Tên vũ khí                        | Loại       | Cấp | Sát thương tổng
------------------------------------------------------------------------
1   | Fusion(Iron Sword + Flame Saber)  | Weapon     | 5   | 270

Chọn chức năng (1-6): 2

--- RÈN VŨ KHÍ VẬT LÝ ---
Nhập tên vũ khí: bronze axe
Nhập sát thương gốc: 100
Nhập cấp cường hóa: 2

>> Rèn vũ khí vật lý thành công!
Tên vũ khí: Bronze Axe
Loại: Weapon
Cấp cường hóa: 2
Sát thương tổng: 120

Chọn chức năng (1-6): 3

--- RÈN KIẾM MA THUẬT ---
Nhập tên kiếm ma thuật: thunder blade
Nhập sát thương gốc: 300
Nhập cấp cường hóa: 5
Nhập sức mạnh phép thuật: 70

>> Rèn kiếm ma thuật thành công!
Tên vũ khí: Thunder Blade
Loại: MagicSword
Cấp cường hóa: 5
Sát thương gốc: 300
Sức mạnh phép thuật: 70
Sát thương tổng: 420
✨ Thunder Blade phát sáng với 70 sức mạnh phép thuật!

Chọn chức năng (1-6): 4

--- THẨM ĐỊNH VŨ KHÍ ---
Vũ khí thứ nhất:
Fusion(Iron Sword + Flame Saber) | Loại: Weapon | Sát thương: 270

Vũ khí thứ hai:
Bronze Axe | Loại: Weapon | Sát thương: 120

Kết quả: Fusion(Iron Sword + Flame Saber) mạnh hơn Bronze Axe.

Chọn chức năng (1-6): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1-6!

Thoát Lò Rèn. Hẹn gặp lại Anh hùng!
```

## Ghi chú

- Cấp cường hóa nhập từ menu phải > 0 (theo ví dụ "Nhập cấp cường hóa bằng 0" của đề); class `Weapon` vẫn cho mặc định `upgrade_level = 0`.
- `__add__` kiểm tra `isinstance(other, Weapon)` vì dung hợp cần `base_damage` / `upgrade_level` (mọi trang bị hiện có đều là Weapon); `__gt__` kiểm tra `isinstance(other, Equipment)` theo đúng đề.
- Ở Chức năng 5, mỗi vũ khí hiển thị **sát thương gốc** (đúng giá trị được cộng dồn) để công thức 100 + 120 = 220, 220 + 5 × 10 = 270 dễ đối chiếu.

## Cách chạy

```bash
python main.py
```
