class CPU:

    def __init__(self, count_cores: int, base_frequency: float) -> None:
        self.count_cores = count_cores
        self.base_frequency = base_frequency


class KitRAM:

    def __init__(self, count_modules: int, base_frequency: float, size: int) -> None:
        self.count_modules = count_modules
        self.base_frequency = base_frequency
        self.size = size


class MotherBoard:

    def __init__(self, count_ram_slots: int, cpu: CPU, kit_ram: KitRAM) -> None:
        self.count_ram_slots = count_ram_slots
        self.kit_ram = kit_ram
        self.cpu = cpu
