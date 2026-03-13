![BNR](https://github.com/user-attachments/assets/a2f7ae7c-6ca0-4c8d-b5f0-3c0f6517fefc)

# Curs valutar BNR - Integrare pentru Home Assistant 🏦🇷🇴
[![HACS Custom](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/cnecrea/cursbnr)](https://github.com/cnecrea/cursbnr/releases)
![Total descărcări pentru toate versiunile](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/cnecrea/cursbnr/main/statistici/shields/descarcari.json)


Această integrare pentru Home Assistant oferă monitorizare completă a cursurilor valutare și a dobânzilor oficiale furnizate de **BNR**. Integrarea afișează informații despre cursuri valutare oficiale, schimb valutar și dobânzi ROBOR/EURIBOR/IRCC. 🚀

---

## 🌟 Caracteristici

### 🏦 **Curs valutar BNR**:
-  Curs valutar RON → EUR.
-  Curs valutar RON → USD.
-  Curs valutar RON → GBP.
-  Curs valutar RON → CHF.

**📊 Atribute disponibile**:
  - Valoare curentă.
  - Valoare anterioară.
  - Schimbare.
  - Schimbare procentuală.

---

### 🇷🇴 **Schimb valutar BNR**:
-  Schimb valutar RON → EUR.
-  Schimb valutar RON → USD.
-  Schimb valutar RON → GBP.
-  Schimb valutar RON → CHF.

**📊 Atribute disponibile**:
  - Vânzare.
  - Cumpărare.

---

### 📈 **Dobânzi**:
-  Dobânzi ROBOR pentru 1, 3, 6 și 12 luni.
-  Dobânzi EURIBOR pentru 1, 3, 6 și 12 luni.
-  Indicele IRCC zilnic.
-  Indicele IRCC trimestrial.

**📊 Atribute disponibile**:
  - Valori pentru fiecare perioadă (1 lună, 3 luni, 6 luni, 12 luni).
  - Modificare (pentru IRCC și EURIBOR).

---

## ⚙️ Configurare

### 🛠️ Interfața UI:
1. Adaugă integrarea din meniul **Setări > Dispozitive și Servicii > Adaugă Integrare**.
2. Configurează opțiunile:
   - **Intervalul de actualizare** (implicit: 3600 secunde).

---

## 🚀 Instalare

### 💡 Instalare prin HACS:
1. Adaugă [depozitul personalizat](https://github.com/cnecrea/cursbnr) în HACS. 🛠️
2. Caută integrarea **Curs valutar BNR** și instaleaz-o. ✅
3. Repornește Home Assistant și configurează integrarea. 🔄

### ✋ Instalare manuală:
1. Clonează sau descarcă [depozitul GitHub](https://github.com/cnecrea/cursbnr). 📂
2. Copiază folderul `custom_components/cursbnr` în directorul `custom_components` al Home Assistant. 🗂️
3. Repornește Home Assistant și configurează integrarea. 🔧

---

## ✨ Exemple de utilizare

### 🔔 Automatizare:
Notificare când cursul EUR depășește 5 lei:

```yaml
alias: Notificare Curs EUR Ridicat
description: Notificare dacă cursul EUR depășește 5 lei
trigger:
  - platform: numeric_state
    entity_id: sensor.bnr_rates_ron_eur
    above: 5
action:
  - service: notify.mobile_app_your_phone
    data:
      title: "Curs EUR Ridicat!"
      message: "Cursul EUR este {{ states('sensor.bnr_rates_ron_eur') }} lei."
mode: single
```
---

## ☕ Susține dezvoltatorul

Dacă ți-a plăcut această integrare și vrei să sprijini munca depusă, **invită-mă la o cafea**! 🫶  
Nu costă nimic, iar contribuția ta ajută la dezvoltarea viitoare a proiectului. 🙌  

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Susține%20dezvoltatorul-orange?style=for-the-badge&logo=buy-me-a-coffee)](https://buymeacoffee.com/cnecrea)

Mulțumesc pentru sprijin și apreciez fiecare gest de susținere! 🤗

--- 
## 🧑‍💻 Contribuții

Contribuțiile sunt binevenite! Deschide un **Issue** sau trimite un **Pull Request** în [GitHub](https://github.com/cnecrea/cursbnr/issues).

🌟 Suport

Dacă îți place această integrare, oferă-i un ⭐ pe [GitHub](https://github.com/cnecrea/cursbnr)! 😊
