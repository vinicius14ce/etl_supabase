from datetime import datetime
from pathlib import Path

DIR_MAIN = Path(__file__).resolve().parent.parent
DIR_LOGS = DIR_MAIN / "logs"
FILE_ERROR_LOG = DIR_LOGS / "error_etl.log"

def check_dir():
    DIR_LOGS.mkdir(
        parents=True,
        exist_ok=True
    )

def get_timestamp(): 
    now = datetime.now()
    return {
        "date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M:%S")
    }

def log_error(
        stage,
        error,
        file=None,
        substep=None,
        return_value=None
):
    check_dir()
    now = get_timestamp()
    date = now["date"]
    time = now["time"]

    log = (
        "\n"
        + "=" * 80
        + "\n"
        + "LOG: ERROR \n"
        + "=" * 80
        + "\n"
        + f"Fase: {stage}\n"
        + f"Substep: {substep}\n"
        + f"File: {file if file else '-'}\n"
        + f"Return Value: {return_value if return_value else '-'}\n"
        + f"Date: {date}\n"
        + f"Time: {time}\n"
        + f"Error: {error}\n"
        
        + "=" * 80
        + "\n"
    )

    print(log)

    with open(
        FILE_ERROR_LOG,
        "a",
        encoding="utf-8"
    ) as file_log: 
        file_log.write(log)