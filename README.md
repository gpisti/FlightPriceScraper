# Repülőjegy Árak Web Scraper

Ez a Python projekt lehetővé teszi repülőjegy-árak és úticélok scrapelését a Kiwi.com webhelyről. A projekt a Selenium és PrettyTable könyvtárakat használja a webböngésző emulálásához és a felhasználóbarát kimenetek létrehozásához.

--Rendszerkövetelmények--

A projekt futtatásához szükséges a következő Python csomagok telepítése:
1. selenium

2. prettytable

A Selenium további telepítése előtt szükséges egy webböngészővezérlő telepítése (például a Firefox Driver).

BEÁLLÍTÁS

A projekt konfigurációs paramétereket használ a repülőjegyek lekérdezéséhez:

1. WAIT_TIMEOUT: Meghatározza, mennyi időt szánjon a kód a repülőjegyek lementésére. Alapértelmezett érték: 5 másodperc.


2. PATH_FOR_ADATOKTXT: Az adatok.txt fájl elérési útvonala, ahol az adatokat tároljuk. Módosítsa ezt az elérési utat az igényei szerint.


3. DAYS: Adatok frissítése esetén ennyi napot lefedve szedi össze az új adatokat. Alapértelmezett érték: 90 nap.



HASZNÁLAT

A projekt fő funkciói a következők:

1. Városok kilistázása: Kilistázza az elérhető városok neveit.

2. Város alapú keresés: Megkeresi, mikor a legolcsóbb utazni egy adott városba.

3. Dátum alapú keresés: Megkeresi, hova a legolcsóbb utazni egy adott dátumon.

4. Overall legolcsóbb: Megkeresi, hogy mikor és hova a legolcsóbb utazni az összes adat alapján.

5. Adatok frissítése: Frissíti az adatokat, és új adatokat szed össze az adatok.txt fájlban.

A futtatáshoz indítsa el a Python szkriptet. Ha az adatok.txt fájl nem létezik, a projekt először inicializálja az adatokat a webből. Az összes adatot egy allData változó tárolja, amivel a projekt dolgozik.
