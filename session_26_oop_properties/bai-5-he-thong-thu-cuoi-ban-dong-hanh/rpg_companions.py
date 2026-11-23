"""Hệ thống Bạn đồng hành (Companion System) - Rikkei RPG.

Sơ đồ lớp:
    Companion (ABC)          name, level = 1; @abstractmethod unleash_skill()
       |                     __add__: lai tạo 2 sinh vật CÙNG LOÀI
       |-- Pet               + bonus_atk   (Thú cưng - hỗ trợ chiến đấu)
       |-- Mount             + bonus_speed (Thú cưỡi - hỗ trợ di chuyển)
       +-- Dragon(Pet, Mount)  có cả bonus_atk và bonus_speed

MRO Dragon: Dragon -> Pet -> Mount -> Companion -> ABC -> object.
Mọi __init__ nhận **kwargs và gọi super().__init__(**kwargs) nên khởi tạo
Dragon đi qua đủ Pet, Mount, Companion đúng một lần.

Chạy:
    python rpg_companions.py          # chạy kịch bản kiểm thử bắt buộc
    python rpg_companions.py --menu   # chạy menu tương tác
"""

import sys
from abc import ABC, abstractmethod

MENU_LINE = "=" * 46


class Companion(ABC):
    """Khuôn mẫu chung của mọi sinh vật đồng hành (không khởi tạo trực tiếp)."""

    kind = "Companion"
    battle_cry = "ra đòn"

    def __init__(self, name, level=1, **kwargs):
        """Khởi tạo tên, cấp độ (mặc định 1) và chuyển tiếp kwargs theo MRO."""
        super().__init__(**kwargs)
        self.name = name
        self.level = level

    @abstractmethod
    def unleash_skill(self):
        """Kỹ năng đặc trưng - trả về mô tả hiệu ứng (mỗi dòng một hiệu ứng)."""

    def combined_stats(self, other):
        """Chỉ số của con lai (lớp con cộng thêm phần của mình qua super())."""
        return {}

    def stats_text(self):
        """Chuỗi hiển thị chỉ số (lớp con bổ sung)."""
        return ""

    def __add__(self, other):
        """Lai tạo: chỉ khi CÙNG LOÀI; trả về sinh vật mới."""
        if type(self) is not type(other):
            raise TypeError("Chỉ có thể lai tạo 2 sinh vật cùng loài!")
        return type(self)(name=f"{self.name} {other.name}",
                          level=max(self.level, other.level) + 1,
                          **self.combined_stats(other))

    def __str__(self):
        """[Loại] Tên | Cấp | chỉ số."""
        return f"[{self.kind}] {self.name} | Cấp: {self.level} | {self.stats_text()}"


class Pet(Companion):
    """Thú cưng: tăng sát thương."""

    kind = "Pet"
    battle_cry = "gầm gừ"

    def __init__(self, name, bonus_atk=0, **kwargs):
        """Khởi tạo bonus_atk, phần còn lại chuyển cho lớp kế tiếp trong MRO."""
        super().__init__(name=name, **kwargs)
        self.bonus_atk = bonus_atk

    def unleash_skill(self):
        """Tấn công kẻ thù."""
        return f"Tấn công kẻ thù, gây {self.bonus_atk} sát thương!"

    def combined_stats(self, other):
        """Cộng dồn bonus_atk."""
        stats = super().combined_stats(other)
        stats["bonus_atk"] = self.bonus_atk + other.bonus_atk
        return stats

    def stats_text(self):
        """Atk: +X."""
        return " | ".join(filter(None, [f"Atk: +{self.bonus_atk}", super().stats_text()]))


