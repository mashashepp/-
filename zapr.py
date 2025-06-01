import requests
import json
import asyncio
import aiohttp


class Zapros:
    def __init__(self, url, token):
        self.__url = url
        self.__headers = {"Authorization": token}
        self.__async_session = None

    def __zapros_sync(self, endpoint: str) -> dict | None:
        all_url = self.__url + endpoint
        try:
            t = requests.get(all_url, headers=self.__headers)
            t.raise_for_status()
            return t.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Ошибка авторизации")
            else:
                print("Ошибка запроса")
        except requests.exceptions.RequestException:
            print("Ошибка запроса")
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON")
        return None

    async def __get_async_session(self):
        if self.__async_session is None:
            self.__async_session = aiohttp.ClientSession()
        return self.__async_session

    async def close_session(self):
        if self.__async_session:
            await self.__async_session.close()
            self.__async_session = None

    async def players_id_zapros(self, id: int) -> dict | None:
        session = await self.__get_async_session()
        all_url = self.__url + '/players/' + str(id)
        try:
            async with session.get(all_url, headers=self.__headers) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Сетевая ошибка: {e}")
        except asyncio.TimeoutError:
            print(f"Таймаут запроса")
        except json.JSONDecodeError as e:
            print(f"Ошибка декодирования JSON: {e}")
        except Exception as e:
            print(f"Ошибка: {e}")
        return None


    def matches_zapros(self):
        return self.__zapros_sync('/matches')

    def teams_zapros(self):
        return self.__zapros_sync('/teams')

    def team_id_zapros(self, id:int):
        i = str(id)
        return self.__zapros_sync('/teams/' + i)