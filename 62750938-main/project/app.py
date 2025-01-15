from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, g, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import json
# To deal with the images:
import os
from werkzeug.utils import secure_filename


from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")


# The allergens list is constant so it won't go to the database. Same with the units
ALLERGENS = [
    "Peanuts", "Tree nuts", "Milk", "Eggs", "Fish",
    "Crustacean shellfish", "Soy", "Wheat", "Sesame",
    "Gluten", "Lupin", "Molluscs", "Celery", "Mustard"
]

UNITS = ["Kg","g","L","ml","Unit(s)"]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():

    user = session.get("user_id")
    order = db.execute(
    "SELECT * FROM orders ORDER BY id DESC LIMIT 1"
    )
    processed_data = json.loads(order[0]['products'])

    recipes_list = db.execute(
        "SELECT * FROM recipes ORDER BY last_updated LIMIT 5"
    )

    return render_template("index.html", user=user, processed_data=processed_data,recipes_list=recipes_list)


@app.route("/add_ingredient", methods=["GET", "POST"])
def add_ingredient():
    if request.method == "GET":
        if request.args.get("delete") == 'true':
            db.execute(
                "DELETE FROM ingredients WHERE id = ?", request.args.get("id")
            )

            return redirect("/ingredients")
        if request.args.get("id"):
            ingredient = db.execute(
                "SELECT * FROM ingredients WHERE id=?", request.args.get("id")
            )
            page_title = "Edit " + ingredient[0]['name']
            selected_allergens = ingredient[0]['allergens']
            allergens_list = ALLERGENS
            supplier_options = db.execute(
                "SELECT id, name FROM suppliers"
            )
            type_options = db.execute(
                "SELECT id, name FROM ingredient_types"
            )
            selected_type = ingredient[0]['type']
            selected_supplier = ingredient[0]['supplier']
            ingredient = ingredient[0]
            units = UNITS
            is_edit = True

            return render_template("add_ingredient.html", page_title=page_title, selected_allergens=selected_allergens, allergens_list=allergens_list, supplier_options=supplier_options, type_options=type_options, selected_type=selected_type, selected_supplier=selected_supplier, ingredient=ingredient, units=units, is_edit=is_edit)

        else:
            page_title = "Add ingredient"
            selected_allergens = []
            allergens_list = ALLERGENS
            supplier_options = db.execute(
                "SELECT id, name FROM suppliers"
            )
            type_options = db.execute(
                "SELECT id, name FROM ingredient_types"
            )
            selected_type = []
            selected_supplier = []
            ingredient = []
            units = UNITS

            return render_template("add_ingredient.html", page_title=page_title, selected_allerges=selected_allergens, allergens_list=allergens_list, supplier_options=supplier_options, type_options=type_options, selected_type=selected_type, selected_supplier=selected_supplier, ingredient=ingredient, units=units)

@app.route("/ingredients", methods=["GET", "POST"])
def ingredients():
    if request.method == "POST":
        data = request.form
        allergens = json.dumps(data.getlist('allergens'))


        if data['is_edit'] == 'True':
            db.execute(
                "UPDATE ingredients SET name = ?, type = ?, quantity = ?, unit = ?, yield = ?, price_unit = ?, adjusted_price = ?, vat_percentage = ?, price_with_vat = ?, supplier = ?, allergens = ?, adjusted_price_with_vat = ?, obs = ? WHERE id = ?",
                data.get('name'), data.get('type'), data.get('quantity'), data.get('unit'), data.get('yield'), data.get('price_unit'), data.get('adjusted_price'), data.get('vat_percentage'), data.get('price_with_vat'), data.get('supplier'), allergens, data.get('adjusted_price_with_vat'), data.get('obs'), data.get('id')
            )
            return redirect("/ingredients")
        else:
            insert = db.execute(
                "INSERT INTO ingredients (name, type, quantity, unit, yield, price_unit, adjusted_price, vat_percentage, price_with_vat, supplier, allergens, adjusted_price_with_vat, obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                data.get('name'), data.get('type'), data.get('quantity'), data.get('unit'), data.get('yield'), data.get('price_unit'), data.get('adjusted_price'), data.get('vat_percentage'),
                data.get('price_with_vat'), data.get('supplier'), allergens, data.get('adjusted_price_with_vat'), data.get('obs')
            )
            return redirect("/ingredients")

    else:
        user = session.get("user_id")


        ingredients_list = db.execute (
            "SELECT i.*, t.name AS type_name, s.name AS supplier_name FROM ingredients AS i JOIN ingredient_types AS t ON i.type = t.id JOIN suppliers AS s ON i.supplier = s.id"
        )
        #We use this instruction to transform the string into a list so it can be formated by jinja in the templates.
        for ingredient in ingredients_list:
            ingredient['allergens'] = json.loads(ingredient['allergens'])

        return render_template("ingredients.html", ingredients_list=ingredients_list)

