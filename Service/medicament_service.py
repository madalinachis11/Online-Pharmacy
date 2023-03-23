from typing import List

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.medicament import Medicine
from Domain.medicament_validator import MedicamentValidator
from Domain.random import RandomMedicament
from Domain.update_list_operation import UpdateListOperation
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class MedicamentService:
    def __init__(self,
                 medicine_repository: Repository,
                 medicament_validator: MedicamentValidator,
                 undo_redo_service: UndoRedoService):
        self.medicament_repository = medicine_repository
        self.medicament_validator = medicament_validator
        self.undo_redo_service = undo_redo_service

    def add_medicine(self,
                     id_medicine: str,
                     name_medicine: str,
                     producer: str,
                     price: float,
                     medical_prescription: str):
        """
        Functia de adaugare a unui medicament.
        """
        medicament = Medicine(id_medicine,
                              name_medicine,
                              producer,
                              price,
                              medical_prescription)

        self.medicament_validator.validate(medicament)
        self.medicament_repository.create(medicament)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.medicament_repository, medicament)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_medicine(self,
                        id_medicine: str,
                        name_medicine: str,
                        producer: str,
                        price: float,
                        medical_prescription: str):
        """
        Functia de modificare a unui medicament.
        """
        medicament_vechi = self.medicament_repository.read(id_medicine)
        medicament = Medicine(id_medicine,
                              name_medicine,
                              producer,
                              price,
                              medical_prescription)
        self.medicament_validator.validate(medicament)
        self.medicament_repository.update(medicament)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.medicament_repository, medicament_vechi, medicament)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_medicine(self,
                        id_medicine: str):
        medicament = self.medicament_repository.read(id_medicine)
        self.medicament_repository.delete(id_medicine)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.medicament_repository, medicament)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Medicine]:
        return self.medicament_repository.read()

    def generate_medicamente_random(self, number_of_medicine):
        """
        Genereaza un numar de medicamente cu date aleatorii valide
        :param number_of_medicine: numarul de medicamente de generat, int
        :return: None
        Functie recursiva.
        """

        if number_of_medicine == 0:
            return []
        else:
            rand_id_medicine = RandomMedicament.random_int()
            rand_name_medicine = RandomMedicament.random_string()
            rand_producer = RandomMedicament.random_string()
            rand_price = RandomMedicament.random_int(1, 1000)
            rand_medical_prescription = RandomMedicament.random_bool()
            if rand_medical_prescription == 1:
                rand_medical_prescription = 'Da'
            else:
                rand_medical_prescription = 'Nu'
            generated_medicament = Medicine(rand_id_medicine,
                                            rand_name_medicine,
                                            rand_producer,
                                            rand_price,
                                            rand_medical_prescription)
            self.medicament_validator.validate(generated_medicament)
            self.medicament_repository.create(generated_medicament)
            return [generated_medicament] + self.generate_medicamente_random(number_of_medicine - 1)

    def full_search(self, string_to_search):
        """
        Cauta full text.
        :param string_to_search:stringul pe care il cautam
        :return:
        """

        search_results = []
        medicament_list = self.medicament_repository.read()
        for each_medicament in medicament_list:
            if each_medicament.search(string_to_search):
                search_results.append(each_medicament)
        return search_results

    def creste_preturile_medicamentului(self, procentaj, price):
        """
        Afiseaza medicamentele cu pretul crescut cu un anumit procentaj.
        :param procentaj: numar intreg
        :param price: numar intreg
        :return:
        """
        medicamente = self.medicament_repository.read()
        filtered_medicamente = list(filter(lambda x: x.price < price, medicamente))
        result = []
        for medicament in filtered_medicamente:
            medicament.price += (procentaj/100*medicament.price)
            self.medicament_repository.update(medicament)
            result.append(medicament)

        self.undo_redo_service.clear_redo()
        updated_operation = UpdateListOperation(self.medicament_repository, medicamente, result)
        self.undo_redo_service.add_to_undo(updated_operation)
