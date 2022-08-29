#IEC API

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Docker(optional)

### Project setup

```sh
# clone the repo
$ git clone https://github.com/akhlaq1/IEC_Python_Backend.git

# move to the project folder
$ cd CharlesAPI
```

### Creating virtual environment 📦

- Using [virtualenv](https://virtualenv.pypa.io/en/latest/) 📦
- Create a `virtual environment` for this project 📦

```shell
# creating virtual environment
$ virtualenv venv

# activating the virtual environment
$ source venv/bin/activate

# installing dependencies
$ pip install -r requirements.txt
```

### Running app

- If you feel that everything can be run, then run the Flask API

```sh
python app.py
```

### Running the Application in Docker 🐳

- If you want to execute the API using Docker:

1. Install Docker (https://docs.docker.com/get-docker/)

- To Start the container:

```sh
$ docker-compose up -d
```

- To Stop the container

```sh
$ docker-compose down
```

- To rebuild the container (After any update to the code)

```sh
$ docker-compose build
```

- To Access the API

  Replace the IP from 127.0.0.1 to the internal IP of your system

## License 📝

This project is licensed under the terms of the [MIT license](LICENSE).
