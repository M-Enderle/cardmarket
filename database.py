from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd

set_names = pd.read_csv("set_names.csv")

engine = create_engine('sqlite:///database.db', echo=False, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Card(Base):

    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)
    set_code = Column(String)
    set_name = Column(String)
    set_short = Column(String)
    to_buy = Column(Integer)
    available_sets = Column(String)

    offers = relationship("Offer", back_populates="card")

    def __init__(self, name, url, set_short, set_code, set_name, to_buy, sets):
        self.name = str(name)
        self.url = str(url)
        self.set_short = str(set_short)
        self.set_code = str(set_code)
        self.set_name = str(set_name)
        self.to_buy = to_buy
        self.sets = sets

    def __repr__(self):
        return self.name

    def get_offers(self, seller_country="7", min_condition="4", languages=None):

        if languages is None:
            languages = ["1"]

        session = Session()

        offers = session.query(Offer).filter_by(card_id=self.id).all()

        for offer in offers:
            session.delete(offer)
        session.commit()

        url_addition = f"?sellerCountry={seller_country}&language={','.join([str(x) for x in languages])}&amount={self.to_buy}"
        
        if self.sets:
            sets = ",".join([str(x) for x in self.sets])
            url_addition += f"&idExpansion=={sets}"

        if min_condition:
            url_addition += f"&minCondition={min_condition}"

        r = requests.get(self.url + url_addition)
        soup = BeautifulSoup(r.text, "html.parser")

        table = soup.find("div", class_="table article-table table-striped")

        # all offers are class "row no-gutters article-row"
        offers = table.find_all("div", class_="row no-gutters article-row")

        # find the sellers
        seller_urls = [offer.find("span", class_="d-flex has-content-centered mr-1").find("a")["href"] for offer in offers]
        seller_names = [offer.find("span", class_="d-flex has-content-centered mr-1").find("a").text for offer in offers]

        # insert all sellers into the database if not already there
        for i in range(len(seller_urls)):
            if not session.query(Seller).filter_by(url=seller_urls[i]).first():
                session.add(Seller(seller_names[i], seller_urls[i]))
                session.commit()

        # get the seller ids
        seller_ids = [session.query(Seller).filter_by(url=seller_urls[i]).first().id for i in range(len(seller_urls))]

        # get the price in span "font-weight-bold color-primary small text-right text-nowrap"
        prices = [offer.find("span", class_="font-weight-bold color-primary small text-right text-nowrap").text for offer in offers]

        # convert from 0,09 € to floatr
        prices = [float(price.replace(",", ".").replace(" €", "")) for price in prices]
        
        # get the cheapest offer
        cheapest = min(prices)

        # insert all offers into the database
        for i in range(len(seller_ids)):

            # filter out the offers that are more than 1.75€ more expensive than the cheapest
            if prices[i] > cheapest + 1.75:
                continue

            # filter out the offers that exist already
            if not session.query(Offer).filter_by(card_id=self.id, seller_id=seller_ids[i]).first():
                session.add(Offer(self.id, seller_ids[i], prices[i]))
                session.commit()

        session.close()

    @property
    def sets(self):
        return pickle.loads(self.available_sets)

    @sets.setter
    def sets(self, value):
        self.available_sets = pickle.dumps(value)

    @property
    def short_setnames(self):
        return [set_names[set_names["set_code"] == int(x)]["short"].values[0] for x in self.sets]

    # make a setter
    @short_setnames.setter
    def short_setnames(self, value):
        self.sets = [set_names[set_names["short"] == x]["set_code"].values[0] for x in value]

class Seller(Base):

    __tablename__ = 'sellers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    url = Column(String)

    offers = relationship("Offer", back_populates="seller")
    
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def __repr__(self):
        return self.name

class Offer(Base):

    __tablename__ = 'offers'

    card_id = Column(Integer, ForeignKey('cards.id'), primary_key=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), primary_key=True)
    price = Column(String)

    card = relationship("Card", back_populates="offers")
    seller = relationship("Seller", back_populates="offers")
    
    def __init__(self, card_id, seller_id, price):
        self.card_id = card_id
        self.seller_id = seller_id
        self.price = price

    def __repr__(self):
        return f"{self.seller_id} - {self.price}"

Base.metadata.create_all(engine)