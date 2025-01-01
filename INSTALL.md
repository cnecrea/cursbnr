Acest YAML este creat pentru a afișa informațiile din integrarea Curs valutar BNR într-un dashboard Lovelace. Cardurile includ detalii despre cursurile oficiale ale principalelor valute, ratele de schimb valutar în numerar și dobânzile oficiale, precum ROBOR, EURIBOR și IRCC. Fiecare card este configurat pentru a evidenția atât valorile principale, cât și atributele relevante ale fiecărui senzor.

```yaml
views:
  - title: Monitorizare Financiară
    icon: mdi:bank
    cards:
      - type: markdown
        content: >
          ### 🏦 Monitorizare Cursuri Valutare și Dobânzi
          Acest dashboard afișează informații actualizate despre cursurile valutare oficiale, schimburi valutare în numerar și dobânzi furnizate de BNR.
          Toate datele sunt actualizate automat în funcție de intervalul configurat în integrare.

      # Card pentru Cursuri Valutare
      - type: entities
        title: Curs Valutar BNR
        entities:
          - entity: sensor.bnr_rates_ron_eur
            name: Curs EUR
          - type: attribute
            entity: sensor.bnr_rates_ron_eur
            attribute: Valoare curentă
            name: Valoare curentă
          - type: attribute
            entity: sensor.bnr_rates_ron_eur
            attribute: Valoare anterioară
            name: Valoare anterioară
          - type: attribute
            entity: sensor.bnr_rates_ron_eur
            attribute: Schimbare
            name: Schimbare
          - type: attribute
            entity: sensor.bnr_rates_ron_eur
            attribute: Schimbare procentuală
            name: Schimbare procentuală

          - entity: sensor.bnr_rates_ron_usd
            name: Curs USD
          - type: attribute
            entity: sensor.bnr_rates_ron_usd
            attribute: Valoare curentă
            name: Valoare curentă
          - type: attribute
            entity: sensor.bnr_rates_ron_usd
            attribute: Valoare anterioară
            name: Valoare anterioară
          - type: attribute
            entity: sensor.bnr_rates_ron_usd
            attribute: Schimbare
            name: Schimbare
          - type: attribute
            entity: sensor.bnr_rates_ron_usd
            attribute: Schimbare procentuală
            name: Schimbare procentuală

      # Card pentru Schimburi Valutare
      - type: entities
        title: Schimb Valutar (Cash)
        entities:
          - entity: sensor.bnr_fx_rates_cash_eur
            name: Schimb EUR
          - type: attribute
            entity: sensor.bnr_fx_rates_cash_eur
            attribute: Vânzare
            name: Vânzare
          - type: attribute
            entity: sensor.bnr_fx_rates_cash_eur
            attribute: Cumpărare
            name: Cumpărare

          - entity: sensor.bnr_fx_rates_cash_usd
            name: Schimb USD
          - type: attribute
            entity: sensor.bnr_fx_rates_cash_usd
            attribute: Vânzare
            name: Vânzare
          - type: attribute
            entity: sensor.bnr_fx_rates_cash_usd
            attribute: Cumpărare
            name: Cumpărare

      # Card pentru Dobânzi ROBOR, EURIBOR și IRCC
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
