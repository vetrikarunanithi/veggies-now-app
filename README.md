# Amudham Care — Skincare — Flask + JSON

A minimal, modern skincare storefront inspired by innovist.com using **Flask + HTML/CSS + JSON (no database)**, featuring:
- User signup/login, session cart, checkout, order history.
- Admin login, product management (add/edit/delete), order viewing.
- JSON storage in `data/` for users, products, and orders.

## Quick Start
1. Create and activate a virtual env (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:
   ```bash
   flask --app app.py --debug run
   ```
   App runs at http://127.0.0.1:5000

### Default Admin
- Email: admin@site.com
- Password: admin123

### Notes
- Products images use URLs; you can host images elsewhere or place files in `static/img` and reference `/static/img/...`.
- JSON files live in `data/`. They are simple and human-editable.
