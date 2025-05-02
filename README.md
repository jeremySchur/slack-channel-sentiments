# slack-channel-sentiments

## Prerequisites
Before you get started, ensure you have the following installed:

- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)

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
make run
```

To stop the application:

```bash
make stop
```