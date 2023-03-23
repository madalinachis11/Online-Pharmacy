from typing import Dict, Optional, List, Union

import jsonpickle

from Domain.membership_card import MembershipCard


class MembershipCardRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, MembershipCard]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, membership_card: MembershipCard) -> None:
        """
        Functia de adaugare a unui card de client.
        :param membership_card: cardul de client
        :return: un nou card de client
        """

        membership_cards = self.__read_file()
        if self.read(membership_card.id_membership_card) is not None:
            raise KeyError(
                f'Exista deja un card cu id-ul {membership_card.id_membership_card}.')

        membership_cards[membership_card.id_membership_card] = membership_card
        self.__write_file(membership_cards)

    def read(self,
             id_membership_card=None) -> Union[Optional[MembershipCard], List[MembershipCard]]:
        """
        Functia citeste un card de client impreuna cu id-ul sau.
        """

        membership_cards = self.__read_file()
        if id_membership_card:
            if id_membership_card in membership_cards:
                return membership_cards[id_membership_card]
            else:
                return None

        return list(membership_cards.values())

    def update(self,
               membership_card: MembershipCard) -> None:
        """
        Functia de modificare a unei tranzactii.
        :param membership_card: cardul de client.
        :return: noul medicament modificat
        """

        membership_cards = self.__read_file()
        if self.read(membership_card.id_membership_card) is None:
            msg = f'Nu exista un card cu id-ul {membership_card.id_membership_card} de actualizat.'
            raise KeyError(msg)

        membership_cards[membership_card.id_membership_card] = membership_card
        self.__write_file(membership_cards)

    def delete(self,
               id_membership_card: str) -> None:
        """
        Functia de stergere a unui card de client.
        :param id_membership_card: id-ul cardului de client
        :return: cardurile de client fara cardul pe care am dorit sa-l stergem
        """
        membership_cards = self.__read_file()
        if self.read(id_membership_card) is None:
            raise KeyError(
                f'Nu exista un card cu id-ul {id_membership_card} pe care sa il stergem.')

        del membership_cards[id_membership_card]
        self.__write_file(membership_cards)
