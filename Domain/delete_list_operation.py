from typing import List

from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository

"""
Această clasă DeleteListOperation implementează o operație de ștergere în bloc
pentru o listă de entități dintr-un depozit. Constructorul primește un depozit
și o listă de entități care vor fi șterse din depozit. Metoda undo va adăuga
fiecare entitate înapoi în depozitul dat prin apelarea metodei create.
Metoda redo va șterge din nou fiecare entitate din lista dată, prin apelarea
metodei delete pe ID-ul entității asociate, această metodă putând fi utilizată pentru operațiile de undo/redo.
"""


class DeleteListOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 deleted_list: List[Entity]):
        self.repository = repository
        self.deleted_list = deleted_list

    def undo(self):
        for i in self.deleted_list:
            self.repository.create(i)

    def redo(self):
        for i in self.deleted_list:
            self.repository.delete(i.id_entity)
