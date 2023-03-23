from abc import ABC
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    id_entity: str


"""
Această clasă Entity este o clasă abstractă care este decorată cu decoratorul @dataclass,
care automat generează metodele __init__(), __repr__() și __eq__() pentru a permite crearea
și compararea obiectelor de tip entitate.

Clasa Entity are un singur atribut id_entity de tip str, care este folosit pentru a identifica
unic o entitate într-un depozit. Această clasă poate fi folosită ca clasă de bază pentru a defini
entitățile specifice domeniului de aplicare. Clasele derivate trebuie să implementeze această clasă
și să adauge orice atribute suplimentare necesare în funcție de necesitățile domeniului.
"""