# Bài 5 - Vận dụng chuyên sâu: Hệ thống thú cưỡi & bạn đồng hành (Companion System)

## Đề bài

Giám đốc Sản phẩm game "Rikkei RPG" muốn ra mắt "Hệ thống Bạn đồng hành": người chơi mang theo Thú cưng (Pet - hỗ trợ chiến đấu) và Thú cưỡi (Mount - hỗ trợ di chuyển); đặc biệt có thể thu thập "Rồng Thần" vừa để cưỡi vừa chiến đấu. Code rời rạc từng con vật sẽ trùng lặp logic, khó quản lý kỹ năng, và tính năng "Lai tạo thú" (ghép 2 con vật lại) liên tục gây sập server vì người chơi cố tình lai tạo một con Ngựa với một... thanh kiếm. Nhiệm vụ: thiết kế kiến trúc OOP chuẩn mực.

| Thành phần | Yêu cầu |
|---|---|
| Khuôn mẫu chung (ABC) | `Companion` trừu tượng: `name`, `level` mặc định 1, ép mọi sinh vật phải có `unleash_skill()` |
| Kế thừa | `Pet` + `bonus_atk`: "Tấn công kẻ thù, gây [X] sát thương!"; `Mount` + `bonus_speed`: "Tăng tốc độ di chuyển thêm [X] điểm!" |
| Đa kế thừa (MRO) | `Dragon` kế thừa cả `Pet` và `Mount`; kích hoạt kỹ năng triển khai CẢ hai kỹ năng |
| Lai tạo (Operator Overloading) | `+` để lai tạo 2 sinh vật CÙNG LOẠI: tên mới ghép lại, cấp độ tăng thêm 1, chỉ số (atk / speed) cộng dồn |
| Đa hình | `active_companions = []`; khi "Chiến đấu" lặp qua mảng và gọi `unleash_skill()` một cách đồng nhất |

### Bẫy dữ liệu

| Bẫy | Xử lý |
|---|---|
| Bẫy 1 - Bảo vệ kiến trúc (ABC Trap) | `Companion("Lỗi")` bị chặn ở cấp độ ngôn ngữ lập trình (`TypeError`) |
| Bẫy 2 - Đi giáo lai tạo (Operator Trap) | `Pet + Mount` hoặc `Pet + 100` → `TypeError: "Chỉ có thể lai tạo 2 sinh vật cùng loài!"` |
| Bẫy 3 - Nút thắt MRO (Init Trap) | `Dragon` khởi tạo bằng `super()` + `**kwargs` đi qua toàn bộ MRO nên có đủ `bonus_atk` và `bonus_speed` |

## (1) Báo cáo phân tích và thiết kế giải pháp

### Phân tích bài toán (I/O)

- **Input:** thông tin khởi tạo `name` (chuỗi), `bonus_atk` (số), `bonus_speed` (số); hành động lệnh `+` giữa object 1 và object 2.
- **Output:** object sinh vật mới (khi lai tạo thành công); thông báo console khi tung chiêu thức; lỗi văng ra nếu dính Bẫy 1, Bẫy 2.

### Đề xuất giải pháp (Architecture & Logic)

| Vấn đề | Giải pháp |
|---|---|
| Bẫy 1 | `Companion(ABC)` + `@abstractmethod unleash_skill` → không tạo được object khuôn mẫu, lớp con buộc phải có kỹ năng |
| Bẫy 2 | `Companion.__add__` kiểm tra `type(self) is type(other)` (đúng loài, không chỉ "cùng họ": `Pet + Dragon` cũng bị chặn), sai thì `raise TypeError` |
| Bẫy 3 | Mọi `__init__` nhận tham số riêng và chuyển `**kwargs` cho `super().__init__(**kwargs)`; MRO `Dragon → Pet → Mount → Companion → ABC → object` nên mỗi lớp được khởi tạo đúng một lần |
| Cộng chỉ số khi lai | `combined_stats(other)` hợp tác qua `super()`: `Pet` thêm `bonus_atk`, `Mount` thêm `bonus_speed`; `Dragon` tự động có cả hai theo MRO |
| Kỹ năng Dragon | `super().unleash_skill()` (Pet - lớp kế tiếp trong MRO) + `super(Pet, self).unleash_skill()` (Mount - lớp sau Pet) |
| Đa hình khi xuất chiến | `battle()` gọi `unleash_skill()` của mọi object; mỗi lớp có `battle_cry` riêng (gầm gừ / hí vang / thị uy) |

