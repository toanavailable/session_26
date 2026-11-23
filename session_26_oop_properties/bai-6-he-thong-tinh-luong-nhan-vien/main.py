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
