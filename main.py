from menu import DRINKS

money_left = 0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def print_report():
    """
    :param: no input checking for 'report' occurs outside this function
    :return: returns report output
    """
    report_format = f"Water : {resources['water']}ml \n Milk : {resources['milk']}ml " \
                    f"\n Coffee : {resources['coffee']}g \n Money : ${money_left} "
    print(report_format)
    return


def is_resource_sufficient(drink):
    """
    :param: drink
    :return: returns whether resource is sufficient for a given drink order
    """
    is_sufficient = False
    insufficient_resource = []
    # TODO: Check if there's a more Pythonic way to check values in list of nested dictionaries
    if resources.get('water') >= DRINKS[drink].get('ingredients').get('water'):
        # espresso does not contain milk therefore, if validate whether milk key exists first
        if DRINKS[drink].get('ingredients').get('milk'):
            if resources.get('milk') >= DRINKS[drink].get('ingredients').get('milk'):
                if resources.get('coffee') >= DRINKS[drink].get('ingredients').get('coffee'):
                    print(f"There are sufficient ingredients to make {drink}")
                    is_sufficient = True
                else:
                    print("Sorry there is not enough coffee")
                    return is_sufficient
            else:
                print("Sorry there is not enough milk")
        # continue checking for coffee resource when drink does not require milk
        else:
            if resources.get('coffee') >= DRINKS[drink].get('ingredients').get('coffee'):
                print(f"There are sufficient ingredients to make {drink}")
                is_sufficient = True
            else:
                print("Sorry there is not enough coffee")
                return is_sufficient
    else:
        print("Sorry there is not enough water")
    return is_sufficient


def process_coins(price, amount_deposited, user_input):
    """
    function takes user's payment in denominations of $1, 50, 20 and 10 cents and amount deposited so far
    calculates if the price of drink is paid fully and
    :param drink selection
    :param amount_deposited:
    :param price: price of drink
    :return: change due to the customer

    """

    print(f"the cost of your drink is ${price}. You have currently paid {amount_deposited} please insert sufficient "
          f"change!")
    dollars = int(input("how many dollars? "))
    fifty_cent = int(input("how many fifty cents? ")) * 0.5
    twenty_cent = int(input("how many twenty cents? ")) * 0.2
    ten_cent = int(input("how many ten cents? ")) * 0.1
    total_paid = dollars + fifty_cent + twenty_cent + ten_cent

    if total_paid == price:
        change_to_return = total_paid - price
        print(f"you have given exact change of {total_paid}, no change is due to you.")
        make_coffee(user_input)
        print(f"{user_input} has been dispensed!")
        return change_to_return
    if total_paid > price:
        change_to_return = total_paid - price
        print(f"you have given {total_paid}, change of {change_to_return} is due to you.")
        make_coffee(user_input)
        print(f"{user_input} has been dispensed!")
        return change_to_return

    if total_paid < price:
        outstanding_amount = total_paid - price
        return outstanding_amount


def make_coffee(drink):
    """
    :param: drink: takes selected drink and updates resource remaining after making drink
    """
    global resources
    have_milk = False
    coffee_used = DRINKS[drink].get('ingredients').get('coffee')
    milk_used = 0
    if DRINKS[drink].get("ingredients").get('milk'):
        have_milk = True
        milk_used = DRINKS[drink].get('ingredients').get('milk')
    water_used = DRINKS[drink].get('ingredients').get('water')

    # update resources
    resources['water'] -= water_used
    if have_milk:
        resources['milk'] -= milk_used
    resources['coffee'] -= coffee_used

    return


def coffee_machine():
    is_on = True
    #   take user input
    #     drinks = list(DRINKS.keys())
    drinks = [key for key in DRINKS.keys()]
    is_sufficient = True
    while is_on and is_sufficient:
        user_input = input(f"What would you like? Our drinks menu offers {drinks} ")
        if user_input.lower() == 'off':
            is_on = False
            return
        if user_input.lower() == 'report':
            print_report()
            # return
        elif user_input.lower() in ['espresso', 'cappuccino', 'latte']:
            is_sufficient = is_resource_sufficient(user_input)
            # if sufficient resources ask for coins
            if is_sufficient:
                price = DRINKS[user_input.lower()].get('cost')
                amount_deposited = 0
                amount = process_coins(price, amount_deposited, user_input)
                while amount < 0:
                    continue_deposit = input(f"You still have to top up ${amount * -1} to purchase {user_input}. Type "
                                             f"'Y' if you wish to top up or 'N' if you don't wish to proceed with "
                                             f"your purchase: ")
                    amount_deposited = price + amount
                    if continue_deposit == 'Y':
                        amount = process_coins(price, amount_deposited, user_input)
                    else:
                        print(
                            f"You have decided not to continue buy the drink, change of {amount_deposited} has been "
                            f"refunded")
                        # return
                global money_left
                money_left += price
                # return
        else:
            print(f"{user_input} is not on the menu! Please try again")
            # return


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    coffee_machine()

