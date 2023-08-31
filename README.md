# Gunicorn/Uvicorn/FastAPI loguru issue

This git repo have the same structure of our current FastAPI backend, just in a much smaller scale. The logger setup is inspired from the discussions and suggestion from https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/

Whenever I want to add a new file logger for specific module, I will go `backend/http/logger_setup.py` to update the `configure_logger` function (See "Reproduce the issues" below).

Whenver the codebase changes(and tested), we will send a HUP signal to the Gunicorn master process to gracefully reload the server. This is just a small single line script and we wrote it in `Makefile`, under the `reload` section. So to reload Gunicorn, we can just do:

```bash
make reload
```

This works fine except loguru handlers are not updated at all(i.e. adding more handlers or removing handlers). The loguru handlers are only updated if we do `sudo supervisorctl restart gunlog`.

## Setting up on your local machine

1. This only works in Linux/Unix system. If you are using Windows, please consider using WSL2
2. Make sure you have `Python3.10+` and `supervisord` installed
3. create an virtual environment and install the required packages:
    ```bash
    python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
    ```
4. In `gunlog.supervisor.ini`, **MAKE SURE** to change the `directory` field and `command` to match your local directory

5. setup symlink for `gunlog.supervisor.ini` to your `supervisord` `etc` path (may be diifferent for various systems, see the top comment in `gunlog.supervisor.ini` as an example)

6. run the following commands for supervisord to manage the server:
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    ```
7. Check the gunicorn server is started => `sudo supervisorctl status`, you should see something like this
    ```console
     gunlog                         RUNNING   pid 11459, uptime 1:43:22
    ```

## Reproduce the issues

1. Visit localhost:8015/docs on broswer, this is the Swagger Docs provided by FastAPI
2. Go to `backend/http/logger_setup.py`, Try to add or remove loguru handlers. For example, you can add a handler to filter the module `backend.features.zoo`:

    ```python
     #backend/http/logger_setup.py
    ...
    logger.configure(
        handlers=[
            {"sink": 'log/master.log', "level": logging.INFO},
            {"filter":"backend.features.foo","sink": 'log/foo.log', "level": logging.INFO},
            {"filter":"backend.features.zoo","sink": 'log/zoo.log', "level": logging.INFO},
            # ^ NEW handler
    ]
    )
    # you can also use logger.add:
    #logger.add("log/zoo.log", filter="backend.features.zoo", level="INFO")
    ```

3. run `make reload` to send HUP signal to Gunicorn and reload the changes

4. Check `GET /loguru` endpoint, it return the `loguru.logger` object, it still have the old handlers
5. if you followed the example from step 2, you should see that there are no logs in `log/zoo.log`