@app.route("/add_recipe", methods=["GET"])
def add_recipe():


    if request.method == "GET":
        if request.args.get("delete") == 'true':
            db.execute(
                "DELETE FROM recipes WHERE id = ?", request.args.get("id")
            )

            return redirect("/recipes")


        if request.args.get("id"):
            id = request.args.get("id")

            recipe = db.execute(
                "SELECT * FROM recipes WHERE id = ?", id
            )[0]
            page_title = "Edit recipe"
            is_edit = "true"

            #Pass the ingredients and subrecipe list to fill the select on the add ingredient
            ingredients_options= db.execute(
                "SELECT id, name FROM ingredients"
            )

            ingredients_list = db.execute(
                "SELECT ri.*, i.name AS name FROM recipe_ingredients as ri JOIN ingredients AS i ON ri.ingredient_id = i.id WHERE recipe_id = ?", id
            )



            return render_template("add_recipe.html", page_title=page_title, recipe=recipe, is_edit=is_edit, ingredients_list=ingredients_list,ingredients_options=ingredients_options)

        else:
            page_title = "Add recipe"
            recipe = []
            is_edit = "false"

            #Pass the ingredients and subrecipe list to fill the select on the add ingredient
            ingredients_options= db.execute(
                "SELECT id, name FROM ingredients"
            )

            return render_template("add_recipe.html", page_title=page_title, recipe=recipe, ingredients_options=ingredients_options)

    return render_template("apology.html")


@app.route("/recipes", methods=["GET", "POST"])
def recipes():

    if request.method == "POST":
        data = request.form
        print(data)
        user = session.get("user_id")

        if 'photo' in request.files:  # Check if a photo was uploaded
            photo = request.files['photo']
            if photo.mimetype in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
                os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
                filename = secure_filename(photo.filename)
                photo.save(os.path.join(upload_dir, filename))
            else:
                return render_template("apology.html")
            # Update the photo field with the relative path to the file
            photoURL = os.path.join('static', 'images', filename)
        else:
            photoURL = ''


        if data['is_edit'] == 'true':
            db.execute(
                "UPDATE recipes SET name = ?, yield = ?, method = ?, photo = ?, price_portion = ?, price_total = ?, description = ?, created_by = ?, last_updated = CURRENT_TIMESTAMP, is_subrecipe = ? WHERE id = ?",
                data.get('name'), data.get('yield'), data.get('method'), photoURL, data.get('price_portion'), data.get('price_total'), data.get('description'), user, data.get('is_subrecipe'), data.get('id')
            )
            return redirect("/recipes")
        else:
            insert = db.execute(
                "INSERT INTO recipes (name, yield, method, photo, price_portion, price_total, description, created_by, is_subrecipe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                data.get('name'), data.get('yield'), data.get('method'), photoURL, data.get('price_portion'), data.get('price_total'), data.get('description'), user, data.get('is_subrecipe')
            )
            return redirect("/recipes")

    else:
        user = session.get("user_id")


        recipes_list = db.execute (
            "SELECT * FROM recipes"
        )

        return render_template("recipes.html", recipes_list=recipes_list)

