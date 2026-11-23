# Bài 1 - Lỗi kế thừa và so sánh sức mạnh hệ thống nhân vật game

## Đề bài

Rikkei Studios xây dựng hệ thống chiến đấu cho tựa game nhập vai giả tưởng (RPG):

- **Lớp cha `Character`** (nhân vật cơ bản): `name` (tên), `hp` (máu), `attack_power` (sức tấn công); hàm khởi tạo `__init__` để gán các thuộc tính trên.
- **Lớp con `Warrior`** (kế thừa `Character`): kế thừa toàn bộ thuộc tính của cha, thêm `bonus_armor` (giáp cộng thêm); `__init__` dùng `super()`; `get_total_power()` tính tổng sức mạnh (`attack_power + bonus_armor`); `__gt__(self, other)` nạp chồng toán tử lớn hơn (>) để so sánh sức mạnh giữa 2 chiến binh.

Hệ thống ghép trận (Matchmaking) cần so sánh sức mạnh của 2 người chơi bằng toán tử > hoặc < (VD `warrior_1 > warrior_2`). Lập trình viên mới đưa code lên máy chủ thì game bị crash ngay lập tức vì:

- **Tính kế thừa (Inheritance) & `super()`:** khai báo lớp con kế thừa lớp cha trên lý thuyết nhưng trong hàm khởi tạo lại không hề "triệu hồi" hàm khởi tạo của lớp cha → chiến binh mất sạch máu, tên và sát thương cơ bản.
- **Nạp chồng toán tử (Operator Overloading):** dùng `>` để so sánh 2 đối tượng `Warrior` phức tạp mà không định nghĩa trước tiêu chí so sánh.

## Mã nguồn hiện tại (Legacy Code)

File: [`script_legacy.py`](script_legacy.py)

```python
# Lớp cha: Nhân vật cơ bản
class Character:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

# Lớp con: Chiến binh cận chiến
class Warrior(Character):
    def __init__(self, name, hp, attack_power, bonus_armor):
        # Lỗi 1: Bỏ quên hàm super()
        self.bonus_armor = bonus_armor

    def get_total_power(self):
        return self.attack_power + self.bonus_armor

# --- KỊCH BẢN MATCHMAKING LỖI ---
# Tạo 2 đối tượng chiến binh
w1 = Warrior("Arthur", 1000, 150, 50)  # Sức mạnh tổng: 200
w2 = Warrior("Lancelot", 900, 180, 10)  # Sức mạnh tổng: 190

# In thông báo xuất trận
print(f"Chiến binh {w1.name} xuất trận!")

# So sánh sức mạnh bằng toán tử >
if w1 > w2:
    print(f"{w1.name} mạnh hơn {w2.name}!")
else:
    print(f"{w2.name} mạnh hơn hoặc hòa!")
```

```
$ python script_legacy.py
Traceback (most recent call last):
  File "script_legacy.py", line 23, in <module>
    print(f"Chiến binh {w1.name} xuất trận!")
                        ^^^^^^^
AttributeError: 'Warrior' object has no attribute 'name'
```

## (1) Phân tích lỗi (Code Review)

**Câu 1. Vì sao `print(f"Chiến binh {w1.name}...")` văng `AttributeError` dù đã khai báo kế thừa?**

`Warrior` tự định nghĩa `__init__` riêng nên đã **ghi đè (override)** `__init__` của `Character`. Khi tạo `Warrior(...)`, Python chỉ chạy `Warrior.__init__`, mà hàm này chỉ gán `self.bonus_armor`, không gọi tới khởi tạo của lớp cha → các dòng `self.name = ...`, `self.hp = ...`, `self.attack_power = ...` không bao giờ được chạy. Kế thừa chỉ cho lớp con **dùng chung phương thức**; thuộc tính của instance chỉ tồn tại khi có code gán chúng.

**Câu 2. Không dùng `super().__init__(...)` thì có cách nào khác (dù không khuyến khích) để gọi khởi tạo của `Character`?**

