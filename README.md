# Mozio Carlos G. Test
This repo aims to solve the test for Mozio API Integration Dev.

### About it
When I was working on the project it just came to my mind that the simplest way to give functionality was to make it as a CLI. Thats why you will see a very simple and straight forward installation with docker.

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
The only prerequisite is to have installed docker in your computer. 

_Below are the instructions of how to start and run the project._

2. Clone the project
   ```sh
   git clone https://github.com/imnotbeto/mozio-cg-test.git
   ```
3. Enter to the root directory
   ```sh
   cd mozio-cg-test
   ```
4. Build docker image
   ```sh
   docker build . -t mozio-cg:v0
   ```

5. Run image container
   ```sh
   docker run \
   --name mazio-cg-test \
   -e MOZIO_URL='https://api-testing.mozio.com' \
   -e MOZIO_AUTH_TOKEN='6bd.........6f9' \
   --rm -it mozio-cg:v0
   ```
   If you have difficulties while trying to run this command just execute it as a one liner.
    ```sh
    docker run --name mazio-cg-test -e MOZIO_URL='https://api-testing.mozio.com' -e MOZIO_AUTH_TOKEN='6bd.........6f9' --rm -it mozio-cg:v0
   ```


6. While the container is running you can also open a second terminal and run the tests by executing the following command:
   ```sh
   docker exec -it mazio-cg-test python -m unittest
   ```


<p align="right">(<a href="#mozio-carlos-g-test">back to top</a>)</p>
