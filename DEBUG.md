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

### Normale (INFO/DEBUG)
- `Integrarea Curs valutar BNR a fost configurată cu succes` — setup reușit
- `Senzori creați dinamic: ...` — senzorii au fost creați pe baza datelor disponibile
- `Senzor eliminat complet: ...` — senzor eliminat pentru că datele au dispărut
- `Prima rulare - se preiau datele indiferent de oră` — prima cerere API
- `Ora curentă este în afara intervalului 13:00-17:00` — se păstrează datele existente

### Erori
- `Eroare la comunicarea cu API-ul BNR` — API indisponibil, se reîncearcă automat
- `Eroare HTTP 4xx/5xx la preluarea datelor` — probleme server API
- `Nu s-a putut converti valoarea la float` — date invalide în răspunsul API

---

## 5. Diagnostice

Alternativă la logare manuală — folosește diagnosticele integrate:

1. **Setări > Dispozitive și servicii > Curs valutar BNR**
2. Cele **trei puncte** → **Download diagnostics**
3. Fișierul JSON conține: configurare, stare coordinator, senzori activi, rezumat date

---

## 6. Cum să postezi cod în discuții

Pentru a posta log-uri sau cod pe GitHub, folosește blocuri de cod:

<pre>
```yaml
2026-03-14 13:35:12 DEBUG custom_components.cursbnr.coordinator: Prima rulare - se preiau datele indiferent de oră
2026-03-14 13:35:13 DEBUG custom_components.cursbnr.coordinator: Datele au fost preluate cu succes de la API
2026-03-14 13:35:13 INFO  custom_components.cursbnr.sensor: Senzori creați dinamic: bnr_rates_ron_eur, bnr_rates_ron_usd
```
</pre>

Rezultatul va fi formatat și ușor de citit:

```yaml
2026-03-14 13:35:12 DEBUG custom_components.cursbnr.coordinator: Prima rulare - se preiau datele indiferent de oră
2026-03-14 13:35:13 DEBUG custom_components.cursbnr.coordinator: Datele au fost preluate cu succes de la API
2026-03-14 13:35:13 INFO  custom_components.cursbnr.sensor: Senzori creați dinamic: bnr_rates_ron_eur, bnr_rates_ron_usd
```
