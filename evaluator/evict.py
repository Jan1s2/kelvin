import json
import subprocess
from .utils import generate_identification


def create_docker_list(labels):
    def fmt_value(v):
        if isinstance(v, list):
            return json.dumps(v)
        return v

    filters = [f"--filter=label={k}={fmt_value(v)}" for k, v in labels.items()]
    docker_list = [
        "docker",
        "ps",
        *filters,
        "--format",
        "{{.ID}}",
    ]
    return docker_list


def create_docker_kill(ids):
    docker_kill = ["docker", "kill", *ids]
    return docker_kill


def job_failure_callback(job, connection, exc_type, exc_value, traceback):
    if "Task exceeded maximum timeout value" not in str(exc_value):
        return
    meta = job.args[3]
    identification = generate_identification(meta)
    docker_list_cmd = create_docker_list(identification)
    try:
        docker_list = subprocess.check_output(docker_list_cmd).decode().split("\n")[:-1]
        docker_kill_cmd = create_docker_kill(docker_list)
        subprocess.run(docker_kill_cmd)
    except subprocess.CalledProcessError:
        return
