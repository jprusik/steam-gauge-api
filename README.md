# Steam Gauge API

**NOTE: THIS REPO IS A WORK-IN-PROGRESS REBUILD OF THE [STEAM GAUGE](https://github.com/jprusik/steam-gauge) BACK-END AND PRESENTLY LACKS FEATURE PARITY AND OPTIMIZATIONS SUITABLE FOR PRODUCTION ENVIRONMENTS.**

[Steam Gauge](https://www.mysteamgauge.com) is a collection of web apps driven by technologies like [Flask](http://flask.pocoo.org) and [React](https://reactjs.org) in order to produce data-rich Steam account summaries.

This repository represents development of the dedicated Flask back-end API app which can not only handle and respond to requests to project's data stores, but also serves as a pass-through to Valve's developer APIs, including the Web and Big Picture APIs. This app has undergone several revisions (including a migration from Python 2 to 3) and is presently being refactored to utilize improved software design patterns.

## Requirements

- Python 3.6.5 or higher (earlier versions of Python 3 have not been tested)
- Package requirements can be found in [`requirements.txt`](app/requirements.txt) and installed with [pip](https://pip.pypa.io) (Note: if you opt to use MySQL, you may have to download and `make` [mysql-connector-python](https://dev.mysql.com/downloads/connector/python/) manually)

## Usage

- Create `.env` in the app directory and give values to your app constants (see [`.env.example`](./.env.example)).
- To run locally, execute `wsgi.py` with Flask from the app root: `flask run`.
- Access with your client (by default) at `http://localhost:5000`.

### Docker

If you have Docker installed, you can build and run a container to access the api

```shell
docker build -f Dockerfile.dev -t sgapi:dev . && docker run --env-file ./.env -d -p 5000:5000 sgapi:dev
```

## Limitations & Known Issues

- Presently, there is no testing to mitigate regressions.

## Author

Jonathan Prusik [@jprusik](https://github.com/jprusik)
www.classynemesis.com
