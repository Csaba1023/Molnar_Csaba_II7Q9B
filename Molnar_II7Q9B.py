from abc import ABC, abstractmethod
import datetime


class Jarat(ABC):
    def __init__(self, jaratszam, celallomas, jegyar, indulasi_ido):
        self.jaratszam = jaratszam
        self.celallomas = celallomas
        self.jegyar = jegyar
        self.indulasi_ido = indulasi_ido  # datetime objektum

    @abstractmethod
    def info(self):
        pass


class BelfoldiJarat(Jarat):
    def __init__(self, jaratszam, celallomas, indulasi_ido):
        super().__init__(jaratszam, celallomas, jegyar=10000, indulasi_ido=indulasi_ido)

    def info(self):
        return f"Belföldi járat - {self.jaratszam}: {self.celallomas}, Ár: {self.jegyar} Ft, Indulás: {self.indulasi_ido}"


class NemzetkoziJarat(Jarat):
    def __init__(self, jaratszam, celallomas, indulasi_ido):
        super().__init__(jaratszam, celallomas, jegyar=50000, indulasi_ido=indulasi_ido)

    def info(self):
        return f"Nemzetközi járat - {self.jaratszam}: {self.celallomas}, Ár: {self.jegyar} Ft, Indulás: {self.indulasi_ido}"


class LegiTarsasag:
    def __init__(self, nev):
        self.nev = nev
        self.jaratok = []

    def hozzaad_jarat(self, jarat):
        self.jaratok.append(jarat)

    def keres_jarat(self, jaratszam):
        for jarat in self.jaratok:
            if jarat.jaratszam == jaratszam:
                return jarat
        return None

    def listaz_jaratok(self):
        return [jarat.info() for jarat in self.jaratok]


class JegyFoglalas:
    def __init__(self):
        self.foglalasok = {}

    def foglalas(self, jarat, db):
        if jarat.indulasi_ido < datetime.datetime.now():
            print("Ez a járat már lezárult, nem foglalható.")
            return 0
        if jarat.jaratszam in self.foglalasok:
            self.foglalasok[jarat.jaratszam]['db'] += db
        else:
            self.foglalasok[jarat.jaratszam] = {'jarat': jarat, 'db': db}
        ar = jarat.jegyar * db
        print(f"Foglalás sikeres: {db} jegy a(z) {jarat.info()} járatra. Összeg: {ar} Ft")
        return ar

    def lemondas(self, jaratszam):
        if jaratszam in self.foglalasok:
            del self.foglalasok[jaratszam]
            print(f"Foglalás törölve: {jaratszam}")
        else:
            print("Nincs ilyen foglalás.")

    def listaz_foglalasok(self):
        if not self.foglalasok:
            print("Nincs jelenlegi foglalás.")
        for adat in self.foglalasok.values():
            jarat = adat['jarat']
            db = adat['db']
            print(f"{jarat.info()}, Foglalt jegyek száma: {db}")


# Előkészítés
legitarsasag = LegiTarsasag("Hungarian Airlines")
legitarsasag.hozzaad_jarat(BelfoldiJarat("B101", "Budapest", datetime.datetime(2025, 6, 5, 9, 0)))
legitarsasag.hozzaad_jarat(BelfoldiJarat("B102", "Debrecen", datetime.datetime(2025, 6, 6, 14, 30)))
legitarsasag.hozzaad_jarat(NemzetkoziJarat("N201", "London", datetime.datetime(2025, 6, 10, 6, 0)))

foglalaskezelo = JegyFoglalas()

# Felhasználói interfész
def menu():
    while True:
        print("\n--- Repülőjegy Foglalási Rendszer ---")
        print("1. Járatok listázása")
        print("2. Jegy foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("0. Kilépés")

        valasztas = input("Válassz egy opciót: ")

        if valasztas == "1":
            for info in legitarsasag.listaz_jaratok():
                print(info)
        elif valasztas == "2":
            print("Elérhető járatok:")
            for info in legitarsasag.listaz_jaratok():
                print(info)
            jaratszam = input("Add meg a foglalni kívánt járatszámot: ")
            jarat = legitarsasag.keres_jarat(jaratszam)
            if jarat:
                try:
                    db = int(input("Hány jegyet szeretnél foglalni? "))
                    if db <= 0:
                        print("Érvénytelen jegyszám.")
                    else:
                        foglalaskezelo.foglalas(jarat, db)
                except ValueError:
                    print("Érvénytelen szám.")
            else:
                print("Nincs ilyen járat.")
        elif valasztas == "3":
            jaratszam = input("Add meg a lemondandó foglalás járatszámát: ")
            foglalaskezelo.lemondas(jaratszam)
        elif valasztas == "4":
            foglalaskezelo.listaz_foglalasok()
        elif valasztas == "0":
            print("Kilépés a rendszerből.")
            break
        else:
            print("Érvénytelen opció.")


if __name__ == "__main__":
    with open("adatok.txt", "w", encoding="utf-8") as f:
        f.write("Molnár Csaba\nBSC mérnökinformatikus\nII7Q9B\n")

    menu()

