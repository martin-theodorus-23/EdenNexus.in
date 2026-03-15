import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import database

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "edennexus-secret-key-123")

@app.route("/")
def index():
    if "user" not in session:
        flash("Please log in to access the system.", "warning")
        return redirect(url_for("login"))
    return render_template("index.html")

@app.route("/users")
def users():
    if "user" not in session:
        return redirect(url_for("login"))
    all_users = database.get_all_users()
    return render_template("users.html", users=all_users)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()

        if not username or not email:
            flash("Please provide both a username and an email.", "warning")
        elif database.user_exists(username, email):
            # Update their last active timestamp
            database.update_last_active(username)
            session["user"] = username
            flash(f"Access granted. Welcome back, {username}.", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials or unregistered node.", "danger")
            
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        otp = request.form.get("otp", "").strip()
        
        if not username or not email or not otp:
            flash("All fields are required.", "warning")
        elif otp != "123456":
            flash("Invalid Security Code.", "danger")
        elif database.user_exists(username, email):
            flash("Agent already exists. Please log in.", "warning")
            return redirect(url_for("login"))
        else:
            # Register user as verified and default lvl_1
            database.add_user(username, email, verified=True, level="lvl_1")
            session["user"] = username
            flash("Node established successfully.", "success")
            return redirect(url_for("index"))
            
    return render_template("signup.html")

@app.route("/plans")
def plans():
    """Displays the available subscription tiers."""
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("plans.html")

@app.route("/checkout/<tier>", methods=["GET", "POST"])
def checkout(tier):
    """Simulates a payment gateway and upgrades the user."""
    if "user" not in session:
        return redirect(url_for("login"))

    # Map the URL parameter to the correct database level
    tier_map = {
        "standard": "lvl_1",
        "pro": "lvl_2",
        "nexus": "lvl_3"
    }

    if tier not in tier_map:
        flash("Invalid plan selected.", "danger")
        return redirect(url_for("plans"))

    if request.method == "POST":
        # In a real app, Stripe/Razorpay logic goes here.
        # For the demo, we just assume payment is successful.
        new_level = tier_map[tier]
        database.update_user_level(session["user"], new_level)
        
        flash(f"Payment successful! System access upgraded to {new_level.upper()}.", "success")
        return redirect(url_for("index"))

    return render_template("checkout.html", tier=tier.title())

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Connection terminated.", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)