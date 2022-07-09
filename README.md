
# Snake-Backend

*WIP*

Snake-Backend performs background operations with [Snake-Server](https://github.com/ivan1993spb/snake-server).

See: https://snakeonline.xyz/

## How to start the backend

1. Setup envs:
    ```bash
    echo "SNAKE_API_ADDRESS=https://snakeonline.xyz/api" > .env
    ```
2. Start Redis:
    ```bash
    docker run --name redis --rm -d -p 6379:6379 redis
    ```
3. Start workers. You have to start at least one:
    ```bash
    dramatiq lib.actors
    ```
4. Start a scheduler:
    ```bash
    python scheduler.py
    ```

## Features

- Working with server API via CLI interface
  * [ ] Show basic information about server
- Bots features
  * [ ] Manage a swarm of bots
- Work with games
  * [ ] Create and delete games by schedule
  * [ ] Mass game creation
  * [ ] Export and import map proportions
- Generating images of maps
  * [x] Daemon - walk through games and generate images
    + [x] By schedule

## Game screenshots

![examples/g8s75x25-big.jpeg](examples/g8s75x25-big.jpeg)

[More screenshot examples here](examples)

## Requirements

- Snake-Server >= v4.3.0

## License

See [LICENSE](LICENSE).
