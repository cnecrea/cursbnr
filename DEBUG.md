# Debugging pentru integrarea Curs valutar BNR

Ghid pentru activarea logării detaliate și analiza problemelor.

---

## 1. Activează logarea detaliată

Editează `configuration.yaml` și adaugă:

```yaml
logger:
  default: warning
  logs:
    custom_components.cursbnr: debug
    custom_components.cursbnr.coordinator: debug
    custom_components.cursbnr.sensor: debug
    custom_components.cursbnr.helpers: debug
```

Repornește Home Assistant pentru a aplica modificările.

---

## 2. Ce module poți monitoriza

Integrarea e structurată pe module separate. Poți activa debug selectiv:

| Modul | Ce loghează |
|---|---|
| `custom_components.cursbnr` | Setup, unload, options listener |
| `custom_components.cursbnr.coordinator` | Preluare date API, interval orar, erori fetch |
| `custom_components.cursbnr.sensor` | Creare/eliminare dinamică senzori, SensorManager |
| `custom_components.cursbnr.helpers` | Conversii date, extragere valori, erori parsare |
| `custom_components.cursbnr.config_flow` | ConfigFlow și OptionsFlow |

Dacă vrei doar coordinator + sensor (cele mai utile):

```yaml
logger:
  default: warning
  logs:
    custom_components.cursbnr.coordinator: debug
    custom_components.cursbnr.sensor: debug
```

---

## 3. Analizează logurile

### Localizare
Logurile se află în fișierul `home-assistant.log` din directorul principal al Home Assistant.

### Filtrare
```bash
grep 'custom_components.cursbnr' home-assistant.log
```

### Filtrare doar erori
```bash
grep 'custom_components.cursbnr' home-assistant.log | grep -i 'error\|warning'
```

---

## 4. Mesaje frecvente

Integrarea citește un singur fișier JSON, generat pe server din șase surse. Fiecare sursă apare separat în jurnal, cu data celor mai noi date.

### Normale (INFO/DEBUG)
- `Integrarea Curs valutar BNR a fost configurată cu succes` — setup reușit
- `Prima rulare - se preiau datele indiferent de oră` — prima cerere API
- `Datele au fost preluate: HTTP 200, … octeți, … ms; fișier generat pe server la …` — preluare reușită și cât de proaspăt e fișierul de pe server
- `ROBOR: OK — date din 26.10.2026, 6 rânduri` — starea fiecărei surse (Curs valutar BNR, Schimb valutar CEC, ROBOR, EURIBOR, IRCC zilnic, IRCC trimestrial)
- `Senzori cu date disponibile: …` — ce senzori pot exista acum
- `Senzori creați dinamic: ...` — senzorii au fost creați pe baza datelor disponibile
- `Ora curentă (…) este în afara intervalului 13:00-17:00` — se păstrează datele existente
- `ROBOR: datele sunt din nou disponibile` — sursa și-a revenit (INFO)

### Avertismente (o singură dată, nu la fiecare actualizare)
- `ROBOR: datele nu sunt disponibile, senzorul este eliminat până revin. Detalii: …` — sursa n-a răspuns și serverul nu avea date anterioare; în detalii apare adresa și codul HTTP
- `ROBOR: sursa nu răspunde, se afișează ultimele date disponibile (26.10.2026). Detalii: …` — serverul a păstrat ultimele date bune; senzorul rămâne, cu data lor
- `Eroare la preluarea datelor, se păstrează datele anterioare: …` — fișierul de pe server nu s-a putut citi

### Erori
- `Eroare la comunicarea cu API-ul BNR` — serverul cu fișierul JSON nu răspunde, se reîncearcă automat
- `Eroare HTTP 4xx/5xx la preluarea datelor` — probleme pe serverul cu fișierul JSON
- `Nu s-a putut converti valoarea la float` — date invalide în răspuns

---

## 5. Diagnostice

Alternativă la logare manuală — folosește diagnosticele integrate:

1. **Setări > Dispozitive și servicii > Curs valutar BNR**
2. Cele **trei puncte** → **Download diagnostics**
3. Fișierul JSON conține:
   - configurarea și starea coordinator-ului, cu ultima preluare (durată, mărime, când a fost generat fișierul pe server)
   - **starea fiecărei surse**: `ok`, `stale` (serverul a păstrat datele anterioare), `error` sau `missing`, data celor mai noi date și mesajul de eroare de la sursă
   - erorile raportate de server (`_meta`) și senzorii activi

---

## 6. Cum să postezi cod în discuții

Pentru a posta log-uri sau cod pe GitHub, folosește blocuri de cod:

<pre>
```yaml
2026-10-26 13:35:12 DEBUG custom_components.cursbnr.coordinator: Prima rulare - se preiau datele indiferent de oră
2026-10-26 13:35:13 DEBUG custom_components.cursbnr.coordinator: Datele au fost preluate: HTTP 200, 4741 octeți, 182 ms; fișier generat pe server la 2026-10-26T13:30:02+02:00
2026-10-26 13:35:13 DEBUG custom_components.cursbnr.coordinator: ROBOR: OK — date din 26.10.2026, 6 rânduri
2026-10-26 13:35:13 INFO  custom_components.cursbnr.sensor: Senzori creați dinamic: bnr_rates_ron_eur, bnr_rates_ron_usd
```
</pre>

Rezultatul va fi formatat și ușor de citit:

```yaml
2026-10-26 13:35:12 DEBUG custom_components.cursbnr.coordinator: Prima rulare - se preiau datele indiferent de oră
2026-10-26 13:35:13 DEBUG custom_components.cursbnr.coordinator: Datele au fost preluate: HTTP 200, 4741 octeți, 182 ms; fișier generat pe server la 2026-10-26T13:30:02+02:00
2026-10-26 13:35:13 DEBUG custom_components.cursbnr.coordinator: ROBOR: OK — date din 26.10.2026, 6 rânduri
2026-10-26 13:35:13 INFO  custom_components.cursbnr.sensor: Senzori creați dinamic: bnr_rates_ron_eur, bnr_rates_ron_usd
```
