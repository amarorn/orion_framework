from ...core.interfaces.ILogger import ILogger

class ConsoleLogger(ILogger):
    def info(self, msg: str):
        print(f"[INFO] {msg}")
    def warn(self, msg: str):
        print(f"[WARN] {msg}")
    def error(self, msg: str):
        print(f"[ERROR] {msg}")