Gọi trực tiếp qua tên lớp cha và tự truyền `self`: `Character.__init__(self, name, hp, attack_power)`. Không khuyến khích vì: gắn cứng tên lớp cha (đổi cấu trúc kế thừa phải sửa khắp nơi); phải truyền `self` thủ công dễ sai; với đa kế thừa sẽ **bỏ qua MRO**, có thể gọi trùng hoặc bỏ sót lớp cha khác. `super()` tự tìm lớp kế tiếp theo MRO nên an toàn và linh hoạt hơn.

**Câu 3. Sửa xong Lỗi 1, chạy tới `if w1 > w2:` thì lỗi gì? Tại sao Python không tự so sánh?**

`TypeError: '>' not supported between instances of 'Warrior' and 'Warrior'`. Toán tử `>` thực chất gọi `w1.__gt__(w2)`; class tự định nghĩa không có sẵn `__gt__` nên Python **không biết tiêu chí** so sánh (theo máu, theo sát thương, theo tổng sức mạnh...?) và từ chối thay vì đoán bừa.

**Câu 4. Để `>` so sánh dựa trên `get_total_power()` cần khai báo Dunder method nào? Nhận mấy tham số?**

Khai báo `__gt__(self, other)` trong `Warrior`: nhận **2 tham số**: `self` (vế trái của `>`) và `other` (vế phải). Trả về `self.get_total_power() > other.get_total_power()`; nên kiểm tra `isinstance(other, Warrior)`, sai kiểu thì `return NotImplemented`.

Minh họa:

```
>>> Sửa Lỗi 1 (thêm super) nhưng chưa có __gt__:
Chiến binh Arthur xuất trận!
TypeError: '>' not supported between instances of 'Warrior' and 'Warrior'
>>> Warrior.__mro__: ['Warrior', 'Character', 'object']
>>> w > 100 (không phải Warrior):
TypeError: '>' not supported between instances of 'Warrior' and 'int'
```

## (2) Sửa lỗi (Refactoring)

File: [`script.py`](script.py)

```python
"""Hệ thống nhân vật game Rikkei Studios - bản đã sửa (Inheritance + __gt__)."""


class Character:
    """Nhân vật cơ bản: tên, máu, sức tấn công."""

    def __init__(self, name, hp, attack_power):
        """Khởi tạo các thuộc tính chung của mọi nhân vật."""
        self.name = name
        self.hp = hp
        self.attack_power = attack_power


class Warrior(Character):
    """Chiến binh cận chiến: kế thừa Character, có thêm giáp cộng thêm."""

    def __init__(self, name, hp, attack_power, bonus_armor):
        """Gọi super().__init__() để lớp cha khởi tạo name, hp, attack_power."""
        super().__init__(name, hp, attack_power)
        self.bonus_armor = bonus_armor

    def get_total_power(self):
        """Sức mạnh chiến đấu = attack_power + bonus_armor."""
        return self.attack_power + self.bonus_armor

    def __gt__(self, other):
        """Nạp chồng toán tử >: so sánh tổng sức mạnh giữa 2 chiến binh."""
        if not isinstance(other, Warrior):
            return NotImplemented
        return self.get_total_power() > other.get_total_power()


if __name__ == "__main__":
    w1 = Warrior("Arthur", 1000, 150, 50)    # Sức mạnh tổng: 200
    w2 = Warrior("Lancelot", 900, 180, 10)   # Sức mạnh tổng: 190

    print(f"Chiến binh {w1.name} xuất trận!")

    if w1 > w2:                               # Python gọi w1.__gt__(w2)
        print(f"{w1.name} mạnh hơn {w2.name}!")
    else:
        print(f"{w2.name} mạnh hơn hoặc hòa!")
```

```
$ python script.py
Chiến binh Arthur xuất trận!
Arthur mạnh hơn Lancelot!
```

Kết quả khớp yêu cầu của đề: Arthur (150 + 50 = 200) mạnh hơn Lancelot (180 + 10 = 190).

## Cách chạy

```bash
python script_legacy.py
python script.py
```
