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
