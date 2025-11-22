

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import secrets
import string

app = Flask(__name__)
app.secret_key = "key_storm_at_2025_final"
DB_NAME = "passwords.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
init_db()

# فقط کاراکترهایی که ۱۰۰٪ همه جا قبول می‌شه (حتی بانک ملت، دیجی‌کالا، اینستا، گوگل)
def generate_password(length=20):
    length = max(8, min(100, int(length)))
    # این مجموعه دقیقاً همونیه که همه سایت‌های دنیا قبول دارن
    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-"
    return ''.join(secrets.choice(allowed_chars) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    password = None
    if request.method == 'POST':
        website = request.form.get('website', '').strip()
        try:
            length = int(request.form.get('length', 20))
        except:
            length = 20

        if not website:
            flash('اسم سایت رو بنویس داداش!', 'error')
        else:
            password = generate_password(length)
            with sqlite3.connect(DB_NAME) as conn:
                conn.execute("INSERT INTO passwords (website, password) VALUES (?, ?)", (website, password))
                conn.commit()
            flash(f'رمز امن برای {website} ساخته شد!', 'success')

    return render_template('index.html', password=password)

@app.route('/passwords')
def show_passwords():
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM passwords ORDER BY created_at DESC")
        passwords = cur.fetchall()
    return render_template('passwords.html', passwords=passwords)

@app.route('/delete/<int:pw_id>')
def delete_password(pw_id):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("DELETE FROM passwords WHERE id = ?", (pw_id,))
        conn.commit()
    flash('رمز حذف شد!', 'success')
    return redirect(url_for('show_passwords'))

if __name__ == '__main__':
    print("KeyStorm v3.0 - ۱۰۰٪ امن و بدون مشکل کپی!")
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)