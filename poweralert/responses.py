# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


from datetime import datetime
from esp import esp


# ---------------------------------------------------------------------------- #
# --- Response Configuration ------------------------------------------------- #
# ---------------------------------------------------------------------------- #


alert = '\n⚡ PowerAlert ⚡\n'
ESP = esp.ESP()


def time_format(time: str) -> str:
    dt_obj = datetime.fromisoformat(time)
    return dt_obj.strftime('%Y/%m/%d - %H:%M')


# ---------------------------------------------------------------------------- #
# --- Response Class --------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class Responses():
   
    async def status(self) -> str:
        code, message, result = await ESP.status()
        if code != 200:
            return f"{alert}Error occured: {message}"
                
        cpt = result['capetown']
        eskom = result['eskom']
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
        # Todo search for area in ESP
        return None


    def area():
        # Todo show area details from ESP
        return None
    