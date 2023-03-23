from datetime import datetime, date
from fileinput import filename

from Domain.medicament import Medicine
from Domain.medicament_validator import MedicamentValidator
from Domain.membership_card_validator import MembershipCardValidator
from Domain.transaction import Transaction
from Domain.transaction_validator import TransactionValidator
from Repository import medicine_repository
from Repository.json_repository import JsonRepository
from Repository.repository import Repository
from Service import medicament_service, transaction_service
from Service.medicament_service import MedicamentService
from Service.membership_card_service import MembershipCardService
from Service.transaction_service import TransactionService
from utils import clear_file


def test_medicament_service():
    def test_add_medicament():
        filename = 'test_med_service.json'
        clear_file(filename)
        medicine_repository = JsonRepository(filename)
        medicament_validator = MedicamentValidator()
        service = MedicamentService(medicine_repository,
                                    medicament_validator)

        service.add_medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
        assert len(service.get_all()) == 1
        added = medicine_repository.read('1')
        assert added is not None
        assert added.id_entity == '1'
        assert added.name_medicine == "NoSPA"
        assert added.producer == 'Cineva'
        assert added.price == 25.5
        assert added.medical_prescription == 'Da'

        try:
            service.add_medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

    def test_delete_medicament():
        filename = 'test_med_service.json'
        clear_file(filename)
        medicine_repository = JsonRepository(filename)
        medicament_validator = MedicamentValidator()
        service = MedicamentService(medicine_repository,
                                    medicament_validator)
        service.add_medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
        service.add_medicine('2', 'NoSPA', 'Cineva', 25.5, 'Da')

        try:
            service.delete_medicine('3')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

        service.delete_medicine('1')
        assert len(service.get_all()) == 1
        deleted = medicine_repository.read('1')
        assert deleted is None
        remaining = medicine_repository.read('2')
        assert remaining is not None
        assert remaining.id_entity == '2'
        assert remaining.nume == "NoSPA"
        assert remaining.producator == 'Cineva'
        assert remaining.pret == 25.5
        assert remaining.reteta == 'Da'

    def test_update_medicament():
        filename = 'test_med_service.json'
        clear_file(filename)
        medicine_repository = JsonRepository(filename)
        medicament_validator = MedicamentValidator()
        service = MedicamentService(medicine_repository,
                                    medicament_validator)
        service.add_medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
        service.add_medicine('2', 'NoSPA', 'Cineva', 25.5, 'Da')

        service.update_medicine('1', 'NoSPA', 'Cineva', 25.5, 'Da')
        updated = medicine_repository.read('1')
        assert updated is not None
        assert updated.id_entity == '1'
        assert updated.name_medicine == "NoSPA"
        assert updated.producer == 'Cineva'
        assert updated.price == 50
        assert updated.medical_prescription == 'Da'

        unchanged = medicine_repository.read('2')
        assert unchanged is not None
        assert unchanged.id_entitate == '2'
        assert unchanged.nume == "NoSPA"
        assert unchanged.producator == 'Cineva'
        assert unchanged.pret == 50
        assert unchanged.reteta == 'Da'

        try:
            service.update_medicine('3', 'NoSPA', 'Cineva', 25.5, 'Da')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False


