from Domain.medicament import Medicine


class MedicamentValidator:

    def validate(self, medicament: Medicine):
        valid_drugs = ['Da', 'Nu']
        if medicament.medical_prescription not in valid_drugs:
            raise ValueError('Raspunsul trebuie'
                             f'sa fie unul dintre {valid_drugs}')
        erori = []
        if medicament.price < 0:
            erori.append("Pretul  nu este valid ")
        if len(erori) > 0:
            raise ValueError(erori)
