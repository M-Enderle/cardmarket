import streamlit as st
import pandas as pd
from database import Card, Seller, Offer, Session
from streamlitHelpers import get_url, generate_cart, compared_cart

set_names = pd.read_csv("set_names.csv")

# set to full page width
st.set_page_config(layout="wide")

# title
st.title("MKM Helper")
st.sidebar.title("Steps")

# make a button to clear session state on the sidebar
if st.sidebar.button("Clear session state"):

    # delete all contents of the database
    session = Session()
    session.query(Card).delete()
    session.query(Seller).delete()
    session.query(Offer).delete()
    session.commit()

    st.session_state.clear()

step = st.sidebar.radio("Steps", ["Upload data", "Retrieve cards", "Validate cards", "Get offers", "Stats", "Generate cart", "Support me"], label_visibility="hidden")

# upload file
if step == "Upload data":

    if not st.session_state.get("decklist_plain", None):
        session = Session()
        session.query(Card).delete()
        session.query(Seller).delete()
        session.query(Offer).delete()
        session.commit()

    st.markdown("# ")
    st.markdown("In this step, you can upload a file or paste a decklist exported from tappedout.net. The programm will then retrieve all cards from the decklist and search them on MKM.")
    st.markdown("# ")

    # ask the user to upload a txt file
    uploaded_file = st.file_uploader("Upload the decklist exported from tappedout", type="txt")

    st.markdown("## OR")

    # or make a text field very big to paste the decklist
    decklist = st.text_area("Paste the decklist exported from tappedout", height=500)

    # if the user uploaded a file, show a success message
    if uploaded_file is not None:
        st.success("File uploaded successfully")
        st.session_state.decklist_plain = uploaded_file.read().decode("utf-8")
        st.sidebar.success("File uploaded successfully")

    if decklist:
        st.success("Decklist pasted successfully")
        st.session_state.decklist_plain = decklist

if step == "Retrieve cards":

    session = Session()

    if not st.session_state.get("decklist_plain", None):
        st.error("Please upload a file or paste a decklist first")
        st.stop()

    st.markdown("# ")
    st.markdown("In this step, the programm will retrieve all cards from the decklist and search them on MKM.")
    st.markdown("# ")
    st.markdown("Retrieving cards...")

    # create a progress bar
    progress_bar = st.progress(0)

    st.markdown("# ")
    st.markdown("Log:")

    file_contents = st.session_state.decklist_plain

    lines = [line for line in file_contents.split("\n") if line != ""]
    st.markdown(f"Found {len(lines)} cards")

    for i, line in enumerate(lines):
        amount = int(line.split(" ", 1)[0])
        name = line.split(" ", 1)[1].split(" (", 1)[0]
        set_short = line.split(" (", 1)[1].split(") ", 1)[0]

        # check if the card exists in the database
        if session.query(Card).filter(Card.name == name, Card.set_short == set_short).first():
            progress_bar.progress((i+1)/len(lines))
            continue

        if set_short in set_names["short"].values:
            set_name = set_names[set_names["short"] == set_short]["set_name_eng"].values[0]
            set_code = set_names[set_names["short"] == set_short]["set_code"].values[0]
        else:
            set_name = None
            set_code = None

        url, sets = get_url(name)
        if not url:
            st.markdown(f"Warning: Could not find card '{name}' on MKM. You will be asked in the next step to enter the URL manually.")

        card = Card(name=name, set_short=set_short, set_name=set_name, set_code=set_code, url=url, to_buy=amount, sets=sets)
        session.add(card)
        session.commit()

        progress_bar.progress((i+1)/len(lines))

    session.close()
    st.success("Retrieved all cards successfully")
        
