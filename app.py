from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, session, jsonify
)
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash


# ---------------------------------------------
# INITIAL SETUP
# ---------------------------------------------

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a-very-secret-key-change-this'

# --- Database Configuration ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Kadire_sai',
    'database': 'Nutriguide_db'
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


# ---------------------------------------------
# AUTH PAGES
# ---------------------------------------------

@app.route('/')
def splash():
    return render_template('splash.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True, buffered=True)

            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.', 'error')
                return redirect(url_for('login'))

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        try:
            conn = get_db_connection()
            cursor = conn.cursor(buffered=True)

            cursor.execute("SELECT id FROM users WHERE username=%s OR email=%s", (username, email))
            if cursor.fetchone():
                flash("Username or email already exists.", 'error')
                return redirect(url_for('signup'))

            hashed_password = generate_password_hash(password)
            cursor.execute(
                "INSERT INTO users (fullname, email, username, password_hash) VALUES (%s, %s, %s, %s)",
                (fullname, email, username, hashed_password)
            )
            conn.commit()

            flash("Account created! Please login.", 'success')
            return redirect(url_for('login'))

        finally:
            cursor.close()
            conn.close()

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('index'))


# ---------------------------------------------
# MAIN PAGES
# ---------------------------------------------

@app.route('/index')
def index():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, slug, emoji FROM categories ORDER BY id")
        categories = cursor.fetchall()
    except:
        categories = []
    finally:
        cursor.close()
        conn.close()

    return render_template('index.html', session=session, categories=categories)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/lifestyle')
def lifestyle():
    return render_template('lifestyle.html')


@app.route('/women')
def women():
    return render_template('women.html')


@app.route('/kids')
def kids():
    return render_template('kids.html')


@app.route('/corporates')
def corporates():
    return render_template('corporates.html')


@app.route('/how_it_work')
def how_it_work():
    return render_template('how_it_work.html')


@app.route('/praises1')
def praises1():
    return render_template('praises1.html')


@app.route('/iplan1')
def iplan1():
    return render_template('iplan1.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/shareyourparses', methods=['GET', 'POST'])
def shareyourparses():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            flash("All fields required!", "error")
            return redirect(url_for('shareyourparses'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO praises (name, email, message) VALUES (%s, %s, %s)",
                (name, email, message)
            )
            conn.commit()
            flash("Thank you for your message!", "success")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('shareyourparses'))

    return render_template('shareyourparses.html')


# ---------------------------------------------
# RECIPES (Nutribites)
# ---------------------------------------------

@app.route('/nutribites')
def nutribites():
    return render_template('nutribites.html')


@app.route('/salad')
def salad():
    return render_template('salad.html')


@app.route('/soup')
def soup():
    return render_template('soup.html')


@app.route('/sandwich')
def sandwich():
    return render_template('sandwich.html')


@app.route('/pasta')
def pasta():
    return render_template('pasta.html')


@app.route('/dessert')
def dessert():
    return render_template('dessert.html')


@app.route('/smoothie')
def smoothie():
    return render_template('smoothie.html')


@app.route('/paneer')
def paneer():
    return render_template('paneer.html')


@app.route('/fruit')
def fruit():
    return render_template('fruit.html')


# ---------------------------------------------
# CALORIE CALCULATOR
# ---------------------------------------------

@app.route('/calorie', methods=['GET', 'POST'])
def calorie():
    if request.method == 'POST':
        food_item = request.form['food_item']
        quantity = float(request.form['quantity'])

        # --- Calorie database ---
        calorie_db = {
            "rice": 1.30, "chapati": 3.10, "brown rice": 1.11,
            "chicken biryani": 1.90, "mutton biryani": 2.10,
            "egg": 1.55, "milk": 0.42, "curd": 0.98,
            "apple": 0.52, "banana": 0.89,
            "dosa": 1.68, "idli": 1.60,
            "dal": 1.16, "paneer": 2.65,
            "burger": 2.95, "pizza": 2.66,
            "chips": 5.36, "almonds": 5.76,
        }

        key = food_item.lower()
        calories = quantity * calorie_db.get(key, 0)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO calorie_intake (food_item, quantity, calories) VALUES (%s, %s, %s)",
                (food_item, quantity, calories)
            )
            conn.commit()
            flash(f"{food_item} = {round(calories, 2)} calories added!", "success")

        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('calorie'))

    return render_template('calorie.html')


# ---------------------------------------------
# CONTACT ENQUIRY
# ---------------------------------------------

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_enquiry', methods=['POST'])
def submit_enquiry():
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    service = request.form.get("service")
    requirement = request.form.get("requirement")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO enquiries (name, email, phone, service, requirement) VALUES (%s, %s, %s, %s, %s)",
            (name, email, phone, service, requirement)
        )
        conn.commit()
        flash("Enquiry submitted!", "success")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('contact'))


# ---------------------------------------------
# FOOD MENU (Requires Login)
# ---------------------------------------------

def login_required():
    if 'user_id' not in session:
        flash("Please login first.", "error")
        return False
    return True


@app.route('/veg')
def veg_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('veg.html')


@app.route('/nonveg')
def nonveg_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('nonveg.html')


@app.route('/biryani')
def biryani_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('biryani.html')


@app.route('/salads')
def salads_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('salads.html')


@app.route('/drinks')
def drinks_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('drinks.html')


@app.route('/desserts')
def desserts_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('desserts.html')


@app.route('/shakes')
def shakes_menu():
    if not login_required(): return redirect(url_for('login'))
    return render_template('shakes.html')


@app.route('/cart')
def cart():
    if not login_required(): return redirect(url_for('login'))
    return render_template('cart.html')


# -----------------------------------------------------
# RUN APP
# -----------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)