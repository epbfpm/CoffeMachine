import os
import data
import math
from art import title
from sys import exit


def clear():
    """It was supposed to clear the screen, but doesn't work"""
    return os.system('cls' if os.name == 'nt' else 'clear')


def end():
    done = input('Insert "y" to restart: ')
    if done == 'y':
        clear()
        coffee_machine()


def check_choice(user_choice):
    """Checks whether te user's choice is one of the maintenance ones and returns them"""
    if user_choice == 'off':
        exit()
    elif user_choice == 'report':
        print(f'''
        Water: {data.resources['water']} ml
        Milk: {data.resources['milk']} ml
        Coffee: {data.resources['coffee']} ml
        Money: ${data.resources['money']}
        ''')
        done = input('Insert "y" to restart: ')
        if done == 'y':
            coffee_machine()
    else:
        return True


def check_resources(user_choice):
    """Checks whether there are enough resources to complete
    the order and returns warnings if it does not"""
    maintenance = False
    if 'water' in data.MENU[user_choice]['ingredients']:
        if data.MENU[user_choice]['ingredients']['water'] > data.resources['water']:
            maintenance = True
            print('Sorry there is not enough water.')
    if 'milk' in data.MENU[user_choice]['ingredients']:
        if data.MENU[user_choice]['ingredients']['milk'] > data.resources['milk']:
            print('Sorry there is not enough milk.')
            maintenance = True
    if 'coffee' in data.MENU[user_choice]['ingredients']:
        if data.MENU[user_choice]['ingredients']['coffee'] > data.resources['coffee']:
            print('Sorry there is not enough coffee.')
            maintenance = True
    if not maintenance:
        return True


def check_coin_is_num(user_choice, coins):
    """Checks whether the amount of coins inserted is a
    number ad returns the total amount inserted"""
    price = data.MENU[user_choice]["cost"]
    while True:
        try:
            if check_resources:
                coins += 0.25 * int(input('How many quarters?: '))
                if coins < price:
                    coins += 0.10 * int(input('How many dimes?: '))
                    if coins < price:
                        coins += 0.5 * int(input('How many nickles?: '))
                        if coins < price:
                            coins += 0.1 * int(input('How many pennies?: '))
                return coins
        except ValueError:
            print('Please enter only numbers')


def check_coins(user_choice):
    """Checks whether the amount inserted is enough to make the transaction"""
    print(f'The price is of a {user_choice} is ${data.MENU[user_choice]["cost"]}. Insert the coins.')
    price = data.MENU[user_choice]["cost"]
    right_amount = True
    coins = 0
    while right_amount:
        coins = check_coin_is_num(user_choice, coins)
        if coins == price:
            print('The amount inserted is correct.')
            right_amount = False
        elif coins > price:
            print(f'You\'ve inserted ${coins}. Here is ${math.ceil(coins - price)} dollars in change.')
            right_amount = False
            coins = price
        else:
            print(f'You\'ve inserted ${coins}. Insert the remaining amount of ${price - coins}')


def coffee_machine():
    check = True
    while check:
        choice = input(title)
        if choice not in data.MENU:
            check = True
        else:
            choice_pass = check_choice(choice)
            if choice_pass:
                resources_pass = check_resources(choice)
                if resources_pass:
                    check_coins(choice)
                    if 'water' in data.MENU[choice]['ingredients']:
                        data.resources['water'] -= data.MENU[choice]['ingredients']['water']
                    if 'milk' in data.MENU[choice]['ingredients']:
                        data.resources['milk'] -= data.MENU[choice]['ingredients']['milk']
                    if 'coffee' in data.MENU[choice]['ingredients']:
                        data.resources['coffee'] -= data.MENU[choice]['ingredients']['coffee']
                    data.resources['money'] += data.MENU[choice]['cost']
                    print(f'Here is your {choice}. Enjoy!')
                    end()
                else:
                    print('Please alert staff.')
                    end()
            else:
                end()


coffee_machine()

