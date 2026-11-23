# Bài 6 - BTTH: Hệ thống tính lương nhân viên

## Đề bài

**Mục tiêu:** áp dụng tính trừu tượng bằng `ABC` và `@abstractmethod`; tính kế thừa thông qua class cha `Employee` và các class con; tính đa hình thông qua việc gọi chung một method `calculate_salary()` nhưng mỗi loại nhân viên có cách tính lương khác nhau; thiết kế Class và Object; sử dụng constructor (`__init__`) và `super()` trong kế thừa.

Công ty có 3 loại nhân viên: toàn thời gian (`FullTimeEmployee`), bán thời gian (`PartTimeEmployee`), thực tập sinh (`InternEmployee`). Mỗi nhân viên đều có mã nhân viên, họ tên và cách tính lương riêng.

```
              Employee (ABC)
                    |
     -------------------------------
     |              |              |
FullTimeEmployee PartTimeEmployee InternEmployee
```

| Class | Thuộc tính | Công thức lương |
|---|---|---|
| `Employee` (ABC) | `employee_id`, `name`; `display_info()`; `@abstractmethod calculate_salary()` | - (không tạo object trực tiếp) |
| `FullTimeEmployee` | + `base_salary`, `bonus` | `base_salary + bonus` |
| `PartTimeEmployee` | + `working_hours`, `hourly_rate` | `working_hours * hourly_rate` |
| `InternEmployee` | + `allowance` | `allowance` |

Mock data:

```python
employees = [
    FullTimeEmployee("E001", "Nguyen Van A", 15000000, 3000000),
    PartTimeEmployee("E002", "Tran Thi B", 80, 50000),
    InternEmployee("E003", "Le Van C", 3000000)
]
```

### Menu

```
=== EMPLOYEE SALARY MANAGER ===
1. Xem danh sách nhân viên
2. Tính lương toàn bộ nhân viên
3. Thoát chương trình
================================
Chọn chức năng (1-3):
```

- Ngoài khoảng 1-3: "Lựa chọn không hợp lệ. Vui lòng thử lại." rồi hiển thị lại menu.
- Chức năng 1 `display_employees(employees)`: duyệt danh sách, gọi `display_info()` của từng nhân viên.
- Chức năng 2 `display_salaries(employees)`: gọi chung `employee.calculate_salary()`, **không** dùng `if`, `elif`, `match-case` hoặc kiểm tra kiểu dữ liệu để phân loại nhân viên; lương hiển thị `f"{salary:,.0f} VND"`.
- Chức năng 3: "Cảm ơn bạn đã sử dụng Employee Salary Manager!".

## Phân tích

- **Trừu tượng:** `Employee(ABC)` có `@abstractmethod calculate_salary()` → không tạo được `Employee(...)` (xem kiểm tra bên dưới) và mọi lớp con bắt buộc có công thức lương.
- **Kế thừa:** 3 lớp con dùng `super().__init__(employee_id, name)` tái sử dụng khởi tạo chung và `display_info()` của lớp cha.
- **Đa hình:** `display_salaries` chỉ gọi `employee.calculate_salary()`; loại nhân viên hiển thị ở `display_info()` lấy từ class attribute `employee_type` của từng lớp nên cũng không cần `if`.

## Mã nguồn

File: [`main.py`](main.py)

