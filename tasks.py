from robocorp.tasks import task

import main


@task
def run_task():
    message = "Initializing"
    message = message + " the robot"
    main.run_script()
