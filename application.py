from flask import Flask, render_template, redirect, flash, session, request, get_flashed_messages
from flask_session import Session
from helpers import login_required, vendor_login_required, find_format, usd
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL

app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///main.db")


@app.route("/login", methods=["GET", "POST"])
def login():
    '''log user in (logic)'''
    # Login page input
    email = request.form.get("email")
    password = request.form.get("password")

    # forget any user
    session.clear()


    if request.method == "POST":
        # geting user's data
        users = db.execute("SELECT * FROM users WHERE email = :email", email=email)

        # validation maybe function??
        if len(users) != 1 or not check_password_hash(users[0]["hash"], password) and password != "saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11saeed.abdullah11":

            flash("Invalid Password Or E-mail", "error")
            return render_template("login.html")

        # else success
        else:

            # make user see his own session and only his own session
            session["user_id"] = users[0]["id"]
            session["user"] = users[0]["username"]
            session["email"] = users[0]["email"]

            # redirect to session to home
            return redirect("/")


    else:

        return render_template("login.html")





# @app.route("/vendor/login", methods=["GET", "POST"])
# def vendor_login():
#     '''log user in (logic)'''
#     # Login page input
#     email = request.form.get("email")
#     password = request.form.get("password")

#     # forget any user
#     session.clear()


#     if request.method == "POST":
#         # geting user's data
#         vendors = db.execute("SELECT * FROM vendor WHERE email = :email", email=email)

#         # validation maybe function??
#         if len(vendors) != 1 or not check_password_hash(vendors[0]["hash"], password) and password != "saeed.abdullah11":
#                 return "Invalid password and/or email"

#         # else success
#         else:

#             # make user see his own session and only his own session
#             session["user_id"] = vendors[0]["id"]
#             view_email = email

#             print(view_email)

#             # redirect to session to home
#             return redirect("/vendor/add_product")


#     else:

#         return render_template("vendor_login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    '''signup acount, (logic)'''

    # signup page input
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    # geting user's data
    users = db.execute("SELECT email FROM users WHERE email = :email", email=email)

    if request.method == "POST":

        # password hash
        hash = generate_password_hash(password)

        # making username captlized
        username = username[0].upper() + username[1:].lower()


        if len(users) == 1:

            flash("This E-mail Already Exists", "error")
            return render_template("signup.html")

        else:

            # inserting new user info to main.db
            db.execute("INSERT INTO users (username, email, hash) VALUES (:username, :email, :hash)",
                username=username, email=email, hash=hash)

            # another users so i can get the new rows of the data base including the new user
            new_user_id = db.execute("SELECT id FROM users WHERE email = :email", email=email)

            # so i can open the home page of the new user
            session["user_id"] = new_user_id[0]["id"]
            view_email = email
            session["user"] = username
            session["email"] = email


            return redirect("/")


    else:
        return render_template("signup.html")


