class CPU:
    __slots__ = ("count_cores", "base_frequency")

    def __init__(self, count_cores: int, base_frequency: float) -> None:
        self.count_cores = count_cores
        self.base_frequency = base_frequency


class KitRAM:
    __slots__ = ("count_modules", "base_frequency", "size")

    def __init__(self, count_modules: int, base_frequency: float, size: int) -> None:
        self.count_modules = count_modules
        self.base_frequency = base_frequency
        self.size = size


class MotherBoard:
    __slots__ = ("count_ram_slots", "ram", "cpu")

    def __init__(self, count_ram_slots: int, cpu: CPU, kit_ram: KitRAM) -> None:
        self.count_ram_slots = count_ram_slots
        self.ram = kit_ram
        self.cpu = cpu
