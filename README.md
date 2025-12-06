# Lottie's Closet
Lottie's Closet is your all-in-one, AI-powered shopping assistant. Simply search for the clothing item you'd wish to find, and Lottie will create an optimal search query based on your saved sizing and preferences data, returning relevant Google Shopping items in a clean and efficient user interface.  

---

## Features
- Flask web application
- User data privacy
- Integration with OpenAI and SerpAPI
- User-friendly interface

---

## Installation
In your local code environment, run the following command in your terminal to clone the lotties-closet repository from GitHub: `git clone https://github.com/cfeigin/lotties-closet.git`. TODO

OR After downloading closet.zip to your computer, unzip 

Navigate into the closet directory via: `cd closet`.

### Setup
1. To ensure that dependencies don't conflict with system Python, create and activat a virtual environment.

    For Linux/MacOS/WSL, run the following commands: 
        
        python3 -m venv .venv  
        source .venv/bin/activate

    For Windows PowerShell, run the following commands: 
        
        python -m venv .venv  
        .\.venv\Scripts\activate

    You should now see `(venv)` at the start of your command line prompt. 
2. To install all required libraries, run the following command: `pip install -r requirements.txt`.
3. API keys? TODO

To launch the application, ensure that you are located in the closet directory. Your command prompt should end in `/closet`. Then, type the following command: `flask run`. Your terminal should provide a link via which to use the application.

## Usage
When you click the link provided by your terminal, you will be taken to the login page. If you are a returning user, enter your username and password to start searching. If you are a new user, navigate to the "Register" page via the navbar at the top of the page. You will be asked for your name, a desired username, and a password. Though your name and password may take any value, attempting to create an account with a username already in use will result in automatic redirection to an error page. 

Once your account is created, you will be taken to the user preferences form, which will ask a number of questions pertaining to your sizing preferences (e.g. height, weight, shoe size). All fields are completely optional and may be left blank if desired. All input will be verified on the backend and invalid submissions will be rejected. After completing the form and clicking "Submit," you will be taken to the home page. You may view your saved preferences via the "View Preferences" page linked in the navbar, and you may update these preferences anytime by navigating to the "Update Preferences" page. 

On the home page, you may enter any natural language search query into the search bar. Example input is provided. After clicking the "search" button, you will be able to see the optimized query that Lottie used, as well as a number of Google Shopping results in a grid layout. Clicking "View Item" under any shopping result will open the Google Shopping page for that item in another tab. 

Happy shopping! 