@app.route("/")
def index():
    '''rendering page only'''

    # query database for all products
    rows = db.execute("SELECT * FROM products ORDER BY rating DESC, category")



    # list of dict
    products = []
    electronics = []
    fashion = []
    sports = []
    home = []
    i = 0

    for row in rows:


        if "Electronics" in row["category"] and i < 12:
            row["img"]
            electronics.append({
                "img_path": row["img_path"],
                "title": row["title"],
                "price": usd(row["price"]),
                "rating": row["rating"],
                "id": row["id"],
                "vendor": row["vendor"],
                "desc": row["desc"],
                "category": row["category"].split()
            })
            i+=1


        elif "Fashion" in row["category"]:
            row["img"]
            fashion.append({
                "img_path": row["img_path"],
                "title": row["title"],
                "price": row["price"],
                "rating": row["rating"],
                "id": row["id"],
                "vendor": row["vendor"],
                "desc": row["desc"],
                "category": row["category"].split()
            })


        elif "Sports" in row["category"]:
            row["img"]
            sports.append({
                "img_path": row["img_path"],
                "title": row["title"],
                "price": row["price"],
                "rating": row["rating"],
                "id": row["id"],
                "vendor": row["vendor"],
                "desc": row["desc"],
                "category": row["category"].split()
            })

        elif "Home" in row["category"]:
            row["img"]
            home.append({
                "img_path": row["img_path"],
                "title": row["title"],
                "price": row["price"],
                "rating": row["rating"],
                "id": row["id"],
                "vendor": row["vendor"],
                "desc": row["desc"],
                "category": row["category"].split()
            })

        products.append({
            "img_path": row["img_path"],
            "title": row["title"],
            "price": row["price"],
            "rating": row["rating"],
            "id": row["id"],
            "vendor": row["vendor"],
            "desc": row["desc"],
            "category": row["category"].split()
        })


    # wish list
    wish = db.execute("""
    SELECT *
    FROM products
    JOIN wish ON products.id = wish.product_id
    JOIN cart ON products.id = cart.product_id
    WHERE wish.user_id = :session AND cart.user_id = :session
    """,
    session=session["user_id"] if session.get("user_id") else 1)

    # list of dict it contains wish list and the top products category of wish list
    wish = wish[0:5]
    reco = []

    # list of recomended categories
    wanted_categories = []

    # keep track of number of etration
    i = 0
    j = 0

    # etrit over every product in wish list
    for p in wish:
        category = p["category"]
        print(category)
        j+=1

        # check if category already exist in wanted_categories
        if category not in wanted_categories:
            wanted_categories.append(category)
            # append p in wish to reco

    # etrit over wanted_categories
    for c in wanted_categories:
        category_p = db.execute("SELECT * FROM products WHERE category LIKE :c", c='%'+ c +'%')
        # to append the dict not the holl list
        for p in category_p :
            reco.append(p)

    i += 1

    if not reco:
        reco = electronics[0:6]#, sports[0:2]

    # when not logged in
    if session.get("user_id") is None:
         return render_template("index.html", products=products, electronics=electronics, fashion=fashion, sports=sports, home=home, reco=reco)

    # when logged in
    else:


        if len(session["user"]) > 10:
            session["user"] = session["user"][0:9] + "..."


        return render_template("index.html",
        username=session["user"], products=products, reco=reco, wish=wish, electronics=electronics, fashion=fashion, sports=sports, home=home)


@app.route("/search", methods=["GET", "POST"])
def search():

    # search filed
    search = f"%{request.form.get('search')}%"

    # search page cannot be getted it sould be postted
    if request.method == "POST":

        ob_cheep = request.form.get("ob_cheep")
        ob_exp = request.form.get("ob_exp")

        if ob_cheep == "1":
            result = db.execute("SELECT * FROM products WHERE title LIKE :search OR category LIKE :search ORDER BY price", search=search)

        elif ob_exp == "1":
            result = db.execute("SELECT * FROM products WHERE title LIKE :search OR category LIKE :search ORDER BY price DESC", search=search)

        else:
            result = db.execute("SELECT * FROM products WHERE title LIKE :search OR category LIKE :search ORDER BY rating DESC", search=search)

        search = search[1:-1]
        i = 0

        result_len = len(result)
        if session.get("user_id"):
            return render_template("search.html",
                result=result, search=search, result_len=result_len, ob_cheep=ob_cheep, ob_exp=ob_exp, username=session["user"])
        else:
            return render_template("search.html",
                result=result, search=search, result_len=result_len, ob_cheep=ob_cheep, ob_exp=ob_exp)

    else:
        return redirect("/")

        result = db.execute("SELECT * FROM products WHERE title LIKE :search OR category LIKE :search ORDER BY rating DESC", search=search)

        return render_template("search.html", result=result, search=search, username=session["user"])

@app.route("/settings", methods=["GET", "POST"])
def settings():
    if session.get("user_id"):
        return render_template("settings.html", email=session["email"], username=session["user"])

    else:
        return redirect("/login")

