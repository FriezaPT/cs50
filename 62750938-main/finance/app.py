import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""
    user = session.get("user_id")
    user_row = db.execute(
        "SELECT * FROM users WHERE id = ?", user
    )
    cash = float(user_row[0]["cash"])

    user_portfolio = db.execute(
        "SELECT * FROM portfolios WHERE user_id = ?", user
    )
    treated_info = {}
    portfolio_value = 0
    for current in user_portfolio:
        try:
            data = lookup(current["symbol"])

        except Exception as e:
            return apology(f"Invalid Symbol: {current["symbol"]}")

        treated_info[current["symbol"]] = {}
        treated_info[current["symbol"]]["name"] = data["name"]
        treated_info[current["symbol"]]["quantity"] = current["quantity"]
        treated_info[current["symbol"]]["unit_price"] = data["price"]
        treated_info[current["symbol"]]["total_value"] = usd(
            int(current["quantity"]) * float(data["price"]))
        portfolio_value = portfolio_value + (int(current["quantity"]) * float(data["price"]))

    total_value = usd(cash + portfolio_value)
    cash = usd(cash)

    return render_template("index.html", cash=cash, treated_info=treated_info, total_value=total_value)
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():

    if request.method == "POST":
        try:
            data = lookup(request.form.get("symbol"))
            if "error" in data:
                return apology(data["error"])

        except Exception as e:
            return apology(str(e))

        try:
            value = int(request.form.get("shares"))
            if value < 1:
                return apology("Invalid number")
        except ValueError:
            return apology("Invalid number")

        user = session.get("user_id")
        symbol = request.form.get("symbol")
        quantity = int(request.form.get("shares"))
        unit_price = float(data["price"])
        total_price = unit_price * quantity

        user_row = db.execute(
            "SELECT cash FROM users WHERE id = ?", user
        )

        cash_before = int(user_row[0]["cash"])
        cash_after = cash_before - total_price
        if cash_after < 1:
            return apology("Insufficient funds.")

        print(symbol, user, quantity, unit_price, total_price, cash_after)

        symbol = str(symbol)
        user = int(user)
        quantity = int(quantity)
        unit_price = float(unit_price)
        total_price = float(total_price)
        cash_after = float(cash_after)

        rows = db.execute(
            "INSERT INTO transactions (symbol, user_id, quantity, unit_price, total_price, cash_after, type) VALUES (?, ?, ?, ?, ?, ?, 'buy')",
            symbol, user, quantity, unit_price, total_price, cash_after
        )

        portfolio = db.execute(
            "SELECT * FROM portfolios WHERE user_id = ? AND symbol = ?", user, symbol
        )

        if len(portfolio) == 1:
            update_portfolio = db.execute(
                "UPDATE portfolios SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ? AND symbol = ?", int(
                    portfolio[0]["quantity"]) + quantity, user, symbol
            )
        else:
            create_portfolio = db.execute(
                "INSERT INTO portfolios (user_id, symbol, quantity) VALUES (?,?,?)", user, symbol, quantity
            )

        update_user = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash_after, user
        )

        return redirect("/")

    else:
        return render_template("buy.html")

    """Buy shares of stock"""
    return apology("TODO")


@app.route("/history")
@login_required
def history():

    user = session.get("user_id")

    user_transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id = ?", user
    )

    return render_template("history.html", user_transactions=user_transactions)
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    if request.method == "POST":
        try:
            data = lookup(request.form.get("symbol"))
            data["price"] = usd(data["price"])
            return render_template("quoted.html", data=data)
        except Exception as e:
            return apology("Invalid Symbol")

    else:
        return render_template("quote.html")

    """Get stock quote."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    # If POST was sent
    if request.method == "POST":

        if len(request.form.get("username")) < 1 or len(request.form.get("password")) < 4 or request.form.get("password") != request.form.get("confirmation"):
            return apology("Invalid username or password")

        user = request.form.get("username")
        pass_hash = generate_password_hash(request.form.get("password"))

        try:
            # Query database for username
            rows = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", user, pass_hash)

            # Redirect to the login page
            return redirect("/")

        except Exception as e:
            return apology(str(e))
    else:
        return render_template("register.html")

    """Register user"""
    return apology("TODO")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        user = session.get("user_id")
        try:
            data = lookup(request.form.get("symbol"))
        except Exception as e:
            return apology("Invalid Symbol")

        number = int(request.form.get("shares"))
        owned = db.execute(
            "SELECT quantity FROM portfolios WHERE user_id = ? AND symbol = ?", user, request.form.get(
                "symbol")
        )

        if number < 1:
            return apology("Please enter a valid number to sell")
        elif number > int(owned[0]['quantity']):
            return apology("You don't have that many stocks to sell (You own " + str(owned[0]['quantity']) + ") and want to sell " + str(number))

        # All tests passed, lets update the BDs
        total_price = float(data["price"]) * number

        user_data = db.execute(
            "SELECT cash FROM users WHERE id = ?", user
        )

        cash_after = float(user_data[0]["cash"]) + total_price

        # Transaction update
        transaction = db.execute(
            "INSERT INTO transactions (symbol, user_id, quantity, unit_price, total_price, cash_after, type) VALUES (?, ?, ?, ?, ?, ?, 'sell')",
            request.form.get("symbol"), user, number, float(data["price"]), total_price, cash_after
        )

        # Portfolio update
        final_quantity = int(owned[0]['quantity']) - number

        if final_quantity == 0:
            update_portfolio = db.execute(
                "DELETE FROM portfolios WHERE user_id = ? AND symbol = ?", user, request.form.get(
                    "symbol")
            )
        else:
            update_portfolio = db.execute(
                "UPDATE portfolios SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE user_id = ? AND symbol = ?", final_quantity, user, request.form.get(
                    "symbol")
            )

        # User update

        user_update = db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", cash_after, user
        )

        return redirect("/")

    else:
        user = session.get("user_id")
        list = db.execute(
            "SELECT symbol FROM portfolios WHERE user_id = ?", user
        )

        return render_template("sell.html", list=list)

    """Sell shares of stock"""
    return apology("TODO")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    if request.method == "POST":
        if not request.form.get("current"):
            return apology("No Current Password")
        elif not request.form.get("password"):
            return apology("No New Password")
        elif not request.form.get("confirmation"):
            return apology("No confirmation password")

        # if all the fields are filled, treat the data

        user = session.get("user_id")

        user_data = db.execute(
            "SELECT * FROM users WHERE id = ?", user
        )

        if not check_password_hash(
            user_data[0]["hash"], request.form.get("current")
        ):
            return apology("Invalid password", 403)

        # If the current password passes the test, we can check if the new password and confirmation are the same, and if they are, update the DB and log the user out

        if request.form.get("password") == request.form.get("confirmation"):
            update_password = db.execute(
                "UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(
                    request.form.get("password")), user
            )
        else:
            return apology("New password and confirmation do not match")

        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")
    else:
        return render_template("change.html")
