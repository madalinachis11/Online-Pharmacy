from dataclasses import dataclass


@dataclass
class MedicineNumberSales:
    def __init__(self, medicament, vanzari):
        self.medicament = medicament
        self.vanzari = vanzari

    def __str__(self):
        return f"Medicament {self.medicament} are {self.vanzari} vanzari."