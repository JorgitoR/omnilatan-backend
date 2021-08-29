# Omnilatan Back-end challange
E-commerce to manage users, product, orders, payments and shipments. 


# Features
- we have two type of user ieg. customer and seller
- A user customer can purchase product as part of an order
- A user seller can sell products
- A payment can apply to one or more orders and an order can be paid by one or more payments.
- An order can delivered by one or more shipments.
- A notification to the purchasers (users) should be sent when a shipment is sent/re-ceived.
- The user can see the products in the cart shopping

# Specifications

- Django REST Framework for API
- Email to send token verification
- Django to develop the web project


# How work this project?
I have two differents type of user "chef" and "employee" for this I implemented the AbstractUser model and switch the AUTH_USER_MODEL on our settings, I never use the built-in Django User model directly, even if the built-in Django User implementation fulfill all the requirements on our application this is because the built-in Django model have some old design decisions (which are kept that way because of backwards compatibility)

The users have different roles, I implemented  <a href="https://github.com/JorgitoR/Cornershop-s-Backend-Test/blob/main/Menu/decorators.py">decorators</a> for this, eg the employee can't create a menu or see what request your coworkers





