@app.route("/single_recipe", methods=["GET", "POST"])
def single_recipe():

    if request.method == "GET":
        id = request.args.get("id")
        recipe = db.execute(
            "SELECT * FROM recipes WHERE id = ?", id
        )
        recipe = recipe[0]
        page_title = recipe['name']

        recipe_ingredients = db.execute(
            "SELECT recipe_ingredients.*, ingredients.name, ingredients.unit, ingredients.price_unit, ingredients.price_unit * recipe_ingredients.quantity AS total_price FROM recipe_ingredients JOIN ingredients ON recipe_ingredients.ingredient_id = ingredients.id WHERE recipe_ingredients.recipe_id = ?", recipe['id']
        )

        return render_template("view_single_recipe.html", recipe=recipe,page_title=page_title,recipe_ingredients=recipe_ingredients)
    return redirect("/recipes")

@app.route("/recipe_ingredient", methods=["GET","POST"])
def recipe_ingredient():
    if request.method == "POST":
        data = request.form
        print(data)
        if data.get("is_edit") == '1':
            update= db.execute(
                "UPDATE recipe_ingredients SET ingredient_id = ?, quantity = ?, obs = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?", data.get("ingredient_id"), data.get("ingredient_quantity"), data.get("ingredient_observations"), data.get("recipe_ingredient_id")
            )
            return redirect("/add_recipe?id=" + data.get("recipe_id"))
        else:
            insert = db.execute(
                "INSERT INTO recipe_ingredients (recipe_id, ingredient_id, quantity, obs) VALUES (?, ?, ?, ?)", request.form["recipe_id"], request.form["ingredient_id"], request.form["ingredient_quantity"], request.form["ingredient_observations"]
            )
        return redirect("/add_recipe?id=" + request.form["recipe_id"])

    if request.method == "GET":
        if request.args.get("delete") == 'true':
            db.execute(
                "DELETE FROM recipe_ingredients WHERE id = ?", request.args.get("ingredient_id")
            )

            return redirect("/add_recipe?id=" + request.args.get("recipe_id"))
    #handle the form to add an ingredient to the recipe
    return redirect("/add_recipe")



@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():

    if request.method == "GET":
        suppliers_list = db.execute(
            "SELECT * FROM suppliers"
        )
        return render_template("suppliers.html", suppliers_list=suppliers_list)

    if request.method == "POST":
        data = request.form
        if data.get("is_edit"):
            update = db.execute(
                "UPDATE suppliers SET name = ?, contact_person = ?, phone = ?, email = ?, obs= ? WHERE id = ?", data.get("name"), data.get("contact_person"), data.get("phone"), data.get("email"), data.get("obs"), data.get("id")
            )
            return redirect("/suppliers")
        else:
            insert = db.execute(
                "INSERT INTO suppliers (name, contact_person, phone, email, obs) VALUES (?, ?, ?, ?, ?)", data.get("name"), data.get("contact_person"), data.get("phone"), data.get("email"), data.get("obs")
            )
            return redirect("/suppliers")

    return render_template("apology.html")

@app.route("/add_supplier", methods=["GET", "POST"])
def add_supplier():
    if request.method == "POST":
        return 0

    if request.method == "GET":
        if request.args.get("delete") == 'true':
            db.execute(
                "DELETE FROM suppliers WHERE id = ?", request.args.get("id")
            )
            return redirect("/suppliers")

        elif request.args.get("id"):
            supplier = db.execute(
                "SELECT * FROM suppliers WHERE id = ?", request.args.get("id")
            )
            supplier = supplier[0]
            page_title = "Edit supplier"
            is_edit = 1
            return render_template("add_supplier.html", page_title=page_title, supplier=supplier, is_edit=is_edit)
        else:
            page_title = "Add supplier"
            supplier = []
            return render_template("add_supplier.html", page_title=page_title, supplier=supplier)


