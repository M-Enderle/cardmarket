import requests
import time
import bs4
from database import Card, Offer, Session

def get_url(name):

    url = "https://www.cardmarket.com/de/Magic/Cards/{}".format(name.replace(" ", "-").replace(",", "").replace("'", ""))
    r = requests.get(url)

    if r.status_code == 200:
        if "Invalid product!" in r.text:
            return None, []
        else:
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            div = soup.find("div", {"id": "articleFilterProductExpansion"})
            inputs = div.find_all("input")
            sets = [input["value"] for input in inputs]
            return url, sets

    else:
        if r.status_code == 404:
            return None, []
        elif r.status_code == 429:
            time.sleep(10)
            return get_url(name)
        else:
            return None, []

def generate_cart():

    session = Session()

    cards = session.query(Card).all()
    offers = session.query(Offer).all()

    def get_sellers_stock(remaining_cards):
        sellers = {}
        for card in remaining_cards:
            for offer in card.offers:
                if offer.seller not in sellers:
                    sellers[offer.seller] = []
                sellers[offer.seller].append(offer)
        sellers = {k: v for k, v in sorted(sellers.items(), key=lambda item: len(item[1]), reverse=True)}
        return sellers

    cart = {}
    remaining_cards = cards.copy()

    while True:
        # get the sellers with the most stock
        sellers = get_sellers_stock(remaining_cards)
        # get the seller with the most stock
        seller = list(sellers.keys())[0]
        # get the offers of the seller
        offers = sellers[seller]
        cart[seller] = []
        # add all offers to the cart
        for offer in offers:
            cart[seller].append(offer)
            remaining_cards.remove(offer.card)
        # if there are no more cards left, break
        if len(remaining_cards) == 0:
            break

    for _ in range(10):
        for seller in cart:
            for offer in cart[seller]:
                card = offer.card
                card_replaced = False
                for other_seller in cart:
                    if card_replaced:
                        break
                    if other_seller == seller:
                        continue
                    for other_offer in other_seller.offers:
                        if other_offer.card == card:
                            if float(other_offer.price) < float(offer.price):
                                cart[seller].remove(offer)
                                cart[other_seller].append(other_offer)
                                card_replaced = True
                                break

    return cart

def compared_cart():
    cart_cheapest_offer = {}
    session = Session()
    cards = session.query(Card).all()

    for card in cards:
        cheapest_offer = None
        for offer in card.offers:
            if cheapest_offer == None:
                cheapest_offer = offer
            elif float(offer.price) < float(cheapest_offer.price):
                cheapest_offer = offer
        if cheapest_offer.seller not in cart_cheapest_offer:
            cart_cheapest_offer[cheapest_offer.seller] = []
        cart_cheapest_offer[cheapest_offer.seller].append(cheapest_offer)

    return cart_cheapest_offer