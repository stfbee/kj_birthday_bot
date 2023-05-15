# Скрипт для непропускания дней рождений

Проходит по гугл таблицам, выбирает берет оттуда даты рождения. Считает, сравнивает, гудит, пердит. Постит сообщение в чят телеги (в дефолтный канал, если у вас топики)

## Примеры
Например у нас есть таблица
|   | A      | B          |
|---|--------|------------|
| 1 | чуви 1 | 06.06.1986 |
| 2 | чуви 2 | 31.05.1989 |
| 3 | чуви 3 |            |
| 4 | чуви 4 | 15.02.1990 |

По ней скрипт запостит в чятег такое сообщение:
```
🔥🔥🔥
чуви 2 - 34 года чере 17 дней
чуви 1 - 37 лет через 23 дня 
```
Список будет отсортирован по ближнему др, пустые значения проигнорируются, др через 60+ дней тоже.

## Переменные окружения

### GOOGLE_TOKEN_JSON `*`
`{"type":"service_account","pr...`

Идите в [дашборд гугл клауда](https://console.cloud.google.com/apis/dashboard), создавайте там проект, потом с разделе [Сredentials](https://console.cloud.google.com/apis/credentials) создавайте тестовый аккаунт и качайте json с токеном. Его содержимое и надо впихнуть в переменную.

### SPREADSHEET_ID `*`
`1ST6x0NTgzsy12OEWkxa5XwzsqPhXzI1K_vZg4AEiKtE`

Айдишник вашего гугл дока, написан в адресной строке. Повезет, если он у вас (полу-)публичный, иначе ⚰️⚰️🪦🏳️‍🌈, ищите сами инфу, мб поможет добавить сервисный аккаунт в документ.

### RANGE_NAME
`'Лист1'!A1:B20`

Тут все просто - область, в которых лежат данные имя-дата рождения. Возможно придется подправить код, чтобы оно более гибко билось, там сейчас берется первый и третий столбец (потому что у меня такие данные).

### TG_BOT_TOKEN `*`
`1012885859:AAGxOfgTavh0mlwE1lyzdLMxAbuXRbhxY42`

Брать в [@BotFather](https://t.me/BotFather). Бота добавить в чат, никаких дополнительных разрешений ему давать не надо.

### TG_CHAT_ID
`-1001510955421`

Как получить айдишник чата быстро - я хз, получал через дебаггер бота. Возможно, поможет [эта статья](https://www.alphr.com/find-chat-id-telegram/)

`*` - Секретные переменные