from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository

"""
Această clasă DeleteOperation implementează o operație de ștergere a unei singure
entități dintr-un depozit. Constructorul primește un depozit și entitatea care va
fi ștearsă din depozit. Metoda undo va adăuga înapoi entitatea în depozitul dat
prin apelarea metodei create. Metoda redo va șterge din nou entitatea din depozit
prin apelarea metodei delete pe ID-ul entității asociate. Această clasă este utilizată
pentru implementarea operațiilor de undo/redo.
"""


class DeleteOperation(UndoRedoOperation):

    def __init__(self, repository: Repository,
                 deleted_object: Entity):
        self.repository = repository
        self.deleted_object = deleted_object

    def undo(self):
        self.repository.create(self.deleted_object)

    def redo(self):
        self.repository.delete(self.deleted_object.id_entity)