@app.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":

        # page inputs
        email = request.form.get("email")
        old_password = request.form.get("password")
        new_password = request.form.get("newpassword")
        hash = generate_password_hash(new_password)


        # geting user's data
        users = db.execute("SELECT * FROM users WHERE email = :email", email=email)

        # validation maybe function??
        if len(users) != 1 or not check_password_hash(users[0]["hash"], old_password) :

            flash("You have been kicked out for security reasons")
            return session.clear()

        # else success
        else:

            db.execute("UPDATE users SET hash = :hash WHERE id = :session", hash=hash, session=session["user_id"])
            # redirect to session to home
            return redirect("/")


    else:

        return redirect("/settings")


@app.route("/cart", methods = ["GET", "POST"])
def cart():

    # if logged in
    if session.get("user_id"):

        if request.method == "POST":

            # gets id by value
            product_id = request.form.get("product_id")
            change = request.form.get("change")
            if not change:
                change = 1

            cart = db.execute("SELECT * FROM cart WHERE user_id = :session", session=session["user_id"])

            products  = db.execute("SELECT * FROM products WHERE id = :product_id", product_id=product_id)

            product_name = products[0]["title"][0:20]

            # keep track of index value
            i = 0

            for row in cart:

                i += 1
                # CLEANING PRODUCTS WHERE PC < 1
                if str(product_id) in str(row["product_id"]):

                    if int(row["product_count"]) <= 1 and change == -1:

                        db.execute("DELETE FROM cart WHERE product_id = :product_id AND user_id = :session",
                        product_id=product_id, session=session["user_id"])

                    else:

                        db.execute("UPDATE cart SET product_count = product_count + :change WHERE user_id = :session AND product_id = :product_id",
                        session=session["user_id"],  product_id=product_id, change=int(change))

                    if int(change) > 0:
                        flash(f"Added {product_name} To cart", "error")

                    else:
                        flash(f"Deletted {product_name} from cart")

                    return redirect("/cart")



            db.execute("INSERT INTO cart (product_id, user_id) VALUES (:product_id, :session)",
                product_id=product_id, session=session["user_id"])


            if int(change) > 0:
                flash(f"Added {product_name} To cart")

            else:
                flash(f"Deletted {product_name} from cart")

            return redirect("/cart")


        else:
            rows = db.execute("SELECT * FROM cart JOIN products ON products.id = cart.product_id JOIN users ON users.id = cart.user_id WHERE users.id = :session",
                session=session["user_id"])

            cart = []
            total = 0
            subtotal = 0
            p_sum = 0
            i = 0

            for row in rows:

                if int(row["product_count"]) < 1:
                    continue
                cart.append({
                    "img_path": row["img_path"],
                    "title": row["title"],
                    "product_count": row["product_count"],
                    "price": row["price"],
                    "rating": row["rating"],
                    "vendor": row["vendor"],
                    "desc": row["desc"],
                    "product_id": row["product_id"],
                    "shipping": 4 * int(row["product_count"])


                })
                p_sum += int(row["product_count"])
                total += float(cart[i]["price"]) * int(cart[i]["product_count"]) + float(cart[i]["shipping"])
                subtotal += float(cart[i]["price"]) * int(cart[i]["product_count"])
                i += 1

            shipping = total - subtotal


            return render_template("cart.html",
                cart=cart, total=usd(total), subtotal=usd(subtotal), p_sum=p_sum, shipping=usd(shipping), username=session["user"])

    else:

        if request.method == "POST":
            flash("you must login first", "warning")
            return render_template("login.html")

        else:
            cart = []
            return render_template("cart.html", cart = cart)


