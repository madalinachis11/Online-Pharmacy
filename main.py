from Domain.medicament_validator import MedicamentValidator
from Domain.membership_card_validator import MembershipCardValidator
from Domain.transaction_validator import TransactionValidator
from Repository.json_repository import JsonRepository
from Service.medicament_service import MedicamentService
from Service.membership_card_service import MembershipCardService
from Service.transaction_service import TransactionService
from Service.undo_redo_service import UndoRedoService
from Tests.test_domain import test_domain
from Tests.test_repository import test_repository
from Tests.test_service import test_all_services
from Tests.undo_redo_tests import test_all
from UserInterface.Console import Console


def main():
    undo_redo_service = UndoRedoService()
    medicine_repository = JsonRepository('drugs.json')
    medicament_validator = MedicamentValidator()
    medicament_service = MedicamentService(medicine_repository,
                                           medicament_validator,
                                           undo_redo_service)

    transaction_repository = JsonRepository('transactions.json')
    membership_card_repository = JsonRepository('membershipcard.json')
    transaction_validator = TransactionValidator()
    transaction_service = TransactionService(transaction_repository,
                                             transaction_validator,
                                             medicine_repository,
                                             membership_card_repository,
                                             undo_redo_service)

    membership_card_repository = JsonRepository('membershipcard.json')
    membership_card_validator = MembershipCardValidator()
    membership_card_service = MembershipCardService(membership_card_repository,
                                                    membership_card_validator,
                                                    medicine_repository,
                                                    transaction_repository,
                                                    undo_redo_service)

    console = Console(medicament_service,
                      transaction_service,
                      membership_card_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    test_repository()
    test_domain()
    test_all_services()
    test_all()
    main()
