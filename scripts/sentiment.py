from textblob import TextBlob



def clean_text(text):
    """
    Remove leading and trailing whitespace from text.
    Converts input to string if not already.
    """
    return str(text).strip()


def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0:
            return 1
        elif polarity < 0:
            return -1
        else:
            return 0
    except:
        return "ERROR"
    