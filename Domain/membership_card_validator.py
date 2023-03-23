from datetime import date
from Domain.membership_card import MembershipCard


class MembershipCardValidator:

    def validate(self, other: MembershipCard):
        errors = ''
        try:
            test_CNP = int(other.CNP)
        except KeyError as ke:
            errors += '\n' + str(ke)
        if int(other.id_entity) < 1:
            raise ExceptieID('\n ID-ul trebuie sa fie strict pozitiv.')

        if len(other.CNP) < 13:
            errors += '\nCNP-ul are o lungime invalida.'

        if type(other.date_of_birth) is not date:
            errors += '\nData nasterii are un format invalid.'

        if type(other.date_of_registration) is not date:
            errors += '\nData inregistrarii are un format invalid.'

        if len(errors):
            raise ValueError(errors)
