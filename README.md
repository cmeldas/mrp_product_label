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