@app.route("/ingredient_types", methods=["GET", "POST"])
def ingredient_types():

    if request.method == "GET":
        ingredient_types_list = db.execute(
            "SELECT * FROM ingredient_types"
        )
        return render_template("ingredient_types.html", ingredient_types_list=ingredient_types_list)

    if request.method == "POST":
        data = request.form
        if data.get("is_edit"):
            update = db.execute(
                "UPDATE ingredient_types SET name = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?", data.get("name"), data.get("id")
            )
            return redirect("/ingredient_types")
        else:
            insert = db.execute(
                "INSERT INTO ingredient_types (name) VALUES (?)", data.get("name")
            )
            return redirect("/ingredient_types")

    return render_template("apology.html")


@app.route("/add_ingredient_types", methods=["GET", "POST"])
def add_ingredient_types():
    if request.method == "POST":
        return 0

    if request.method == "GET":
        if request.args.get("delete") == 'true':
            db.execute(
                "DELETE FROM ingredient_type WHERE id = ?", request.args.get("id")
            )
            return redirect("/ingredient_types")

        elif request.args.get("id"):
            ingredient_type = db.execute(
                "SELECT * FROM ingredient_types WHERE id = ?", request.args.get("id")
            )
            ingredient_type = ingredient_type[0]
            page_title = "Edit ingredient type"
            is_edit = 1
            return render_template("add_ingredient_types.html", page_title=page_title, ingredient_type=ingredient_type, is_edit=is_edit)
        else:
            page_title = "Add ingredient type"
            ingredient_type = []
            return render_template("add_ingredient_types.html", page_title=page_title, ingredient_type=ingredient_type)


@app.route("/orders", methods=["GET", "POST"])
def orders():

    if request.method == "POST":
        data = request.form
        # Example of data: {"order_1": "true", "order_2": "true", "order_3": "true", "quantity_1": "6", "quantity_2": "6", "quantity_3": "20"}
        # At this point, it's the id of the ingredient that will serve as the unifier

        # This part converts the data from the form into pairs of ingredient id as key and quantity as value
        processed_data = {}
        for key, value in data.items():
            if (key.startswith("order_")):
                if (value == "true"):
                    key_suffix = key[len("order_"):]
                    if key_suffix not in processed_data:
                        processed_data[key_suffix] = {}
                    processed_data[key_suffix]['quantity'] = data['quantity_' + key[len("order_"):]]



        # Get the result back to get the order

        # Flesh out the information from the ingredient to show the user
        ingredient_info = db.execute(
            "SELECT i.*, t.name AS type_name, s.name AS supplier_name FROM ingredients AS i JOIN ingredient_types AS t ON i.type = t.id JOIN suppliers AS s ON i.supplier = s.id"
        )
        user = session.get("user_id")
        user_name = db.execute(
            "SELECT name FROM users WHERE id = ?", user
        )


        for key,value in processed_data.items():
            for ingredient in ingredient_info:
                if (int(key) == ingredient['id']):
                    processed_data[key]['name'] = ingredient['name']
                    processed_data[key]['supplier'] = ingredient['supplier_name']
                    processed_data[key]['cost'] = (ingredient['price_unit'] / ingredient['quantity']) * float(processed_data[key]['quantity'])

        total_cost = sum(item['cost'] for item in processed_data.values())

        # Insert the order in the DB to keep history
        order = db.execute(
            "INSERT INTO orders (products, placed_by, estimated_price) VALUES (?,?,?)", json.dumps(processed_data),user,total_cost
        )



        return render_template("order_confirmed.html",processed_data=processed_data, order = order, user_name= user_name, total_cost=total_cost)

    if request.method == "GET":
        if request.args.get("id"):
            order = db.execute(
                "SELECT * FROM orders WHERE id = ?", request.args.get("id")
            )
            processed_data = json.loads(order[0]['products'])

            user_name = db.execute(
                "SELECT name FROM users WHERE id = ?", order[0]['placed_by']
            )
            total_cost = order[0]['estimated_price']
            order_id = request.args.get("id")
            return render_template("order_confirmed.html",processed_data=processed_data, order_id=order_id, user_name= user_name, total_cost=total_cost)


        orders = db.execute(
            "SELECT * FROM orders;"
        )
        users = db.execute(
            "SELECT id, name FROM users"
        )
        user_dict = {}
        for user in users:
            user_dict[user['id']] = user['name']

        for order in orders:
            order['products'] = json.loads(order['products'])
            order['placed_by'] = order['placed_by'] = user_dict[order['placed_by']]
            suppliers = set()
            for product in order['products'].values():
                suppliers.add(product['supplier'])
            order['suppliers'] = ", ".join(suppliers)




        return render_template("order_list.html",orders=orders)



    return render_template("apology.html")

