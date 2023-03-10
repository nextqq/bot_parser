from bs4 import BeautifulSoup
import traceback
import logging
import asyncio
import aiohttp

logger = logging.getLogger()


async def parse_tr(row: BeautifulSoup) -> (dict, list):
    all_td = row.find_all('td')
    midl_column = all_td[1].find_all('div')

    result = {
        'id': all_td[0].find('a').text.strip(),
        'name': midl_column[0].find('a').text.strip(),
    }

    try:
        types_task = [
            {
                'task_id': all_td[0].find('a').text.strip(),
                'name': item.text.strip(),
            } for item in midl_column[1].find_all('a')]
    except Exception:
        types_task = []

    try:
        result['difficulty'] = int(all_td[3].find('span').text.strip())
    except Exception:
        result['difficulty'] = 0

    try:
        result['answer_count'] = int((all_td[4].find('a').text.strip().replace('x', '')))
    except Exception:
        result['answer_count'] = 0

    return result, types_task


class ParserTable:

    def __init__(self, url: str, firs_page: int = 1):
        self.types_list = []
        self.tasks_list = []
        self.url = url
        self.firs_page = firs_page

    @classmethod
    async def _get_page_text(cls, session: aiohttp.ClientSession, method: str, url: str):
        async with session.request(
                method=method,
                url=url,
                headers={'accept-language': 'ru'}

        ) as resp:
            assert resp.status == 200, logger.error(f'Status code: {resp.status}  || {resp}')
            return await resp.text()

    async def _get_number_last_page(self):
        async with aiohttp.ClientSession() as session:
            page = await self._get_page_text(session, method="GET", url=self.url.format(self.firs_page))
        soup_page = BeautifulSoup(page, "lxml")
        page_num = int(soup_page.find('div', class_='pagination').find_all('li')[-2].find('span').get('pageindex'))
        return page_num + 1

    async def parse_pages(self):
        last_page = await self._get_number_last_page()
        async with aiohttp.ClientSession() as session:
            for page in range(self.firs_page, last_page):
                page = await self._get_page_text(session=session, method='GET', url=self.url.format(page))
                soup_page = BeautifulSoup(page, "lxml")
                rows = soup_page.find('table', class_='problems').find_all('tr')[1:]
                dict_rows = []
                types_rows = []
                for item in rows:
                    tasks_dict, types_tasks_list = await parse_tr(item)
                    dict_rows.append(tasks_dict)
                    types_rows += types_tasks_list

                self.tasks_list += dict_rows
                self.types_list += types_rows