def test_transaction_service():
    def test_add_transaction():
        filename = 'test_trans_service.json'
        clear_file(filename)
        transaction_repository = JsonRepository(filename)
        transaction_validator = TransactionValidator()
        service = TransactionService(transaction_repository)

        service.add_transaction('1', '1', '1', 200,
                                datetime(2020, 7, 11, 11, 11))
        assert len(service.get_all()) == 1
        added = transaction_repository.read('1')
        assert added is not None
        assert added.id_entity == '1'
        assert added.id_medicine == '1'
        assert added.id_membership_card == '1'
        assert added.number_pieces == 200
        assert added.sale == 12.50
        assert added.total_sale == 100.50
        assert added.date_of_registration == datetime(2020, 7, 11, 11, 11)

        try:
            service.add_transaction('1', '1', '1', 200,
                                    datetime(2020, 7, 11, 11, 11))
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

    def test_delete_transaction():
        filename = 'test_med_service.json'
        clear_file(filename)
        transaction_repository = JsonRepository(filename)
        transaction_repository_validator = TransactionValidator()
        service = TransactionService(transaction_repository)
        service.add_transaction('1', '1', '1', 200, datetime(2020, 7, 11, 11, 11))
        service.add_transaction('2', '1', '1', 200, datetime(2020, 7, 11, 11, 11))

        try:
            service.delete_transaction('3')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

        service.delete_transaction('1')
        assert len(service.get_all()) == 1
        deleted = transaction_repository.read('1')
        assert deleted is None
        remaining = transaction_repository.read('2')
        assert remaining is not None
        assert remaining.id_entity == '2'
        assert remaining.id_medicine == '1'
        assert remaining.id_membership_card == '1'
        assert remaining.numer_pieces == 200
        assert remaining.sale == 12.50
        assert remaining.total_Ssale == 100.50
        assert remaining.date_of_registration == datetime(2012, 12, 12, 12, 12)

    def test_update_transaction():
        filename = 'test_trans_service.json'
        clear_file(filename)
        transaction_repository = JsonRepository(filename)
        transaction_validator = MedicamentValidator()
        service = TransactionService(transaction_repository)
        service.add_transaction('1', '1', '1', 200,
                                datetime(2020, 7, 11, 11, 11))
        service.add_transaction('2', '1', '1', 200,
                                datetime(2000, 7, 11, 11, 11))

        service.update_transaction('1', '1', '1', 200, datetime(2000, 7, 11, 11, 11))
        updated = transaction_repository.read('1')
        assert updated is not None
        assert updated.id_entity == '1'
        assert updated.id_medicine == '1'
        assert updated.id_membership_card == '1'
        assert updated.numer_pieces == 201
        assert updated.date_of_registration == datetime(2020, 7, 11, 11)

        unchanged = transaction_repository.read('2')
        assert unchanged is not None
        assert unchanged.id_entitate == '2'
        assert unchanged.id_medicine == '1'
        assert unchanged.id_membership_card == '1'
        assert unchanged.numer_pieces == 200
        assert unchanged.date_of_registration == datetime(2020, 7, 11, 11)

        try:
            service.update_transaction('3', '1', '1', 200, datetime(2020, 7, 11, 11, 11))
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

def test_afisare_tranzactii_din_interval():
    filename = 'test_tranzactie.txt'
    clear_file(filename)
    transaction_repository = JsonRepository(filename)
    transaction_validator = TransactionValidator(transaction_repository)

    filename = 'test_medicament.txt'
    clear_file(filename)
    medicine_repository = JsonRepository(filename)
    medicament_validator = MedicamentValidator()
    medicament_service = MedicamentService(medicine_repository, medicament_validator)
    medicament_service.add_medicine('100', 'jshnn', 'ggffk', 10, 'Da')
    medicament_service.add_medicine('101', 'ksjdn', 'LKjsm', 15, 'Nu')

    filename = 'test_client.txt'
    clear_file(filename)
    membership_card_repository = Repository(filename)
    membership_card_validator = MembershipCardValidator()
    membership_card_service = MembershipCardService(membership_card_repository, membership_card_validator)
    membership_card_service.add_membership_card(100, 'Sima', 'Felix', '5010116010389')

    service = TransactionService(transaction_repository,
                                 transaction_validator,
                                 medicine_repository,
                                 membership_card_repository)

    service.add_transaction('100', '100', '100', 100,
                            datetime(2020, 9, 10, 22, 22))
    service.add_transaction('101', '101', '100', 200,
                            datetime(2020, 10, 8, 10, 10))
    service.add_transaction('102', '100', '100', 100,
                            datetime(2020, 10, 9, 19, 19))
    service.add_transaction('103', '101', '100', 100,
                            datetime(2020, 10, 10, 10, 10))
    service.add_transaction('104', '100', '100', 100,
                            datetime(2020, 11, 10, 10, 10))
    service.get_day_interval(datetime(2020, 10, 7, 10, 10), datetime(2020, 10, 11, 10, 10))
    lista_tranzactii = transaction_service.get_day_interval(datetime(2020, 10, 7, 10, 10),
                                                            datetime(2020, 10, 11, 10, 10))
    assert len(lista_tranzactii) == 3

