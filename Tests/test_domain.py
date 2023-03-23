from datetime import date, datetime

from Domain.medicament import Medicine
from Domain.membership_card import MembershipCard
from Domain.transaction import Transaction


def test_medicament():

    m = Medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
    assert m.id_entity == '1'
    assert m.name_medicine == 'NoSPA'
    assert m.producer == 'Cineva'
    assert m.price == 25.5
    assert m.medical_prescription == 'Da'


def test_membership_card():

    c = MembershipCard('1', 'Chis', 'Madalina', '6031102013915', date(2021, 11, 2))
    assert c.id_entity == '1'
    assert c.first_name_member == 'Chis'
    assert c.second_name_member == 'Madalina'
    assert c.CNP == '6031102013915'
    assert c.date_of_registration == date(2021, 11, 2)


def test_tranzactie():

    t = Transaction('1', '1', '11', 5, 5.75, 51.75, datetime(2012, 12, 12, 12, 12))
    assert t.id_entity == '1'
    assert t.id_medicine == '1'
    assert t.id_membership_card == '11'
    assert t.number_pieces == 5
    assert t.sale == 5.75
    assert t.total_sale == 51.75
    assert t.date_and_time == datetime(2012, 12, 12, 12, 12)


def test_domain():
    test_medicament()
    test_tranzactie()
    test_membership_card()
