from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from .postgres import insert_channel
import asyncio
import os

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
client = AsyncWebClient(token=SLACK_TOKEN)

def update_public_channels(channels):
    """
        Update the list of public channels in the database
        :param channels: Dictionary of channels to update
        :return: None
    """
    try:
        response = asyncio.run(client.conversations_list(types="public_channel"))
        for channel in response['channels']:
            if channel['id'] not in channels:
                insert_channel(channel['id'], channel['name'])
                channels[channel['id']] = {"name": channel['name']}
        return None
    except SlackApiError as e:
        print(f"Error fetching channel list: {e.response['error']}")
        return None

def fetch_channel_messages(channel_id, cursor=None, oldest=0, limit=200):
    """
        Fetch messages from a given channel
        :param channel_id: Channel ID to fetch messages from
        :param cursor: Pagination cursor
        :param oldest: Timestamp to start fetching messages from
        :param limit: Number of messages to fetch
        :return: promise for response containing the messages
    """
    if oldest == None:
        oldest = 0

    return client.conversations_history(
        channel=channel_id,
        cursor=cursor,
        oldest=oldest,
        limit=limit
    )

def fetch_replies(channel_id, thread_ts, cursor=None, limit=200):
    """
        Fetch replies to a given thread in a channel
        :param channel_id: Channel ID of the thread
        :param thread_ts: Timestamp of the thread
        :param cursor: Pagination cursor
        :param limit: Number of replies to fetch
        :return: promise for response containing the replies
    """
    return client.conversations_replies(
        channel=channel_id,
        ts=thread_ts,
        cursor=cursor,
        limit=limit
    )

async def process_message(message, channel_id, messages_list):
    """
        Process a message and add it to the messages list
        :param message: Message to process
        :param channel_id: Channel ID of the message
        :param messages_list: List to store the messages
        :return: None
    """
    if message.get('type') == 'message' and not message.get('subtype'):
        messages_list.append({"user_id": message.get('user', ''),
                              "channel_id": channel_id,
                              "text": message.get('text', ''),
                              "ts": message.get('ts', '')})
        
        if 'thread_ts' in message:
            await fetch_and_add_replies(channel_id, message['thread_ts'], messages_list)

    return None

async def fetch_and_add_replies(channel_id, thread_ts, messages_list):
    """
        Fetch replies to a thread and add them to the messages list
        :param channel_id: Channel ID of the thread
        :param thread_ts: Timestamp of the thread
        :param messages_list: List to store the messages
        :return: None
    """
    reply_cursor = None
    while True:
        try:
            replies_response = await fetch_replies(channel_id, thread_ts, reply_cursor)
        except SlackApiError as e:
            if e.response.status_code == 429:
                delay = int(e.response.headers.get('Retry-After', 60))
                await asyncio.sleep(delay)
                continue
            else:
                raise e
        for reply in reversed(replies_response.get('messages', [])):
            # Skip the first message (original thread message)
            if reply == replies_response.get('messages', [])[0]:
                continue
            if reply.get('type') == 'message' and not reply.get('subtype'):
                messages_list.append({"user_id": reply.get('user', ''),
                                      "channel_id": channel_id,
                                      "text": reply.get('text', ''),
                                      "ts": reply.get('ts', '')})

        if not replies_response.get('has_more', False):
            break
        reply_cursor = replies_response['response_metadata'].get('next_cursor', None)

    return None

async def get_new_channel_messages(channel_id, channel):
    """
        Get all messages from a channel and process them
        :param channel_id: Channel ID to fetch messages from
        :param channel: Channel object containing metadata
        :return: Tuple of channel_id, messages, and last_read_timestamp
    """
    messages = []
    try:
        cursor = None
        while True:
            try:
                response = await fetch_channel_messages(
                    channel_id=channel_id,
                    cursor=cursor,
                    oldest=channel.get('last_read_timestamp')
                )
            except SlackApiError as e:
                if e.response.status_code == 429:
                    delay = int(e.response.headers.get('Retry-After', 60))
                    print(f"Rate limit hit. Retrying after {delay} seconds...")
                    await asyncio.sleep(delay)
                    continue
                else:
                    raise e

            for message in response.get('messages', []):
                await process_message(message, channel_id, messages)

            if not response.get('has_more', False):
                break
            cursor = response['response_metadata'].get('next_cursor', None)
    except SlackApiError as e:
        print(f"Error fetching messages from channel {channel_id}: {e.response['error']}")
    return channel_id, messages, (messages[0]['ts'] if len(messages) > 0 else None)

async def get_new_messages(channels):
    """
        Get new messages from all channels and update the channels dictionary
        :param channels: Dictionary of channels to update
        :return: None
    """
    results = await asyncio.gather(*[
        get_new_channel_messages(channel_id, channel)
        for channel_id, channel in channels.items()
    ])

    for channel_id, new_messages, ts in results:
        channels[channel_id]['messages'] = new_messages
        channels[channel_id]['last_read_timestamp'] = ts
