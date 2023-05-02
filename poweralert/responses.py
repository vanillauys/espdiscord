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

def time_format_hrs(time: str) -> str:
    dt_obj = datetime.fromisoformat(time)
    return dt_obj.strftime('%H:%M (%A)')


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


    async def search(self, name: str) -> str:
        if name is None:
            return f"{alert}Error occured: incorrect arguments."
        code, message, result = await ESP.area_search(name)
        if code != 200:
            return f"{alert}Error occured: {message}"
        r_message = alert
        for area in result:
            r_message += f"🏠 {area['name']}\n"
            r_message += f"  id:\t\t  {area['id']}\n"
            r_message += f"  region:\t  {area['region']}\n\n"
        return r_message


    async def area(self, area_id: str) -> str:
        if area_id is None:
            return f"{alert}Error occured: incorrect arguments."
        code, message, result = await ESP.area_information(area_id)
        if code != 200:
            return f"{alert}Error occured: {message}"

        events = result["events"]
        info = result["info"]

        r_message = alert 
        r_message += f"🏠 {info['name']}: {info['region']}\n\n"

        r_message += "💡Events:\n\n"
        for event in events:
            r_message += f"{event['note']}\n"
            r_message += f"\t{time_format_hrs(event['start'])} - {time_format_hrs(event['end'])}\n"
        
        
        return r_message
    

    async def schedule(self, area_id: str) -> str:
        if area_id is None:
            return f"{alert}Error occured: incorrect arguments."
        code, message, result = await ESP.area_information(area_id)
        if code != 200:
            return f"{alert}Error occured: {message}"

        schedule = result["schedule"]
        r_message = alert
        r_message += f"📅 Schedule:\n\n"
        for index, item in enumerate(schedule['days']):
            if index < 4:
                r_message += f"💡{item['name']} - {item['date']}\n"
                for index, stages in enumerate(item['stages']):
                    if index != 0 and index < 7:
                        r_message += f"Stage {index}\n"
                        for stage in stages:
                            r_message += f"\t{stage}\n"
                        r_message += "\n"
        return r_message 


    async def quota(self) -> str:
        code, message, result = await ESP.quota()
        if code != 200:
            return f"{alert}Error occured: {message}"
        
        r_message = f"{alert}Used {result['allowance']['count']} of {result['allowance']['limit']} credits."
        return r_message
        
