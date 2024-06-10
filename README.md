# AFII Django Trade Platform 💽

This is a trade capture system built using Python, Django and JavaScript. Its main page is a web application containing three sections - a form for submitting new trades, a trade blotter for editing trades before they are committed, and a graph section for displaying information about committed trades. 

## Features

### User Registration and Login

To use the application, the user must first create an account. After registration, they will be prompted to log in.

### New Trade Submission

- **New Trade Form**: The user can create new trades in the "New Trade" section. The form features a radio selector to designate the instrument type of the trade.


### Trade Blotter

- **Edit Trades**: Trades appear in the "Trade Blotter" section. To edit a trade, the user can click on the pencil icon in the "Action" column of the table. This will open a form where the trade's details can be modified.
- **Delete Trades**: Trades can be deleted by clicking the delete button on the edit form or the rubbish bin icon in the "Action" column.
- **Commit Trades**: Once the user is satisfied with their staged trades, click the "Upload Trades" button to commit them to the backend.

### Graph Section

- **Trade Analytics**: The graph section displays information about all committed trades in the system, from all users.
- **Historical Data**: A dropdown menu allows the user to select and view trades up to five years in the past.
- **Graphical Insights**:
  - **Distribution of Trades**: The top graph shows the distribution of trades by instrument type or strategy (selectable from a dropdown) over the selected time period.
  - **Volume Analysis**: The second graph allows the user to select an individual instrument type and view the spread of trade volume for a given numerical field's value.

## Local Installation

### Prerequisites

Make sure you have the following installed on your system:
- Python (3.x recommended, 3.11.5 used for development)
- pip (Python package installer)
- Virtualenv (optional but recommended)

### Cloning the Repository

1. Clone the repository using HTTPS:
    ```bash
   https://github.com/16000psi/afii-challenge.git
    ```
   Or using SSH:
    ```bash
    git@github.com:16000psi/afii-challenge.git
    ```

2. Navigate to the project directory:
    ```bash
    cd envirotrade
    ```

### Installing dependencies


1. Create a virtual environment:
    ```bash
    python -m venv env
    ```

2. Activate the virtual environment:

    - On Windows:
        ```bash
        .\env\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source env/bin/activate
        ```


3. Install the required dependencies using `pip`:
    ```bash
    pip install -r requirements.txt
    ```
4. Execute database migrations:
    ```bash
    python manage.py migrate
    ```

5. Populate the database with dummy data:
    ```bash
    python manage.py generate_dummy_data
    ```

6. Run the application:
    ```bash
    python manage.py runserver
    ```

**The application should now be running at [http://localhost:8000/signup/](http://localhost:8000/signup/)**

7. Create an account and get started!
    
N.B. This application uses a CDN to access a JavaScript data visualisation library (chart.js). As a result, the application will not work properly unless you are connected to the internet. 