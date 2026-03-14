![BNR](https://github.com/user-attachments/assets/a2f7ae7c-6ca0-4c8d-b5f0-3c0f6517fefc)

# Curs valutar BNR - Integrare pentru Home Assistant

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/releases)
[![Licență](https://img.shields.io/github/license/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/blob/main/LICENSE.md)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2025.11%2B-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![GitHub Stars](https://img.shields.io/github/stars/cnecrea/cursbnr?style=flat&logo=github)](https://github.com/cnecrea/cursbnr/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/cnecrea/cursbnr?style=flat&logo=github)](https://github.com/cnecrea/cursbnr/network/members)
[![GitHub Watchers](https://img.shields.io/github/watchers/cnecrea/cursbnr?style=flat&logo=github)](https://github.com/cnecrea/cursbnr/watchers)
[![GitHub Issues](https://img.shields.io/github/issues/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/issues)
[![Ultimul Commit](https://img.shields.io/github/last-commit/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/commits/main)
[![Commit-uri/lună](https://img.shields.io/github/commit-activity/m/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/commits/main)
[![Dimensiune Repo](https://img.shields.io/github/repo-size/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr)
[![Limbaj Principal](https://img.shields.io/github/languages/top/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr)
[![Total descărcări](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cnecrea/cursbnr/main/statistici/shields/descarcari.json)](https://github.com/cnecrea/cursbnr/releases)
[![Descărcări ultima versiune](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cnecrea/cursbnr/main/statistici/shields/ultima_release.json)](https://github.com/cnecrea/cursbnr/releases/latest)
![Badge](https://hitscounter.dev/api/hit?url=https%3A%2F%2Fgithub.com%2Fcnecrea%2Fcursbnr&label=afi%C8%99%C4%83ri&icon=github&color=%23198754&message=&style=flat&tz=Europe%2FBucharest)


Integrare pentru Home Assistant care oferă monitorizare completă a cursurilor valutare și a dobânzilor oficiale furnizate de BNR. Senzorii se creează dinamic — apar doar când datele sunt disponibile și se elimină automat când datele dispar.

---

## Caracteristici

### Curs valutar BNR
- Curs valutar RON → EUR, USD, GBP, CHF

Atribute disponibile: valoare curentă, valoare anterioară, schimbare, schimbare procentuală.

### Schimb valutar (CEC)
- Schimb valutar RON → EUR, USD, GBP, CHF

Atribute disponibile: vânzare, cumpărare.

### Dobânzi
- Dobânzi ROBOR pentru 1, 3, 6 și 12 luni
- Dobânzi EURIBOR pentru 1, 3, 6 și 12 luni
- Indicele IRCC zilnic
- Indicele IRCC trimestrial

Atribute disponibile: valori pe perioade, modificare.

---

## Configurare

1. Adaugă integrarea din **Setări > Dispozitive și Servicii > Adaugă Integrare**.
2. Caută **Curs valutar BNR**.
3. Configurează intervalul de actualizare (implicit: 300 secunde / 5 minute).

Intervalul poate fi modificat ulterior din **Opțiuni** fără a reconfigura integrarea.

---

## Instalare

### Prin HACS (recomandat)
1. Adaugă [depozitul personalizat](https://github.com/cnecrea/cursbnr) în HACS.
2. Caută integrarea **Curs valutar BNR** și instaleaz-o.
3. Repornește Home Assistant și configurează integrarea.

### Manual
1. Descarcă [ultima versiune](https://github.com/cnecrea/cursbnr/releases) de pe GitHub.
2. Copiază folderul `cursbnr` în directorul `custom_components/` al Home Assistant.
3. Repornește Home Assistant și configurează integrarea.

Pentru detalii complete, consultă [INSTALL.md](INSTALL.md).

---

## Structura integrării

| Fișier | Rol |
|---|---|
| `const.py` | Constante centralizate, definiții senzori |
| `coordinator.py` | DataUpdateCoordinator pentru preluarea datelor |
| `__init__.py` | Setup, unload, options listener |
| `config_flow.py` | ConfigFlow + OptionsFlow |
| `sensor.py` | SensorManager dinamic + clase senzori |
| `helpers.py` | Funcții utilitare de extragere și conversie date |
| `diagnostics.py` | Suport diagnostice Home Assistant |

---

## Exemplu de automatizare

Notificare când cursul EUR depășește 5 lei:

```yaml
alias: Notificare Curs EUR Ridicat
trigger:
  - platform: numeric_state
    entity_id: sensor.curs_valutar_ron_eur
    above: 5
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Curs EUR Ridicat!"
      message: "Cursul EUR este {{ states('sensor.curs_valutar_ron_eur') }} lei."
mode: single
```

---

## Susține dezvoltatorul

Dacă ți-a plăcut această integrare și vrei să sprijini munca depusă, invită-mă la o cafea!

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Susține%20dezvoltatorul-orange?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/cnecrea)

---

## Contribuții

Contribuțiile sunt binevenite! Deschide un [Issue](https://github.com/cnecrea/cursbnr/issues) sau trimite un Pull Request.

Dacă îți place integrarea, oferă-i un ⭐ pe [GitHub](https://github.com/cnecrea/cursbnr)!
