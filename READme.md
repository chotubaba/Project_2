# Project 2 Django Final
```markdown
A Django web application for user management and financial operations, including account creation, login, balance operations, transaction history, and currency exchange.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Connecting to DBeaver for SQLite Queries](#connecting-to-dbeaver-for-sqlite-queries)
- [Contributing](#contributing)
- [Next Steps](#next-steps)
- [License](#license)
```

```markdown
## PROJECT DESCRIPTION
Project Description
Overview
This Django web application facilitates user management and financial operations. It includes features for account creation, login, balance operations, transaction history, and currency exchange. The project is designed to demonstrate robust error handling, user authentication, and financial transaction processing.

Features
User Authentication and Management

Create Account: Users can register using the CreateUserView.
Login: Users can log in through the CustomLoginView.
Logout: Users can log out using the logout_view function.
Financial Operations

Balance Operations: Users can deposit or withdraw funds using the BalanceOperationsView. The balance is calculated by summing all deposits and subtracting all withdrawals.
Transaction History: Users can view their transaction history, including deposits and withdrawals, through the ViewTransactionHistoryView.
Currency Exchange

Currency Exchange View: Users can convert amounts between different currencies using the CurrencyExchangeView. The exchange rates are fetched from an external API.
```


**Detailed Description**
```markdown
Authentication Views
CreateUserView: Facilitates user registration using the User model and CreateUserForm. It uses the create_account.html template and redirects to the login page upon successful account creation.

CustomLoginView: Handles user login using the login.html template and redirects to the main menu upon successful login.
logout_view: Logs out the user and redirects to the login page.

Main Menu
MainMenuView: Displays the main menu to authenticated users and handles exceptions gracefully.

Balance Operations
getBalance(user): A utility function to calculate the user’s balance by summing all successful deposits and subtracting all successful withdrawals.
BalanceOperationsView: A view that handles balance-related operations (deposit and withdraw). It validates the operations and updates the user's balance accordingly.

Transaction History
ViewTransactionHistoryView: A view that displays the transaction history for the logged-in user, sorted by date.

Currency Exchange
getCurrencyParams(): A utility function that fetches currency exchange rates from an external API and formats them for display.
CurrencyExchangeView: A view that allows users to convert amounts between different currencies. It processes and validates the input, fetches the exchange rate, and calculates the exchanged amount.
```

```markdown
Error Handling and Security
Error Handling: Robust error handling mechanisms are implemented to manage exceptions gracefully and provide meaningful error messages to users.
Security: Django's built-in security features such as CSRF protection, authentication, and validation checks are thoroughly utilized.

Testing
Comprehensive Testing: Unit tests are written for each view and function using Django’s testing framework to ensure all components work correctly under different scenarios.

Next Steps
Enhancements: Further improvements could include more detailed error messages, additional validation checks, and enhanced security measures.


```markdown
### Views and Functions

**Logout Function (`logout_view`)**

  Handles user logout and redirects to the login page.

**Operations Functions (`getBalance` and transaction operations in `BalanceOperationsView`)**

  - **`getBalance(user)`**: Calculates the user's balance based on deposit and withdrawal history.
  - **`BalanceOperationsView Class`**: Handles both GET and POST requests for balance operations.
  - **`get(self, request)`**: Retrieves the user's balance and renders the `operations.html` template.
  - **`post(self, request)`**: Processes deposit and withdrawal operations based on form input, updates history, and renders the updated balance in the template.

**Create User (`CreateUserView`) and Login (`CustomLoginView`)**

  - **`CreateUserView`**: Utilizes `CreateView` to handle user registration using the `User` model and `CreateUserForm`.
  - **`CustomLoginView`**: Extends `LoginView` to customize login behavior and context data.


**Main Menu (`MainMenuView`)**

  Displays the main menu template (`main_menu.html`) with the user's username if authenticated.


**Transaction History (`ViewTransactionHistoryView`)**

  Displays the transaction history for the logged-in user, sorted by date.


