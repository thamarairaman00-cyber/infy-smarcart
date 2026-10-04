from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# -----------------------------
# PRODUCT DATA
# -----------------------------

products = [
    {
        "id": 1,
        "name": "iPhone 15",
        "price": 69999,
        "category": "Apple",
        "rating": 4.7,
        "stock": 10,
        "image": "https://images.unsplash.com/photo-1592750475338-74b7b21085ab"
    },
    {
        "id": 2,
        "name": "Samsung Galaxy S24",
        "price": 74999,
        "category": "Samsung",
        "rating": 4.6,
        "stock": 15,
        "image": "https://images.unsplash.com/photo-1610945265064-0e34e5519bbf"
    },
    {
        "id": 3,
        "name": "OnePlus 12",
        "price": 64999,
        "category": "OnePlus",
        "rating": 4.5,
        "stock": 20,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97"
    },
    {
        "id": 4,
        "name": "Google Pixel 8",
        "price": 59999,
        "category": "Google",
        "rating": 4.4,
        "stock": 12,
        "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97"
    }
]

cart = []
orders = []


# -----------------------------
# HTML DESIGN
# -----------------------------

HTML = """

<!DOCTYPE html>

<html>

<head>

<title>INFY SmartCart</title>

<meta name="viewport" content="width=device-width, initial-scale=1">

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f6f8;
    color: #222;
}

nav {
    background: #111827;
    color: white;
    padding: 18px 5%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
}

.logo {
    font-size: 24px;
    font-weight: bold;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 8px;
}

.hero {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: white;
    text-align: center;
    padding: 70px 20px;
}

.hero h1 {
    font-size: 42px;
}

.hero p {
    font-size: 20px;
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
    padding: 35px 0;
}

.search {
    text-align: center;
    margin-bottom: 30px;
}

.search input {
    width: 70%;
    padding: 14px;
    border: 1px solid #ccc;
    border-radius: 8px;
}

.products {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.card {
    background: white;
    padding: 18px;
    border-radius: 12px;
    box-shadow: 0 3px 12px #ddd;
}

.card img {
    width: 100%;
    height: 210px;
    object-fit: cover;
    border-radius: 10px;
}

.card h2 {
    font-size: 20px;
}

.price {
    font-size: 22px;
    font-weight: bold;
}

.rating {
    color: #f59e0b;
}

button {
    background: #2563eb;
    color: white;
    border: none;
    padding: 11px 16px;
    border-radius: 7px;
    cursor: pointer;
    margin: 5px;
}

button:hover {
    background: #1d4ed8;
}

.cart-item {
    background: white;
    padding: 20px;
    margin: 15px 0;
    border-radius: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.box {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 10px #ddd;
    margin-bottom: 20px;
}

input,
select {
    padding: 12px;
    width: 100%;
    margin: 8px 0;
    border: 1px solid #ccc;
    border-radius: 7px;
}

.success {
    text-align: center;
    background: white;
    padding: 60px;
    margin: 50px auto;
    max-width: 700px;
    border-radius: 15px;
}

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.stat {
    background: white;
    text-align: center;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 3px 10px #ddd;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
}

th,
td {
    padding: 15px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}

.ai {
    background: #111827;
    color: white;
    padding: 20px;
    border-radius: 12px;
    margin-top: 30px;
}

footer {
    background: #111827;
    color: white;
    text-align: center;
    padding: 25px;
    margin-top: 50px;
}

@media(max-width:900px) {

    .products {
        grid-template-columns: repeat(2, 1fr);
    }

    .stats {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media(max-width:600px) {

    .products {
        grid-template-columns: 1fr;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .hero h1 {
        font-size: 30px;
    }

    .search input {
        width: 100%;
    }

    .cart-item {
        flex-direction: column;
    }
}

</style>

</head>

<body>

<nav>

<div class="logo">
🛒 INFY SmartCart
</div>

<div>

<a href="/">Home</a>

<a href="/cart">
Cart ({{ cart_count }})
</a>

<a href="/admin">
Admin
</a>

</div>

</nav>


{% if page == "home" %}

<section class="hero">

<h1>Smartphones at Smart Prices</h1>

<p>
Find your perfect smartphone with INFY SmartCart
</p>

</section>


<div class="container">

<div class="search">

<form method="GET" action="/">

<input
name="search"
placeholder="Search smartphones..."
value="{{ search }}"
>

<button type="submit">
Search
</button>

</form>

</div>


<h2>📱 Popular Smartphones</h2>


<div class="products">

{% for p in products %}

<div class="card">

<img src="{{ p.image }}">

<h2>
{{ p.name }}
</h2>

<p>
Category: {{ p.category }}
</p>

<p class="rating">
⭐ {{ p.rating }}/5
</p>

<p class="price">
₹{{ "{:,}".format(p.price) }}
</p>

<p>
Stock: {{ p.stock }}
</p>

<a href="/product/{{ p.id }}">

<button>
View Details
</button>

</a>

<a href="/add/{{ p.id }}">

<button>
Add to Cart
</button>

</a>

</div>

{% endfor %}

</div>


<div class="ai">

<h2>🤖 AI Shopping Assistant</h2>

<p>
Looking for a smartphone? INFY SmartCart can help you
choose a phone based on your budget and requirements.
</p>

<p>
Example: For premium users choose iPhone 15 or Galaxy S24.
For performance and value choose OnePlus 12.
</p>

</div>

</div>


{% elif page == "product" %}


<div class="container">

<div class="box">

<img
src="{{ product.image }}"
style="width:300px;max-width:100%;border-radius:10px;"
>

<h1>
{{ product.name }}
</h1>

<h2>
₹{{ "{:,}".format(product.price) }}
</h2>

<p>
Category: {{ product.category }}
</p>

<p>
⭐ {{ product.rating }}/5
</p>

<p>
Available Stock: {{ product.stock }}
</p>

<h3>Product Description</h3>

<p>
Premium smartphone with modern design,
powerful performance, excellent camera,
and long-lasting battery.
</p>

<a href="/add/{{ product.id }}">

<button>
🛒 Add to Cart
</button>

</a>

</div>

</div>


{% elif page == "cart" %}


<div class="container">

<h1>🛒 Shopping Cart</h1>

{% if cart %}

{% for item in cart %}

<div class="cart-item">

<div>

<h2>
{{ item.name }}
</h2>

<p>
₹{{ "{:,}".format(item.price) }}
</p>

</div>

<a href="/remove/{{ item.id }}">

<button>
Remove
</button>

</a>

</div>

{% endfor %}


<div class="box">

<h2>
Total: ₹{{ "{:,}".format(total) }}
</h2>

<a href="/checkout">

<button>
Proceed to Checkout
</button>

</a>

</div>

{% else %}

<div class="box">

<h2>Your cart is empty.</h2>

<a href="/">

<button>
Continue Shopping
</button>

</a>

</div>

{% endif %}

</div>


{% elif page == "checkout" %}


<div class="container">

<div class="box">

<h1>📦 Checkout</h1>

<form method="POST">

<label>Full Name</label>

<input
name="name"
required
placeholder="Enter your name"
>

<label>Address</label>

<input
name="address"
required
placeholder="Enter delivery address"
>

<label>City</label>

<input
name="city"
required
placeholder="Enter city"
>

<label>Pincode</label>

<input
name="pincode"
required
placeholder="Enter pincode"
>

<h2>Payment Simulation</h2>

<select name="payment">

<option>UPI</option>

<option>Credit Card</option>

<option>Debit Card</option>

<option>Cash on Delivery</option>

</select>

<h2>
Order Total: ₹{{ "{:,}".format(total) }}
</h2>

<button type="submit">
💳 Pay & Place Order
</button>

</form>

</div>

</div>


{% elif page == "success" %}


<div class="success">

<h1>
✅ Order Placed Successfully!
</h1>

<h2>
Thank you for shopping with INFY SmartCart.
</h2>

<p>
Your order has been created successfully.
</p>

<a href="/">
<button>
Continue Shopping
</button>
</a>

</div>


{% elif page == "admin" %}


<div class="container">

<h1>⚙️ Admin Dashboard</h1>


<div class="stats">

<div class="stat">

<h1>{{ products|length }}</h1>

<p>Total Products</p>

</div>


<div class="stat">

<h1>120</h1>

<p>Total Users</p>

</div>


<div class="stat">

<h1>{{ orders|length }}</h1>

<p>Total Orders</p>

</div>


<div class="stat">

<h1>₹2,40,000</h1>

<p>Revenue</p>

</div>

</div>


<br>


<div class="box">

<h2>📦 Product Management</h2>

<table>

<tr>

<th>Product</th>

<th>Price</th>

<th>Stock</th>

<th>Rating</th>

</tr>


{% for p in products %}

<tr>

<td>
{{ p.name }}
</td>

<td>
₹{{ "{:,}".format(p.price) }}
</td>

<td>
{{ p.stock }}
</td>

<td>
⭐ {{ p.rating }}
</td>

</tr>

{% endfor %}

</table>

</div>


<div class="box">

<h2>🚚 Order Management</h2>

<select>

<option>Pending</option>

<option>Confirmed</option>

<option>Processing</option>

<option>Shipped</option>

<option>Delivered</option>

</select>

</div>

</div>

{% endif %}


<footer>

<p>
© 2026 INFY SmartCart | INFYHACKATHON 2.0
</p>

</footer>

</body>

</html>

"""