def test_delete_tranzactii_din_interval():
    filename = 'test_tranzactie.txt'
    clear_file(filename)
    tranzactie_repository = JsonRepository(filename)
    tranzactie_validator = TransactionValidator(tranzactie_repository)
    masina_repository = Repository(filename)
    masina_validator = MedicamentValidator()
    masina_service = MedicamentService(masina_repository, masina_validator)
    medicament_service.add_medicine('100', 'Porche',2005 , 10000, 'da')
    medicament_service.add_medicine('101', 'Dacia',2009, 15000, 'da')

    filename = 'test_client.txt'
    clear_file(filename)
    clear_file('client_html_test.txt')
    client_repository = Repository(filename)
    client_validator = MembershipCardValidator()
    client_service = MembershipCardService(client_repository, client_validator)
    client_service.add_membership_card(100, 'Sima', 'Felix', '5010116010389')

    service = TransactionService(tranzactie_repository,tranzactie_validator, masina_repository, client_repository)

    service.add_transaction('100', '100', '100', 100,
                            datetime(2020, 9, 10, 10, 10))
    service.add_transaction('101', '101', '100', 100,
                            datetime(2020, 10, 8, 10, 10))
    service.add_transaction('102', '100', '100', 100,
                            datetime(2020, 10, 9, 10, 10))
    service.add_transaction('103', '101', '100', 100,
                            datetime(2020, 10, 10, 10, 10))
    service.add_transaction('104', '100', '100', 100,
                            datetime(2020, 11, 10, 10, 10))
    service.delete_day_interval(datetime(2020, 10, 7, 10, 10),
                                datetime(2020, 10, 11, 10, 10))
    lista_tranzactii = service.get_all()
    assert len(lista_tranzactii) == 2
    assert lista_tranzactii[0].id_entity == '100'
    assert lista_tranzactii[1].id_entity == '104'

def test_full_search_medicamente():
    clear_file('test_medicament.txt')
    clear_file('test_tranzactie.txt')
    medicine_repository = Repository('test_masina.txt')
    masina_validator = MedicamentValidator()
    masina_service = MedicamentService(medicine_repository, masina_validator)
    masina_service.add_medicine('100', 'Ketonal', 'Eu', 15.18, 'Da')
    masina_service.add_medicine('101', 'Colebil', 'Tu', 15, 'Nu')
    assert len(masina_service.full_search('Nu')) == 2

def test_full_search_clienti():
    clear_file('test_client.txt')
    clear_file('test_tranzactie.txt')
    membership_card_repository = Repository('test_client.txt')
    membership_card_validator = MembershipCardValidator()
    membership_card_service = MembershipCardService(membership_card_repository,
                                                    membership_card_validator)
    membership_card_service.add_membership_card(15, 'Dona',
                                                'Alba',
                                                '6010113410234')
    membership_card_service.add_membership_card(16, 'Sheperd',
                                                'Derek',
                                                '5010113410234')
    membership_card_service.add_membership_card(17, 'Grey',
                                                'Meredith',
                                                '6040113410257')
    assert len(membership_card_service.full_search('Derek')) == 1

def test_medicamente_ordonate():
    clear_file('client_test.txt')
    clear_file('test_tranzactie.txt')
    clear_file('test_masina.txt')
    medicament_repository = Repository('test_masina.txt')
    medicament_validator = MedicamentValidator()
    tranzactie_repository = JsonRepository('test_tranzactie.txt')
    tranzactie_validator = TransactionValidator(tranzactie_repository)
    medicament_service = MedicamentService(medicament_repository,
                                           medicament_validator)
    medicament_service.add_medicine('100', 'Magnerot', 'Panamera', 100, 'Da')
    medicament_service.add_medicine('101', 'Corlentor', 'Logan', 150, 'Nu')

    client_repository = Repository('client_test.txt')

    client_validator = MembershipCardValidator()
    client_service = MembershipCardService(client_repository, client_validator)
    tranzactie_service = TransactionService(tranzactie_repository,
                                            tranzactie_validator,
                                            medicament_repository,
                                            client_repository)

    client_service.add_membership_card(15, 'Dona', 'Alba', '6010113410234')
    client_service.add_membership_card(16, 'Sheperd', 'Derek', '5010113410234')
    client_service.add_membership_card(17, 'Grey', 'Meredith', '6040113410257')

    tranzactie_service.add_transaction('100', '100', '15', 100,
                                       datetime(2020, 9, 10, 10, 10))
    tranzactie_service.add_transaction('101', '101', '16', 200,
                                       datetime(2020, 10, 8, 10, 10))
    tranzactie_service.add_transaction('102', '100', '17', 400,
                                       datetime(2020, 10, 9, 10, 10))

    lista_ordonata = tranzactie_service.descending_order_medicine()
    assert lista_ordonata[0].id_masina == '2'
    assert lista_ordonata[1].id_masina == '1'


