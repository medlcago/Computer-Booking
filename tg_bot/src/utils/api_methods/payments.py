import aiohttp


class PaymentAPI:
    PATH = "payments"

    def __init__(self, base_url: str, api_key: str):
        self.url = f"{base_url}/{self.PATH}"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key
        }

    async def create_payment(self, **data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=f"{self.url}/", json=data, headers=self.headers) as response:
                if response.status == 201:
                    return await response.json()

    async def get_user_payments(self, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/user/id{user_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
