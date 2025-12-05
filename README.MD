🛋️ Furniture E-Commerce API

A fully featured **E-Commerce backend** built using **Django REST Framework**.
The project provides product browsing, cart handling, ordering, authentication with email activation, newsletter subscription, and a simple blog system — all based on a custom Figma design.

🚀 Features

🔐 Authentication & User Management

* User registration with email activation link
* JWT authentication via DRF SimpleJWT
* Newsletter subscription system — subscribed users receive project updates
* Signals for:

  * Sending activation/subscription emails
  * Updating product ratings

🛒 E-Commerce Functionality

* Get list of furniture products
* Like products or add them to cart
* Cart stored in cache (not a database model)

  * Cart is temporary
  * Cleared when an order is created
* Create orders from cart items

📝 Blog System

* Users can browse blog posts about furniture

⚙️ Admin & Developer Tools

* Jazzmin for a modern admin panel UI
* Management command to populate database with testing data after cloning

🧰 Tech Stack

| Component         | Tech                                   |
| ----------------- | -------------------------------------- |
| Backend Framework | Django, Django REST Framework          |
| Authentication    | DRF SimpleJWT                          |
| Email             | Django Email Backend                   |
| Cache             | Django Cache Framework (used for cart) |
| Admin UI          | Jazzmin                                |
| Other             | Custom signals, management commands    |

📦 Installation & Setup

1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Linux & Mac
venv\Scripts\activate      # Windows
```

3. Install Dependencies

```bash
pip install -r requirements/base.txt
```

4. Apply Migrations

```bash
python manage.py migrate
```

5. Run Test Data Command (optional)

Populates the database with demo products, categories, and posts:

```bash
python manage.py populate_fake_data
```

6. Start the Server

```bash
python manage.py runserver
```

💡 How the Cart Works

The cart uses **cache storage** instead of a database model because it is temporary and only needed while users are adding products.
Once an order is created, the cart is cleared and a new one begins automatically.
This makes the system simpler and more efficient.

📮 Email System

Account Activation

After registration, the user receives an activation email containing a confirmation link.
Their account becomes active only after clicking the link.

Newsletter Subscription

Users may subscribe to a newsletter.
A signal automatically provides updates to subscribed users whenever new content or changes occur in the project.

🛠 Admin Panel

The project uses **Jazzmin** to provide a modern, clean admin UI where administrators can manage:

* Accounts
* Blog
* Common
* Orders
* Products
