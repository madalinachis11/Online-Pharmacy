from datetime import datetime, date

from Domain.medicament import Medicine
from Domain.membership_card import MembershipCard
from Domain.transaction import Transaction
from Repository.json_repository import JsonRepository
from Repository.repository import Repository
from Repository.transaction_repository import TransactionRepository
from utils import clear_file


def test_repository():
    filename = 'test_drugs.json'
    clear_file(filename)
    medicine_repository = JsonRepository(filename)
    added = Medicine('1', 'Paracetamol', 'Zentiva', 2, 'Nu')
    medicine_repository.create(added)
    assert medicine_repository.read(added.id_entity) == added

    filename = 'test_transaction.json'
    clear_file(filename)
    transaction_repository = JsonRepository(filename)
    added = Transaction('1', '2', '3', 50, 15.75, 22.75, datetime(2019, 11, 29, 15, 56))
    transaction_repository.create(added)
    assert transaction_repository.read(added.id_entity) == added

    filename = 'test_membership_card.json'
    clear_file(filename)
    membership_card_repository = JsonRepository(filename)
    added = MembershipCard('1',
                           'Chis',
                           'Madalina',
                           '6021012637281',
                           date(2002, 10, 24))
    membership_card_repository.create(added)
    assert membership_card_repository.read(added.id_entity) == added
