import platform, subprocess
from dataclasses import dataclass
from typing import List, Dict
@dataclass
class SystemInfo:
    mem: List
    cpu: Dict
    system: str = platform.system()

    def __init__(self):
        self.mem = []
        self.cpu = self.cpu_state()

    def mem_state(self) -> List:
        return []

    def cpu_state(self) -> Dict[str, str]:
        if self.system == "Linux":
            key_pairs: List = []
            with open('/proc/cpuinfo') as f:
                for i, v in enumerate(f.readlines(), start=0):
                    value = v.strip().replace("\t", "").format()
                    key_pair = value.replace(" ", "").split(":")
                    key_pairs.append(key_pair)
            cpu_info_dict = {item[0]: item[1] for item in key_pairs if len(item) == 2}
            return cpu_info_dict
        elif self.system == "Windows":
            result = subprocess.run(["wmic", "cpu", "get", "name"], stdout=subprocess.PIPE, text=True)
            return {"Processor": result.stdout.strip().splitlines()[1]}
        elif self.system == "Darwin":
            result = subprocess.run(["sysctl", "-n", "machdep.cpu.brand_string"], stdout=subprocess.PIPE, text=True)
            return {"Processor": result.stdout.strip().splitlines()[1]}
        else:
            processor = platform.processor()
            if processor:
                return {"Processor": processor}
            else:
                return {"Processor": "N/A"}

