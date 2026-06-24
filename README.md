# dam-prices-api
Backend service for fetching, parsing, and analyzing Day-Ahead Market (DAM) hourly electricity prices from oree.com.ua.
## Prerequisites

Make sure you have the following installed on your local machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
1. Fork the repo (GitHub repository)
2. Clone the forked repo
    ```
    git clone the-link-from-your-forked-repo
    ```
    - You can get the link by clicking the `Clone or download` button in your repo
3. Create a .env file in the root directory and fill in your configuration variables
    ```
    cp .env.example .env
    ```
4. Build and start the Docker containers:
    ```
    docker compose up --build -d
    ```
5. To perform the initial import of data from oree.com.ua starting from a specific date, use the custom management command inside the running container:
    ```
    docker compose exec app python manage.py import_dam --start-date 2026-05-01
    ```
6. Once the containers are running, the API documentation is accessible locally at:
    ```
    http://localhost:8000/api/docs/
    ```
    