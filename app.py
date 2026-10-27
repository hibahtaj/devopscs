import os
from flask import Flask, render_template, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'local-dev-only-change-me')

MENU = [
    {'id': 1, 'name': 'Veg Burger', 'price': 99, 'emoji': '🍔'},
    {'id': 2, 'name': 'Margherita Pizza', 'price': 199, 'emoji': '🍕'},
    {'id': 3, 'name': 'French Fries', 'price': 79, 'emoji': '🍟'},
    {'id': 4, 'name': 'White Sauce Pasta', 'price': 169, 'emoji': '🍝'},
    {'id': 5, 'name': 'Chocolate Shake', 'price': 119, 'emoji': '🥤'},
    {'id': 6, 'name': 'Chocolate Brownie', 'price': 89, 'emoji': '🍫'},
]

@app.get('/')
def home():
    return render_template('home.html')

@app.get('/menu')
def menu():
    return render_template('menu.html', items=MENU)

@app.post('/add/<int:item_id>')
def add_to_cart(item_id):
    if not any(item['id'] == item_id for item in MENU):
        flash('Item not found.')
        return redirect(url_for('menu'))
    cart = session.get('cart', {})
    key = str(item_id)
    cart[key] = cart.get(key, 0) + 1
    session['cart'] = cart
    flash('Added to cart!')
    return redirect(url_for('menu'))

@app.get('/cart')
def cart():
    selected = []
    total = 0
    for item in MENU:
        quantity = session.get('cart', {}).get(str(item['id']), 0)
        if quantity:
            subtotal = item['price'] * quantity
            selected.append({**item, 'quantity': quantity, 'subtotal': subtotal})
            total += subtotal
    return render_template('cart.html', items=selected, total=total)

@app.post('/remove/<int:item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    cart.pop(str(item_id), None)
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.post('/place-order')
def place_order():
    if not session.get('cart'):
        flash('Add something to your cart first.')
        return redirect(url_for('menu'))
    session.pop('cart', None)
    return redirect(url_for('confirmation'))

@app.get('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.get('/health')
def health():
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
