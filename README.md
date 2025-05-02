# slack-channel-sentiments

## Prerequisites
Before you get started, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup

### Create a Slack App
1. Create a Slack app by following the instructions in the [Slack API documentation](https://api.slack.com/apps).
2. Use the `app_manifest.yaml` file provided in this repository to configure your app. You can upload the manifest directly in the Slack app creation process.

### Create a `.env` File
Create a `.env` file at the root of the repository with the following environment variables:

```env
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
SLACK_TOKEN=your_slack_user_token
```

Replace `your_postgres_username` and `your_postgres_password` with your desired PostgreSQL credentials.

## Running the Application
To start the application, use the following command:

```bash
docker compose up -d
```

This will run the application in detached mode.

To stop the application, use:

```bash
docker compose down
```

### Alternative with Make
If you have [GNU Make](https://ftp.gnu.org/gnu/make/) installed, you can use the following commands as an alternative:

To start the application:

```bash
make up
```

To stop the application:

```bash
make down
```

## Fetching Messages for Sentiment Analysis

The application fetches messages from Slack for sentiment analysis. By default, messages are retrieved once a day at 0:00.

### Modifying Fetch Frequency
To adjust the frequency of message retrieval, update the schedule in `sentiment_analysis/src/main.py`. Be cautious when increasing the frequency, as it may result in missed replies to messages.