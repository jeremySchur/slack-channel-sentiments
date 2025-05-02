CREATE TABLE IF NOT EXISTS channel (
    id VARCHAR(13) PRIMARY KEY, -- Channel_id with max length of 13 characters
    avg_sentiment DECIMAL(3, 2), -- Average sentiment score between -1.00 and 1.00
    last_read VARCHAR(18), -- Timestamp of last read message
    name VARCHAR(80) -- Slack channels can only be 80 characters long
);