# -----------------------------
# HOME
# -----------------------------

@app.route("/")
def home():

    search = request.args.get("search", "")

    if search:

        filtered = [
            p for p in products
            if search.lower() in p["name"].lower()
        ]

    else:

        filtered = products

    return render_template_string(
        HTML,
        page="home",
        products=filtered,
        cart_count=len(cart),
        search=search
    )


# -----------------------------
# PRODUCT DETAILS
# -----------------------------

@app.route("/product/<int:product_id>")
def product_details(product_id):

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if not product:
        return "Product not found", 404

    return render_template_string(
        HTML,
        page="product",
        product=product,
        cart_count=len(cart)
    )


# -----------------------------
# ADD TO CART
# -----------------------------

@app.route("/add/<int:product_id>")
def add_to_cart(product_id):

    product = next(
        (p for p in products if p["id"] == product_id),
        None
    )

    if product and product["stock"] > 0:

        cart.append(product)

    return redirect("/cart")


# -----------------------------
# REMOVE FROM CART
# -----------------------------

@app.route("/remove/<int:product_id>")
def remove_from_cart(product_id):

    for item in cart:

        if item["id"] == product_id:

            cart.remove(item)

            break

    return redirect("/cart")


# -----------------------------
# CART
# -----------------------------

@app.route("/cart")
def view_cart():

    total = sum(
        item["price"]
        for item in cart
    )

    return render_template_string(
        HTML,
        page="cart",
        cart=cart,
        total=total,
        cart_count=len(cart)
    )


# -----------------------------
# CHECKOUT
# -----------------------------

@app.route("/checkout", methods=["GET", "POST"])
def checkout():

    if request.method == "POST":

        if not cart:

            return redirect("/cart")

        customer_name = request.form.get("name")
        address = request.form.get("address")
        city = request.form.get("city")
        pincode = request.form.get("pincode")
        payment = request.form.get("payment")

        total = sum(
            item["price"]
            for item in cart
        )

        order = {
            "customer": customer_name,
            "address": address,
            "city": city,
            "pincode": pincode,
            "payment": payment,
            "total": total,
            "status": "Pending"
        }

        orders.append(order)

        cart.clear()

        return render_template_string(
            HTML,
            page="success",
            cart_count=0
        )

    total = sum(
        item["price"]
        for item in cart
    )

    return render_template_string(
        HTML,
        page="checkout",
        total=total,
        cart_count=len(cart)
    )


# -----------------------------
# ADMIN
# -----------------------------

@app.route("/admin")
def admin():

    return render_template_string(
        HTML,
        page="admin",
        products=products,
        orders=orders,
        cart_count=len(cart)
    )




if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
    )