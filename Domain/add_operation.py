from Domain.entity import Entity
from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository

"""
Acest cod definește clasa AddOperation care moștenește clasa UndoRedoOperation. 
Scopul acestei clase este de a furniza funcționalitate pentru anularea și
 refacerea unei operațiuni de adăugare într-un depozit.
"""


class AddOperation(UndoRedoOperation):

    def __init__(self,
                 repository: Repository,
                 added_entity: Entity):
        self.repository = repository
        self.added_entity = added_entity
        """
        Metoda __init__ primește două argumente: un obiect repository și un obiect added_entity.
         Obiectul repository reprezintă depozitul în care entitatea va fi adăugată, iar obiectul
          added_entity reprezintă entitatea care va fi adăugată în depozit.
        """

    def undo(self):
        self.repository.delete(self.added_entity.id_entity)

    def redo(self):
        self.repository.create(self.added_entity)

        """
        Metoda undo este definită pentru a șterge entitatea care a fost adăugată de către
        AddOperation.Aceasta apelează metoda delete a obiectului repository, trecând
        id_entity al added_entity caparametru.
        
        Metoda redo este definită pentru a adăuga din nou entitatea care a fost ștearsă
         anterior de către metoda undo. Aceasta apelează metoda create a obiectului
          repository, trecând added_entity ca parametru.
        """