**Currency Exchange (`CurrencyExchangeView`)**

Provides functionality to convert an amount from one currency to another using an external API:
  - **API Endpoint**: [Currency Exchange API](https://fake-api.apps.berlintech.ai/api/currency_exchange)
  - Handles GET and POST requests, validates form data, retrieves currency rates, and computes the exchanged amount.

  ```

## INSTALLATION

To get the project up and running on your local machine, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/chotubaba/Project_2.git 
   ```

2. **Navigate to the Project Directory**

    ```bash
    cd Project_2_Django_Final/intermediate_assessment_Django_1
    ```

3. **Set Up a Virtual Environment**

    ```bash
    python -m venv venv
    ```

**Activate the Virtual Environment**

For macOS/Linux:

    ```bash
    source venv/bin/activate
    ```

For Windows:

    ```bash
    venv\Scripts\activate
    ```

**Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply Database Migrations**
   
    ```bash
    pip install -r requirements.txt
    ```

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

** Create a Superuser (Optional for Admin Access) **

    ```bash
    python manage.py createsuperuser
    ```
** Usage : Run the Development Server **

    ```bash
    python manage.py runserver
    ```

**Access the Application**

    Open your browser and navigate to:
    ```bash
    http://localhost:8000
    ```

5. **Connecting to DBeaver for SQLite Queries**
        - Open DBeaver and create a new SQLite connection.
        - Navigate to the Database File:
        - Click on Database > New Database Connection.
        - Choose SQLite.
        - Browse to the db.sqlite3 file located in the project root directory.
        - Connect and execute queries against your SQLite database as needed.

6. **Testing**
   
-Running All Tests :
    To run all tests in the project, execute:
    ```bash
    python3 manage.py test
    ```

-Testing Specific Components
    To test individual models, methods, classes, or templates, specify the path to the test module. 
    For example, to test the ViewTransactionHistoryView:
    ```bash
    python3 manage.py test app.tests.test_TransactionHistoryView
    ```


7. ** Adding __pycache__ Files to .gitignore **
    __pycache__ files are generated by Python to store bytecode-compiled versions of your Python files.

- To prevent these files from being tracked by Git, ensure your .gitignore file includes the following line:

    ```bash
    __pycache__/
    ```

- ** Remove Existing __pycache__ Directories from Git Tracking **


    Step 1: Add __pycache__ to .gitignore
        ```bash
        echo "__pycache__/" >> .gitignore
        ```

    Step 2: Remove __pycache__ directories from Git tracking
      ```bash
      find . -name "__pycache__" -type d -exec git rm -r --cached {} +
      ```

    Step 3: Commit the changes
      ```bash
      git add .gitignore
      git commit -m "Add __pycache__ to .gitignore and remove from tracking"
      ```

    Step 4: Push the changes
      ```bash
      git push origin branch_name
      ```

8. **Security:**
  Review and implement Django's built-in security features such as CSRF protection (csrf_token), authentication (LoginRequiredMixin), and validation checks (e.g., amount <= 0,   invalid operations).


9. **Contributing**
  Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
  
  Please make sure to update tests as appropriate.
  
    1. Fork the Repository: Click on the "Fork" button at the top right of this repository page.

    2. Create a New Branch:*
        ```bash
        git checkout -b feature-branch
        ```
    3. Commit Your Changes:
    
        ```bash
        git commit -am 'Add new feature'
        ```
    4. Push to the Branch:
    
        '''bash
        git push origin feature-branch
        '''

4. Create a Pull Request: Go to the repository on GitHub and click **"New Pull Request".**

Please refer to our Code of Conduct for more details.

```markdown
10.**License**
This project is licensed under the MIT License. See the LICENSE file for details.

[MIT](https://choosealicense.com/licenses/mit/)

This `README.md` file includes all the necessary steps for installation, usage, testing, and contributing, with clear sections and formatting for easy navigation.
```