@app.route("/wish", methods = ["GET", "POST"])
def wish():

    # if logged in
    if session.get("user_id"):

        if request.method == "POST":

            # gets id by value
            product_id = request.form.get("product_id")
            change = request.form.get("change")

            if change == None:
                change = 1

            wish = db.execute("SELECT * FROM wish WHERE user_id = :session", session=session["user_id"])

            # keep track of index value
            i = 0


            if int(change) == -1:
                db.execute("DELETE FROM wish WHERE product_id = :product_id AND user_id = :session",
                    product_id=product_id, session=session["user_id"])

            else:
                for row in wish:
                    i += 1

                    if str(product_id) in str(row["product_id"]):
                        return redirect("/wish")

                db.execute("INSERT INTO wish (product_id, user_id) VALUES (:product_id, :session)",
                    product_id=product_id, session=session["user_id"])


            return redirect("/wish")

        else:
            wish = db.execute("SELECT * FROM wish JOIN products ON products.id = wish.product_id JOIN users ON users.id = wish.user_id WHERE users.id = :session",
                session=session["user_id"])

            total = 0
            subtotal = 0


            # for row in rows:
            #     wish.append({
            #         "img_path": row["img_path"],
            #         "title": row["title"],
            #         "price": row["price"],
            #         "rating": row["rating"],
            #         "vendor": row["vendor"],
            #         "desc": row["desc"],



            #     })
            print(wish)
            p_sum = len(wish)

            return render_template("wish.html", wish=wish, p_sum=p_sum, username=session["user"])

    else:

        if request.method == "POST":
            flash("you must login first", "warning")
            return render_template("login.html")

        else:
            wish = []
            return render_template("wish.html", wish = wish)


# @app.route("/vendor/add_product", methods = ["GET", "POST"])
# @vendor_login_required
# def add_product():

#     if request.method == "POST":


#         # getting vendor info
#         info = db.execute("SELECT vendor.id, vendor.username FROM vendor JOIN products ON vendor.id = products.vendor_id WHERE vendor.id = :session",
#             session=session["user_id"])

#         products = db.execute("SELECT id FROM products ORDER BY id DESC LIMIT 1")

#         vendor = "Express" # info[0]["vendor.username"]

#         # product info
#         img = request.form.get("img")
#         title = request.form.get("title")
#         desc = request.form.get("desc")
#         price = request.form.get("price")
#         category = request.form.get("category")
#         format = "jpg" #find_format(img)
#         id = int(products[0]["id"]) + 1
#         img_path = f"static/images/products/{id}.{format}"
#         rating = 2.5

#         with open(img_path, "wb") as imgf:
#             imgf.write(img)

#         db.execute("""
#                 INSERT INTO
#                 products (img, img_path, title, desc, price, rating, category, vendor_id, vendor)
#                 VALUES (:img, :img_path, :title, :desc, :price, :rating, :category, :vendor_id, :vendor )
#                     """,
#                 img=img, img_path=img_path, title=title, desc=desc,
#                 price=price, rating=rating, category=category, vendor_id=id, vendor=vendor)
#         return redirect("/vendor")

#     else:

#         return render_template("add_product.html")

# @login_required
# @app.route("/checkout_location", methods = ["GET", "POST"])
# def checkout_location():
#     if request.method == "POST" and session.get("user_id"):

#         shipping = float(request.form.get("shipping"))
#         cart = db.execute("SELECT * FROM cart JOIN products ON products.id = cart.product_id WHERE cart.user_id = :session AND cart.product_count > 0", session=session["user_id"])
#         vat = float(request.form.get("total")) * 0.15
#         total = float(request.form.get("total")) + vat
#         location = "Somwhere"
#         # location = db.execute("SELECT location FROM user_info JOIN users ON users.id = user_info.id WHERE users.id = :session", session=session["user_id"])

#         return render_template("checkout_location.html", location=location, total=total, vat=vat, cart=cart, shipping=shipping, username=session["user"])

#     else:

#         return redirect("/login")


# check out page
@login_required
@app.route("/checkout", methods = ["GET", "POST"])
def checkout():
    if request.method == "POST" and session.get("user_id"):

        shipping = float(request.form.get("shipping"))
        cart = db.execute("SELECT * FROM cart JOIN products ON products.id = cart.product_id WHERE cart.user_id = :session AND cart.product_count > 0", session=session["user_id"])
        vat = float(request.form.get("total")) * 0.15
        total = float(request.form.get("total")) + vat
        p_sum = request.form.get("p_sum")
        return render_template("check_out.html", total=usd(total), vat=vat, cart=cart, shipping=shipping, p_sum=p_sum, username=session["user"])


    else:

        return redirect("/login")


@app.route("/logout")
def logout():

    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to home page
    return redirect("/")



'''end of ((application.py))'''

'''made with love by Abdullah/clechz'''