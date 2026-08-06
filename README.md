# Vinylite — Music Gallery (Django)

A simple, warm-toned music gallery app: sign up, sign in, add songs with
streaming links, search the gallery, and build playlists.

## Run it

```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser.

## Project layout

- `musicgallery/` — Django project settings and root urls.py
- `gallery/` — the app: models.py, views.py, forms.py, urls.py
  - `gallery/static/gallery/css/style.css` — all styling
  - `gallery/templates/gallery/` — all HTML pages
- No JS frameworks, no separate frontend — just Django, HTML, and CSS.

## Notes on a couple of design decisions

- **Passwords**: stored using Django's built-in `User` model, which hashes
  passwords automatically (never stored as plain text). This is safer than
  a hand-rolled table and was the one part I did not build "from scratch."
- **Sign in by email**: since sign-in only asks for gmail + password, the
  account's `username` is set to the email under the hood so Django's
  authentication can look it up.
- **Logout destination**: you asked for logout to redirect to "the home
  page," but the home page requires being logged in — that would create a
  loop. I sent logout to the welcome (sign in / sign up) page instead,
  which is the reachable equivalent. Easy to change in
  `gallery/views.py` → `logout_view` if you want something else.

<img width="1919" height="994" alt="Screenshot 2026-08-06 221555" src="https://github.com/user-attachments/assets/611799b2-4f59-4e20-b3dd-42a87862eab0" />

<img width="1920" height="991" alt="Screenshot 2026-07-26 041116" src="https://github.com/user-attachments/assets/342b1731-e849-4eb6-bad7-7816606459fd" />

<img width="1920" height="980" alt="Screenshot 2026-07-26 041238" src="https://github.com/user-attachments/assets/f6d84cb8-83a4-4b78-8fec-e76e4b307850" />

<img width="1920" height="995" alt="Screenshot 2026-07-26 211438" src="https://github.com/user-attachments/assets/904a8aa4-6551-4756-84ed-e4c6dd80c5b2" />

<img width="1920" height="989" alt="Screenshot 2026-07-26 041145" src="https://github.com/user-attachments/assets/f6c77af8-de76-4bd4-ae21-1770d7eff6dd" />

