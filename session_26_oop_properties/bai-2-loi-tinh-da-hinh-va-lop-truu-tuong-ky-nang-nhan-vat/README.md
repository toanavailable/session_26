# Bài 2 - Lỗi tính đa hình và lớp trừu tượng trong kỹ năng nhân vật (RPG Game)

## Đề bài

Hệ thống chiến đấu quản lý nhiều hệ nhân vật khác nhau, tất cả phải tuân theo một khuôn mẫu chung để hệ thống dễ điều khiển:

- **Lớp cha `Hero`** (Tướng cơ bản): đóng vai trò là một **Lớp trừu tượng (Abstract Base Class)**, làm khuôn mẫu cho mọi tướng; có phương thức trừu tượng `use_ultimate(self)`: không có code xử lý bên trong, chỉ mang tính chất "ép buộc" các lớp con phải tự định nghĩa chiêu cuối của riêng mình.
- **Lớp con `Mage`** (Pháp sư): kế thừa `Hero`, ghi đè `use_ultimate()` để tung chiêu "Mưa Sao Băng".
- **Lớp con `Assassin`** (Sát thủ): kế thừa `Hero`, **bắt buộc** phải ghi đè `use_ultimate()` để tung chiêu "Ám Sát".

Trong chế độ Auto-Battle, máy chủ có tính năng "Tổng Tấn Công": duyệt danh sách tất cả các tướng đang có mặt trên sân và gọi phương thức `use_ultimate()` của từng tướng cùng một lúc. Nhờ **Tính đa hình** và **Duck Typing**, hệ thống không cần `if/else` kiểm tra tướng là Pháp sư hay Sát thủ.

**Vấn đề:** thực tập sinh không dùng thư viện `abc` mà chỉ ném lỗi `NotImplementedError` thủ công trong lớp cha. Ở lớp `Assassin`, bạn ấy **quên** ghi đè `use_ultimate()` mà tự đặt tên khác là `stealth_kill()`. Game không báo lỗi khi khởi tạo trận đấu; lỗi chỉ phát nổ khi 2 bên lao vào giao tranh và hệ thống cố gắng kích hoạt chiêu cuối.

## Mã nguồn hiện tại (Legacy Code)

File: [`script_legacy.py`](script_legacy.py)

```python
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
```

```
$ python script_legacy.py
--- LOADING TRẬN ĐẤU ---
Tải trận đấu thành công! Các tướng đã sẵn sàng...

--- GIAO TRANH TỔNG BẮT ĐẦU ---
🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!
Traceback (most recent call last):
  File "script_legacy.py", line 27, in <module>
    hero.use_ultimate()
    ~~~~~~~~~~~~~~~~~^^
  File "script_legacy.py", line 5, in use_ultimate
    raise NotImplementedError("Lớp con bắt buộc phải có chiêu cuối use_ultimate!")
NotImplementedError: Lớp con bắt buộc phải có chiêu cuối use_ultimate!
```

## (1) Phân tích lỗi (Code Review)

**Câu 1. Vòng lặp `for hero in team_heroes: hero.use_ultimate()` thể hiện tính đa hình thế nào?**

Cùng **một lời gọi** `hero.use_ultimate()` nhưng mỗi object thực hiện **hành vi khác nhau** tùy lớp của nó (Pháp Sư tung Mưa Sao Băng, Sát Thủ tung Ám Sát). Vòng lặp không cần biết `hero` thuộc lớp nào, không có `if isinstance(...)`: chỉ cần object "biết" `use_ultimate()` (Duck Typing). Thêm tướng mới chỉ cần tạo lớp con mới, không phải sửa vòng lặp.

**Câu 2. Không dùng `abc`, vì sao `Assassin()` vẫn khởi tạo thành công? Báo lỗi muộn gây thảm họa gì?**

