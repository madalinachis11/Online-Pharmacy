from Domain.medicament import Medicine
from Domain.membership_card import MembershipCard
from Repository.membership_card_repository import MembershipCardRepository
from utils import clear_file


def test_membership_card_repository():
    filename = 'test_membership_card.json'
    clear_file(filename)
    membership_card_repository = MembershipCardRepository(filename)
    added = MembershipCard('1',
                           'Chis',
                           'Madalina',
                           '6023475637281',
                           '11.07.2002',
                           '12.11.2021')
    membership_card_repository.create(added)
    assert membership_card_repository.read(added.id_membership_card) == added