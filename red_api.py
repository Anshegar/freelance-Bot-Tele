import praw

# Redit API

client_id = '...'
# secret(секрет)
client_secret = '...'
# APP Name(необчзательно что бы совпадало с созданым app, но для исключение внеапных ошибко лучше чтоб совпадало)
user_agent = '...'
# user name (логин в reddit)
username = '...'
# user pass
password =  '...'



# Создание СРЕДЫ reddit через OAUth reddit
# Заносим выше описаные данные в настройки praw ( для подключения к reddit API) - https://praw.readthedocs.io/en/latest/getting_started/authentication.html
# Дополнительно: Что бы НЕПАЛИТЬ данные можно их создать в виде словаря user_values в другом файле и ипортировать этот словарь писать client_id = user_values['client_id']
# user_values ={'client_id':'rpExt0XMdxyUKw', 'client_secret':'QtriQIRPqj819ZmuWaKHk1zU-kA', 'user_agent':'SC_Sentimental', 'username':'Redit_for_work', 'password':'19840812' }
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     username = username,
                     password = password,
                     user_agent = user_agent
                     )

# Для проверки правильности ввода данных в praw
#print(reddit.user.me())

# !!! ВАЖНО !!! - Иногда МЕТОДЫ СРЕДЫ praw.Reddit , не подставляются к обычной переменной поэтому можно создать функцию ( да и вообще через функции лучше всего делать, ибо красивей)
# Функция для создания  Reddit ОБЪЕКТА, потом допищшу ибо нихуя не понятно как эти сраные словари имплементирвоать в код!!!!
def create_reddit_object():
    reddit_def = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent
                         )
    return reddit_def
