import requests
import json
import click
from pyfiglet import Figlet
from clint.textui import colored, puts, indent

f = Figlet(font='slant')


@click.command()
@click.argument('num', type=float)
@click.argument('base')
@click.argument('symbols', default='')
def main(num, base, symbols):
    print(f.renderText("PyConverter"))

    num = num
    base = base.upper()
    symbols = symbols.upper()

    exchange_data = load_exchange_data(base)

    try:
        display(calc_rate(num, exchange_data, base, symbols), num, base)

    except Exception:
        print("That's not the easter egg you're looking for...")


def display(data, num, base):
    puts(f"{num} {base} = ")
    with indent(6, quote=" >"):
        for k, v in data.items():
            puts(f"{k}: {v}")


# calculate exchange
def calc_rate(num, exchange_data, base, symbols):
    rates = dict()

    # TOTALNIE NIE EASTER EGG
    if base != "PLN" and symbols == 'SASIN':
        raise Exception("NOT POSSIBLE")

    elif symbols == 'SASIN':
        n = num / 70000000
        rates[symbols] = "{:.20f}".format(n)

    elif symbols == '':

        for key, value in exchange_data['rates'].items():
            rates[key] = value * num

    else:
        rates[symbols] = exchange_data['rates'][symbols] * num

    return rates


# wczytanie / pobieranie danych
def load_exchange_data(base):
    try:
        with open(f"exchangedata_{base}.json", "r") as e_data:
            data = json.load(e_data)
            puts(colored.cyan(f"USING CACHED DATA ({data['date']})"))
            return data
    except IOError:
        return get_and_dump_rates(base)


# pobieranie i zapisanie danych
def get_and_dump_rates(base):
    puts(colored.cyan("REQUESTING FOR " + base))
    r = requests.get(
        f"https://api.exchangeratesapi.io/latest?base={ base }")

    with open(f"exchangedata_{base}.json", "w") as outfile:
        json.dump(r.json(), outfile)
        return r.json()


if __name__ == "__main__":
    main()
