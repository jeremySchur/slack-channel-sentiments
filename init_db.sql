CREATE TABLE IF NOT EXISTS channels (
    id VARCHAR(13) PRIMARY KEY, -- Channel_id with max length of 13 characters
    avg_sentiment DECIMAL(3, 2), -- Average sentiment score between -1.00 and 1.00
    last_read VARCHAR(18), -- Timestamp of last read message
    name VARCHAR(80) -- Slack channels can only be 80 characters long
);

CREATE TABLE IF NOT EXISTS messages (
    user_id VARCHAR(13), -- User ID associated with the message
    channel_id VARCHAR(13), -- Foreign key to channel table
    text TEXT, -- Message text
    sentiment DECIMAL(3, 2), -- Sentiment score between -1.00 and 1.00
    created_at VARCHAR(18), -- Timestamp of message creation
    PRIMARY KEY (user_id, channel_id, created_at), -- Composite primary key
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE -- Foreign key constraint with cascade delete
);