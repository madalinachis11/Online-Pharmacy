
from typing import Dict, Union, Optional, List

import jsonpickle as jsonpickle

from Domain.medicament import Medicine


class MedicamentRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Medicine]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, medicament: Medicine) -> None:
        """
        Functia de adaugare a unui medicament.
        :param medicament:medicamentul care trebuie adaugat
        :return:medicamentul adaugat
        """

        drugs = self.__read_file()
        if self.read(medicament.id_medicine) is not None:
            raise KeyError(
                f'Exista deja un medicament cu id-ul {medicament.id_medicine}')

        drugs[medicament.id_medicine] = medicament
        self.__write_file(drugs)

    def read(self,
             id_medicine=None) -> Union[Optional[Medicine], List[Medicine]]:
        """
        Functia citeste un medicament impreuna cu id-ul sau.
        """

        drugs = self.__read_file()
        if id_medicine:
            if id_medicine in drugs:
                return drugs[id_medicine]
            else:
                return None

        return list(drugs.values())

    def update(self, medicament: Medicine) -> None:
        """
        Functia de modificare a unui medicament.
        :param medicament:medicamentul care se va actualiza.
        :return: noul medicament actualizat
        """

        drugs = self.__read_file()
        if self.read(medicament.id_medicine) is None:
            msg =\
                f'Nu exista un medicament cu id-ul {medicament.id_medicine} de actualizat.'
            raise KeyError(msg)

        drugs[medicament.id_medicine] = medicament
        self.__write_file(drugs)

    def delete(self, id_medicine: str) -> None:
        """
        Functia de stergere a unui medicament.
        :param id_medicine:id-ul medicamentului
        :return:Medicamentele fara medicamentul pe care am dorit sa il stergem.
        """
        drugs = self.__read_file()
        if self.read(id_medicine) is None:
            raise KeyError(
                f'Nu exista un medicament cu id-ul {id_medicine} pe care sa il stergem.')

        del drugs[id_medicine]
        self.__write_file(drugs)
