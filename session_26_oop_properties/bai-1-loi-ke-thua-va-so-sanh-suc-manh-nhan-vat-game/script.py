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
