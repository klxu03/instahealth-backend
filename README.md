# instahealth-backend

Get [Python](https://www.python.org/downloads/) lol.

First change your current directory to the `instahealth-backend` directory.

Create a virtual environment by running `python -m venv .venv` and enter it by running `.venv\Scripts\activate.bat` on Windows or `source .venv/bin/activate` on Linux. You can exit the virtual environment by running `deactivate`.

Install dependencies by running `pip install -r requirements.txt`.

Set the environment variable `FLASK_ENV` to `development` for better debugging and hot reloading by running `set FLASK_ENV=development` on Windows or `export FLASK_ENV=development` on Linux.

Set the environment variable `IH_PASSWORD` to the password of the InstantHealth Gmail account.

Create the database using `flask init-db`.

Run the app using `flask run`.

