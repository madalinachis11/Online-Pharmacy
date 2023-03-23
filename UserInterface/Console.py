
from Service.medicament_service import MedicamentService
from Service.membership_card_service import MembershipCardService
from Service.transaction_service import TransactionService
from datetime import datetime

from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 medicament_service: MedicamentService,
                 transaction_service: TransactionService,
                 membership_card_service: MembershipCardService,
                 undo_redo_service: UndoRedoService):
        self.medicament_service = medicament_service
        self.transaction_service = transaction_service
        self.membership_card_service = membership_card_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[medicament|trans|membcard] - adaugare medicament sau tranzactie sau card de client.')
        print('u[medicament|trans|membcard] - update medicament sau tranzactie sau card de client.')
        print('d[medicament|trans|membcard] - delete medicament sau tranzactie sau card de client.')
        print('s[medicament|trans|membcard] - show all medicament sau tranzactie sau card de client.')
        print('ainterval-Afișarea tuturor tranzacțiilor dintr-un interval de zile dat.')
        print('sinterval-Stergerea tuturor tranzacțiilor dintr-un interval de zile dat.')
        print('random - genereaza n medicamente')
        print('fullsearch - Căutare medicamente și clienți. Căutare full text.')
        print('orddesc - Afișarea medicamentelor ordonate descrescător după numărul de vânzări.')
        print('scumpire - Scumpirea cu un procentaj dat a tuturor'
              ' medicamentelor cu prețul mai mic decât o valoare dată.')
        print('reducere - Afișarea cardurilor client ordonate descrescător după valoarea reducerilor obținute.')
        print('undo - Undo.')
        print('redo - Redo.')
        print('x. Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea: ')

            if opt == 'amedicament':
                self.handle_add_medicament()
            elif opt == 'atrans':
                self.handle_add_transaction()
            elif opt == 'amembcard':
                self.handle_add_membership_card()
            elif opt == 'umedicament':
                self.handle_update_medicament()
            elif opt == 'utrans':
                self.handle_update_transaction()
            elif opt == 'umembcard':
                self.handle_update_membership_card()
            elif opt == 'dmedicament':
                self.handle_delete_medicament()
            elif opt == 'dtrans':
                self.handle_delete_transaction()
            elif opt == 'dmembcard':
                self.handle_delete_membership_card()
            elif opt == 'smedicament':
                self.handle_show_all(self.medicament_service.get_all())
            elif opt == 'strans':
                self.handle_show_all(self.transaction_service.get_all())
            elif opt == 'smembcard':
                self.handle_show_all(self.membership_card_service.get_all())
            elif opt == 'ainterval':
                self.handle_search_day_interval()
            elif opt == 'sinterval':
                self.handle_delete_day_interval()
            elif opt == 'random':
                self.handle_random_medicamente()
            elif opt == 'fullsearch':
                self.handle_full_text_search()
            elif opt == 'orddesc':
                self.handle_show_descending_medicine()
            elif opt == 'scumpire':
                self.handle_scumpire_cu_procentaj()
            elif opt == 'reducere':
                self.handle_show_descending_card()
            elif opt == 'undo':
                self.undo_redo_service.do_undo()
            elif opt == 'redo':
                self.undo_redo_service.do_redo()
            elif opt == 'x':
                break
            else:
                print('Comanda invalida, reincearca.')

    def handle_add_medicament(self):
        try:
            id_medicine = input('Introduceti id-ul medicamentului: ')
            name_medicine = input('Introduceti numele medicamentului: ')
            producer = input('Introduceti producatorul medicamentului: ')
            price = float(input('Introduceti pretul medicamentului: '))
            medical_prescription = input('Introduceti Da daca medicamentul necesita o prescriptie'
                                         ' medicala sau nu Nu in caz contrar: ')

            self.medicament_service.add_medicine(id_medicine,
                                                 name_medicine,
                                                 producer,
                                                 price,
                                                 medical_prescription)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_medicament(self):
        try:
            id_medicament_modificat = input("introduceti id-ul medicamentului pe care doriti sa il modificati:")
            name_medicine = input('Introduceti numele medicamentului: ')
            producer = input('Introduceti producatorul medicamentului: ')
            price = float(input('Introduceti pretul medicamentului: '))
            medical_prescription = input(
                'Introduceti Da daca medicamentul necesita o prescriptie medicala sau nu Nu in caz contrar: ')

            self.medicament_service.update_medicine(id_medicament_modificat,
                                                    name_medicine,
                                                    producer,
                                                    price,
                                                    medical_prescription)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_medicament(self):
        try:
            id_medicament = input("Introduceti id-ul medicamentului pe care doriti sa il stergeti: ")
            self.medicament_service.delete_medicine(id_medicament)
            self.transaction_service.delete_if_delete_medicament(id_medicament)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_show_all(self, objects):
        for obj in objects:
            print(obj)

    def handle_show_all_trans(self, trans):
        for tran in trans:
            print(tran)
            price = self.medicament_service.medicament_repository.read(tran.id_medicine).price
            print(price)
            prescriptie = self.medicament_service.medicament_repository.read(tran.id_medicine).medical_prescription
            print(" pretul tranzactiei: " + self.transaction_service.price(price, prescriptie, tran.id_membership_car))

    def handle_add_transaction(self):
        try:
            id_transaction = input('Introduceti id-ul tranzactiei: ')
            id_medicine = input('Introduceti id-ul medicamentului: ')
            id_membership_card = input('Introduceti id-ul cardului de client: ')
            if id_membership_card == '':
                id_membership_card = None
            number_pieces = int(input('Introduceti numarul de bucati: '))
            ziua = int(input('Introduceti ziua tranzactiei: '))
            luna = int(input('Introduceti luna tranzactiei: '))
            an = int(input('Introduceti anul tranzactiei: '))
            ora = int(input('Introduceti ora tranzactiei: '))
            minut = int(input('Introduceti minutul tranzactiei: '))
            date_and_time = datetime(an, luna, ziua, ora, minut)

            self.transaction_service.add_transaction(id_transaction,
                                                     id_medicine,
                                                     id_membership_card,
                                                     number_pieces,
                                                     date_and_time)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_transaction(self):
        try:
            id_tranzactie_modificat = input("introduceti id-ul tranzactiei pe care doriti sa o modificati:")
            id_medicine = input('Introduceti id-ul medicamentului: ')
            id_membership_card = input('Introduceti id-ul cardului de client: ')
            number_pieces = int(input('Introduceti numarul de bucati al tranzactiei: '))
            ziua = int(input('Introduceti ziua tranzactiei: '))
            luna = int(input('Introduceti luna tranzactiei: '))
            an = int(input('Introduceti anul tranzactiei: '))
            ora = int(input('Introduceti ora tranzactiei: '))
            minut = int(input('Introduceti minutul tranzactiei: '))
            date_and_time = datetime(an, luna, ziua, ora, minut)

            self.transaction_service.update_transaction(id_tranzactie_modificat,
                                                        id_medicine,
                                                        id_membership_card,
                                                        number_pieces,
                                                        date_and_time)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_transaction(self):
        try:
            id_transaction = input("Introduceti id-ul tranzactiei pe care doriti sa o stergeti: ")
            self.transaction_service.delete_transaction(id_transaction)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_add_membership_card(self):
        try:
            id_membership_card = int(input('Introduceti id-ul cardului de client: '))
            first_name_member = input('Introduceti numele clientului: ')
            second_name_member = input('Introduceti prenumele clientului: ')
            CNP = input('Introduceti codul numeric personal al clientului: ')

            self.membership_card_service.add_membership_card(id_membership_card,
                                                             first_name_member,
                                                             second_name_member,
                                                             CNP)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_membership_card(self):
        try:
            id_membership_card_modificat = int(input("introduceti id-ul cardului de"
                                                     " client pe care doriti sa il modificati:"))
            first_name_member = input('Introduceti numele clientului: ')
            second_name_member = input('Introduceti prenumele clientului: ')
            CNP = input('Introduceti codul numeric personal al clientului: ')
            self.membership_card_service.update_membership_card(id_membership_card_modificat,
                                                                first_name_member,
                                                                second_name_member,
                                                                CNP)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_membership_card(self):
        try:
            id_membership_card = input("Introduceti id-ul cardului de client pe care doriti sa il stergeti: ")
            self.membership_card_service.delete_membership_card(id_membership_card)
            self.transaction_service.delete_if_delete_member_card(id_membership_card)
        except ValueError as ve:
            print('Eroare de validare:', ve)
        except KeyError as ke:
            print('Eroare de ID:', ke)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_search_day_interval(self):
        zi = int(input('Introduceti ziua de inceput:'))
        luna = int(input('Introduceti luna de inceput:'))
        an = int(input('Introduceti anul de inceput:'))
        start_date = datetime(an, luna, zi)
        zi = int(input('Introduceti ziua de final:'))
        luna = int(input('Introduceti luna de final:'))
        an = int(input('Introduceti anul de final:'))
        end_date = datetime(an, luna, zi)
        print(self.transaction_service.get_day_interval(start_date, end_date))

    def handle_delete_day_interval(self):
        try:
            zi = int(input('Introduceti ziua de inceput:'))
            luna = int(input('Introduceti luna de inceput:'))
            an = int(input('Introduceti anul de inceput:'))
            start_date = datetime(an, luna, zi)
            zi = int(input('Introduceti ziua de final:'))
            luna = int(input('Introduceti luna de final:'))
            an = int(input('Introduceti anul de final:'))
            end_date = datetime(an, luna, zi)
            stergeri = self.transaction_service.delete_day_interval(start_date, end_date)
            print()
            if stergeri == 0:
                print('Nu au fost gasite tranzactii in perioada precizata.')
            else:
                print(f'Au fost sterse {stergeri} tranzactii cu succes!')
            print()

        except Exception as ex:
            print(f'\nEroare: \n{ex}\n --> reincearca!\n')

    def handle_random_medicamente(self):
        try:
            medicamente_number = int(input('Dati numarul de medicamente spre generare: ').strip())
            generated_list = self.medicament_service.generate_medicamente_random(medicamente_number)
            for each_medicamente in generated_list:
                print(each_medicamente)
            print(f'\nBaza de date a fost populata cu {len(generated_list)} medicamente aleatorii!')
        except KeyError as ke:
            print(f'\nEroare: \n{ke}\n --> reincearca!\n')

    def handle_full_text_search(self):
        try:
            string_to_search = input('Introduceti ce cautati: ').strip()
            if string_to_search == '':
                raise KeyError('\nSecventa de cautat este goala.')

            search_results =\
                self.medicament_service.full_search(string_to_search) +\
                self.membership_card_service.full_search(string_to_search)
            if len(search_results) == 0:
                print('\nNu au fost gasite rezultate!\n')
            else:
                print(f'\nRezultatele cautarii: ({len(search_results)} matches)\n')
                for result in search_results:
                    print(result)
                print()
        except Exception as ex:
            print(f'\nEroare: \n{ex}\n --> reincearca!\n')

    def handle_show_descending_medicine(self):
        for i in self.transaction_service.descending_order_medicine():
            print(i)

    def handle_show_descending_card(self):
        for i in self.transaction_service.descending_order_card():
            print(i)

    def handle_scumpire_cu_procentaj(self):
        procentaj = int(input("Introduceti procentajul pe care vrei sa-l aduni: "))
        price = int(input("Introduceti pretul de la care vrei sa incepi adunarea: "))
        self.medicament_service.creste_preturile_medicamentului(procentaj, price)
