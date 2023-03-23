from Domain.transaction import Transaction
from Repository.repository import Repository


class TransactionValidator:

    def validate(self, other: Transaction):

        errors = []
        if other.id_entity is None:
            raise ValueError('\nID-ul introdus nu este un numar.')

        if int(other.id_entity) < 1:
            errors += '\nNu sunt acceptate ID-uri mai mici decat 1.'

        if other.id_entity in self.__id_storage:
            errors += f'\nExista deja o rezervare cu ID-ul {other.id_entity}.'

        if len(errors):
            raise ValueError(errors)
