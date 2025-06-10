# Customer Experience Analytics

This project analyzes customer reviews of Ethiopian bank mobile apps to extract insights about user sentiment and experience.

## Project Structure

```
week2/
├── .github/
│   └── workflows/
│       └── test.yml
├── data/
│   └── raw/
│       └── cbe_reviews_YYYYMMDD.csv
├── nootebook/
│   ├── scrapper.ipynb
│   ├── scrapper_boa.ipynb
│   └── scrapper_dashen.ipynb
├── scripts/
│   ├── bank_scraper.py
│   ├── importer.py
│   └── sentiment.py
└── README.md
```

## Main Components

- **/scripts/bank_scraper.py**: Scrapes app info and reviews from the Google Play Store.
- **/scripts/importer.py**: Loads and preprocesses review data from CSV files.
- **/scripts/sentiment.py**: Performs sentiment analysis on review text.
- **/nootebook/scrapper.ipynb**: Example notebook for scraping, importing, and analyzing reviews.

## Usage

1. **Scrape Reviews**  
   Use the notebook `scrapper.ipynb` to scrape reviews or import existing review data.

2. **Import Data**  
   Load reviews from a CSV file:
   ```python
   from importer import import_reviews
   df = import_reviews("data/raw/cbe_reviews_YYYYMMDD.csv")
   ```

3. **Preprocess Data**  
   Clean and prepare the data as needed (drop columns, convert dates, etc.).

4. **Sentiment Analysis**  
   Apply sentiment analysis:
   ```python
   from sentiment import analyze_sentiment
   df['sentiment'] = df['content'].apply(analyze_sentiment)
   ```

5. **Analysis**  
   Use pandas or visualization tools to analyze sentiment distribution and trends.

## Requirements

- Python 3.8+
- pandas
- textblob
- vaderSentiment (optional, for alternative sentiment analysis)
- google-play-scraper (if scraping reviews)

Install dependencies:
```bash
pip install pandas textblob vaderSentiment google-play-scraper
```

## Notes

- You can use either the built-in sentiment analysis (TextBlob) or VADER for lightweight analysis.
- For deep learning models, install PyTorch or TensorFlow (optional, not required for TextBlob/VADER).
- Data files should be placed in `data/raw/`.

## License

MIT License