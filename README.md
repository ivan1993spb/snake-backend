
# Snake-Backend

*In process of development*

The Snake-Backend does backend operations with the Snake-Server.

See the Snake-Server source code here: https://github.com/ivan1993spb/snake-server

Try out the game: http://snakeonline.xyz/

## How to start

1. Setup environment:
    ```bash
    echo "SNAKE_API_ADDRESS=http://snakeonline.xyz/api" > .env
    ```
2. Start a local redis instance:
    ```bash
    docker run --name redis --rm -d -p 6379:6379 redis:5.0-alpine
    ```
3. Start workers. You have to start at least one:
    ```bash
    dramatiq lib.actors
    ```
4. Start scheduler:
    ```bash
    python app.py
    ```

## Futures

- Work with server API via CLI interface
  * [ ] Show basic information about server
- Bots futures
  * [ ] Start a swarm of bots
  * [ ] Stream game replays
- Work with games
  * [ ] Create and delete games by schedule - game rotation
  * [ ] Mass game creation
  * [ ] Export and import map proportions
- Generating images of maps
  * [x] Demon - walk through games and generate images
    + [x] By schedule

## Game screenshot examples

![examples/g2s30x30-big.jpeg](examples/g2s30x30-big.jpeg)
![examples/g4s70x75-tiny.jpeg](examples/g4s70x75-tiny.jpeg)
![examples/g1s150x75-big.jpeg](examples/g1s150x75-big.jpeg)
![examples/g5s200x100-medium.jpeg](examples/g5s200x100-medium.jpeg)
![examples/g10s25x75-small.jpeg](examples/g10s25x75-small.jpeg)
![examples/g9s25x75-big.jpeg](examples/g9s25x75-big.jpeg)
![examples/g10s25x75-tiny.jpeg](examples/g10s25x75-tiny.jpeg)
![examples/g3s30x75-medium.jpeg](examples/g3s30x75-medium.jpeg)
![examples/g11s80x75-tiny.jpeg](examples/g11s80x75-tiny.jpeg)
![examples/g12s25x75-medium.jpeg](examples/g12s25x75-medium.jpeg)
![examples/g12s25x75-big.jpeg](examples/g12s25x75-big.jpeg)
![examples/g12s25x75-tiny.jpeg](examples/g12s25x75-tiny.jpeg)
![examples/g1s150x75-tiny.jpeg](examples/g1s150x75-tiny.jpeg)
![examples/g1s150x75-small.jpeg](examples/g1s150x75-small.jpeg)
![examples/g12s25x75-small.jpeg](examples/g12s25x75-small.jpeg)
![examples/g4s70x75-small.jpeg](examples/g4s70x75-small.jpeg)
![examples/g6s250x250-tiny.jpeg](examples/g6s250x250-tiny.jpeg)
![examples/g3s30x75-tiny.jpeg](examples/g3s30x75-tiny.jpeg)
![examples/g4s70x75-medium.jpeg](examples/g4s70x75-medium.jpeg)
![examples/g5s200x100-tiny.jpeg](examples/g5s200x100-tiny.jpeg)
![examples/g2s30x30-small.jpeg](examples/g2s30x30-small.jpeg)
![examples/g9s25x75-small.jpeg](examples/g9s25x75-small.jpeg)
![examples/g7s25x25-tiny.jpeg](examples/g7s25x25-tiny.jpeg)
![examples/g3s30x75-small.jpeg](examples/g3s30x75-small.jpeg)
![examples/g10s25x75-medium.jpeg](examples/g10s25x75-medium.jpeg)
![examples/g7s25x25-small.jpeg](examples/g7s25x25-small.jpeg)
![examples/g9s25x75-medium.jpeg](examples/g9s25x75-medium.jpeg)
![examples/g6s250x250-small.jpeg](examples/g6s250x250-small.jpeg)
![examples/g3s30x75-big.jpeg](examples/g3s30x75-big.jpeg)
![examples/g11s80x75-big.jpeg](examples/g11s80x75-big.jpeg)
![examples/g7s25x25-medium.jpeg](examples/g7s25x25-medium.jpeg)
![examples/g2s30x30-medium.jpeg](examples/g2s30x30-medium.jpeg)
![examples/g6s250x250-medium.jpeg](examples/g6s250x250-medium.jpeg)
![examples/g11s80x75-small.jpeg](examples/g11s80x75-small.jpeg)
![examples/g8s75x25-medium.jpeg](examples/g8s75x25-medium.jpeg)
![examples/g4s70x75-big.jpeg](examples/g4s70x75-big.jpeg)
![examples/g11s80x75-medium.jpeg](examples/g11s80x75-medium.jpeg)
![examples/g8s75x25-big.jpeg](examples/g8s75x25-big.jpeg)
![examples/g2s30x30-tiny.jpeg](examples/g2s30x30-tiny.jpeg)
![examples/g5s200x100-small.jpeg](examples/g5s200x100-small.jpeg)
![examples/g1s150x75-medium.jpeg](examples/g1s150x75-medium.jpeg)
![examples/g7s25x25-big.jpeg](examples/g7s25x25-big.jpeg)
![examples/g10s25x75-big.jpeg](examples/g10s25x75-big.jpeg)
![examples/g8s75x25-tiny.jpeg](examples/g8s75x25-tiny.jpeg)
![examples/g6s250x250-big.jpeg](examples/g6s250x250-big.jpeg)
![examples/g9s25x75-tiny.jpeg](examples/g9s25x75-tiny.jpeg)
![examples/g8s75x25-small.jpeg](examples/g8s75x25-small.jpeg)
![examples/g5s200x100-big.jpeg](examples/g5s200x100-big.jpeg)

## Requirements

- the Snake-Server >= v4.3.0

## License

See [LICENSE](LICENSE).
