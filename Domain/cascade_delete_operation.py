from typing import List

from Domain.undo_redo_operation import UndoRedoOperation
from Repository.repository import Repository

"""
Acest cod definește clasa CascadeDeleteOperation care moștenește clasa UndoRedoOperation.
Scopul acestei clase este de a furniza funcționalitate pentru anularea și refacerea unei
operațiuni de ștergere în cascada într-un depozit.
"""


class CascadeDeleteOperation(UndoRedoOperation):
    def __init__(
            self,
            repository: Repository,
            transaction_repository: Repository,
            cascade_list: List
    ):
        self.__repository = repository
        self.__transactionRepository = transaction_repository
        self.__cascadeList = cascade_list

        """
        Metoda __init__ primește trei argumente: un obiect repository,
        un obiect transaction_repository și o listă cascade_list. Obiectul repository
        reprezintă depozitul principal în care vor fi efectuate operațiile de ștergere,
        obiectul transaction_repository reprezintă un depozit temporar pentru tranzacții,
        iar lista cascade_list conține entitățile care vor fi șterse în cascada.
        """

    def do_undo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__repository.create(
                self.__cascadeList[len(self.__cascadeList) -1 ]
            )


            """
            Metoda do_undo este definită pentru a efectua operația de anulare a ștergerii
            în cascada. Pentru fiecare entitate din lista cascade_list, aceasta adaugă
            entitatea înapoi în depozitul principal folosind metoda create.
            Metoda do_undo din clasa CascadeDeleteOperation parcurge lista cascadeList
            și adaugă înapoi în depozitul principal ultima entitate din listă (cea care a
            fost ștearsă prima dată în cascada). Acest lucru se realizează prin apelarea
            metodei create a depozitului principal (repository) și trecerea ultimei entități
            din listă ca parametru. Deoarece iterează până la len(self.__cascadeList) - 1,
            ultima entitate nu este adăugată înapoi în depozitul principal prin această metodă.
            """

    def fo_redo(self):
        for i in range(len(self.__cascadeList) - 1):
            self.__transactionRepository.delete(
                self.__cascadeList[0].entity.id_entity
            )
        self.__repository.delete(
            self.__cascadeList[len(self.__cascadeList) - 1].entity.id

        )

"""
Metoda fo_redo este definită pentru a efectua operația de refacere a ștergerii în cascada.
Aceasta șterge fiecare entitate din lista cascade_list din depozitul temporar pentru tranzacții
folosind metoda delete, apoi șterge entitatea finală din depozitul principal folosind metoda delete.
Această metodă fo_redo din clasa CascadeDeleteOperation parcurge lista cascadeList și șterge fiecare
entitate din depozitul temporar pentru tranzacții (transaction_repository) folosind metoda delete.
Aceasta ia primul element din listă și utilizează ID-ul entității asociate pentru a șterge entitatea
din depozitul temporar pentru tranzacții. Apoi, această metodă șterge entitatea finală din depozitul
principal (repository) utilizând metoda delete și ID-ul entității asociate cu ultimul element din listă.
"""