def test_membership_card_service():
    def test_add_membership_card():
        filename = 'test_membcard_service.json'
        clear_file(filename)
        membership_card_repository = JsonRepository(filename)
        membership_card_validator = MembershipCardValidator()
        medicine_repository = JsonRepository(filename)
        transaction_repository = JsonRepository(filename)
        service = MembershipCardService(membership_card_repository,
                                        membership_card_validator,
                                        medicine_repository,
                                        transaction_repository)

        service.add_membership_card(1, 'Chis', 'Madalina', '6031102013915')
        assert len(service.get_all()) == 1
        added = transaction_repository.read('1')
        assert added is not None
        assert added.id_entity == 1
        assert added.first_name_member == 'Chis'
        assert added.second_name_member == 'Madalina'
        assert added.CNP == '6031102013915'

        try:
            service.add_membership_card(1, 'Chis', 'Madalina', '6031102013915')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

    def test_delete_membership_card():
        filename = 'test_membcard_service.json'
        clear_file(filename)
        membership_card_repository = JsonRepository(filename)
        membership_card_validator = MembershipCardValidator()
        service = TransactionService(membership_card_repository, )
        service.add_transaction(1, 'Chis', 'Madalina', '6031102013915')
        service.add_transaction(2, 'Chis', 'Madalina', '6031102013915')

        try:
            service.delete_transaction('3')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False

        service.delete_transaction('1')
        assert len(service.get_all()) == 1
        deleted = membership_card_repository.read('1')
        assert deleted is None
        remaining = membership_card_repository.read('2')
        assert remaining is not None
        assert remaining.id_entity == 2
        assert remaining.first_name_member == 'Chis'
        assert remaining.second_name_member == 'Madalina'
        assert remaining.CNP == '6031102013915'

    def test_update_membership_card():
        filename = 'test_membcard_service.json'
        clear_file(filename)
        membership_card_repository = JsonRepository(filename)
        membership_card_validator = MembershipCardValidator()
        medicine_repository = JsonRepository(filename)
        transaction_repository = JsonRepository(filename)
        service = MembershipCardService(membership_card_repository,
                                        membership_card_validator,
                                        medicine_repository,
                                        transaction_repository)
        service.add_membership_card(1, 'Chis', 'Madalina', '6031102013915')
        service.add_membership_card(2, 'Chis', 'Madalina', '6031102013915')

        service.update_membership_card(1, 'Chis', 'Madalina', '6031102013915')
        updated = membership_card_repository.read('1')
        assert updated is not None
        assert updated.id_entity == '1'
        assert updated.first_name_member == 'Chis'
        assert updated.second_name_member == 'Madalina'
        assert updated.CNP == '60031102013915'

        unchanged = membership_card_repository.read('2')
        assert unchanged is not None
        assert unchanged.id_entitate == 2
        assert unchanged.first_name_member == 'Chis'
        assert unchanged.second_name_member == 'Madalina'
        assert unchanged.CNP == '60031102013915'

        try:
            service.update_membership_card(3, 'Chis', 'Madalina',
                                           '6031102013915')
            assert False
        except KeyError:
            assert True
        except Exception:
            assert False


def test_all_services():
    test_medicament_service()
    test_transaction_service()
    test_membership_card_service()


