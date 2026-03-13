# Instalare și configurare dashboard Lovelace

Acest YAML este creat pentru a afișa informațiile din integrarea Curs valutar BNR într-un dashboard Lovelace. Cardurile includ cursuri oficiale, rate de schimb valutar în numerar și dobânzi (ROBOR, EURIBOR, IRCC).

> **Notă:** Senzorii se creează dinamic — apar doar când API-ul returnează date pentru categoria respectivă. Dacă un senzor nu apare, înseamnă că datele nu sunt disponibile momentan.

---

## Senzori disponibili

### Curs valutar BNR
| Senzor | Entity ID |
|---|---|
| Curs RON → EUR | `sensor.curs_valutar_ron_eur` |
| Curs RON → USD | `sensor.curs_valutar_ron_usd` |
| Curs RON → GBP | `sensor.curs_valutar_ron_gbp` |
| Curs RON → CHF | `sensor.curs_valutar_ron_chf` |

### Schimb valutar (CEC)
| Senzor | Entity ID |
|---|---|
| Schimb RON → EUR | `sensor.schimb_valutar_ron_eur` |
| Schimb RON → USD | `sensor.schimb_valutar_ron_usd` |
| Schimb RON → GBP | `sensor.schimb_valutar_ron_gbp` |
| Schimb RON → CHF | `sensor.schimb_valutar_ron_chf` |

### Dobânzi și indici
| Senzor | Entity ID |
|---|---|
| Dobânda ROBOR | `sensor.dobanda_robor` |
| Dobânda EURIBOR | `sensor.dobanda_euribor` |
| IRCC zilnic | `sensor.ircc_zilnic` |
| IRCC trimestrial | `sensor.ircc_trimestrial` |

---

## Exemplu dashboard Lovelace

```yaml
views:
  - title: Monitorizare Financiară
    icon: mdi:bank
    cards:
      - type: markdown
        content: >
          ### Monitorizare Cursuri Valutare și Dobânzi

          Datele sunt actualizate automat conform intervalului configurat în integrare.

      # Card Cursuri Valutare
      - type: entities
        title: Curs Valutar BNR
        entities:
          - entity: sensor.curs_valutar_ron_eur
            name: Curs EUR
          - type: attribute
            entity: sensor.curs_valutar_ron_eur
            attribute: Valoare curentă
            name: Valoare curentă
          - type: attribute
            entity: sensor.curs_valutar_ron_eur
            attribute: Valoare anterioară
            name: Valoare anterioară
          - type: attribute
            entity: sensor.curs_valutar_ron_eur
            attribute: Schimbare
            name: Schimbare
          - type: attribute
            entity: sensor.curs_valutar_ron_eur
            attribute: Schimbare procentuală
            name: Schimbare procentuală

          - entity: sensor.curs_valutar_ron_usd
            name: Curs USD
          - type: attribute
            entity: sensor.curs_valutar_ron_usd
            attribute: Valoare curentă
            name: Valoare curentă
          - type: attribute
            entity: sensor.curs_valutar_ron_usd
            attribute: Valoare anterioară
            name: Valoare anterioară
          - type: attribute
            entity: sensor.curs_valutar_ron_usd
            attribute: Schimbare
            name: Schimbare
          - type: attribute
            entity: sensor.curs_valutar_ron_usd
            attribute: Schimbare procentuală
            name: Schimbare procentuală

      # Card Schimb Valutar
      - type: entities
        title: Schimb Valutar (Cash)
        entities:
          - entity: sensor.schimb_valutar_ron_eur
            name: Schimb EUR
          - type: attribute
            entity: sensor.schimb_valutar_ron_eur
            attribute: Vânzare
            name: Vânzare
          - type: attribute
            entity: sensor.schimb_valutar_ron_eur
            attribute: Cumpărare
            name: Cumpărare

          - entity: sensor.schimb_valutar_ron_usd
            name: Schimb USD
          - type: attribute
            entity: sensor.schimb_valutar_ron_usd
            attribute: Vânzare
            name: Vânzare
          - type: attribute
            entity: sensor.schimb_valutar_ron_usd
            attribute: Cumpărare
            name: Cumpărare

      # Card Dobânzi ROBOR și EURIBOR
      - type: entities
        title: Dobânzi ROBOR și EURIBOR
        entities:
          - entity: sensor.dobanda_robor
            name: Dobânda ROBOR
          - type: attribute
            entity: sensor.dobanda_robor
            attribute: 1 lună
            name: 1 lună
          - type: attribute
            entity: sensor.dobanda_robor
            attribute: 3 luni
            name: 3 luni
          - type: attribute
            entity: sensor.dobanda_robor
            attribute: 6 luni
            name: 6 luni
          - type: attribute
            entity: sensor.dobanda_robor
            attribute: 12 luni
            name: 12 luni

          - entity: sensor.dobanda_euribor
            name: Dobânda EURIBOR
          - type: attribute
            entity: sensor.dobanda_euribor
            attribute: 1 lună
            name: 1 lună
          - type: attribute
            entity: sensor.dobanda_euribor
            attribute: 3 luni
            name: 3 luni
          - type: attribute
            entity: sensor.dobanda_euribor
            attribute: 6 luni
            name: 6 luni
          - type: attribute
            entity: sensor.dobanda_euribor
            attribute: 12 luni
            name: 12 luni

      # Card Indici IRCC
      - type: entities
        title: Indici IRCC
        entities:
          - entity: sensor.ircc_zilnic
            name: IRCC zilnic
          - type: attribute
            entity: sensor.ircc_zilnic
            attribute: Modificare
            name: Modificare

          - entity: sensor.ircc_trimestrial
            name: IRCC trimestrial
          - type: attribute
            entity: sensor.ircc_trimestrial
            attribute: Modificare
            name: Modificare
```
