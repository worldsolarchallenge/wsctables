# WSC Tables

This project is in aid of the [Bridgestone World Solar Challenge](https://www.worldsolarchallenge.org/).

This application downloads data from various sources of truth, and serves it as
information to be rendered on the public facing web site.

## Build and Run

To build and run locally, you can use docker and the Makefile. We use [Docker Desktop](https://www.docker.com/products/docker-desktop) to make setup easy.

Once you have docker set up, on a Mac, or Linux:

```
make run
```

and then navigate to [http://localhost:5000](http://localhost:5000).

The key files are:

* [src/wsctables/views.py](src/wsctables/views.py) -- The main web app code. This is the most relevant bit to modify to suit your needs.
* [src/wsctables/templates/](src/wsctables/templates/) -- Contains HTML templates which are used to render web pages.
* [pyproject.toml](pyproject.toml) -- Defines how to install the python module.
* [Dockerfile](Dockerfile) -- Definition of how to build a docker image to run this app.
* [Makefile](Makefile) -- A makefile which contains commands and targets to build and run the app.
* [README.md](README.md) -- This README file.
* [.github/](.github/) -- Definition of the continuous integration steps.


## Deployment

The resulting docker container can be published to a docker repository, and run in any environment that can host docker containers, for example, Kubernetes.

## Getting in touch

Please reach out to the BWSC Technical Faculty, or the BWSC community members via the on-line forum linked from the [BWSC Web Site](https://www.worldsolarchallenge.org/). Contributions welcome, via pull request on [github.com](https://github.com/worldsolarchallenge/wsctables).
# wsctables


## Other notes: 
On mac OS X: LIBMEMCACHED=/opt/homebrew/Cellar/libmemcached/1.0.18_2 pip install pylibmc
