# How to run the application
----------------------------

## Requirements

* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).

**Note**: To run the application it is enough that only the `docker compose` tool is installed on the system. There is no need to install dependencies manually, the whole project will be automatically assembled and run inside the docker container.

## Build and run application

* Start the stack with Docker Compose:

    ```bash
    docker compose up --build backend
    ```

* Now you can open your browser and interact with these URLs:

    - View [README document as a web page](http://localhost:8000);

    - Automatic interactive documentation with Swagger UI (from the OpenAPI): [http://localhost:8000/docs](http://localhost:8000/docs)

    - Alternative automatic documentation with ReDoc (from the OpenAPI): [http://localhost:8000/redoc](http://localhost:8000/redoc)

**Note**: The first time you start your stack, it might take a minute for it to be ready.

To check the logs, run:

```bash
docker compose logs backend
```

### API endpoints

Once the docker container is successfully launched, you can make requests to the API endpoints of the application on the port 8000.

All endpoints are fully meet the requirements of the [task](https://docs.google.com/document/d/1sAqFWAIO1gIZbajQzFgW1f72qmfI8bdE-FE-JDCc5zU).

Detailed examples of requests can be found in the `./examples/` directory.
