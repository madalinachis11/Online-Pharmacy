
from typing import Dict, Optional, List, Union

import jsonpickle

from Domain.transaction import Transaction


class TransactionRepository:

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Transaction]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, transaction: Transaction) -> None:
        """
        Functia de adaugare a unei noi tranzactii.
        :param transaction: tranzactia luata in discutie.
        :return: noua tranzactie adaugata
        """

        transactions = self.__read_file()
        if self.read(transaction.id_transaction) is not None:
            raise KeyError(
                f'Exista deja o tranzactie cu id-ul {transaction.id_transaction}.')

        transactions[transaction.id_transaction] = transaction
        self.__write_file(transactions)

    def read(self,
             id_transaction=None) -> Union[Optional[Transaction], List[Transaction]]:
        """
        Functia citeste o tranzactie impreuna cu id-ul sau.
        """

        transactions = self.__read_file()
        if id_transaction:
            if id_transaction in transactions:
                return transactions[id_transaction]
            else:
                return None

        return list(transactions.values())

    def update(self, transaction: Transaction) -> None:
        """
        Functia de modificare a unei tranzactii.
        :param transaction: tranzactia luata in discutie.
        :return:noua tranzactie modificata
        """

        transactions = self.__read_file()
        if self.read(transaction.id_transaction) is None:
            msg = f'Nu exista o tranzactie cu id-ul {transaction.id_transaction} de actualizat.'
            raise KeyError(msg)

        transactions[transaction.id_transaction] = transaction
        self.__write_file(transactions)

    def delete(self, id_transaction: str) -> None:
        """
        Functia de stergere a unei tranzactii.
        :param id_transaction: id-ul tranzactiei.
        :return: tranzactiile fara tranzactia care dorim sa fie stearsa
        """
        transactions = self.__read_file()
        if self.read(id_transaction) is None:
            raise KeyError(
                f'Nu exista o tranzactie cu id-ul {id_transaction} pe care sa o stergem.')

        del transactions[id_transaction]
        self.__write_file(transactions)
