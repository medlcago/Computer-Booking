import aiohttp


class TicketAPI:
    PATH = "tickets"

    def __init__(self, base_url: str, api_key: str):
        self.url = f"{base_url}/{self.PATH}"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key
        }

    async def create_ticket(self, **data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{self.url}/", json=data, headers=self.headers) as response:
                if response.status == 201:
                    return await response.json()

    async def close_ticket(self, ticket_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f"{self.url}/id{ticket_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_all_tickets(self, ticket_status: str | None):
        params = {}
        if ticket_status is not None:
            params["ticket_status"] = ticket_status

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_user_tickets_by_user_id(self, user_id: int, ticket_status: str | None):
        params = {}
        if ticket_status is not None:
            params["ticket_status"] = ticket_status

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/user/id{user_id}", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