@app.route("/order_ingredients", methods=["GET", "POST"])
def order_ingredients():

    if request.method == "POST":
        data = request.form
        if data.get("referer") == "ingredient":
            ingredients_list = db.execute (
                "SELECT i.*, t.name AS type_name, s.name AS supplier_name FROM ingredients AS i JOIN ingredient_types AS t ON i.type = t.id JOIN suppliers AS s ON i.supplier = s.id"
            )
            #We use this instruction to transform the string into a list so it can be formated by jinja in the templates.
            for ingredient in ingredients_list:
                ingredient['allergens'] = json.loads(ingredient['allergens'])


            selected_ingredients = {}
            ingredient_ids = request.form.getlist('ingredients')
            for ingredient_id in ingredient_ids:
                quantity = 0
                selected_ingredients[ingredient_id] = {'quantity': quantity}


            user_id = session.get("user_id")
            supplier_list = db.execute(
                "SELECT * FROM suppliers"
            )

            return render_template("order.html", data=data,ingredients_list=ingredients_list,selected_ingredients=selected_ingredients, user_id=user_id, supplier_list=supplier_list)


        if data.get("referer") == "recipe":
            ingredients_list = db.execute (
                "SELECT i.*, t.name AS type_name, s.name AS supplier_name FROM ingredients AS i JOIN ingredient_types AS t ON i.type = t.id JOIN suppliers AS s ON i.supplier = s.id"
            )
            #We use this instruction to transform the string into a list so it can be formated by jinja in the templates.
            for ingredient in ingredients_list:
                ingredient['allergens'] = json.loads(ingredient['allergens'])

            user_id = session.get("user_id")
            supplier_list = db.execute(
                "SELECT * FROM suppliers"
            )

            # Get the selected recipes from the checkboxes that are selected, making it a list with recipe id as key and quantity as value
            selected_recipes = {}
            for key in data:
                if key.startswith("checkbox_"):
                    selected_recipes[key.split("_")[1]] = data['quantity_' + key.split("_")[1]]



            selected_ingredients={}
            # Construct the selected_ingredients variable by iterating through the recipes and adding the ingredients and quantity
            for recipe,quantity in selected_recipes.items():
                recipe_ingredients = db.execute(
                    "SELECT * FROM recipe_ingredients WHERE recipe_id = ?", recipe
                )
                print(recipe_ingredients)
                # Now with the ingredients we need to get the quantity
                for ingredient in recipe_ingredients:
                    ingredient_id = str(ingredient['ingredient_id'])
                    ingredient_quantity = float(ingredient['quantity'])
                    recipe_quantity = int(quantity)
                    if ingredient_id not in selected_ingredients:
                        selected_ingredients[ingredient_id] = {'quantity': 0}
                    selected_ingredients[ingredient_id]['quantity'] += ingredient_quantity * recipe_quantity



            return render_template("order.html", data=data,ingredients_list=ingredients_list,selected_ingredients=selected_ingredients, user_id=user_id, supplier_list=supplier_list, selected_recipes=selected_recipes)

    return render_template("apology.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template("apology.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    # If POST was sent
    if request.method == "POST":

        if len(request.form.get("username")) < 1 or len(request.form.get("password")) < 4 or request.form.get("password") != request.form.get("confirmation"):
            return render_template("apology.html")

        user = request.form.get("username")
        pass_hash = generate_password_hash(request.form.get("password"))

        try:
            # Query database for username
            rows = db.execute("INSERT INTO users (name, hash) VALUES (?, ?)", user, pass_hash)

            # Redirect to the login page
            return redirect("/")

        except Exception as e:
            return render_template("apology.html")
    else:
        return render_template("register.html")
