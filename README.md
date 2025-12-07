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
In your local code environment, run the following command in your terminal to clone the lotties-closet repository from GitHub: `git clone https://github.com/cfeigin/lotties-closet.git`. 

Navigate into the lotties-closet directory via: `cd lotties-closet`.

### Setup
1. To ensure that dependencies don't conflict with system Python, create and activate a virtual environment.

    For Linux/MacOS/WSL, run the following commands: 
        
        python3 -m venv .venv  
        source .venv/bin/activate

    For Windows PowerShell, run the following commands: 
        
        python -m venv .venv  
        .\.venv\Scripts\activate

    If the above fails, you may need to install `venv`. Do so via the following terminal command: `sudo apt install python3-venv`. Once installing `venv`, follow the above steps again to creat and activate your virtual environment.

    You should now see `(venv)` at the start of your command line prompt. 
2. To install all required libraries, run the following command: `pip install -r requirements.txt`.
3. Create a file called `.env`. Within the `.env` file, input your OpenAI and SerpAPI keys using exactly the following scheme: 

        SERP_API_KEY=...
        OPEN_API_KEY=...

    Replace the elipses (...) with your respective API keys. Do not enclose the keys in quotation marks and do not include any semicolons in the file. In the end, your `.env` file should only have two lines.

    To protect your API key, ensure that your `.gitignore` contains the following somewhere in the file: 

        .env

    This should already be done for you, but in the event that `.env` is not included in `.gitignore`, add it on its own line of the file (with no quotes, semicolons, or any text decoration).

### Showtime

To launch the application, ensure that you are located within the lotties-closet directory. Your command prompt should end in `/lotties-closet`. If it doesn't, navigate to the directory via `cd lotties-closet`. Then, type the following command into your terminal: `flask run`. Your terminal should provide a link via which to locally host the application. 

## Usage
When you click the link provided by your terminal, you will be taken to the login page. If you are a returning user, enter your username and password to start searching. If you are a new user, navigate to the "Register" page via the navbar. You will be asked for your name, a desired username, and a password. Though your name and password may take any value, attempting to create an account with a username that is already in use by another user will result in automatic redirection to the error page. 

Once your account is created, you will be taken to the user preferences form, which will ask a number of questions (e.g. height, weight, shoe size). All fields are completely optional and may be left blank if desired. All invalid input will be rejected. After completing the form and clicking "Update Preferences", you will be taken to the home page. You may view your saved preferences via the "View Preferences" page linked in the navbar, and you may update these preferences anytime by navigating to the "Update Preferences" page. 

On the home page, you may enter any natural language search query into the search bar. Example input is provided. After clicking the "Search" button, you will be able to see the optimized query that Lottie used, as well as relevant Google Shopping results in a grid layout. Clicking "View Item" under any shopping result will open the Google Shopping page for that item in a new tab. 

Happy shopping! 

