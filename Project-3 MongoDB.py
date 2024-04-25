#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymongo
from bson import ObjectId


# In[2]:


client = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = client["OnlineStore"]

users = mydb["Users"]
products = mydb["Products"]
cart = mydb["ShoppingCart"]
orders = mydb["Orders"]


# In[6]:


def add_user(firstname, lastname, email, phone, dob, address):
    user_data = {
        "firstname": firstname,
        "lastname": lastname,
        "email": email,
        "phone": phone,
        "dob": dob,
        "address": address
    }
    users.insert_one(user_data)
    print("User added successfully.")

def products_by_category(category):
    return list(products.find({"category": category}))

def product_by_id(product_id):
    return products.find_one({"_id": ObjectId(product_id)})

def add_to_cart(user_id, product_ids):
    if not isinstance(product_ids, list):
        product_ids = [product_ids]
    cart.insert_one({"user_id": user_id, "products": product_ids})
    print("Product added to cart.")

def delete_from_cart(cart_id, products_to_delete):
    products_to_delete = [ObjectId(pid) for pid in products_to_delete]
    cart.update_one({"_id": cart_id}, {"$pull": {"products": {"$in": products_to_delete}}})
    print("Product removed from cart.")

def view_cart(user_id):
    user_cart = cart.find_one({"user_id": user_id})
    if user_cart:
        print("Products in Your Cart:")
        for product_id in user_cart["products"]:
            product = product_by_id(product_id)
            if product:  # Check if product is not None
                print(f"- {product['title']} at ${product['price']:.2f}")
            else:
                print(f"Product with ID {product_id} not found in the database.")
    else:
        print("Your cart is empty.")

def checkout(user_id):
    order_summary(user_id)
    cart.delete_one({"user_id": user_id})
    print("Checkout completed. Cart is now empty.")

def order_summary(user_id):
    user_cart = cart.find_one({"user_id": user_id})
    if user_cart:
        total = 0
        products_in_cart = user_cart["products"]
        print("Order Summary:")
        for product_id in products_in_cart:
            product = product_by_id(product_id)
            if product:
                print(f"- Product: {product['title']}, Price: ${product['price']:.2f}")
                total += product["price"]
            else:
                print(f"Product ID {product_id} not found.")
        print(f"Total Amount: ${total:.2f}")
    else:
        print("No items in the cart.")


# In[7]:


def main_menu():
    while True:
        print("""
1. Add User
2. View Products by Category
3. Add Product to Cart
4. Delete Product from Cart
5. View Cart
6. Checkout
0. Exit""")
        choice = input("Enter your choice: ")
        if choice == '1':
            firstname = input("First Name: ")
            lastname = input("Last Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            address = input("Address: ")
            add_user(firstname, lastname, email, phone, dob, address)
        elif choice == '2':
            category = input("Enter the category: ")
            products = products_by_category(category)
            for product in products:
                print(f"- {product['title']} at ${product['price']:.2f}")
        elif choice == '3':
            user_id = input("User ID: ")
            product_id = input("Product ID: ")
            add_to_cart(user_id, product_id)
        elif choice == '4':
            cart_id = input("Cart ID: ")
            product_id = input("Product ID to remove: ")
            delete_from_cart(cart_id, [product_id])
        elif choice == '5':
            user_id = input("User ID: ")
            view_cart(user_id)
        elif choice == '6':
            user_id = input("User ID: ")
            checkout(user_id)
        elif choice == '0':
            print("Exiting program.")
            break
        else:
            print("Invalid choice, please try again.")


# In[8]:


if __name__ == '__main__':
    main_menu()


# In[ ]:




