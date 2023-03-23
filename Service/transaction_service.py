
from typing import List
from datetime import datetime
from Domain.cascade_delete_operation import CascadeDeleteOperation
from Domain.medicament import Medicine
from utils import my_sorted
from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class TransactionService:
    def __init__(self,
                 transaction_repository: Repository,
                 transaction_validator: TransactionValidator,
                 medicine_repository: Repository,
                 membership_card_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.transaction_repository = transaction_repository
        self.transaction_validator = transaction_validator
        self.medicine_repository = medicine_repository
        self.membership_card_repository = membership_card_repository
        self.undo_redo_service = undo_redo_service

    def add_transaction(self,
                        id_transaction: str,
                        id_medicine: str,
                        id_membership_card: str,
                        number_pieces: int,
                        date_and_time: datetime) -> None:
        """
        Functia de adaugare a unei tranzactii.
        """
        if self.membership_card_repository.read(id_membership_card) is not None:
            price = self.medicine_repository.read(id_medicine).price
            if(
                    self.medicine_repository.read(
                        id_medicine
                    ).medical_prescription
                    == "da"
            ):
                total = price * number_pieces
                sale = (price * number_pieces) * 0.15
                total_sale = total - sale
            else:
                total = price * number_pieces
                sale = (price * number_pieces) * 0.10
                total_sale = total - sale
        else:
            price = self.medicine_repository.read(id_medicine).price_medicine
            total_sale = price * number_pieces
            sale = 0

        transaction = Transaction(id_transaction,
                                  id_medicine,
                                  id_membership_card,
                                  number_pieces,
                                  sale,
                                  total_sale,
                                  date_and_time)
        self.transaction_repository.create(transaction)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_transaction(self,
                           id_transaction: str,
                           id_medicine: str,
                           id_membership_card: str,
                           number_pieces: int,
                           date_and_time: datetime):
        """
        Functia de modificare a unei tranzactii.
        """
        transaction_old = self.transaction_repository.read(id_transaction)
        transaction = Transaction(id_transaction,
                                  id_medicine,
                                  id_membership_card,
                                  number_pieces,
                                  date_and_time)
        self.transaction_repository.update(transaction)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.transaction_repository, transaction_old, transaction)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_transaction(self, id_transaction: str):
        transaction = self.transaction_repository.read(id_transaction)
        self.transaction_repository.delete(id_transaction)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.transaction_repository, transaction)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[Transaction]:
        return self.transaction_repository.read()

    def get_day_interval(self, start_date: datetime, end_date: datetime):
        return list(filter(lambda transaction:
                           start_date <=
                           transaction.date_and_time
                           <= end_date,
                           self.transaction_repository.read()))

    def delete_day_interval(self, start_date: datetime, end_date: datetime):
        trans_list = self.transaction_repository.read()
        stergeri = 0
        for trans in filter(lambda x: start_date <= x.date_and_time <= end_date, trans_list):
            self.delete_transaction(trans.id_entity)
            stergeri += 1
        return stergeri

        self.undo_redo_service.clear_redo()
        deleted_operation = DeleteOperation(self.transaction_repository, stergeri)
        self.undo_redo_service.add_to_undo(deleted_operation)

    def delete_if_delete_medicament(self, id_deleted_med):
        trans_list = self.transaction_repository.read()
        for trans in trans_list:
            if trans.id_medicine == id_deleted_med:
                self.transaction_repository.delete(trans.id_entity)

    def delete_if_delete_member_card(self, id_deleted_member):
        trans_list = self.transaction_repository.read()
        for trans in trans_list:
            if trans.id_membership_card == id_deleted_member:
                self.transaction_repository.delete(trans.id_entity)

    def price(self, med_price, med_pres, is_member):
        if is_member is not None:
            if med_pres == 'Nu':
                return med_price * 0.9
            if med_pres == 'Da':
                return med_price * 0.85
        else:
            return med_price

    def descending_order_medicine(self):
        result = {transaction.id_medicine: 0 for transaction in
                  self.transaction_repository.read()}
        for i in self.transaction_repository.read():
            result[i.id_medicine] += int(i.number_pieces)
        return list(map(
            lambda x: self.medicine_repository.read(x),
            my_sorted(list(result), key=lambda x: result[x],
                      reverse=True)))

    def descending_order_card(self):
        result = {transaction.id_membership_card: 0 for transaction in
                  self.transaction_repository.read()}
        for i in self.transaction_repository.read():
            result[i.id_membership_card] += i.sale
        lst = list(result)
        return list(map(
            lambda x: self.membership_card_repository.read(x),
            my_sorted(lst, key=lambda x: result[x], reverse=True)))

    def number_of_sales_recursiv(self, medicament: Medicine, rez, i):
        if i == len(rez):
            return 0
        if medicament.id_entity == rez[i].id_medicine:
            return 1 + self.number_of_sales_recursiv(medicament, rez, i + 1)
        return self.number_of_sales_recursiv(medicament, rez, i + 1)