### Các bước thực hiện

1. Khởi tạo module, import `ABC` và `abstractmethod`.
2. Định nghĩa `Companion(ABC)`: `__init__`, `__add__` (có kiểm tra loài), `@abstractmethod unleash_skill()`.
3. Định nghĩa `Pet` và `Mount` kế thừa `Companion`; ghi đè `__init__` (gọi `super()`) và `unleash_skill`.
4. Định nghĩa `Dragon(Pet, Mount)`: `__init__` xử lý cả 2 tham số qua `super()`; ghi đè `unleash_skill` dùng `super()` gọi chiêu của các lớp cha.
5. Khối `if __name__ == "__main__":` chạy các kịch bản test.

Lai tạo: tên = `tên 1 + " " + tên 2`; cấp = `max(cấp 1, cấp 2) + 1`; chỉ số = tổng chỉ số 2 con.

## (2) Triển khai và chống lỗi (Source Code)

File: [`rpg_companions.py`](rpg_companions.py)

```python
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
```

## Kết quả chạy kịch bản bắt buộc

```
$ python rpg_companions.py
1. Thử khởi tạo Companion('Test'):
   TypeError: Can't instantiate abstract class Companion without an implementation for abstract method 'unleash_skill'

2. Tạo p1 = Pet('Sói Trắng', bonus_atk=50), p2 = Pet('Sói Đen', bonus_atk=60)
   p1: [Pet] Sói Trắng | Cấp: 1 | Atk: +50
   p2: [Pet] Sói Đen | Cấp: 1 | Atk: +60

3. Lai tạo p3 = p1 + p2:
   p3: [Pet] Sói Trắng Sói Đen | Cấp: 2 | Atk: +110
   Tên: 'Sói Trắng Sói Đen', level: 2, atk: 110

4. Test Bẫy 2: m1 = Mount('Ngựa', bonus_speed=10), thử p1 + m1 và p1 + 10
   p1 + m1 -> TypeError: Chỉ có thể lai tạo 2 sinh vật cùng loài!
   p1 + 10 -> TypeError: Chỉ có thể lai tạo 2 sinh vật cùng loài!

5. Tạo d1 = Dragon('Rồng Lửa', bonus_atk=500, bonus_speed=200):
   d1: [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
   bonus_atk = 500, bonus_speed = 200
   MRO: Dragon -> Pet -> Mount -> Companion -> ABC -> object

6. Đa hình: equipped = [p3, m1, d1]
>> Sói Trắng Sói Đen gầm gừ: Tấn công kẻ thù, gây 110 sát thương!
>> Ngựa hí vang: Tăng tốc độ di chuyển thêm 10 điểm!
>> Rồng Lửa thị uy:
   - Tấn công kẻ thù, gây 500 sát thương!
   - Tăng tốc độ di chuyển thêm 200 điểm!
```

Kiểm tra thêm (lai Rồng với Rồng, Pet với Dragon):

```
>>> d1 + d2 (Rồng lai Rồng - combined_stats đi qua cả Pet và Mount theo MRO):
    [Dragon] Rồng Lửa Rồng Băng | Cấp: 3 | Atk: +800 | Speed: +350
>>> Pet + Dragon (Dragon là lớp con của Pet nhưng KHÁC LOÀI):
    TypeError: Chỉ có thể lai tạo 2 sinh vật cùng loài!
```

## Kết quả chạy menu tương tác

`python rpg_companions.py --menu`: đội hình mặc định Sói Trắng (Pet) và Hắc Mã (Mount); triệu hồi Sói Đen, Rồng Lửa, Ngựa Ô (nhập chỉ số âm bị từ chối) → lai Sói Trắng + Sói Đen → lai Pet + Mount (bị chặn) → chọn sai số thứ tự → xuất chiến → thoát. Khung menu lặp lại được ẩn.

