# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import httpx
from datetime import datetime


# ---------------------------------------------------------------------------- #
# --- Response Configuration ------------------------------------------------- #
# ---------------------------------------------------------------------------- #


alert = '\n⚡ PowerAlert ⚡\n'
base_url = 'http://localhost:8000'


def time_format(time: str) -> str:
    dt_obj = datetime.fromisoformat(time)
    return dt_obj.strftime('%Y/%m/%d - %H:%M')


def status(_: str) -> str:
    response = httpx.get(f"{base_url}/status")
    if response.status_code != 200:
        return f"{alert}Error occured: {response.json()['detail']}"
            
    response = response.json()
    cpt = response['capetown']
    eskom = response['eskom']
    r_message = alert
    r_message += f"Cape Town: Stage {cpt['stage']} (current)\n"
    r_message += "\tNext stages:\n"
    for next_stage in cpt['next_stages']:
        r_message += f"\t -> Stage: {next_stage['stage']}\t"
        r_message += f"{time_format(next_stage['stage_start_timestamp'])}\n"
    r_message += f"Last updated: {time_format(cpt['stage_updated'])}\n\n"

    r_message += f"Eskom: Stage {eskom['stage']} (current)\n"
    r_message += "\tNext stages:\n"
    for next_stage in eskom['next_stages']:
        r_message += f"\t -> Stage: {next_stage['stage']}\t"
        r_message += f"{time_format(next_stage['stage_start_timestamp'])}\n"
    r_message += f"Last updated: {time_format(eskom['stage_updated'])}\n\n"
    return r_message


def search():
    return None


def area():
    return None


class Responses():
    
    
    commands = {
        'status': status,
        'search': search,
        'area': area
    }

    def error(self, message: str) -> str:
        return f"{alert}{message}"

    def handle_response(self, command, message) -> str:

        if command not in self.commands:
            return f'{alert}Command "{command}" not found :('

        return self.commands[command](message)
    