class Mount(Companion):
    """Thú cưỡi: tăng tốc độ di chuyển."""

    kind = "Mount"
    battle_cry = "hí vang"

    def __init__(self, name, bonus_speed=0, **kwargs):
        """Khởi tạo bonus_speed, phần còn lại chuyển cho lớp kế tiếp trong MRO."""
        super().__init__(name=name, **kwargs)
        self.bonus_speed = bonus_speed

    def unleash_skill(self):
        """Tăng tốc độ."""
        return f"Tăng tốc độ di chuyển thêm {self.bonus_speed} điểm!"

    def combined_stats(self, other):
        """Cộng dồn bonus_speed."""
        stats = super().combined_stats(other)
        stats["bonus_speed"] = self.bonus_speed + other.bonus_speed
        return stats

    def stats_text(self):
        """Speed: +X."""
        return " | ".join(filter(None, [f"Speed: +{self.bonus_speed}", super().stats_text()]))


class Dragon(Pet, Mount):
    """Rồng thần: vừa là thú cưng vừa là thú cưỡi (đa kế thừa)."""

    kind = "Dragon"
    battle_cry = "thị uy"

    def __init__(self, name, bonus_atk=0, bonus_speed=0, **kwargs):
        """Một lần super() khởi tạo cả Pet, Mount và Companion theo MRO."""
        super().__init__(name=name, bonus_atk=bonus_atk, bonus_speed=bonus_speed,
                         **kwargs)

    def unleash_skill(self):
        """Triển khai CẢ kỹ năng của Pet và Mount thông qua super()."""
        pet_skill = super().unleash_skill()               # Pet (kế tiếp trong MRO)
        mount_skill = super(Pet, self).unleash_skill()    # Mount (sau Pet trong MRO)
        return f"{pet_skill}\n{mount_skill}"


# =====================================================================
# HÀM DÙNG CHUNG
# =====================================================================
def battle(active_companions):
    """Đa hình: gọi unleash_skill() của mọi sinh vật như nhau."""
    for companion in active_companions:
        effects = companion.unleash_skill().split("\n")
        if len(effects) == 1:
            print(f">> {companion.name} {companion.battle_cry}: {effects[0]}")
        else:
            print(f">> {companion.name} {companion.battle_cry}:")
            for effect in effects:
                print(f"   - {effect}")


def show_team(active_companions):
    """Chức năng 1: xem đội hình."""
    if not active_companions:
        print("Đội hình đang trống. Hãy triệu hồi sinh vật (Chức năng 2, 3).")
        return
    for index, companion in enumerate(active_companions, start=1):
        print(f"{index}. {companion}")


# =====================================================================
# KỊCH BẢN KIỂM THỬ BẮT BUỘC
# =====================================================================
def run_test_scenarios():
    """Chạy 6 kịch bản theo đề bài."""
    print("1. Thử khởi tạo Companion('Test'):")
    try:
        Companion("Test")
    except TypeError as error:
        print(f"   TypeError: {error}")

    print("\n2. Tạo p1 = Pet('Sói Trắng', bonus_atk=50), p2 = Pet('Sói Đen', bonus_atk=60)")
    p1 = Pet("Sói Trắng", bonus_atk=50)
    p2 = Pet("Sói Đen", bonus_atk=60)
    print(f"   p1: {p1}\n   p2: {p2}")

    print("\n3. Lai tạo p3 = p1 + p2:")
    p3 = p1 + p2
    print(f"   p3: {p3}")
    print(f"   Tên: {p3.name!r}, level: {p3.level}, atk: {p3.bonus_atk}")

    print("\n4. Test Bẫy 2: m1 = Mount('Ngựa', bonus_speed=10), thử p1 + m1 và p1 + 10")
    m1 = Mount("Ngựa", bonus_speed=10)
    for label, operation in (("p1 + m1", lambda: p1 + m1), ("p1 + 10", lambda: p1 + 10)):
        try:
            operation()
        except TypeError as error:
            print(f"   {label} -> TypeError: {error}")

    print("\n5. Tạo d1 = Dragon('Rồng Lửa', bonus_atk=500, bonus_speed=200):")
    d1 = Dragon("Rồng Lửa", bonus_atk=500, bonus_speed=200)
    print(f"   d1: {d1}")
    print(f"   bonus_atk = {d1.bonus_atk}, bonus_speed = {d1.bonus_speed}")
    print(f"   MRO: {' -> '.join(cls.__name__ for cls in Dragon.__mro__)}")

    print("\n6. Đa hình: equipped = [p3, m1, d1]")
    equipped = [p3, m1, d1]
    battle(equipped)


