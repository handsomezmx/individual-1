from flask import Flask
from flask import jsonify
app = Flask(__name__)

def change(amount):
    # calculate the resultant change and store the result (res)
    res = []
    coins = [1,5,10,25] # value of pennies, nickels, dimes, quarters
    coin_lookup = {25: "quarters", 10: "dimes", 5: "nickels", 1: "pennies"}

    # divide the amount*100 (the amount in cents) by a coin value
    # record the number of coins that evenly divide and the remainder
    coin = coins.pop()
    num, rem  = divmod(int(amount*100), coin)
    # append the coin type and number of coins that had no remainder
    res.append({num:coin_lookup[coin]})

    # while there is still some remainder, continue adding coins to the result
    while rem > 0:
        coin = coins.pop()
        num, rem = divmod(rem, coin)
        if num:
            if coin in coin_lookup:
                res.append({num:coin_lookup[coin]})
    return res

def paychange(pay,price):
    if pay<price:
        return False
    return change(pay-price)



@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print("I am inside hello world")
    return 'Hello World! I can make change at route: /change or /getchange'

@app.route('/change/<dollar>/<cents>')
def changeroute(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    result = change(float(amount))
    return jsonify(result)
    
    
@app.route('/100/change/<dollar>/<cents>')
def change100route(dollar, cents):
    print(f"Make Change for {dollar}.{cents}")
    amount = f"{dollar}.{cents}"
    amount100 = float(amount) * 100
    print(f"This is the {amount} X 100")
    result = change(amount100)
    return jsonify(result)

@app.route('/getchange/<price>/<paid>')
def getchangeroute(price, paid):
    print("Here is your change")
    fprice = float(price)
    fpaid = float(paid)
    print(f"Make Change for {fpaid-fprice}")
    amount = fpaid-fprice
    result = paychange(fpaid,fprice)
    if result == False:
        print("give more money")
        return "give more money"
    else:
        return jsonify(result)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
