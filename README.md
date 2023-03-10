# Бот парсинга
Бот каждый час парсит страницу https://codeforces.com/problemset/page/1?order=BY_SOLVED_DESC
и выгружает задачи в БД

##### Команды:
/start - инициация бота

/search - поиск по имени задачи


###СТЕК: 
* Python3.7
* PostgreSQL
* asyncio
* Aiogram
* AioHttp
