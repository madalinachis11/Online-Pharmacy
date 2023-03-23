from datetime import date
from typing import List

from Domain.add_operation import AddOperation
from Domain.delete_operation import DeleteOperation
from Domain.membership_card import MembershipCard
from Domain.membership_card_validator import MembershipCardValidator
from Domain.update_operation import UpdateOperation
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class MembershipCardService:
    def __init__(self,
                 membership_card_repository: Repository,
                 membership_card_validator: MembershipCardValidator,
                 medicine_repository: Repository,
                 transaction_repository: Repository,
                 undo_redo_service: UndoRedoService):
        self.membership_card_repository = membership_card_repository
        self.membership_card_validator = membership_card_validator
        self.medicine_repository = medicine_repository
        self.transaction_repository = transaction_repository
        self.undo_redo_service = undo_redo_service

    def add_membership_card(self,
                            id_membership_card: int,
                            first_name_member: str,
                            second_name_member: str,
                            CNP: str):
        """
        Functia de adaugare a unui card de client.
        """
        date_of_registration = date.today()
        membership_card = MembershipCard(id_membership_card,
                                         first_name_member,
                                         second_name_member,
                                         CNP,
                                         date_of_registration)
        self.membership_card_validator.validate(membership_card)
        self.membership_card_repository.create(membership_card)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.membership_card_repository, membership_card)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_membership_card(self,
                               id_membership_card: int,
                               first_name_member: str,
                               second_name_member: str,
                               CNP: str):

        """
        Functia de modificare a unui card de client.
        """
        date_of_registration = date.today()

        membership_card_vechi = self.membership_card_repository.read(id_membership_card)
        membership_card = MembershipCard(id_membership_card,
                                         first_name_member,
                                         second_name_member,
                                         CNP,
                                         date_of_registration)
        self.membership_card_repository.update(membership_card)

        self.undo_redo_service.clear_redo()
        update_operation = UpdateOperation(self.membership_card_repository, membership_card, membership_card_vechi)
        self.undo_redo_service.add_to_undo(update_operation)

    def delete_membership_card(self,
                               id_membership_card: str):
        membership_card = self.membership_card_repository.read(id_membership_card)
        self.membership_card_repository.delete(id_membership_card)

        self.undo_redo_service.clear_redo()
        delete_operation = DeleteOperation(self.membership_card_repository, membership_card)
        self.undo_redo_service.add_to_undo(delete_operation)

    def get_all(self) -> List[MembershipCard]:
        return self.membership_card_repository.read()

    def read_by_id(self, id_membership_card):
        """
        Cauta un card dupa id-ul acestuia.
        :param id_membership_card: Id-ul cardului clientului pe care il cautam.
        :return: cardul clientului cu id-ul cautat.
        """
        return self.membership_card_repository.read(id_membership_card)

    def full_search(self, string_to_search):
        """
        Cauta full text.
        Functionalitate cu lambda.
        :param string_to_search: string-ul pe care il cautam.
        :return:
        """

        search_results = []
        client_list = self.membership_card_repository.read()
        for each_client in client_list:
            if each_client.search(string_to_search):
                search_results.append(each_client)
        return search_results

    def sort_dupa_reduceri_desc(self):
        """
        Ordoneaza descrescator cardurile de client dupa reducerile obtinute.
        :return:
        """

        client_list = self.membership_card_repository.read()
        client_list.sort(key=lambda x: x.reducere, reverse=True)
        return client_list
