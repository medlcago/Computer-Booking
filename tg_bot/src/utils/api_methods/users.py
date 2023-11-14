import aiohttp


class UserAPI:
    PATH = "users"

    def __init__(self, base_url: str, api_key: str):
        self.url = f"{base_url}/{self.PATH}"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key
        }

    async def create_user(self, **data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{self.url}/", json=data, headers=self.headers) as response:
                if response.status == 201:
                    return await response.json()

    async def update_user_details(self, *, user_id: int, **data):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f"{self.url}/id{user_id}", json=data, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_all_users(self, *,
                            is_admin: bool | None = None,
                            is_blocked: bool | None = None,
                            is_active: bool | None = None):
        params = {}
        if is_admin is not None:
            params["is_admin"] = is_admin

        if is_blocked is not None:
            params["is_blocked"] = is_blocked

        if is_active is not None:
            params["is_active"] = is_active

        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/", params=params, headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_user_by_id(self, *, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/id{user_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def change_user_password(self, *, user_id: int, **data):
        async with aiohttp.ClientSession() as session:
            async with session.patch(url=f"{self.url}/id{user_id}/password", json=data,
                                     headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def delete_user(self, *, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=f"{self.url}/id{user_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_user_by_id_with_full_information(self, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/id{user_id}/full", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
