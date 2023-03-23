class MyAlgorithm:


    """
    Clasa MyAlgorithm contine doua metode statice: insertion_sorted si my_mergesorted,
    care implementeaza algoritmul de sortare prin insertie si algoritmul de sortare
    prin interclasare, respectiv.
    """
    @staticmethod
    def insertion_sorted(iter, key=lambda x: x, reverse=False):
        """
        Sorteaza un iterabil cu algoritmul sortarii prin insertie.
        Aceasta este o metodă statică denumită "insertion_sorted"
        care sortează un obiect iterabil folosind algoritmul de
        sortare prin inserție. Algoritmul de sortare prin inserție
        sortează lista prin mutarea fiecărui element în ordinea
        corectă față de celelalte elemente, comparându-le între
        ele și schimbându-le poziția dacă este necesar.

        Metoda primește trei argumente: iter, care este obiectul iterabil
        pe care îl vom sorta, key, o funcție opțională folosită pentru a obține
        o valoare cheie pentru fiecare element din iterabil pentru a fi folosită
        în sortare, și reverse, un argument opțional care este setat la False pentru
        a sorta crescător și la True pentru a sorta descrescător.

        În primul bloc de instrucțiuni, în cazul în care reverse este False, un for loop
        parcurge fiecare element din iter începând cu al doilea element. Actualul element este
        păstrat într-o variabilă și o variabilă j este setată la indexul anterior. Un while loop
        continuă să compare elementul actual cu elementul precedent și să le inverseze poziția în
        cazul în care nu sunt sortate în ordinea corectă. În final, returnează iter.

        În al doilea bloc de instrucțiuni, în cazul în care reverse este True, un for loop parcurge
        fiecare element din iter în ordine inversă. Elementul actual este păstrat într-o variabilă,
        iar o variabilă j este setată la indexul următor. Un while loop continuă să compare elementul
        actual cu elementul următor și să le inverseze poziția în cazul în care nu sunt sortate în ordinea
        corectă. În final, returnează iter.

        :param iter: Iterabil dat.
        :param key: Functia dupa care se compara.
        :param reverse: Decide ordinea crescatoare sau descrescatoare.
        :return: -
        """
        if reverse is False:
            for index in range(1, len(iter)):
                actual = iter[index]
                j = index - 1
                while j >= 0 and key(actual) < key(iter[j]):
                    iter[j+1] = iter[j]
                    j -= 1
                iter[j+1] = actual
        else:
            for index in range(len(iter)-2, -1, -1):
                actual = iter[index]
                j = index + 1
                while j < len(iter) and key(actual) < key(iter[j]):
                    iter[j-1] = iter[j]
                    j += 1
                iter[j-1] = actual
        return iter

    @staticmethod
    def my_mergesorted(lst, key=lambda x: x, reverse=False):
        """
        Sorteaza un iterabil cu algoritmul sortarii prin interclasare.
        Codul dat reprezintă o implementare a algoritmului de sortare prin interclasare pentru sortarea
        unei liste de elemente. Parametrul lst reprezintă lista care trebuie sortată, în timp ce
        parametrii key și reverse sunt opționali și pot fi utilizați pentru a specifica o cheie personalizată
        de sortare și ordinea de sortare, respectiv.

        Algoritmul de sortare prin interclasare funcționează prin împărțirea recursivă a listei în două jumătăți
        până când fiecare jumătate conține doar un element. Apoi, cele două jumătăți sunt interclasate într-o singură
        listă sortată.

        În implementarea dată, lista este împărțită în două jumătăți și apoi fiecare jumătate este sortată recursiv
        prin apelarea funcției my_mergesorted cu aceleași parametri. Apoi, cele două jumătăți sortate sunt interclasate
        utilizând o buclă while și valorile poz_stanga, poz_dreapta, și poz_sortat pentru a urmări pozițiile curente în
        fiecare dintre cele două jumătăți și lista sortată finală.

        În cadrul buclei while, elementele din cele două jumătăți sunt comparate utilizând cheia de sortare (dacă este
        specificată) și ordinea de sortare (ascendentă sau descendentă). Elementul mai mic (sau mai mare, în cazul unei
        ordini de sortare descrescătoare) este plasat în lista sortată finală și poziția curentă este actualizată.

        Apoi, elementele rămase din oricare dintre cele două jumătăți sunt adăugate la lista sortată finală utilizând
        două bucle while suplimentare.

        În cele din urmă, lista sortată finală este returnată.
        :param lst: Iterabilul.
        :param key: Functia dupa care se sorteaza.
        :param reverse: Decide daca sortarea e crescatoare sau descrescatoare.
        :return: rezultatul sortarii
        """

        if len(lst) > 1:
            mijloc = len(lst) // 2
            stanga = lst[:mijloc]
            dreapta = lst[mijloc:]

            s = MyAlgorithm.my_mergesorted(stanga, key, reverse)
            d = MyAlgorithm.my_mergesorted(dreapta, key, reverse)
            poz_stanga, poz_dreapta, poz_sortat = 0, 0, 0
            while poz_stanga < len(stanga) and poz_dreapta < len(dreapta):
                if reverse is False:
                    if key(stanga[poz_stanga]) < key(dreapta[poz_dreapta]):
                        lst[poz_sortat] = stanga[poz_stanga]
                        poz_stanga += 1
                    else:
                        lst[poz_sortat] = dreapta[poz_dreapta]
                        poz_dreapta += 1
                else:
                    if key(stanga[poz_stanga]) > key(dreapta[poz_dreapta]):
                        lst[poz_sortat] = stanga[poz_stanga]
                        poz_stanga += 1
                    else:
                        lst[poz_sortat] = dreapta[poz_dreapta]
                        poz_dreapta += 1
                poz_sortat += 1
            while poz_stanga < len(stanga):
                lst[poz_sortat] = stanga[poz_stanga]
                poz_sortat += 1
                poz_stanga += 1
            while poz_dreapta < len(dreapta):
                lst[poz_sortat] = dreapta[poz_dreapta]
                poz_sortat += 1
                poz_dreapta += 1
        return lst
    