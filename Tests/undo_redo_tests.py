from datetime import datetime, date

from Domain.medicament import Medicine
from Domain.medicament_validator import MedicamentValidator
from Domain.membership_card import MembershipCard
from Domain.membership_card_validator import MembershipCardValidator
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Repository.json_repository import JsonRepository
from Service.medicament_service import MedicamentService
from Service.membership_card_service import MembershipCardService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_undo_redo_medicament_crud():
    medicine_repository = JsonRepository('test_ur_car.json')
    transaction_repository = \
        JsonRepository('test_ur_transaction.json')
    medicament_validator = MedicamentValidator()
    undo_redo_service = UndoRedoService()
    medicament_service = MedicamentService(medicine_repository,
                                           medicament_validator,
                                           undo_redo_service)

    medicament_service.add_medicine('1', 'Paracetamol', 'Zentiva', 70, 'Nu')
    assert medicament_service.get_all() == \
           [Medicine(id_medicine='1',
                     name_medicine='Paracetamol',
                     producer='Zentiva',
                     price=70,
                     medical_prescription='Da')]
    undo_redo_service.do_undo()
    assert medicament_service.get_all() == []
    undo_redo_service.do_redo()
    assert medicament_service.get_all() == \
           [Medicine(id_medicine='1',
                     name_medicine='Paracetamol',
                     producer='Zentiva',
                     price=70,
                     medical_prescription='Da')]

    medicament_service.update_medicine('1', 'Paracetamol', 'Zentiva', 80, 'Da')
    assert medicament_service.get_all() == \
           [Medicine(id_medicine='1',
                     name_medicine='Paracetamol',
                     producer='Zentiva',
                     price=80,
                     medical_prescription='Da')]

    undo_redo_service.do_undo()
    assert medicament_service.get_all() == \
           [Medicine(id_medicine='1',
                     name_medicine='Dacia',
                     producer='Toti',
                     price=80,
                     medical_prescription='Da')]

    undo_redo_service.do_redo()
    assert medicament_service.get_all() == \
           [Medicine(id_medicine='1',
                     name_medicine='Dacia',
                     producer='Toti',
                     price=80,
                     medical_prescription='Yes')]

    medicament_service.delete_medicine('1')
    assert medicament_service.get_all() == []
    undo_redo_service.do_undo()

    undo_redo_service.do_redo()
    medicament_service.add_medicine('1', 'Dacia', 'Toti', 80, 'Da')


def test_undo_redo_card_crud():
    membership_card_repository = JsonRepository('test_ur_card.json')
    undo_redo_service = UndoRedoService()
    medicine_repository = JsonRepository('test_ur_car.json')
    membership_card_validator = MembershipCardValidator()
    transaction_repository = \
        JsonRepository('test_ur_transaction.json')

    membership_card_service = MembershipCardService(membership_card_repository,
                                                    membership_card_validator,
                                                    medicine_repository,
                                                    transaction_repository,
                                                    undo_redo_service)
    date_of_registration = date.today()
    membership_card_service.add_membership_card(1, 'Tudor', 'Dana',
                                                '2030512728394')
    assert membership_card_service.get_all() == \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Tudor',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]
    undo_redo_service.do_undo()
    assert membership_card_service.get_all() == []
    undo_redo_service.do_redo()
    assert membership_card_service.get_all() == \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Tudor',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]
    membership_card_service.update_membership_card(1, 'Dulgheru', 'Dana',
                                                   '2030512728394')
    assert membership_card_service.get_all() ==  \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Dulgheru',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]

    undo_redo_service.do_undo()
    assert membership_card_service.get_all() == \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Tudor',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]
    undo_redo_service.do_redo()
    assert membership_card_service.get_all() ==  \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Dulgheru',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]
    membership_card_service.delete_membership_card('1')
    assert membership_card_service.get_all() == []
    undo_redo_service.do_undo()
    assert membership_card_service.get_all() ==  \
           [MembershipCard(id_membership_card='1',
                           first_name_member='Dulgheru',
                           second_name_member='Dana',
                           CNP='2030512728394',
                           date_of_registration=date.today)]
    undo_redo_service.do_redo()
    assert membership_card_service.get_all() == []

    membership_card_service.add_membership_card(1, 'Popa', 'Dan', '6020326070912')
    membership_card_service.add_membership_card(2, 'Hritac', 'Rodica', '6601225849274')
    membership_card_service.add_membership_card(3, 'Scripcariu', 'Marcel', '1080307390212')
    membership_card_service.add_membership_card(4, 'Dima', 'Maria', '2931017392848')


def test_undo_redo_transaction():
    medicine_repository = JsonRepository('test_ur_car.json')
    membership_card_repository = JsonRepository('test_ur_card.json')
    transaction_repository = JsonRepository('test_ur_transaction.json')
    transaction_validator = TransactionValidator()
    undo_redo_service = UndoRedoService()
    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             medicine_repository,
                                             membership_card_repository,
                                             undo_redo_service)

    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=100,
                        sale=50,
                        total_sale=250,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]
    undo_redo_service.do_undo()
    assert transaction_service.get_all() == []
    undo_redo_service.do_redo()
    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=100,
                        sale=20,
                        total_sale=150,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]

    transaction_service.update_transaction('1', '1', '1',
                                           200, datetime(2012, 12, 12, 12, 12))
    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=200,
                        sale=45,
                        total_sale=250,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]
    undo_redo_service.do_undo()
    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=100,
                        sale=20,
                        total_sale=150,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]
    undo_redo_service.do_redo()
    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=200,
                        sale=50,
                        total_sale=250,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]

    transaction_service.delete_transaction('1')
    assert transaction_service.get_all() == []
    undo_redo_service.do_undo()
    assert transaction_service.get_all() == \
           [Transaction(id_transaction='1',
                        id_medicine='1',
                        id_membership_card='1',
                        number_pieces=200,
                        sale=50,
                        total_sale=250,
                        date_and_time=datetime(2012, 12, 12, 12, 12))]
    undo_redo_service.do_redo()
    assert transaction_service.get_all() == []

    transaction_service.add_transaction('1', '1',
                                        '2', 100, datetime(2010, 10, 10, 10, 10))
    transaction_service.add_transaction('2', '3',
                                        '4', 500, datetime(2009, 9, 9, 9, 9))
    transaction_service.add_transaction('3', '2',
                                        '1', 200, datetime(2015, 12, 15, 15, 15))
    transaction_service.add_transaction('4', '1',
                                        '', 1030, datetime(2016, 10, 16, 16, 16))
    transaction_service.add_transaction('5', '4',
                                        '', 980, datetime(2012, 12, 12, 12, 12))
    transaction_service.delete_day_interval(datetime(2020, 10, 10, 10, 10), datetime(2022, 10, 10, 10, 10))
    assert transaction_service.get_all() == []
    undo_redo_service.do_undo()
    assert len(transaction_service.get_all()) == 5
    undo_redo_service.do_redo()
    assert transaction_service.get_all() == []


def test_all():
    clear_file('test_ur_car.json')
    clear_file('test_ur_card.json')
    clear_file('test_ur_transaction.json')
    test_undo_redo_medicament_crud()


