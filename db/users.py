# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
from deta import Deta
from dotenv import load_dotenv
from schemas import Schemas
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- Users Database --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
schemas = Schemas()

class UsersDB():


    PROJECT_KEY = os.getenv('DETA_DB_KEY')
    deta = Deta(PROJECT_KEY)
    users = deta.Base('users')


    def create_user(self, user: schemas.CreateUser) -> Tuple[int, str]:
        code, _, _ = self.get_user_by_name(user.name)
        if code == 200:
            return 409, f"user '{user.name}' already exists in the db."
        if code == 500:
            return 500, f"an error occured while checking if user '{user.name}' exists in the db."

        data = {
            'name': user.name,
            'area': user.area,
        }
        try:
            self.users.put(data)
            return 200, f"'{user.name}' successfully added to db. ('{user.area}')."
        except Exception:
            return 500, f"An error occured adding '{user.name}'. ('{user.area}')."
    

    def update_user_area(self, user: schemas.CreateUser):
        code, _, db_user = self.get_user_by_name(user.name)
        if code != 200:
            return 500, f"an error occured while updating user '{user.name}'."

        key = db_user['key']
        updates = {
            'name': user.name,
            'area': user.area,
        }
        try:
            self.users.update(updates, key)
            return 200, f"successfully updated user area for '{user.name}'."
        except Exception:
            return 500, f"an error occured while updating user area for '{user.name}'."


    def get_user_by_name(self, name: str) -> Tuple[int, str, Dict]:
        try:
            results = self.users.fetch({'name': name})
            user = results.items

            if not user:
                return 404, f"user '{name}' not found in db.", None

            return 200, f"user '{name}' found in db.", user[0]

        except Exception:
            return 500, f"an error occurred while fetching '{name}'", None