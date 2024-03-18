import random

day_plurals = ["день", "дня", "дней"]
week_plurals = ["неделю", "недели", "недель"]
year_plurals = ["год", "года", "лет"]

emoji_list = ["🍾", "🥳", "🫡", "🎁", "🍻"]


def format_message(kotans):
    s = "🎂🎂🎂\n"
    for kotan in kotans:
        name = kotan.name
        age = kotan.age
        next_age = kotan.next_age
        days = kotan.days_until
        weeks = int(days / 7)

        if days == 0:
            emoji = random.choice(emoji_list)
            s += "%s - сегодня исполнилось %d %s %s\n" % (name, age, plural(age, year_plurals), emoji)
        elif days >= 14:
            s += "%s через %d %s\n" \
                 % (name, weeks, plural(weeks, week_plurals))
        else:
            s += "%s через %d %s\n" \
                 % (name, days, plural(days, day_plurals))
    return s


def plural(count, plurals):
    if count >= 20:
        count %= 10

    if count == 1:
        return plurals[0]
    elif 2 <= count <= 4:
        return plurals[1]
    else:
        return plurals[2]
