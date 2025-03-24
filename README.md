# Django Vehicle Rental System

## Description
This is a Vehicle Rental System made using Django and Bootstrap. It contains the following features:
<br>
1. Multiple Account Creation (separate permissions for vehicle owner and renters)
2. Payment Integration (using Khalti Web Checkout)
3. Advance Search Features
4. User Rating for the Vehicles
5. Reset Password Features
6. Vechile rent confirmation email using Google's smtp client
7. Dashboard for vehicle owner and customer
8. And more

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/SumanGautam1/VehicleRentalSystem.git

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt

3. Create a ```.env``` file in your root directory and configure your ```SECRET_KEY, KHALTI_KEY``` as well as ```MAIL_HOST_PASSWORD and EMAIL_HOST_USER```.
    You can generate a secure key using:
    ```bash
    python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

You can get the KHALTI_KEY from khalti official documentation.
Get the ```MAIL_HOST_PASSWORD and EMAIL_HOST_USER``` from Google appication dashboard.

4. Run migrations:
    ```bash
    python manage.py migrate

5. Create superuser for easier handling of data.
    ```bash
    python manage.py createsuperuser

6. Run migrations again:
    ```bash
    python manage.py makemigrations
    python manage.py migrate

5. Start the development server:
    ```bash
    python manage.py runserver

## UI Screenshots:
### Home Page
![Home Page](assets/homepage.png?raw=true "Home Page")

### Login Page
![Login Page](assets/loginpage.png?raw=true "Login Page")

### Dashboard Page
![Dashboard Page](assets/dashboard.png?raw=true "Dashboard Page")