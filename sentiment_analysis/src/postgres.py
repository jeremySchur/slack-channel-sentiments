import psycopg
import os

DB_PARAMS = {
    "dbname": "sentiment_data",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "db",
    "port": 5432,
}

def get_channels():
    """
        Fetch all channels from the database
        :return: Dictionary of channels with their IDs, names, and last read timestamps
    """
    channels = {}
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, last_read FROM channel;")
            for entry in cur:
                channels[entry[0]] = {"name": entry[1], "last_read_timestamp": entry[2]}
    return channels

def insert_channel(channel_id, channel_name):
    """
        Insert a new channel into the database
        :param channel_id: ID of the channel to insert
        :param channel_name: Name of the channel to insert
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO channel (id, name) VALUES (%s, %s);", (channel_id, channel_name))
        conn.commit()

def update_timestamps(channels):
    """
        Update the last read timestamp for each channel in the database.
        If a channel already has a last_read_timestamp, update it.
        Otherwise, set it to the new timestamp directly.
        :param channels: Dictionary of channels with messages
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for channel_id, channel in channels.items():
                if channel.get("last_read_timestamp"):
                    cur.execute("UPDATE channel SET last_read=%s WHERE id=%s;", (channel.get("last_read_timestamp"), channel_id))
        conn.commit()

def update_avg_sentiments(channels):
    """
        Update the average sentiment for each channel in the database.
        If a channel already has an average sentiment, combine it with the new average.
        Otherwise, set it to the new average directly.
        :param channels: Dictionary of channels with messages
        :return: None
    """
    with psycopg.connect(**DB_PARAMS) as conn:
        with conn.cursor() as cur:
            for channel_id, data in channels.items():
                sentiments = [msg["sentiment"] for msg in data.get("messages", []) if "sentiment" in msg]
                
                if not sentiments:
                    continue

                new_avg = sum(sentiments) / len(sentiments)

                cur.execute("SELECT avg_sentiment FROM channel WHERE id = %s;", (channel_id,))
                result = cur.fetchone()

                if result and result[0] is not None:
                    existing_avg = result[0]
                    combined_avg = (float(existing_avg) + new_avg) / 2
                else:
                    combined_avg = new_avg

                cur.execute(
                    "UPDATE channel SET avg_sentiment = %s WHERE id = %s;",
                    (combined_avg, channel_id)
                )
        conn.commit()