```python
"""Employee Salary Manager - Abstraction, Inheritance, Polymorphism.

          Employee (ABC)
               |
   -------------------------------
   |              |              |
FullTimeEmployee PartTimeEmployee InternEmployee
"""

from abc import ABC, abstractmethod

MENU_LINE = "=" * 32


class Employee(ABC):
    """Nhân viên nói chung - lớp trừu tượng, không tạo object trực tiếp."""

    employee_type = "Employee"

    def __init__(self, employee_id, name):
        """Mã nhân viên và họ tên dùng chung cho mọi loại nhân viên."""
        self.employee_id = employee_id
        self.name = name

    def display_info(self):
        """In thông tin cơ bản của nhân viên."""
        print(f"Mã NV: {self.employee_id} | Họ tên: {self.name} | "
              f"Loại: {self.employee_type}")

    @abstractmethod
    def calculate_salary(self):
        """Mỗi loại nhân viên bắt buộc tự định nghĩa cách tính lương."""


class FullTimeEmployee(Employee):
    """Nhân viên toàn thời gian: lương = lương cơ bản + thưởng."""

    employee_type = "Full-time"

    def __init__(self, employee_id, name, base_salary, bonus):
        """Khởi tạo phần chung bằng super(), thêm lương cơ bản và thưởng."""
        super().__init__(employee_id, name)
        self.base_salary = base_salary
        self.bonus = bonus

    def calculate_salary(self):
        """salary = base_salary + bonus."""
        return self.base_salary + self.bonus


class PartTimeEmployee(Employee):
    """Nhân viên bán thời gian: lương = số giờ làm x lương theo giờ."""

    employee_type = "Part-time"

    def __init__(self, employee_id, name, working_hours, hourly_rate):
        """Khởi tạo phần chung bằng super(), thêm số giờ và đơn giá giờ."""
        super().__init__(employee_id, name)
        self.working_hours = working_hours
        self.hourly_rate = hourly_rate

    def calculate_salary(self):
        """salary = working_hours * hourly_rate."""
        return self.working_hours * self.hourly_rate


class InternEmployee(Employee):
    """Thực tập sinh: lương = trợ cấp."""

    employee_type = "Intern"

    def __init__(self, employee_id, name, allowance):
        """Khởi tạo phần chung bằng super(), thêm trợ cấp."""
        super().__init__(employee_id, name)
        self.allowance = allowance

    def calculate_salary(self):
        """salary = allowance."""
        return self.allowance


def display_employees(employees):
    """Chức năng 1: gọi display_info() của từng nhân viên."""
    print("--- DANH SÁCH NHÂN VIÊN ---")
    for employee in employees:
        employee.display_info()


def display_salaries(employees):
    """Chức năng 2: gọi chung calculate_salary() - KHÔNG kiểm tra loại nhân viên."""
    print("--- BẢNG LƯƠNG NHÂN VIÊN ---")
    for employee in employees:
        salary = employee.calculate_salary()      # Đa hình
        print(f"{employee.employee_id} | {employee.name:<12} | Lương: {salary:,.0f} VND")


def display_menu():
    """In menu chính."""
    print("\n=== EMPLOYEE SALARY MANAGER ===")
    print("1. Xem danh sách nhân viên")
    print("2. Tính lương toàn bộ nhân viên")
    print("3. Thoát chương trình")
    print(MENU_LINE)


def main():
    """Tạo dữ liệu mẫu và chạy vòng lặp menu."""
    employees = [
        FullTimeEmployee("E001", "Nguyen Van A", 15000000, 3000000),
        PartTimeEmployee("E002", "Tran Thi B", 80, 50000),
        InternEmployee("E003", "Le Van C", 3000000),
    ]
    while True:
        display_menu()
        choice = input("Chọn chức năng (1-3): ").strip()
        if choice == "1":
            display_employees(employees)
        elif choice == "2":
            display_salaries(employees)
        elif choice == "3":
            print("Cảm ơn bạn đã sử dụng Employee Salary Manager!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
    main()
```

## Kết quả chạy thử

```
Chọn chức năng (1-3): 1
--- DANH SÁCH NHÂN VIÊN ---
Mã NV: E001 | Họ tên: Nguyen Van A | Loại: Full-time
Mã NV: E002 | Họ tên: Tran Thi B | Loại: Part-time
Mã NV: E003 | Họ tên: Le Van C | Loại: Intern

Chọn chức năng (1-3): 2
--- BẢNG LƯƠNG NHÂN VIÊN ---
E001 | Nguyen Van A | Lương: 18,000,000 VND
E002 | Tran Thi B   | Lương: 4,000,000 VND
E003 | Le Van C     | Lương: 3,000,000 VND

Chọn chức năng (1-3): 5
Lựa chọn không hợp lệ. Vui lòng thử lại.

Chọn chức năng (1-3): abc
Lựa chọn không hợp lệ. Vui lòng thử lại.

Cảm ơn bạn đã sử dụng Employee Salary Manager!
```

Lương khớp mẫu: E001 = 15,000,000 + 3,000,000 = 18,000,000; E002 = 80 × 50,000 = 4,000,000; E003 = 3,000,000.

Kiểm tra lớp trừu tượng:

```
>>> employee = Employee("E001", "Nguyen Van A")
TypeError: Can't instantiate abstract class Employee without an implementation for abstract method 'calculate_salary'
>>> FullTimeEmployee.__mro__: ['FullTimeEmployee', 'Employee', 'ABC', 'object']
```

## Cách chạy

```bash
python main.py
```
