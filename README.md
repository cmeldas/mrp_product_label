# Product Label Management

## Overview

This Odoo module extends the manufacturing capabilities by adding comprehensive label management features for product variants. It's designed to help manufacturers maintain detailed product labeling information that is essential for production and compliance.

## Features

- Enhanced product variant management with label-specific fields:
  - Label Name
  - Label Subtitle
  - Label Ingredients
  - Label Lifetime
  - Label Weight
  - Label Storage Temperature

## Dependencies

- `product`: Base product management
- `mrp`: Manufacturing module
- `mrp_pasteurization`: Manufacturing pasteurization module

## Views Modified

- Product Views (`views/product_views.xml`)
- Manufacturing Order Views (`views/mrp_production_views.xml`)

## Odoo 20

Větev `20.0`, verze `20.0.1.1.0` (vyžaduje `mrp_pasteurization` 20.0). Logika modulu se
nemění, ověřené proti zdrojům Odoo 20:

- `mrp.production` v 20 nemá `_onchange_product_id` (stejně jako 19), modul proto dál používá
  vlastní onchange `_onchange_product_id_label_data` bez `super()`.
- Datum spotřeby závisí na `date_start` a `pasteurisation_start`, obě pole v 20 zůstala.
  Přejmenování `product_uom_id` → `uom_id` se modulu netýká.
- Cron `ir_cron_recompute_label_expiry_date` a pohledy `mrp.mrp_production_form_view`,
  `product.product_normal_form_view` mají v 20 stejnou strukturu.
- Popisek pole `label_description` je nově **Label Description** (česky „Popis na etiketě“).
  Dřív se jmenovalo stejně jako standardní `description` na `product.product` a Odoo při každém
  načtení hlásilo varování o dvou polích se stejným popiskem. Technický název pole se nemění.
- Odoo 20 už nemá Font Awesome, atribut `icon` tlačítek je název ikony Material Symbols.
  Tlačítko „Get new label data from product“ má proto `icon="refresh"` místo `fa-refresh`
  (jinak by místo ikony ukazovalo text „fa-refresh“).
- Autor v manifestu sjednocen na Matouš Čmelík (kontakt zůstává v `maintainer`).
- Nově jsou v `tests/` testy (kopie etikety při vytvoření, onchange ve formuláři, tlačítko
  pro načtení etikety z produktu, datum spotřeby, cron).

**Migrace dat:** žádná. Vlastní sloupce `label_*` na `mrp_production` a `product_product`
zůstávají (na produkci 6. 10. 2026: 720 zakázek s etiketou, 26 variant s etiketou). Nový popisek
pole a jeho český překlad se zapíšou při `-u` modulu.
