from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import torch.nn.functional as F

def analyze_sentiment(messages):
    # Load the tokenizer and model
    tokenizer = RobertaTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
    model = RobertaForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")

    results = []
    for message in messages:
        # Tokenize and encode the message
        inputs = tokenizer(message, return_tensors="pt", truncation=True, padding=True)
        # Perform inference
        outputs = model(**inputs)
        # Apply softmax to get probabilities
        probs = F.softmax(outputs.logits, dim=-1)
        # Get the sentiment with the highest probability
        sentiment = torch.argmax(probs, dim=-1).item()
        results.append((message, sentiment, probs.tolist()))

    return results


if __name__ == "__main__":
    # Example messages
    messages = [
        "I love this product! It's amazing.",
        "This is the worst experience I've ever had.",
        "It's okay, not great but not terrible either."
    ]

    # Analyze sentiment
    sentiments = analyze_sentiment(messages)

    # Print results
    for message, sentiment, probs in sentiments:
        sentiment_label = ["Negative", "Neutral", "Positive"][sentiment]
        print(f"Message: {message}")
        print(f"Sentiment: {sentiment_label}")
        print(f"Probabilities: {probs}")
        print()