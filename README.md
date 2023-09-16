
# API task
Test task





## Deployment

To deploy this project run(make sure you have installed docker and docker-compose)

```bash
  docker-compose --env-file env.dev up -d
```
in browser locate [localhost/](https://localhost/api/v1/schema/swagger-ui) to open api documentation

## Running Tests

To run tests, run the following command

```bash
  docker exec it <app container name>  pytest main
```
or
```bash
docker exec it <app container name>
pytest main
