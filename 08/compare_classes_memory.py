from random import randint
from memory_profiler import profile

from simple_classes import (
    CPU as SimpleCPU,
    KitRAM as SimpleKitRAM,
    MotherBoard as SimpleMotherBoard,
)
from slots_classes import (
    CPU as SlotsCPU,
    KitRAM as SlotsKitRAM,
    MotherBoard as SlotsMotherBoard,
)
from weakref_classes import (
    CPU as WeakrefCPU,
    KitRAM as WeakrefKitRAM,
    MotherBoard as WeakrefMotherBoard,
)


N = 500_000


@profile
def run_simple_classes(count_run):
    cpus = [SimpleCPU(8, 3.2) for _ in range(count_run)]
    kits_of_ram = [SimpleKitRAM(4, 3.2, 8) for _ in range(count_run)]
    motherboards = [
        SimpleMotherBoard(
            4,
            cpus[randint(0, count_run - 1)],
            kits_of_ram[randint(0, count_run - 1)],
        )
        for _ in range(count_run)
    ]
    for cpu in cpus:
        cpu.base_frequency += 1.0
        cpu.count_cores = 32

    for kit_of_ram in kits_of_ram:
        kit_of_ram.base_frequency += 1.0
        kit_of_ram.size = 16

    for motherboard in motherboards:
        motherboard.count_ram_slots *= 2
        motherboard.cpu.count_cores *= 2


@profile
def run_slots_classes(count_run):
    cpus = [SlotsCPU(8, 3.2) for _ in range(count_run)]
    kits_of_ram = [SlotsKitRAM(4, 3.2, 8) for _ in range(count_run)]
    motherboards = [
        SlotsMotherBoard(
            4,
            cpus[randint(0, count_run - 1)],
            kits_of_ram[randint(0, count_run - 1)],
        )
        for _ in range(count_run)
    ]
    for cpu in cpus:
        cpu.base_frequency += 1.0
        cpu.count_cores = 32

    for kit_of_ram in kits_of_ram:
        kit_of_ram.base_frequency += 1.0
        kit_of_ram.size = 16

    for motherboard in motherboards:
        motherboard.count_ram_slots *= 2
        motherboard.cpu.count_cores *= 2


@profile
def run_weakref_classes(count_run):
    cpus = [WeakrefCPU(8, 3.2) for _ in range(count_run)]
    kits_of_ram = [WeakrefKitRAM(4, 3.2, 8) for _ in range(count_run)]
    motherboards = [
        WeakrefMotherBoard(
            4,
            cpus[randint(0, count_run - 1)],
            kits_of_ram[randint(0, count_run - 1)],
        )
        for _ in range(count_run)
    ]
    for cpu in cpus:
        cpu.base_frequency += 1.0
        cpu.count_cores = 32

    for kit_of_ram in kits_of_ram:
        kit_of_ram.base_frequency += 1.0
        kit_of_ram.size = 16

    for motherboard in motherboards:
        motherboard.count_ram_slots *= 2
        motherboard.cpu().count_cores *= 2


if __name__ == "__main__":
    run_simple_classes(N)
    run_slots_classes(N)
    run_weakref_classes(N)
