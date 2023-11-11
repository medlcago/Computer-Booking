import aiohttp


class ComputerAPI:
    PATH = "computers"

    def __init__(self, base_url: str, api_key: str):
        self.url = f"{base_url}/{self.PATH}"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key
        }

    async def add_new_computer(self, **data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url + "/", json=data, headers=self.headers) as response:
                if response.status == 201:
                    return await response.json()

    async def get_computer_by_id(self, computer_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/id{computer_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_computers_by_category(self, category: str, is_reserved: bool | None = None):
        params = {}
        if is_reserved is not None:
            params["is_reserved"] = int(bool(is_reserved))

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/{category}", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_all_computers(self, is_reserved: bool | None = None):
        params = {}
        if is_reserved is not None:
            params["is_reserved"] = int(bool(is_reserved))

        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url + "/", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def update_computer_components(self, computer_id: int, **data):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f"{self.url}/id{computer_id}", json=data, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def delete_computer(self, computer_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=f"{self.url}/id{computer_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
