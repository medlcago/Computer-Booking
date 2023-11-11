import aiohttp


class BookingAPI:
    PATH = "bookings"

    def __init__(self, base_url: str, api_key: str):
        self.url = f"{base_url}/{self.PATH}"
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key
        }

    async def create_computer_booking(self, **data):
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self.url + "/", json=data, headers=self.headers) as response:
                if response.status == 201:
                    return await response.json()

    async def get_all_computer_bookings(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url + "/", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def get_computer_bookings_by_user_id(self, user_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(url=f"{self.url}/user/id{user_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()

    async def delete_computer_booking(self, booking_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.delete(url=f"{self.url}/id{booking_id}", headers=self.headers) as response:
                if response.status == 200:
                    return await response.json()
