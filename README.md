
# Snake-Backend

*In process of development*

The Snake-Backend does backend operations with the Snake-Server.

See the Snake-Server source code here: https://github.com/ivan1993spb/snake-server

Try out the game: http://snakeonline.xyz/

## How to start the backend

1. Setup environment:
    ```bash
    echo "SNAKE_API_ADDRESS=https://snakeonline.xyz/api" > .env
    ```
2. Start a redis instance:
    ```bash
    docker run --name redis --rm -d -p 6379:6379 redis:5.0-alpine
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
  * [ ] Start a swarm of bots
  * [ ] Stream game replays
- Work with games
  * [ ] Create and delete games by schedule - game rotation
  * [ ] Mass game creation
  * [ ] Export and import map proportions
- Generating images of maps
  * [x] Daemon - walk through games and generate images
    + [x] By schedule

## Game screenshots

![examples/g8s75x25-big.jpeg](examples/g8s75x25-big.jpeg)

[More screenshot examples here](examples)

## Requirements

- the Snake-Server >= v4.3.0

## License

See [LICENSE](LICENSE).
