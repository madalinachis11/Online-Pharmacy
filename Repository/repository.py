from typing import Protocol, Type, Union, Optional, List

import jsonpickle

from Domain.entity import Entity


from Repository.exceptions import DuplicateIdError, NoSuchIdError


class Repository(Protocol):

    def __init__(self, filename):
        self.__storage = {}
        self.__filename = filename

    def __write_file(self):
        with open(self.__filename, 'w') as f:
            f.write(jsonpickle.encode(self.__storage))

    def __load_file(self):
        try:
            with open(self.__filename, 'r') as f:
                self.__storage = jsonpickle.decode(f.read())
        except:
            self.__storage = {}

    def read(self, id_entity: object = None) -> Type[Union[Optional[Entity], List[Entity]]]:
        """
         Functia citeste un medicament impreuna cu id-ul sau.
        """
        drugs = self.__read_file()
        if id_entity:
            if id_entity in drugs:
                return drugs[id_entity]
            else:
                return None

        return list(drugs.values())

    def create(self, entity: Entity) -> None:
        """
        Adauga o entitate.
        :param entity: entitatea
        :return:
        """
        if self.read(entity.id_entity) is not None:
            raise DuplicateIdError(f'Exista deja o entitate cu id-ul {entity.id_entity}!')
        self.__storage[entity.id_entity] = entity
        self.__write_file()

    def update(self, entity: Entity) -> None:
        """
        Modifica o entitate.
        :param entity :entitatea data
        :return:
        """
        """
        if self.read(str(entity.id_entity)) is None:
            raise NoSuchIdError(f'Nu exista nicio entitate cu id-ul {entity.id_entity}')
        """
        self.__storage[entity.id_entity] = entity
        self.__write_file()

    def delete(self, id_entity: str) -> None:
        if self.read(id_entity) is None:
            raise NoSuchIdError(f'Nu exista nicio entitate cu id-ul {id_entity}')
        del self.__storage[str(id_entity)]
        self.__write_file()