```
Chọn chức năng (1-6): 1
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20

Chọn chức năng (1-6): 2
Nhập tên thú cưng: Sói Đen
Nhập bonus_atk: 60
>> Triệu hồi thành công: [Pet] Sói Đen | Cấp: 1 | Atk: +60

Chọn chức năng (1-6): 3
Loại (1 - Mount, 2 - Dragon): 2
Nhập tên: Rồng Lửa
Nhập bonus_atk: 500
Nhập bonus_speed: 200
>> Triệu hồi thành công: [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200

Chọn chức năng (1-6): 3
Loại (1 - Mount, 2 - Dragon): 1
Nhập tên: Ngựa Ô
Nhập bonus_speed: -5
Chỉ số không được âm!
Nhập bonus_speed: 15
>> Triệu hồi thành công: [Mount] Ngựa Ô | Cấp: 1 | Speed: +15

Chọn chức năng (1-6): 1
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20
3. [Pet] Sói Đen | Cấp: 1 | Atk: +60
4. [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
5. [Mount] Ngựa Ô | Cấp: 1 | Speed: +15

Chọn chức năng (1-6): 4
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20
3. [Pet] Sói Đen | Cấp: 1 | Atk: +60
4. [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
5. [Mount] Ngựa Ô | Cấp: 1 | Speed: +15
Chọn sinh vật 1: 1
Chọn sinh vật 2: 3
>> Lai tạo thành công! Nhận được: [Pet] Sói Trắng Sói Đen | Cấp: 2 | Atk: +110

Chọn chức năng (1-6): 4
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20
3. [Pet] Sói Đen | Cấp: 1 | Atk: +60
4. [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
5. [Mount] Ngựa Ô | Cấp: 1 | Speed: +15
6. [Pet] Sói Trắng Sói Đen | Cấp: 2 | Atk: +110
Chọn sinh vật 1: 1
Chọn sinh vật 2: 2
Lỗi: Chỉ có thể lai tạo 2 sinh vật cùng loài!

Chọn chức năng (1-6): 4
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20
3. [Pet] Sói Đen | Cấp: 1 | Atk: +60
4. [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
5. [Mount] Ngựa Ô | Cấp: 1 | Speed: +15
6. [Pet] Sói Trắng Sói Đen | Cấp: 2 | Atk: +110
Chọn sinh vật 1: 2
Chọn sinh vật 2: 6
Lỗi: Chỉ có thể lai tạo 2 sinh vật cùng loài!

Chọn chức năng (1-6): 4
1. [Pet] Sói Trắng | Cấp: 1 | Atk: +50
2. [Mount] Hắc Mã | Cấp: 1 | Speed: +20
3. [Pet] Sói Đen | Cấp: 1 | Atk: +60
4. [Dragon] Rồng Lửa | Cấp: 1 | Atk: +500 | Speed: +200
5. [Mount] Ngựa Ô | Cấp: 1 | Speed: +15
6. [Pet] Sói Trắng Sói Đen | Cấp: 2 | Atk: +110
Chọn sinh vật 1: 7
Số thứ tự không hợp lệ!

Chọn chức năng (1-6): 9
Lựa chọn không hợp lệ, vui lòng chọn từ 1-6!

Chọn chức năng (1-6): 5
Lặp qua mảng active_companions, gọi unleash_skill() của từng object:
>> Sói Trắng gầm gừ: Tấn công kẻ thù, gây 50 sát thương!
>> Hắc Mã hí vang: Tăng tốc độ di chuyển thêm 20 điểm!
>> Sói Đen gầm gừ: Tấn công kẻ thù, gây 60 sát thương!
>> Rồng Lửa thị uy:
   - Tấn công kẻ thù, gây 500 sát thương!
   - Tăng tốc độ di chuyển thêm 200 điểm!
>> Ngựa Ô hí vang: Tăng tốc độ di chuyển thêm 15 điểm!
>> Sói Trắng Sói Đen gầm gừ: Tấn công kẻ thù, gây 110 sát thương!

Chọn chức năng (1-6): 6
Hẹn gặp lại trong Rikkei RPG!
```

## Ghi chú

- Đề yêu cầu nộp 1 file `rpg_companions.py`, khối `__main__` chạy 6 kịch bản kiểm thử; menu tương tác (chức năng 1-5 của đề) được thêm vào và bật bằng tham số `--menu`.
- Lai tạo không xóa 2 con bố mẹ khỏi đội hình (đề không yêu cầu); con lai được thêm vào cuối danh sách.

## Cách chạy

```bash
python rpg_companions.py            # kịch bản kiểm thử
python rpg_companions.py --menu     # menu tương tác
```
