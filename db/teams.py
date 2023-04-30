# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import os
from deta import Deta
from dotenv import load_dotenv
from schemas import Schemas
from typing import Dict, Tuple


# ---------------------------------------------------------------------------- #
# --- Teams Database --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


load_dotenv()
schemas = Schemas()

class TeamsDB():

    PROJECT_KEY = os.getenv('DETA_DB_KEY')
    deta = Deta(PROJECT_KEY)
    teams = deta.Base('teams')


    def create_team(self, team: schemas.CreateTeam) -> Tuple[int, str]:
        code, _, _ = self.get_team_by_name(team.name)
        if code == 200:
            return 409, f"team '{team.name}' already exists in the db."
        if code == 500:
            return 500, f"an error occured while checking if team '{team.name}' exists in the db."

        data = {
            'name': team.name,
            'members': team.members
        }
        try:
            self.teams.put(data)
            return 200, f"'{team.name}' successfully added to db."
        except Exception:
            return 500, f"An error occured adding '{team.name}'."


    def get_team_by_name(self, name: str) -> Tuple[int, str, Dict]:
        try:
            results = self.teams.fetch({'name': name})
            team = results.items

            if not team:
                return 404, f"team '{name}' not found in db.", None

            return 200, f"team '{name}' found in db.", team[0]

        except Exception:
            return 500, f"an error occurred while fetching '{name}'", None