from Domain.medicament import Medicine
from Repository.medicine_repository import MedicamentRepository
from Repository.repository import Repository
from utils import clear_file


def test_medicine_repository():
    filename = 'test_drugs.json'
    clear_file(filename)
    medicine_repository = Repository(filename)
    added = Medicine('1', 'Paracetamol', 'Zentiva', 2, 'Nu')
    medicine_repository.create(added)
    assert medicine_repository.read(added.id_entity) == added
