import requests
import time

BASE_URL = "http://localhost:80/api/v1"

products = [
    {
        "name": "MacBook Pro M3 Max",
        "description": "Apple's most powerful laptop for professionals.",
        "price": 3499.00,
        "category": "Laptops",
        "stock": 15
    },
    {
        "name": "Sony WH-1000XM5",
        "description": "Industry leading noise canceling headphones.",
        "price": 398.00,
        "category": "Audio",
        "stock": 42
    },
    {
        "name": "Samsung Odyssey G9",
        "description": "49 inch curved gaming monitor.",
        "price": 1299.99,
        "category": "Monitors",
        "stock": 5
    },
    {
        "name": "Logitech MX Master 3S",
        "description": "Advanced wireless mouse.",
        "price": 99.99,
        "category": "Accessories",
        "stock": 120
    },
    {
        "name": "Keychron Q1 Pro",
        "description": "Custom mechanical keyboard.",
        "price": 199.00,
        "category": "Accessories",
        "stock": 30
    }
]

users = [
    {
        "username": "ahmed_dev",
        "email": "ahmed@example.com",
        "full_name": "Ahmed Al-Dev",
        "password": "StrongPassword123!"
    },
    {
        "username": "sarah_designer",
        "email": "sarah@example.com",
        "full_name": "Sarah Designer",
        "password": "StrongPassword123!"
    },
    {
        "username": "khaled_manager",
        "email": "khaled@example.com",
        "full_name": "Khaled Manager",
        "password": "StrongPassword123!"
    }
]

def seed_products():
    for p in products:
        try:
            r = requests.post(f"{BASE_URL}/products/", json=p)
            print(f"Product {p['name']}: {r.status_code}")
        except Exception as e:
            print(f"Failed to seed product {p['name']}: {e}")

def seed_users():
    for u in users:
        try:
            r = requests.post(f"{BASE_URL}/users/register", json=u)
            print(f"User {u['username']}: {r.status_code}")
        except Exception as e:
            print(f"Failed to seed user {u['username']}: {e}")

if __name__ == "__main__":
    print("Seeding database...")
    seed_users()
    print("Done!")
