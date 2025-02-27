# Cardmarket Helper Tool for Magic: The Gathering 🃏

A Python-based tool designed to optimize the process of purchasing single Magic: The Gathering cards from [Cardmarket](https://www.cardmarket.com/) using a decklist exported from [TappedOut](https://tappedout.net/). 🚀

---

## Installation ⚙️

1. **Clone the Repository** 📥  
   `git clone https://github.com/THDMoritzEnderle/MKM`

2. **Install Dependencies** 🛠️  
   Ensure [Python](https://www.python.org/) is installed on your system, then run:  
   `cd cardmarket`  
   `pip install -r requirements.txt`

3. **Launch the UI** 🎮  
   Start the Streamlit interface with:  
   `streamlit run streamlitInterface.py`

---

## Usage 🎯

### 1. Input Decklist ✍️
- Navigate to [TappedOut](https://tappedout.net/), export your decklist, and copy it to your clipboard.
- Paste the decklist into the input field in the tool.
- Submit by pressing `Ctrl + Enter`. ✅

### 2. Retrieve Cards 🔍
- Switch to the "Retrieve Cards" tab.
- Wait for the progress bar to complete (duration depends on decklist size). ⏳

### 3. Validate Cards ✔️
- Go to the "Validate Cards" tab to review the retrieved card list.
- Some cards may not be found due to naming differences on Cardmarket. To fix this:
  - Use the [Cardmarket Advanced Search](https://www.cardmarket.com/en/Magic/AdvancedSearch) to find the correct card.
  - Enter the generic set URL in the format: `https://www.cardmarket.com/en/Magic/Cards/<Card-Name>` (e.g., `https://www.cardmarket.com/en/Magic/Cards/Lightning-Bolt`).
- Customize the sets you want to buy from (all sets are selected by default for the cheapest option, but this may include illegal sets). ⚖️
- Click "Save" to apply changes. 💾

### 4. Get Offers 🛒
- In the "Get Offers" tab, configure:
  - Card languages 🌐
  - Minimum condition ⭐
  - Seller country (currently only Germany is supported) 🇩🇪
- Click "Get Offers" to fetch available listings (this may take time based on the number of cards).
- Adjust options and rerun as needed. 🔄

### 5. View Stats 📊
- Check the "Stats" tab for a breakdown of top sellers and per-card pricing. 💰

### 6. Generate Cart 🛍️
- Visit the "Generate Cart" tab to see a list of sellers and the cards to buy from each.
- Set a custom shipping price (applied uniformly to all sellers). 📦
- The tool uses a custom algorithm to minimize shipping costs by consolidating purchases, reducing costs by approximately one-third compared to buying the cheapest offer per card. 🧠

---

## Future Improvements 🔮

- [ ] Support for additional countries beyond Germany 🌍
- [ ] Real-time set refreshing when manually entering URLs ♻️
- [ ] Compatibility with more decklist formats 📜

---

## Liability Disclaimer ⚠️

This tool is provided "as is" with no warranties. It uses web scraping to gather data from Cardmarket, which violates their Terms of Service. Use at your own risk—I am not liable for any consequences arising from its use.

---

## Contributing 🤝

Contributions are welcome! For major changes, please:
1. Open an issue to discuss your proposal. 💬
2. Submit a pull request with your updates. 📤

---

## Support the Project ☕

If you find this tool helpful, consider supporting me with a coffee!  
[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/MoritzEnderle)

---

Happy card hunting! 🎉
