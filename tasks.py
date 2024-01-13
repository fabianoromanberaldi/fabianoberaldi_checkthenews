from robocorp.tasks import task

import main


@task
def minimal_task():
    message = "Initializing"
    message = message + " the robot"
    main.run_script()
