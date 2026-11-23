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
