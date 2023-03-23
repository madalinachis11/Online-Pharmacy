from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository


class UpdateOperation(UndoRedoOperation):
    def __init__(self,
                 repository: Repository,
                 obiect_vechi: Entity,
                 obiect_nou: Entity):
        self.repository = repository
        self.obiect_vechi = obiect_vechi
        self.obiect_nou = obiect_nou

    def undo(self):
        self.repository.update(self.obiect_vechi)

    def redo(self):
        self.repository.update(self.obiect_nou)
