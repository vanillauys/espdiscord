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


# ---------------------------------------------------------------------------- #
# --- ESP API Requests ------------------------------------------------------- #
# ---------------------------------------------------------------------------- #


class ESP():

    LISCENCE_KEY = os.getenv('LISCENCE_KEY')
    base_url = "https://developer.sepush.co.za/business/2.0"
    headers = {'token': LISCENCE_KEY}

    async def status(self) -> Tuple[int, str, dict]:
        url = f"{self.base_url}/status"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

        if response.status_code != 200:
            return (response.status_code, response.json()['error'], None)
        else:
            return (
                response.status_code,
                "Successfully retrieved status from esp.",
                response.json()['status']
                )


    async def area_search(self, name: str) -> Tuple[int, str, dict]:
        url = f"{self.base_url}/areas_search"
        params = {'text': name}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            return (response.status_code, response.json()['error'], None)
        else:
            return (
                response.status_code,
                "Successfully retrieved search results from esp.",
                response.json()['areas']
                )


    async def area_information(self, area_id: str) -> Tuple[int, str, dict]:
        url = f"{self.base_url}/area"
        params = {'id': area_id, 'test': 'current'}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            return (response.status_code, response.json()['error'], None)
        else:
            return (
                response.status_code,
                "Successfully retrieved area information from esp.",
                response.json()
                )
    

    async def quota(self) -> Tuple[int, str, dict]:
        url = f"{self.base_url}/api_allowance"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

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
