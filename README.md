**Vaatimusmäärittely**

Oliiviöljyarviointisovellus, jonka avulla käyttäjä voi pitää kirjaa maistamistaan oliiviöljyistä.

Sovellus toimii samalla periaattella, kuin olut- ja viiniarviointisovellukset *Untappd* ja *Vivino*. Siinä on seuraavat ominaisuudet:
1. Käyttäjätunnuksen luonti ja sisäänkirjautuminen
2. Tietokanta, johon käyttäjä voi lisätä arvioitavan oliiviöljyn
3. Yhteenveto käyttäjän arvoimista oliiviöljyistä
4. Yhteenveto oliiviöljyn saamista arvioista; tiedon visualisointia mahdollisesti PyChartilla

Arvion tallentamista varten käyttäjä syöttää seuraavat tiedot:
1. Öljyn nimi ja mahdollinen vuosikerta
2. Öljyn tuottajan nimi
3. Öljyn ostohinta
4. Arvio öljyn mausta asteikolla 0-5
5. Öljyn karaktääri: alustavasti noin 4-6 liukusäädintä asteikolla 0-10. Mahdollisia parametreja ovat vahvuus, täyteläisyys, happamuus, karvaus ja makeus

**Muutosloki**

Välipalautus 2: 
- Web-sovelluksen sivuhierarkian luonti ja alkeellinen sisäänkirjautumislogiikka, jossa käyttäjänimi tallennetaan istuntoon

**Sovelluksen käyttöönotto Ubuntu-koneella**

Avaa ja suorita **key.py** ja kopioi tuloste tiedostoon **.env** muuttujan *SECRET-KEY* arvoksi lainausmerkkien sisään. Tämän jälkeen, suorita seuraavat komennot terminaalissa:
~~~sh
git clone https://github.com/cianci0/rate-your-oil
~~~
~~~sh
cd rate-your-oil
~~~
~~~sh
python3 -m venv venv
~~~
~~~sh
source venv/bin/activate
~~~
~~~sh
pip install flask
~~~
~~~sh
flask run
~~~
