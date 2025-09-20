from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, os, datetime, random, string

app = Flask(__name__)
app.secret_key = "dev_" + "".join(random.choice(string.ascii_letters) for _ in range(24))

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def read_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_products():
    return read_json(PRODUCTS_FILE)

def save_products(products):
    write_json(PRODUCTS_FILE, products)

def get_users():
    return read_json(USERS_FILE)

def save_users(users):
    write_json(USERS_FILE, users)

def get_orders():
    return read_json(ORDERS_FILE)

def save_orders(orders):
    write_json(ORDERS_FILE, orders)

def current_user():
    return session.get("user")

def get_cart_count():
    cart = session.get("cart", {})
    return sum(cart.values())

# ----- Public routes -----
@app.route("/")
def index():
    products = get_products()
    cart_count = get_cart_count()
    # Sort products by price ascending for new arrivals
    new_arrivals = sorted(products, key=lambda p: p.get("price", 0))
    return render_template("index.html", products=products, new_arrivals=new_arrivals, cart_count=cart_count)

@app.route("/product/<int:pid>")
def product(pid):
    products = get_products()
    prod = next((p for p in products if p["id"] == pid), None)
    cart_count = get_cart_count()
    if not prod:
        return "Product not found", 404
    return render_template("product.html", product=prod, cart_count=cart_count)

@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.get_json() or {}
    pid = int(data.get("product_id"))
    qty = int(data.get("qty", 1))
    products = get_products()
    prod = next((p for p in products if p["id"] == pid), None)
    if not prod:
        return jsonify({"ok": False, "message": "Product not found"}), 404
    cart = session.get("cart", {})
    cart[str(pid)] = cart.get(str(pid), 0) + qty
    session["cart"] = cart
    cart_count = get_cart_count()
    return jsonify({"ok": True, "message": f"Added {prod['name']} to cart", "cart_count": cart_count})

@app.route("/cart")
def cart():
    products = get_products()
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = next((x for x in products if x["id"] == int(pid)), None)
        if p:
            items.append({"id": p["id"], "name": p["name"], "price": p["price"], "qty": qty})
            total += p["price"] * qty
    cart_count = get_cart_count()
    return render_template("cart.html", items=items, total=total, cart_count=cart_count)

@app.route("/cart/update", methods=["POST"])
def cart_update():
    data = request.get_json() or {}
    pid = str(data.get("product_id"))
    qty = int(data.get("qty", 1))
    cart = session.get("cart", {})
    if pid in cart:
        cart[pid] = qty
    session["cart"] = cart
    products = get_products()
    items, total = [], 0
    for pid_, qty_ in cart.items():
        p = next((x for x in products if x["id"] == int(pid_)), None)
        if p:
            items.append({"id": p["id"], "name": p["name"], "price": p["price"], "qty": qty_})
            total += p["price"] * qty_
    cart_count = get_cart_count()
    return jsonify({"ok": True, "items": items, "total": total, "cart_count": cart_count})

@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    data = request.get_json() or {}
    pid = str(data.get("product_id"))
    cart = session.get("cart", {})
    if pid in cart:
        cart.pop(pid, None)
    session["cart"] = cart
    products = get_products()
    items, total = [], 0
    for pid_, qty_ in cart.items():
        p = next((x for x in products if x["id"] == int(pid_)), None)
        if p:
            items.append({"id": p["id"], "name": p["name"], "price": p["price"], "qty": qty_})
            total += p["price"] * qty_
    cart_count = get_cart_count()
    return jsonify({"ok": True, "items": items, "total": total, "cart_count": cart_count})

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    products = get_products()
    cart = session.get("cart", {})
    items = []
    total = 0
    for pid, qty in cart.items():
        p = next((x for x in products if x["id"] == int(pid)), None)
        if p:
            items.append({"id": p["id"], "name": p["name"], "price": p["price"], "qty": qty})
            total += p["price"] * qty
    if request.method == "POST":
        if not items:
            return redirect(url_for("cart"))
        user = current_user()
        if not user:
            return redirect(url_for("login"))
        orders = get_orders()
        new_id = (max([o["id"] for o in orders]) + 1) if orders else 1
        order = {
            "id": new_id,
            "user_id": user["id"],
            "user_email": user["email"],
            "items": items,
            "total": total,
            "status": "Processing",
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "shipping": {
                "name": request.form.get("name"),
                "phone": request.form.get("phone"),
                "address": request.form.get("address"),
                "payment": request.form.get("payment"),
            }
        }
        orders.append(order)
        save_orders(orders)
        session["cart"] = {}
        return redirect(url_for("order_success", order_id=new_id))
    cart_count = get_cart_count()
    return render_template("checkout.html", items=items, total=total, cart_count=cart_count)

