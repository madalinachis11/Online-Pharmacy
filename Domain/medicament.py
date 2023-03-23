from Domain.entity import Entity


class Medicine(Entity):

    """
    Descrie un medicament.
    """

    def __init__(self,
                 id_medicine,
                 name_medicine,
                 producer,
                 price,
                 medical_prescription):
        """
        Creeaza un obiect de tip Medicament.

        :param id_medicine: Id-ul medicamentului.
        :param name_medicine: Numele medicamentului.
        :param producer: Producatorul medicamentului.
        :param price: Pretul medicamentului.
        :param medical_prescription: Necesita reteta(Da sau Nu)
        """
        super().__init__(id_medicine)
        self.__name_medicine = name_medicine
        self.__producer = producer
        self.__price = price
        self.__medical_prescription = medical_prescription

    @property
    def name_medicine(self):
        return self.__name_medicine

    @name_medicine.setter
    def name_medicine(self, value):
        self.__name_medicine = value

    @property
    def producer(self):
        return self.__producer

    @producer.setter
    def producer(self, value):
        self.__producer = value


        """
        Acesta este un decorator @property pentru metoda price a obiectului. Decoratorul transformă metoda
        într-un atribut al obiectului și permite accesarea acestuia fără a fi necesară apelarea metodei.
        Mai precis, atunci când se accesează atributul price, se va apela această metodă, care va returna
        valoarea atributului privat __price. Această metodă permite obținerea prețului obiectului curent,
        dar nu permite modificarea acestuia.
        """

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        self.__price = value

    @property
    def medical_prescription(self):
        return self.__medical_prescription

    @medical_prescription.setter
    def medical_prescription(self, value):
        self.__medical_prescription = value

    def __str__(self):
        return f'{self.id_entity} - name:{self.__name_medicine}, producer:{self.__producer}, ' \
               f'price:{self.__price}; medical_prescription: {self.__medical_prescription}'

    def search(self, string_to_search):
        for prop in [str(self.name_medicine), str(self.producer)]:
            if string_to_search in prop:
                return True
        return False


"""
Această metodă search primește un șir de caractere string_to_search și caută acest șir în două proprietăți
ale obiectului curent: name_medicine și producer. Dacă șirul este găsit în una dintre aceste proprietăți,
metoda returnează True, altfel returnează False.

Mai precis, metoda iterează prin cele două proprietăți și verifică dacă string_to_search este inclus în
fiecare dintre acestea, folosind operatorul in. Dacă este găsită o potrivire, se returnează True imediat,
ceea ce înseamnă că nu se va căuta în celelalte proprietăți dacă s-a găsit deja o potrivire. Dacă nicio 
potrivire nu este găsită în cele două proprietăți, metoda returnează False.
"""