# =====================================================================
# MENU TƯƠNG TÁC
# =====================================================================
def input_int(prompt):
    """Nhập số nguyên >= 0 (lặp lại nếu sai)."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("Vui lòng nhập số nguyên!")
            continue
        if value >= 0:
            return value
        print("Chỉ số không được âm!")


def summon_pet(active_companions):
    """Chức năng 2: triệu hồi Thú cưng."""
    name = " ".join(input("Nhập tên thú cưng: ").split())
    pet = Pet(name, bonus_atk=input_int("Nhập bonus_atk: "))
    active_companions.append(pet)
    print(f">> Triệu hồi thành công: {pet}")


def summon_mount_or_dragon(active_companions):
    """Chức năng 3: triệu hồi Thú cưỡi hoặc Rồng thần."""
    kind = input("Loại (1 - Mount, 2 - Dragon): ").strip()
    if kind not in ("1", "2"):
        print("Loại không hợp lệ!")
        return
    name = " ".join(input("Nhập tên: ").split())
    if kind == "1":
        creature = Mount(name, bonus_speed=input_int("Nhập bonus_speed: "))
    else:
        creature = Dragon(name, bonus_atk=input_int("Nhập bonus_atk: "),
                          bonus_speed=input_int("Nhập bonus_speed: "))
    active_companions.append(creature)
    print(f">> Triệu hồi thành công: {creature}")


def breed(active_companions):
    """Chức năng 4: lai tạo bằng toán tử +."""
    show_team(active_companions)
    if len(active_companions) < 2:
        print("Cần ít nhất 2 sinh vật để lai tạo!")
        return
    picks = []
    for order in (1, 2):
        index = input_int(f"Chọn sinh vật {order}: ")
        if not 1 <= index <= len(active_companions):
            print("Số thứ tự không hợp lệ!")
            return
        picks.append(active_companions[index - 1])
    try:
        child = picks[0] + picks[1]
    except TypeError as error:
        print(f"Lỗi: {error}")
        return
    active_companions.append(child)
    print(f">> Lai tạo thành công! Nhận được: {child}")


def run_menu():
    """Menu tương tác."""
    active_companions = [Pet("Sói Trắng", bonus_atk=50), Mount("Hắc Mã", bonus_speed=20)]
    while True:
        print("\n===== HỆ THỐNG BẠN ĐỒNG HÀNH - RIKKEI RPG =====")
        print("1. Xem đội hình sinh vật")
        print("2. Triệu hồi Thú cưng (Pet)")
        print("3. Triệu hồi Thú cưỡi / Rồng thần")
        print("4. Lai tạo sinh vật")
        print("5. Xuất chiến")
        print("6. Thoát")
        print(MENU_LINE)
        choice = input("Chọn chức năng (1-6): ").strip()
        if choice == "1":
            show_team(active_companions)
        elif choice == "2":
            summon_pet(active_companions)
        elif choice == "3":
            summon_mount_or_dragon(active_companions)
        elif choice == "4":
            breed(active_companions)
        elif choice == "5":
            print("Lặp qua mảng active_companions, gọi unleash_skill() của từng object:")
            battle(active_companions)
        elif choice == "6":
            print("Hẹn gặp lại trong Rikkei RPG!")
            break
        else:
            print("Lựa chọn không hợp lệ, vui lòng chọn từ 1-6!")


if __name__ == "__main__":
    if "--menu" in sys.argv:
        run_menu()
    else:
        run_test_scenarios()
