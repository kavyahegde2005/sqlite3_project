from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

def init_db():
    conn = sqlite3.connect("hotel_booking.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS property (
        property_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        property_type TEXT,
        city TEXT,
        price_per_day INTEGER,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS offers (
        offer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT,
        title TEXT,
        description TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM property")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
        INSERT INTO property (name, property_type, city, price_per_day, image)
        VALUES (?, ?, ?, ?, ?)
        """, [
            ('Ocean View Hotel', 'Hotel', 'Goa', 2500, '/static/images/img1.jpg'),
            ('City Apartment', 'Apartment', 'Bangalore', 4800, '/static/images/img2.jpg'),
            ('Luxury Villa', 'Villa', 'Kerala', 4000, '/static/images/img3.jpg'),
            ('Heaven Resorts', 'Resorts', 'Mumbai', 5500, '/static/images/img4.jpg'),
            ('Pearl Bunglow', 'Bunglow', 'Bangalore', 6900, '/static/images/img5.jpg'),
            ('Garden Villa', 'Villa', 'Kerala', 4500, '/static/images/img6.jpg'),
            ('Backyard Villa', 'Villa', 'Andrapradesh', 8200, '/static/images/img7.jpg'),
            ('Grace Cabins', 'Cabins', 'Chennai', 8800, '/static/images/img8.jpg'),
            ('Milestone Cottage', 'Cottages', 'Kerala', 4000, '/static/images/img9.jpg'),
            ('New way Glamping', 'Glamping Sites', 'Meghalaya', 9000, '/static/images/img10.jpg')
        ])

    cursor.execute("SELECT COUNT(*) FROM offers")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO offers (tag, title, description)
        VALUES (?, ?, ?)
        """, (
            'Early 2026 Deals',
            'At least 15% off',
            'Save on your next stay with Early 2026 Deals. Book now, stay until 1 April 2026.'
        ))

    conn.commit()
    conn.close()


init_db()

def get_db_connection():
    conn = sqlite3.connect("hotel_booking.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)",
            (name, email, password, phone)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/search')
def search():
    city = request.args.get('city')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM property WHERE city LIKE ?", (f"%{city}%",))
    results = cursor.fetchall()
    conn.close()

    return render_template('search.html', properties=results, city=city)

@app.route('/stays')
def stays():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM property")
    properties = cursor.fetchall()
    conn.close()
    return render_template('stays.html', properties=properties)

@app.route('/offers')
def offers():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM offers")
    offers = cursor.fetchall()
    conn.close()
    return render_template('offers.html', offers=offers)

@app.route('/property-type')
def property_type():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT property_type, image FROM property")
    properties = cursor.fetchall()
    conn.close()
    return render_template('property_type.html', properties=properties)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        payment_method = request.form['payment_method']
        return redirect(url_for('successs'))

    return render_template('payment.html')

@app.route('/successs')
def successs():
    return render_template('successs.html')

if __name__ == '__main__':
    app.run(debug=True)
