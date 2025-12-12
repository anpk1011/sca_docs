import inspect
import os
from datetime import datetime

class Colors:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RED = "\033[91m"

LOG_FILE = "debug.log"   

def debug(msg="", color="CYAN", log_to_file=True):

    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)

    filename = os.path.basename(info.filename)
    func = frame.f_code.co_name
    line = info.lineno

    clr = getattr(Colors, color, Colors.CYAN)

    text = f"[DEBUG] {filename}:{line} in {func}() -> {msg}"

    # print(f"{clr}{text}{Colors.RESET}")

    if log_to_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {text}\n")
