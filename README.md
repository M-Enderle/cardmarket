# MKM
A helper program to optimize the buying process of single cards using a card list from [tappedout](https://tappedout.net/).
## Install
Clone this repository
```bash
git clone https://github.com/THDMoritzEnderle/MKM
```
Install the dependencies, you need to have [python](https://www.python.org/) installed.
```bash
cd MKM
pip install -r requirements.txt
```
Run the UI with
```bash
streamlit run stramlitInterface.py
```
## Usage

### Input
In the first step, you will be asked to enter a decklist you want to buy.
To retrieve the right format, head to [tappedout](https://tappedout.net/) and copy the decklist to the clipboard.
Then insert the decklist into the input field and click on press `ctrl + Enter` to submit the decklist.

### Retrieving the cards
After submitting the decklist, head to the "Retrieve cards" tab and wait until the progress bar is finished. This
will take a while, depending on the size of the decklist.

### Validating the cards
After the cards are retrieved, you can validate them by clicking on the "Validate cards" tab. Here you can
see a list of all cards. Some may not have been found, because the names on MKM can differ. You can fix this
by locating the cards with missing urls and fill in the correct url. 

To do this, you can use the [advanced search](https://www.cardmarket.com/de/Magic/AdvancedSearch) 
function of MKM. Always insert the url of a generic set, the url should be
in the format `https://www.cardmarket.com/de/Magic/Cards/<Card-Name>`. For example, the url for
`Lightning Bolt` is `https://www.cardmarket.com/de/Magic/Cards/lightning-bolt`.

For each card found earlier, you can now select the sets you want to buy from. By default, all sets are
selected. This is most often the cheapest option, but can lead to buying cards in illegal sets.

Don't forget to save your changes by clicking on the "Save" button.

### Get offers
After validating the cards, you can get the offers by clicking on the "Get offers" tab. Here you can select
the languages of the cards, their minimum condition and the sellers country. As of now, the program only
supports buying from Germany. 

After setting the options, you can click on the "Get offers" button. This will take a while, depending on the
number of cards. You can always rerun this step, if you want to change the options.

### Stats
After getting the offers, you can see the stats by clicking on the "Stats" tab. Here you can see the top sellers
and the price per card.

### Generate cart
After getting the offers, you can generate a cart by clicking on the "Generate cart" tab. Here you will see a 
list of all buyers and what card to buy from them. You can also set a custom shipping price, which is the same for 
all sellers.

The algorithm behind this is self developed and not perfect. It tries to minimize the shipping costs by buying
as many cards from one seller as possible. This reduces costs by 1/3 on average compared to just buying the cheapest
offer for each card.

## Future work

- [ ] Add support for buying from other countries
- [ ] Refresh sets on the fly when manually setting urls
- [ ] Add support for more deck formats

## Support me 
If you like this project, you can support me by buying me a coffee. 

[![buymeacoffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MoritzEnderle)