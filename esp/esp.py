# ---------------------------------------------------------------------------- #
# --- Imports ---------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


import httpx
import asyncio
import os
from dotenv import load_dotenv
from typing import Tuple


# ---------------------------------------------------------------------------- #
# --- ESP Configuration ------------------------------------------------------ #
# ---------------------------------------------------------------------------- #


load_dotenv()
LISCENCE_KEY = os.getenv('LISCENCE_KEY')
base_url = "https://developer.sepush.co.za/business/2.0"
headers = {'token': LISCENCE_KEY}


# ---------------------------------------------------------------------------- #
# --- ESP API Requests ------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


async def status() -> Tuple[int, str, dict]:
    url = f"{base_url}/status"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    if response.status_code != 200:
        return (response.status_code, response.json()['error'], None)
    else:
        return (
            response.status_code,
            "Successfully retrieved status from esp.",
            response.json()['status']
            )


async def area_search(name: str) -> Tuple[int, str, dict]:
    url = f"{base_url}/areas_search"
    params = {'text': name}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return (response.status_code, response.json()['error'], None)
    else:
        return (
            response.status_code,
            "Successfully retrieved search results from esp.",
            response.json()['areas']
            )


async def area_information(area_id: str) -> Tuple[int, str, dict]:
    url = f"{base_url}/area"
    params = {'id': area_id, 'test': 'current'}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code != 200:
        return (response.status_code, response.json()['error'], None)
    else:
        return (
            response.status_code,
            "Successfully retrieved area information from esp.",
            response.json()
            )

# ---------------------------------------------------------------------------- #
# --- Main ------------------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


async def main():
    # Nothing to do here
    pass


if __name__ == "__main__":
    asyncio.run(main())
