from Domain.entity import Entity
from datetime import datetime


class Transaction(Entity):

    def __init__(self,
                 id_transaction,
                 id_medicine,
                 id_membership_card,
                 number_pieces,
                 sale,
                 total_sale,
                 date_and_time: datetime):
        super().__init__(id_transaction)
        self.__id_medicine = id_medicine
        self.__id_membership_card = id_membership_card
        self.__number_pieces = number_pieces
        self.__sale = sale
        self.__total_sale = total_sale
        self.__date_and_time = date_and_time

    @property
    def id_medicine(self):
        return self.__id_medicine

    @id_medicine.setter
    def id_medicine(self, value):
        self.__id_medicine = value

    @property
    def id_membership_card(self):
        return self.__id_membership_card

    @id_membership_card.setter
    def id_membership_card(self, value):
        self.__id_membership_card = value

    @property
    def number_pieces(self):
        return self.__number_pieces

    @number_pieces.setter
    def number_pieces(self, value):
        self.__number_pieces = value

    @property
    def sale(self):
        return self.__sale

    @sale.setter
    def sale(self, value):
        self.__total_sale = value

    @property
    def total_sale(self):
        return self.__total_sale

    @total_sale.setter
    def total_sale(self, value):
        self.total_sale = value

    @property
    def date_and_time(self):
        return self.__date_and_time

    @date_and_time.setter
    def date_and_time(self, value: datetime):
        self.__date_and_time = value

    def __str__(self):
        return f'ID : {self.id_entity} -ID medicament:  {self.id_medicine},' \
               f'ID card client: {self.id_membership_card},Numarul bucatilor : {self.number_pieces},' \
               f'sale: {self.sale}, total_sale: {self.total_sale},' \
               f'Data si ora : {str(self.date_and_time)}'
