from flask import Flask, render_template, request, redirect, session, flash, jsonify
from os import getenv
from numpy import array, mean
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from radar import radarchart

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///<käyttäjänimi>"
db = SQLAlchemy(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "username" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT user_id, password FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
        if not user:
            flash("Incorrect username or password")
            return render_template("login.html")
        else:
            hash_value = user.password
            if check_password_hash(hash_value, password):
                session["username"] = username
                session["user_id"] = user.user_id
                return redirect("/dashboard")
            else:
                flash("Incorrect username or password")
                return render_template("login.html")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        sql = text("SELECT * FROM users WHERE username=:username")
        result = db.session.execute(sql, {"username": username})
        if result.fetchone():
            flash("Username taken, please choose another one", "error")
            return render_template("signup.html")
        hash_value = generate_password_hash(password)
        sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")

@app.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    username = session.get("username")
    return render_template("dashboard.html", username=username)

@app.route("/rate", methods=["GET", "POST"])
@login_required
def rate():
    username = session.get("username")
    regions = db.session.execute(text("SELECT region_name FROM regions")).fetchall()
    regions = [region[0] for region in regions]
    producers = db.session.execute(text("SELECT producer_name FROM producers")).fetchall()

    if request.method == 'POST':
        oil_name = request.form['oil_name']
        oil_region = request.form['region']
        oil_producer = request.form['producer']
        oil_other_producer = request.form['other_producer']
        oil_rating = request.form['oil_rating']
        oil_fruity = int(request.form['fruity'])
        oil_grassy = int(request.form['grassy'])
        oil_salty = int(request.form['salty'])
        oil_sweet = int(request.form['sweet'])
        oil_floral = int(request.form['floral'])
        oil_pungent = int(request.form['pungent'])
        oil_citrusy = int(request.form['citrusy'])

        if oil_producer == 'Other':
            oil_producer = oil_other_producer
            sql = text("INSERT INTO producers (producer_name, region_id) VALUES (:producer_name, (SELECT region_id FROM regions WHERE region_name=:region_name)) RETURNING producer_id")
            result = db.session.execute(sql, {"producer_name": oil_producer, "region_name": oil_region})
            producer_id = result.fetchone()[0]
            db.session.commit()
        else:
            sql = text("SELECT producer_id FROM producers WHERE producer_name=:producer_name")
            result = db.session.execute(sql, {"producer_name": oil_producer})
            producer_id = result.fetchone()[0]

        sql = text("SELECT region_id FROM regions WHERE region_name=:region_name")
        result = db.session.execute(sql, {"region_name": oil_region})
        region_id = result.fetchone()[0]

        sql = text("""
            INSERT INTO oils (oil_name, producer_id, region_id)
            VALUES (:oil_name, :producer_id, :region_id)
            ON CONFLICT (oil_name, producer_id, region_id) DO NOTHING
            RETURNING oil_id
        """)

        result = db.session.execute(sql, {
            "oil_name": oil_name,
            "producer_id": producer_id,
            "region_id": region_id
        })

        oil_id = result.fetchone()

        if oil_id:
            oil_id = oil_id[0]
        else:
            sql = text("""
                SELECT oil_id FROM oils WHERE oil_name = :oil_name AND producer_id = :producer_id AND region_id = :region_id
            """)
            result = db.session.execute(sql, {
                "oil_name": oil_name,
                "producer_id": producer_id,
                "region_id": region_id
            })
            oil_id = result.fetchone()[0]

        db.session.commit()

        user_id = session.get("user_id")
        
        sql = text("""
            INSERT INTO ratings (user_id, oil_id, rating, fruity, grassy, salty, sweet, floral, pungent, citrusy)
            VALUES (:user_id, :oil_id, :rating, :fruity, :grassy, :salty, :sweet, :floral, :pungent, :citrusy)
            ON CONFLICT (user_id, oil_id) DO UPDATE SET
                rating = EXCLUDED.rating,
                fruity = EXCLUDED.fruity,
                grassy = EXCLUDED.grassy,
                salty = EXCLUDED.salty,
                sweet = EXCLUDED.sweet,
                floral = EXCLUDED.floral,
                pungent = EXCLUDED.pungent,
                citrusy = EXCLUDED.citrusy
        """)
        db.session.execute(sql, {
            "user_id": user_id,
            "oil_id": oil_id,
            "rating": oil_rating,
            "fruity": oil_fruity,
            "grassy": oil_grassy,
            "salty": oil_salty,
            "sweet": oil_sweet,
            "floral": oil_floral,
            "pungent": oil_pungent,
            "citrusy": oil_citrusy
        })
        db.session.commit()

        sql = text("SELECT rating, fruity, grassy, salty, sweet, floral, pungent, citrusy FROM ratings WHERE oil_id=:oil_id")
        result = db.session.execute(sql, {"oil_id": oil_id})
        ratings = [list(row) for row in result.fetchall()]
        
        if ratings:
            ratings_array = array(ratings)
            averages = mean(ratings_array, axis=0)
            averages = list(averages)
        else:
            averages = []
        
        radarchart(values=[oil_fruity, oil_grassy, oil_salty, oil_sweet, oil_floral, oil_pungent, oil_citrusy], average_values=averages[1:8])

        return redirect(f"/rating/{oil_id}")

    return render_template("rate.html", regions=regions, producers=producers)

@app.route("/rating/<int:oil_id>")
@login_required
def rating(oil_id):
    country_codes = {
        "Italy": "it", "Spain": "es", "Greece": "gr", "Portugal": "pt", 
        "France": "fr", "Turkey": "tr", "Tunisia": "tn", "European Union": "eu", 
        "Other": "un"
    }

    sql = text("""
        SELECT oils.oil_name, producers.producer_name, regions.region_name, ratings.rating
        FROM oils
        JOIN producers ON oils.producer_id = producers.producer_id
        JOIN regions ON oils.region_id = regions.region_id
        JOIN ratings ON oils.oil_id = ratings.oil_id
        WHERE oils.oil_id = :oil_id AND ratings.user_id = :user_id
    """)
    
    result = db.session.execute(sql, {"oil_id": oil_id, "user_id": session.get("user_id")})
    oil = result.fetchone()

    if oil:
        oil_name, oil_producer, oil_region, oil_rating = oil
        country_code = country_codes.get(oil_region, "un")
        return render_template(
            "rating.html", oil_name=oil_name, oil_producer=oil_producer, 
            oil_region=oil_region, oil_rating=oil_rating, country_code=country_code
        )
    else:
        return redirect("/your-oils")

@app.route("/your-oils", methods=["GET"])
@login_required
def your_oils():
    user_id = session.get("user_id")
    
    sql = text("""
        SELECT oils.oil_id, oils.oil_name, producers.producer_name, regions.region_name, ratings.rating
        FROM ratings
        JOIN oils ON ratings.oil_id = oils.oil_id
        JOIN producers ON oils.producer_id = producers.producer_id
        JOIN regions ON oils.region_id = regions.region_id
        WHERE ratings.user_id = :user_id
    """)
    
    result = db.session.execute(sql, {"user_id": user_id})
    oils = result.fetchall()
    
    return render_template("your-oils.html", oils=oils)

@app.route("/best-oils")
@login_required
def best_oils():
    return render_template("best-oils.html")

@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect("/login")

@app.route("/get_producers/<region_name>", methods=["GET"])
def get_producers(region_name):
    sql = text("""SELECT producer_name 
               FROM producers 
               WHERE region_id = (SELECT region_id FROM regions WHERE region_name=:region_name) 
               ORDER BY producer_name""")
    producers = db.session.execute(sql, {"region_name": region_name}).fetchall()
    producer_list = [producer[0] for producer in producers]
    producer_list.append("Other")
    return jsonify(producer_list)

@app.route("/get_oils/<region_name>/<producer_name>", methods=["GET"])
def get_oils(region_name, producer_name):
    sql = text("""SELECT oil_name 
               FROM oils 
               WHERE region_id = (SELECT region_id FROM regions WHERE region_name=:region_name) 
               AND producer_id = (SELECT producer_id FROM producers WHERE producer_name=:producer_name 
               AND region_id=(SELECT region_id FROM regions WHERE region_name=:region_name)) 
               ORDER BY oil_name""")
    result = db.session.execute(sql, {"producer_name": producer_name, "region_name": region_name})
    oils = [row.oil_name for row in result.fetchall()]
    return jsonify(oils)

@app.route("/get_ratings/<int:oil_id>", methods=["GET"])
@login_required
def get_ratings(oil_id):
    sql = text("SELECT rating, fruity, grassy, salty, sweet, floral, pungent, citrusy FROM ratings WHERE oil_id=:oil_id")
    result = db.session.execute(sql, {"oil_id": oil_id})
    ratings = [list(row) for row in result.fetchall()]
    
    if ratings:
        ratings_array = array(ratings)
        averages = mean(ratings_array, axis=0)
        averages = list(averages)
    else:
        averages = []

    return jsonify(averages)