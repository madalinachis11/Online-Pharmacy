import random
import string


"""
random_int(start=1, stop=500000): Returnează un număr întreg aleator între start și stop, inclusiv cele două limite.
Dacă nu se specifică niciun interval, valorile implicite sunt start=1 și stop=500000.

random_string(length=15): Returnează un șir de caractere aleator de lungime length. Caracterele sunt selectate
din literele mari și mici ale alfabetului englezesc. Dacă nu se specifică nicio lungime, valoarea implicită
este length=15.

random_bool(): Returnează o valoare booleană aleatoare (True sau False) utilizând metoda getrandbits a modulului random.
"""


class RandomMedicament:

    @staticmethod
    def random_int(start=1, stop=500000):
        random.seed()
        r_id = random.randint(start, stop)
        return r_id

    @staticmethod
    def random_string(length=15):
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=length))

    @staticmethod
    def random_bool():
        return bool(random.getrandbits(1))