@app.route("/order-success/<int:order_id>")
def order_success(order_id):
    cart_count = get_cart_count()
    return render_template("order_success.html", order_id=order_id, cart_count=cart_count)

# ----- Auth (user) -----
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        users = get_users()
        user = next((u for u in users if u["email"].lower() == email and u["password"] == password and u.get("role","user") in ["user","admin"]), None)
        if user:
            session["user"] = {"id": user["id"], "email": user["email"], "role": user.get("role","user"), "name": user.get("name","User")}
            return redirect(url_for("index"))
        cart_count = get_cart_count()
        return render_template("login.html", error="Invalid credentials", cart_count=cart_count)
    cart_count = get_cart_count()
    return render_template("login.html", error=None, cart_count=cart_count)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        users = get_users()
        if any(u["email"].lower() == email for u in users):
            cart_count = get_cart_count()
            return render_template("signup.html", error="Email already exists.", cart_count=cart_count)
        new_id = (max([u["id"] for u in users]) + 1) if users else 1
        user = {"id": new_id, "name": name, "email": email, "password": password, "role": "user"}
        users.append(user)
        save_users(users)
        session["user"] = {"id": user["id"], "email": user["email"], "role": "user", "name": user["name"]}
        return redirect(url_for("index"))
    cart_count = get_cart_count()
    return render_template("signup.html", error=None, cart_count=cart_count)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/my-orders")
def my_orders():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    orders = [o for o in get_orders() if o["user_id"] == user["id"]]
    orders = sorted(orders, key=lambda x: x["id"], reverse=True)
    cart_count = get_cart_count()
    return render_template("my_orders.html", orders=orders, cart_count=cart_count)

# ----- Admin -----
def require_admin():
    user = current_user()
    return (user and user.get("role") == "admin")

@app.route("/admin")
def admin_home():
    if not require_admin():
        return redirect(url_for("admin_login"))
    cart_count = get_cart_count()
    return render_template("admin_dashboard.html", cart_count=cart_count)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        users = get_users()
        user = next((u for u in users if u["email"].lower() == email and u["password"] == password and u.get("role") == "admin"), None)
        if user:
            session["user"] = {"id": user["id"], "email": user["email"], "role": "admin", "name": user.get("name","Admin")}
            return redirect(url_for("admin_home"))
        cart_count = get_cart_count()
        return render_template("admin_login.html", error="Invalid admin credentials", cart_count=cart_count)
    cart_count = get_cart_count()
    return render_template("admin_login.html", error=None, cart_count=cart_count)

@app.route("/admin/logout")
def admin_logout():
    if current_user():
        session.pop("user", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/products", methods=["GET", "POST"])
def admin_products():
    if not require_admin():
        return redirect(url_for("admin_login"))
    products = get_products()
    form = {}
    message = None
    edit_id = request.args.get("edit")
    if edit_id:
        try:
            pid = int(edit_id)
            p = next((x for x in products if x["id"] == pid), None)
            if p:
                form = p
        except:
            pass
    if request.method == "POST":
        data = request.form
        pid = data.get("id")
        if not pid:
            new_id = (max([p["id"] for p in products]) + 1) if products else 1
        else:
            new_id = int(pid)
        product = {
            "id": new_id,
            "name": data.get("name"),
            "brand": data.get("brand"),
            "price": int(data.get("price")),
            "mrp": int(data.get("mrp")),
            "description": data.get("description",""),
            "image": data.get("image"),
            "tags": [t.strip() for t in (data.get("tags","").split(",") if data.get("tags") else []) if t.strip()],
            "rating": float(data.get("rating") or 4.5),
            "stock": int(data.get("stock") or 0)
        }
        existing = next((x for x in products if x["id"] == new_id), None)
        if existing:
            for k,v in product.items():
                existing[k] = v
            message = "Product updated."
        else:
            products.append(product)
            message = "Product added."
        save_products(products)
        form = product
    cart_count = get_cart_count()
    return render_template("admin_products.html", products=products, form=form, message=message, cart_count=cart_count)

@app.route("/admin/products/delete/<int:pid>")
def admin_delete_product(pid):
    if not require_admin():
        return redirect(url_for("admin_login"))
    products = get_products()
    products = [p for p in products if p["id"] != pid]
    save_products(products)
    return redirect(url_for("admin_products"))

@app.route("/admin/orders")
def admin_orders():
    if not require_admin():
        return redirect(url_for("admin_login"))
    orders = get_orders()
    orders = sorted(orders, key=lambda x: x["id"], reverse=True)
    cart_count = get_cart_count()
    return render_template("admin_orders.html", orders=orders, cart_count=cart_count)

if __name__ == "__main__":
    app.run(debug=True)
