from robocorp.tasks import task
import main

@task
def minimal_task():
    message = "Hello"
    message = message + " World!"
    main.run_script()
