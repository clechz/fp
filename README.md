# Clechz Storefront

A CS50 final-project e-commerce simulation built with Flask, SQLite, and server-rendered HTML.

The project explores the flow from browsing a catalogue to saving products, adjusting a cart, and reviewing a checkout summary. It does not process payments or complete real orders.

## Implemented flows

| Route | Behavior |
| --- | --- |
| `/` | Catalogue, categories, and category-based suggestions |
| `/signup`, `/login`, `/logout` | Account and session flow |
| `/search` | Search by product title or category, with sorting |
| `/wish` | Add and remove saved products |
| `/cart` | Cart quantities and price summary |
| `/settings`, `/change_password` | Settings page and password-change flow |
| `/checkout` | Review a checkout summary |

## How it is organized

`application.py` contains the Flask routes and database queries. Templates live in `templates/`, browser assets in `static/`, and the SQLite database in `main.db`. The application imports Flask-Session, Werkzeug, CS50 SQL, and a local `helpers` module.

Recommendations use product categories and saved/cart data; they are not a machine-learning recommendation system.

## Running the historical project

The current checkout is incomplete: `application.py` imports `helpers.py`, but that file is absent from the repository root. There is also no dependency manifest establishing a reproducible environment.

Restore the original helper module and compatible dependencies before trying to run the app. Once those are restored, the expected Flask entry point is:

```bash
flask --app application run
```

Use a disposable local database with synthetic data.

## Current status

This is a historical learning project. The login route contains a hard-coded password bypass that must be removed before any deployment. Authentication and password-change behavior need review, and checkout remains a summary rather than an order or payment flow.

The repository documents early full-stack work; it should not be presented as a production storefront.
