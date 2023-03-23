from Domain.medicament import Medicine
from Domain.transaction import Transaction
from Repository.medicine_repository import MedicamentRepository
from Repository.transaction_repository import TransactionRepository
from utils import clear_file


def test_medicine_repository():
    filename = 'test_transaction.json'
    clear_file(filename)
    transaction_repository = TransactionRepository(filename)
    added = Transaction('1', '2', '3', 50, (2019, 11, 29, 15, 56))
    transaction_repository.create(added)
    assert transaction_repository.read(added.id_transaction) == added