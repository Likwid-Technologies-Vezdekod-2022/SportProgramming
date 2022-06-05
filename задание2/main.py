shelf_incomes: list = []
days: list = []
income: int = 0


def get_max_shelf_income():
    max_income = 0
    max_item: dict
    for shelf_item in shelf_incomes:
        if shelf_item['price'] * shelf_item['count'] > max_income:
            max_income = shelf_item['price'] * shelf_item['count']
            max_item = shelf_item

    return max_item


with open('input.txt', 'r', encoding='utf-8') as f:
    anime_list: list[tuple] = []

    n = int(f.readline())

    for number, day in enumerate(f.readlines()):
        released, demand, price = day.strip().split()
        days.append({'released': int(released), 'demand': int(demand), 'price': int(price)})

for day in days:

    if shelf_incomes:
        shelf_today_max_income = get_max_shelf_income()
    else:
        shelf_today_max_income = 0

    demand = day['demand']
    released = day['released']

    if released < demand:

        if shelf_today_max_income:
            if shelf_today_max_income['price'] > day['price']:

                if shelf_today_max_income['count'] < released:
                    count = shelf_today_max_income['count']

                    remaining_to_sell_count = demand - shelf_today_max_income['count']
                    income += remaining_to_sell_count * day['price']

                    remaining_to_shelf = released - remaining_to_sell_count
                    shelf_incomes.append({'price': day['price'], 'count': remaining_to_shelf})

                else:
                    count = released

                income += shelf_today_max_income['price'] * count

                shelf_incomes.remove(shelf_today_max_income)

                remaining_from_max = shelf_today_max_income['price'] * shelf_today_max_income['count'] - \
                                     shelf_today_max_income[
                                         'price'] * count

                if remaining_from_max != 0:
                    shelf_incomes.append({'price': shelf_today_max_income['price'], 'count': remaining_from_max})

        else:
            income += released * day['price']

    elif released > demand:
        if shelf_today_max_income:
            if shelf_today_max_income['count'] < released:
                if shelf_today_max_income['price'] > day['price']:
                    shelved_count = shelf_today_max_income['count']
                    if shelved_count < demand:
                        income += day['price'] * (demand - shelved_count)

                    income += shelved_count * shelf_today_max_income['price']

                    shelf_incomes.remove(shelf_today_max_income)

            elif shelf_today_max_income['count'] == released:
                income += shelf_today_max_income['count'] * shelf_today_max_income['price']

                shelf_incomes.remove(shelf_today_max_income)
                shelf_incomes.append({'count': released, 'price': day['price']})

            elif shelf_today_max_income['count'] > released:
                if shelf_today_max_income['price'] > day['price']:
                    income += demand * shelf_today_max_income['count']
                    remaining_to_shelf = shelf_today_max_income['count'] - demand

                    shelf_incomes.remove(shelf_today_max_income)
                    shelf_incomes.append({'count': remaining_to_shelf, 'price': shelf_today_max_income['price']})

        else:
            shelf_incomes.append({'count': released - demand, 'price': day['price']})
            income += demand * day['price']

print(income)