Với class thông thường, Python **không kiểm tra** lớp con đã override đủ phương thức hay chưa: `use_ultimate()` của lớp cha vẫn là một method hợp lệ (chỉ chứa lệnh `raise`), nên tạo object không có gì sai. Lỗi chỉ xuất hiện khi method thực sự **được gọi** lúc runtime → game sập **giữa trận giao tranh**: người chơi mất trận, mất dữ liệu ván đấu, trải nghiệm tệ, và lỗi lọt qua mọi bước test không chạm tới chiêu cuối của Sát Thủ.

**Câu 3. Dùng `abc` + `@abstractmethod`, nếu `Assassin` vẫn quên override thì lỗi xảy ra ở thời điểm nào?**

Lỗi văng ra ngay **lúc khởi tạo object** `Assassin()`, tức là trong giai đoạn **loading đầu trận**, trước khi giao tranh bắt đầu: `TypeError: Can't instantiate abstract class Assassin without an implementation for abstract method 'use_ultimate'`.

**Câu 4. Nguyên lý Fail Fast được thể hiện thế nào khi áp dụng ABC?**

Fail Fast = phát hiện lỗi **càng sớm càng tốt, càng gần nơi gây ra lỗi càng tốt**. ABC biến lỗi "quên cài đặt chiêu cuối" từ lỗi runtime ngẫu nhiên giữa trận thành lỗi chắc chắn xảy ra khi tạo object (ngay lần chạy thử / test đầu tiên của lập trình viên). Lỗi bị chặn trước khi lên server, không bao giờ tới tay người chơi.

Minh họa với ABC (Assassin vẫn dùng `stealth_kill`):

```
--- LOADING TRẬN ĐẤU ---
TypeError: Can't instantiate abstract class Assassin without an implementation for abstract method 'use_ultimate'
>> Lỗi bị phát hiện ngay lúc tải trận, trước khi giao tranh bắt đầu (Fail Fast).
>>> Hero():
TypeError: Can't instantiate abstract class Hero without an implementation for abstract method 'use_ultimate'
```

## (2) Sửa lỗi (Refactoring)

- `from abc import ABC, abstractmethod`.
- `Hero(ABC)` với `@abstractmethod use_ultimate()` (bỏ `raise NotImplementedError`, thân hàm chỉ còn docstring).
- `Assassin`: đổi tên `stealth_kill()` thành `use_ultimate()`.

File: [`script.py`](script.py)

```python
"""Hệ thống kỹ năng tướng Rikkei Studios - bản đã sửa (ABC + Polymorphism)."""

from abc import ABC, abstractmethod


class Hero(ABC):
    """Lớp trừu tượng: khuôn mẫu bắt buộc mọi tướng phải có chiêu cuối."""

    @abstractmethod
    def use_ultimate(self):
        """Chiêu cuối - lớp con BẮT BUỘC phải override."""


class Mage(Hero):
    """Pháp Sư."""

    def use_ultimate(self):
        """Tung chiêu Mưa Sao Băng."""
        print("🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!")


class Assassin(Hero):
    """Sát Thủ: đổi tên stealth_kill() thành use_ultimate() đúng hợp đồng."""

    def use_ultimate(self):
        """Tung chiêu Ám Sát."""
        print("🗡 Sát Thủ tung chiêu: ÁM SÁT TỪ PHÍA SAU!")


if __name__ == "__main__":
    print("--- LOADING TRẬN ĐẤU ---")
    team_heroes = [Mage(), Assassin()]
    print("Tải trận đấu thành công! Các tướng đã sẵn sàng...")

    print("--- GIAO TRANH TỔNG BẮT ĐẦU ---")
    for hero in team_heroes:              # Đa hình: cùng một lời gọi
        hero.use_ultimate()
```

```
$ python script.py
--- LOADING TRẬN ĐẤU ---
Tải trận đấu thành công! Các tướng đã sẵn sàng...
--- GIAO TRANH TỔNG BẮT ĐẦU ---
🔥 Pháp Sư tung chiêu: MƯA SAO BĂNG!
🗡 Sát Thủ tung chiêu: ÁM SÁT TỪ PHÍA SAU!
```

## Cách chạy

```bash
python script_legacy.py
python script.py
```