if step == "Validate cards":

    # for each card make a new section
    # in the section, show the card name, the set, the amount, the url, the sets
    # if the url is not set, make a text field to enter the url

    if not st.session_state.get("decklist_plain", None):
        st.error("Please upload a file or paste a decklist first")
        st.stop()

    session = Session()

    cards = session.query(Card).all()

    if not cards:
        st.error("Please retrieve the cards first")
        st.stop()
    
    st.markdown("# ")
    st.markdown("In this step, you can validate the cards and enter the URL if it was not found automatically.")
    st.markdown("# ")

    for card in cards:
        cols = st.columns((1, 2, 5, 5, 0.75))
        card.amount = cols[0].number_input("Amount_" + str(card.id), value=card.to_buy, min_value=0, step=1, label_visibility="hidden", )
        card.name = cols[1].text_input("Name_" + str(card.id), value=card.name, label_visibility="hidden")
        card.url = cols[2].text_input("URL_" + str(card.id), value=card.url, label_visibility="hidden")
        card.short_setnames = cols[3].multiselect("Sets_" + str(card.id), options=card.short_setnames, default=card.short_setnames, label_visibility="hidden")

        # save button
        cols[4].markdown("## ")
        if cols[4].button("Save", key=str(card.id) + "_save"):
            session.commit()
            st.success("Saved changes")

if step == "Get offers":

    # check if all cards have a url
    # if not, show an error message

    if not st.session_state.get("decklist_plain", None):
        st.error("Please upload a file or paste a decklist first")
        st.stop()

    session = Session()

    cards = session.query(Card).all()

    if not cards:
        st.error("Please retrieve the cards first")
        st.stop()

    if not all([card.url for card in cards]):
        st.error("Please validate all cards first and enter the URL if it was not found automatically")
        st.stop()

    st.markdown("# ")
    st.markdown("In this step, the programm will retrieve all offers for the cards. You may select some options to filter the offers first.")

    st.markdown("# ")
    st.markdown("### Options")

    cols = st.columns((1,1,1,1,1))

    # multiselect for languages
    languages = cols[0].multiselect("Languages", options=["German", "English"], default=["German", "English"])

    # dropdown for min condition, poor, played, light played, moderate played, near mint, mint
    min_condition = cols[1].selectbox("Min condition", options=["Poor", "Played", "Light played", "Good", "Excellent", "Near mint", "Mint"], index=0)

    # dropdown for sellers country only germany right now
    sellers_country = cols[2].selectbox("Sellers country", options=["Germany"], index=0)

    st.markdown("# ")
    # make a very wide button to start the process
    if st.button("Get offers"):
        st.markdown("# ")
        st.markdown("Retrieving offers...")

        # create a progress bar
        progress_bar = st.progress(0)

        st.markdown("# ")
        st.markdown("Log:")

        languages_dict = {"German": "3", "English": "1"}
        languages_list = [languages_dict[language] for language in languages]

        min_condition_dict = {"Poor": None, "Played": "6", "Light played": "5", "Good": "4", "Excellent": "3", "Near mint": "2", "Mint": "1"}
        min_condition_ = min_condition_dict[min_condition]

        sellers_country_dict = {"Germany": "7"}
        sellers_country_ = sellers_country_dict[sellers_country]

        for i, card in enumerate(cards):

            # get the offers for the card
            offers = card.get_offers(seller_country=sellers_country_, min_condition=min_condition_, languages=languages_list)

            session.commit()

            progress_bar.progress((i+1)/len(cards))

        st.success("Retrieved all offers successfully")

