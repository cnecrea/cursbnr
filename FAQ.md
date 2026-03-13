<a name="top"></a>

# Întrebări frecvente

- [Cum instalez integrarea prin HACS?](#cum-instalez-integrarea-prin-hacs)
- [De ce nu apar toți senzorii?](#de-ce-nu-apar-toți-senzorii)
- [De ce a dispărut un senzor?](#de-ce-a-dispărut-un-senzor)
- [Cum schimb intervalul de actualizare?](#cum-schimb-intervalul-de-actualizare)
- [De ce nu se actualizează datele în afara orelor 13-17?](#de-ce-nu-se-actualizează-datele-în-afara-orelor-13-17)
- [Cum folosesc diagnosticele integrării?](#cum-folosesc-diagnosticele-integrării)
- [Am erori în log, ce fac?](#am-erori-în-log-ce-fac)

---

## Cum instalez integrarea prin HACS?

[Înapoi sus](#top)

1. Asigură-te că HACS este instalat. Verifică în **Setări > Dispozitive și servicii > Integrări** — caută „HACS". Dacă nu e instalat, urmează [ghidul oficial HACS](https://hacs.xyz/docs/use).
2. În HACS, apasă pe cele **trei puncte** din dreapta sus → **Custom repositories**.
3. Introdu `https://github.com/cnecrea/cursbnr` și selectează tipul **Integration**.
4. Apasă **Add**, apoi caută **Curs valutar BNR** și apasă **Download**.
5. Repornește Home Assistant.
6. Mergi la **Setări > Dispozitive și servicii > Adaugă integrare** și caută **Curs valutar BNR**.

---

## De ce nu apar toți senzorii?

[Înapoi sus](#top)

Senzorii se creează dinamic, doar când API-ul BNR returnează date pentru categoria respectivă. Dacă un senzor nu apare, înseamnă că:

- API-ul nu a returnat date pentru acea categorie (de exemplu, ROBOR sau IRCC pot lipsi temporar)
- Conexiunea la API a eșuat la prima încărcare

Verifică în **Developer Tools > States** și caută `cursbnr`. Dacă nu apare nimic, verifică log-urile (vezi [DEBUG.md](DEBUG.md)).

---

## De ce a dispărut un senzor?

[Înapoi sus](#top)

Integrarea elimină automat senzorii când datele lor nu mai sunt disponibile în API. Asta e comportament normal — nu e o eroare. Senzorul va fi recreat automat când datele revin.

Acest mecanism previne starea „Unavailable" — senzorii fie există cu date valide, fie nu există deloc.

---

## Cum schimb intervalul de actualizare?

[Înapoi sus](#top)

1. Mergi la **Setări > Dispozitive și servicii**.
2. Găsește **Curs valutar BNR** și apasă **Configurează**.
3. Modifică intervalul (minim 60 secunde, maxim 3600 secunde).
4. Integrarea se va reîncărca automat cu noul interval.

---

## De ce nu se actualizează datele în afara orelor 13-17?

[Înapoi sus](#top)

BNR publică cursurile valutare în jurul orei 13:00. Integrarea preia date noi doar între orele 13:00 și 17:00 pentru a nu face cereri inutile. În afara acestui interval, se păstrează ultimele date valide.

La prima pornire a integrării, datele sunt preluate indiferent de oră.

---

## Cum folosesc diagnosticele integrării?

[Înapoi sus](#top)

1. Mergi la **Setări > Dispozitive și servicii > Curs valutar BNR**.
2. Apasă cele **trei puncte** → **Download diagnostics**.
3. Fișierul JSON conține: configurarea, starea coordinator-ului, senzorii activi și un rezumat al datelor.

Aceste informații sunt utile pentru depanare și pentru raportarea problemelor pe GitHub.

---

## Am erori în log, ce fac?

[Înapoi sus](#top)

Activează logarea detaliată urmând instrucțiunile din [DEBUG.md](DEBUG.md), apoi verifică log-urile. Cele mai frecvente situații:

- **„Eroare la comunicarea cu API-ul BNR"** — API-ul este temporar indisponibil. Integrarea va reîncerca automat.
- **„Nu există date ROBOR/EURIBOR/IRCC"** — API-ul nu a returnat date pentru acea categorie. Senzorul respectiv nu va fi creat.
- **Warning Recorder despre unit conversion** — Apare dacă ai avut o versiune anterioară cu unități diferite. Poți ignora sau șterge statisticile vechi din **Developer Tools > Statistics**.

Dacă problema persistă, deschide un [Issue pe GitHub](https://github.com/cnecrea/cursbnr/issues) cu log-urile și diagnosticele atașate.
