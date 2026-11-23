# Session 26 - Các tính chất của lập trình hướng đối tượng: Bài tập vận dụng

Tổng hợp 6 bài tập Session 26 về **Kế thừa & `super()`, Đa kế thừa & MRO, Đa hình & Duck Typing, Nạp chồng toán tử (Operator Overloading) và Abstract Base Classes** trong bối cảnh game RPG của Rikkei Studios và hệ thống tính lương.

## Thứ tự bài tập

| STT | Bài tập | Dạng bài | Kiến thức trọng tâm |
|---|---|---|---|
| 1 | [Lỗi kế thừa và so sánh sức mạnh nhân vật game](bai-1-loi-ke-thua-va-so-sanh-suc-manh-nhan-vat-game/) | Vận dụng cơ bản (sửa lỗi) | Quên `super().__init__()` → `AttributeError`; `>` giữa 2 object → `TypeError`; sửa bằng `super()` + `__gt__` |
| 2 | [Lỗi tính đa hình và lớp trừu tượng trong kỹ năng nhân vật](bai-2-loi-tinh-da-hinh-va-lop-truu-tuong-ky-nang-nhan-vat/) | Vận dụng cơ bản (sửa lỗi) | `NotImplementedError` thủ công nổ giữa trận → `ABC` + `@abstractmethod` (Fail Fast); đa hình `use_ultimate()` |
| 3 | [Hệ thống quản lý đội hình Auto-Battler](bai-3-he-thong-quan-ly-doi-hinh-auto-battler/) | Phân tích | `Champion(ABC)` → `Warrior`, `Mage`; `calculate_skill_damage()` đa hình; `__add__` + `__radd__` (cho `sum()`), `__gt__` |
| 4 | [Hệ thống rèn đúc & quản lý kho vũ khí](bai-4-he-thong-ren-duc-quan-ly-kho-vu-khi/) | Sáng tạo | `Equipment(ABC)`, Mixin, `MagicSword(Weapon, MagicMixin)` cooperative `**kwargs`; `__gt__`, `__add__` dung hợp ra Weapon mới |
| 5 | [Hệ thống thú cưỡi & bạn đồng hành](bai-5-he-thong-thu-cuoi-ban-dong-hanh/) | Vận dụng chuyên sâu | `Companion(ABC)`, `Dragon(Pet, Mount)` theo MRO; lai tạo `+` chỉ cùng loài; `super(Pet, self)` gọi kỹ năng Mount |
| 6 | [Hệ thống tính lương nhân viên](bai-6-he-thong-tinh-luong-nhan-vien/) | BTTH | `Employee(ABC)` + 3 lớp con; gọi chung `calculate_salary()` không dùng if/elif |

Mỗi thư mục bài có `README.md` riêng (đề bài, phân tích / trả lời câu hỏi, mã nguồn, kết quả chạy thử). Bài 1 và 2 có `script_legacy.py` (code lỗi gốc) và `script.py` (code đã sửa); bài 5 nộp theo yêu cầu là 1 file `rpg_companions.py`.

## Cách chạy

Yêu cầu Python 3.9+, không cần thư viện ngoài.

```bash
cd bai-1-loi-ke-thua-va-so-sanh-suc-manh-nhan-vat-game && python script.py
cd ../bai-2-loi-tinh-da-hinh-va-lop-truu-tuong-ky-nang-nhan-vat && python script.py
cd ../bai-3-he-thong-quan-ly-doi-hinh-auto-battler && python main.py
cd ../bai-4-he-thong-ren-duc-quan-ly-kho-vu-khi && python main.py
cd ../bai-5-he-thong-thu-cuoi-ban-dong-hanh && python rpg_companions.py && python rpg_companions.py --menu
cd ../bai-6-he-thong-tinh-luong-nhan-vien && python main.py
```