if step == "Stats":

    if not st.session_state.get("decklist_plain", None):
        st.error("Please upload a file or paste a decklist first")
        st.stop()

    session = Session()

    cards = session.query(Card).all()

    if not cards:
        st.error("Please retrieve the cards first")
        st.stop()

    if not all([card.url for card in cards]):
        st.error("Please validate all cards first and enter the URL if it was not found automatically")
        st.stop()

    if not all([card.offers for card in cards]):
        st.error("Please get the offers first")
        st.stop()

    # make a plotly chart with the top 20 sellers with the most offers

    st.markdown("# ")
    st.markdown("In this step, you can see some statistics about the offers.")

    sellers = session.query(Seller).all()

    st.markdown("# ")
    st.markdown("### Top 20 sellers with the most offers for the cards you want to buy")

    import seaborn as sns
    import matplotlib.pyplot as plt

    sns.set_theme(style="whitegrid")
    # make background transparent and remove borders
    sns.set_theme(rc={'axes.facecolor':'none', 'figure.facecolor':'none', 'xtick.color':'white', 
    'ytick.color':'white', 'text.color':'white', 'axes.labelcolor':'white', 'axes.edgecolor':'white', 
    'axes.grid':False, 'axes.spines.left':False, 'axes.spines.bottom':False, 'axes.spines.right':False, 
    'axes.spines.top':False})

    sellers = session.query(Seller).all()
    sellers = sorted(sellers, key=lambda x: len(x.offers), reverse=True)
    sellers = sellers[:20]
    sellers = [(seller.name, len(seller.offers)) for seller in sellers]
    df = pd.DataFrame(sellers, columns=["Seller", "Offers"])
    fig = plt.figure(figsize=(30, 10), dpi=100)
    sns.barplot(x="Seller", y="Offers", data=df)
    st.pyplot(fig)

    # make a chart with the average price per card, group in bins by 50 cent
    st.markdown("# ")
    st.markdown("### Average price per card")

    prices = [sum([float(offer.price) for offer in card.offers]) / len(card.offers) for card in cards]
    prices = sorted(prices)

    # make distplot using plotly
    import plotly.express as px
    fig = px.histogram(x=prices, nbins=50, title="Average price per card")
    fig.update_layout(xaxis_title="Price in €", yaxis_title="Number of offers")
    st.plotly_chart(fig, use_container_width=True)

if step == "Generate cart":

    if not st.session_state.get("decklist_plain", None):
        st.error("Please upload a file or paste a decklist first")
        st.stop()

    session = Session()

    cards = session.query(Card).all()

    if not cards:
        st.error("Please retrieve the cards first")
        st.stop()

    if not all([card.url for card in cards]):
        st.error("Please validate all cards first and enter the URL if it was not found automatically")
        st.stop()

    if not all([card.offers for card in cards]):
        st.error("Please get the offers first")
        st.stop()

    st.markdown("# ")
    st.markdown("In this step, you can generate a cart with the offers you want to buy.")

    # float input for shipping costs
    shipping_costs = st.number_input("Shipping costs", value=1.75, step=0.01)

    cart = generate_cart()

    st.markdown("# ")
    st.markdown("### Cart")

    # the index of the dict is the seller
    for seller, offers in cart.items():
        # make a clickable link to the sellers website
        st.markdown(f"#### [{seller}](https://www.cardmarket.com" + seller.url + ")")
        # make a table with offers, where you can see the name of the card and the price
        df = pd.DataFrame([(offer.card.name, offer.price + " €") for offer in offers], columns=["Card", "Price"])
        df.set_index("Card", inplace=True)
        st.table(df)

    st.markdown("# ")

    total_price = sum([float(offer.price) * offer.card.to_buy for seller, offers in cart.items() for offer in offers])
    total_price += len(cart) * shipping_costs # add 1.75 € for each seller
    st.markdown(f"## Total price: {total_price:.2f} €")

    cart_cheapest = compared_cart()
    total_price_cheapest = sum([float(offer.price) * offer.card.to_buy for seller, offers in cart_cheapest.items() for offer in offers])
    total_price_cheapest += len(cart_cheapest) * shipping_costs # add 1.75 € for each seller
    st.markdown(f"You saved {total_price_cheapest - total_price:.2f} € by buying the optimized combination of offers instead of choosing the cheapest offer for each card.")

if step == "Support me":

    st.markdown("# ")
    
    st.markdown("# HI,")
    st.markdown("##### My name is Moritz Enderle and I am a student in the Bachelors program on Artificial Intelligence in Bavaria, Germany.")
    st.markdown("##### This project took me a lot of time and effort to develop. If you like it, please consider supporting me by buying me a coffee. :coffee:")

    st.markdown("[![ko-fi](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MoritzEnderle)")