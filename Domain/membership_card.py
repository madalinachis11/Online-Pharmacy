from Domain.entity import Entity
from datetime import date


class MembershipCard(Entity):

    def __init__(self, id_membership_card, first_name_member, second_name_member, CNP, date_of_registration):
        super().__init__(id_membership_card)
        self.__first_name_member = first_name_member
        self.__second_name_member = second_name_member
        self.__CNP = CNP
        an = int('20' + CNP[1] + CNP[2])
        if an > date.today().year:
            an = int('19' + CNP[1] + CNP[2])
        luna = int(CNP[3] + CNP[4])
        zi = int(CNP[5] + CNP[6])
        self.__date_of_birth = date(an, luna, zi)

        self.__date_of_registration = date_of_registration
        self.__reducere = 0

    @property
    def first_name_member(self):
        return self.__first_name_member

    @property
    def second_name_member(self):
        return self.__second_name_member

    @property
    def full_name(self):
        return self.__first_name_member + ' ' + self.__second_name_member

    @property
    def CNP(self):
        return self.__CNP

    @CNP.setter
    def CNP(self, value):
        self.__CNP = value

    @property
    def date_of_birth(self):
        return self.__date_of_birth

    @property
    def date_of_registration(self):
        return self.__date_of_registration

    @date_of_registration.setter
    def date_of_registration(self, value: date):
        self.__date_of_registration = value

    @property
    def reducere(self):
        return self.__reducere

    @reducere.setter
    def reducere(self, value):
        self.__reducere = value

    def search(self, string_to_search):
        for prop in [self.full_name, str(self.CNP), str(self.__date_of_registration), str(self.__date_of_birth)]:
            if string_to_search in prop:
                return True
        return False

    def __str__(self):
        return f'ID : {self.id_entity} ' \
               f';-Cardul clientului NUME : {self.first_name_member}; ' \
               f'PRENUME: {self.second_name_member};  CNP : {self.CNP} ;' \
               f' nascut in : {self.date_of_birth} ; inregistrat in : {self.date_of_registration} ; '  \
               f' reducere: {self.__reducere}'
