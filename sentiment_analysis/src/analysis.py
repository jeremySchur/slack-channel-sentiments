from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import torch.nn.functional as F

tokenizer = RobertaTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')
model = RobertaForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')

def calculate_sentiment(message):
    """
        Calculate the sentiment of a message using a pre-trained model.
        :param message: The message text to analyze
        :return: Sentiment score (float)
    """
    inputs = tokenizer(message, return_tensors='pt', truncation=True, padding=True, max_length=100)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    probabilities = F.softmax(outputs.logits, dim=1)[0]
    
    # Convert sentiment label to a numerical score
    # Define a scale: Negative = -1, Neutral = 0, Positive = 1
    sentiment = torch.argmax(probabilities).item()
    if sentiment == 2:
        return probabilities[2].item() - (probabilities[0].item() + probabilities[1].item())  # Positive - (Negative + Neutral)
    elif sentiment == 1:
        return 0 + probabilities[2].item() - probabilities[0].item()  # Neutral + Positive - Negative
    else:
        return -1 * (probabilities[0].item() - (probabilities[1].item() + probabilities[2].item())) # Negative - (Neutral + Positive)

def analyze_sentiments(channels):
    """
        Analyze the sentiments of all messages in all channels and add sentiment scores in-place.
        :param channels: dictionary of channels with messages
        :return: None
    """
    for channel_data in channels.values():
        for message in channel_data.get("messages", []):
            sentiment = calculate_sentiment(message["text"])
            message["sentiment"] = sentiment
