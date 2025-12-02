# Adapted from CS50 Finance problem set

import os

from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session
from openai import OpenAI
from serpapi.google_search import GoogleSearch
from werkzeug.security import check_password_hash, generate_password_hash
# TODO: delete?
from helpers import apology, login_required

# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///closet.db")

# Save API key as environment variable
SERP_API_KEY = os.getenv("SERP_API_KEY")
OPEN_API_KEY = os.getenv("OPEN_API_KEY")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show home page"""
    # Will run if user makes a search
    if request.method == "POST":
        # Get search query from form
        user_query = request.form.get("query")
        # Ensure user inputted a search query
        if not user_query:
            return apology("must provide search query")

       
        refined_query = user_query

        # Use SerpAPI to search Google for clothing items matching refined query
        params = {
            # Scrape Google Shopping for results
            "engine": "google_shopping",
            "q": refined_query,
            "api_key": SERP_API_KEY
        }

        # Make AI client request and get results
        try:
            search = GoogleSearch(params)
            # Limit to first 21 results
            # TODO: implement pagination and don't hard code 21
            results = search.get_dict().get("shopping_results", [])
            num_results = len(results)
            if (num_results < 21):
                results = results[:num_results]
            else: 
                results = results[:21]
        # Handle any errors that may arise
        except Exception as e:
            apology("error fetching results")

        return render_template("index.html", name=db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])[0]["name"], query=refined_query, results=results)


    # Will run is user navigates to home page
    else:
        return render_template("index.html", name=db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])[0]["name"], results=None)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Will execute when user submits the registration form
    if request.method == "POST":
        # Only save name and username for security purposes
        name = request.form.get("name")
        username = request.form.get("username")

        # Check that user inputted a username and password
        if not name: 
            return apology("must provide name")
        if not username:
            return apology("must provide username")
        if not request.form.get("password"):
            return apology("must provide password")

        # Check that password and confirmation are the same
        if request.form.get("confirmation") != request.form.get("password"):
            return apology("passwords must match")

        # Try to insert new user into database and remember that user
        try:
            session["user_id"] = db.execute(
                "INSERT INTO users (name, username, hash) VALUES (?, ?, ?)", name, username, generate_password_hash(request.form.get("password")))
        # Apologize if username already in use
        except ValueError:
            return apology("username already in use")

        # Redirect to personal information form
        return redirect("/preferences")

    # Will execute when user navigates into the register page
    else:
        return render_template("register.html")

@app.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    """Get user's sizing / preference information"""
    # Will execute if user submits preference form
    if request.method == "POST":
        # Get info from sizing form
        info = { 
            "gender" : request.form.get("gender"),
            "height_feet" : request.form.get("height-feet"),
            "height_in" : request.form.get("height-inches"),
            "weight" : request.form.get("weight"),
            "top_size" : request.form.get("top-size"),
            "bottom_size" : request.form.get("bottom-size"),
            "dress_size" : request.form.get("dress-size"),
            "shoe_size" : request.form.get("shoe-size"),
            "shoe_gender" : request.form.get("shoe-gender")
        }

        # Santize input - Any field left blank will be stored as None/NULL in preferences database

        if info["gender"]:
            # Check that gender is "male" or "female"
            if info["gender"] != "male" and info["gender"] != "female":
                return apology("invalid gender")   
        if info["height_feet"]:
            # Check that height_feet is a positive integer
            try:
                info["height_feet"] = int(info["height_feet"])
                if info["height_feet"] < 0:
                    return apology("invalid feet")
            except ValueError:
                return apology("invalid feet")
            # Default to 0 inches if user only inputs feet TODO: not working
            if not info["height_in"]:
                info["height_in"] = 0
            else: 
                # Check that inputted height_in is an integer between 0 and 11
                try:
                    info["height_in"] = int(info["height_in"])
                    if info["height_in"] < 0 or info["height_in"] > 11:
                        return apology("invalid inches")
                except ValueError:
                    return apology("invalid inches")
        elif info["height_in"]:
            # If user only inputs inches, assume 0 feet
            info["height_feet"] = 0
            # Check that inputted height_in is an integer between 0 and 11
            try: 
                info["height_in"] = int(info["height_in"])
                if info["height_in"] < 0 or info["height_in"] > 11:
                    return apology("invalid inches")
            except ValueError:
                return apology("invalid inches")
        if info["weight"]:
            # Check that weight is a positive integer
            try:
                info["weight"] = int(info["weight"])
                if info["weight"] < 1:
                    return apology("invalid weight")
            except ValueError:
                return apology("invalid weight")
            
        # All valid sizes
        sizes = ["xxs", "xs", "s", "m", "l", "xl", "xxl"]
        if info["top_size"]:
            # Check that top_size is a valid size
            if info["top_size"] not in sizes:
                return apology("invalid top size")
        if info["bottom_size"]:
            # Check that bottom_size is a valid size
            if info["bottom_size"] not in sizes:
                return apology("invalid bottom size")
        if info["dress_size"]:
            # Check that dress_size is a valid size
            if info["dress_size"] not in sizes:
                return apology("invalid dress size")
        if info["shoe_size"]:
            # Check that shoe_size is a positive multiple of 0.5 & only goes one decimal place
            try:
                info["shoe_size"] = float(info["shoe_size"])
                if info["shoe_size"] < 1 or (info["shoe_size"] * 2) % 1 != 0 or round(info["shoe_size"], 1) != info["shoe_size"]:
                    return apology("invalid shoe size")
            except ValueError:
                return apology("invalid shoe size")
            # Check that user also inputted shoe gender
            if not info["shoe_gender"]:
                return apology("missing shoe gender")
            # Check that shoe gender is valid
            if info["shoe_gender"] != "mens" and info["shoe_gender"] != "womens":
                return apology("invalid shoe gender")
        elif info["shoe_gender"]:
            # If user only inputs shoe gender, require that they also input shoe size
            return apology("missing shoe size")

        # Create preferences table entry for this user if it doesn't already exist
        try:
            db.execute("INSERT INTO preferences (user_id) VALUES (?)", session["user_id"])
        # Continue if entry already exists
        except ValueError:
            pass

        # Update preferences database with existing info
        for key in info:
            # Need to account for the fact that some fields (e.g. height_in) may be 0 (registered as false by default)
            if info[key] or info[key] == 0:
                db.execute("UPDATE preferences SET ? = ? WHERE user_id = ?", key, info[key], session["user_id"])

        return redirect("/")
    
    # Will execute if user navigates to preference form
    else: 
        return render_template("preferences.html")
    
@app.route("/history")
@login_required
def history():
    name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])[0]["name"]
    entry = db.execute("SELECT * FROM preferences WHERE user_id = ?", session["user_id"])[0]
    return render_template("history.html", name=name, entry=entry)
