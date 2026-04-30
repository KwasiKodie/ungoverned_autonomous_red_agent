# tools/arsenal.py

from .recon_tools import ReconTools
from .exploit_tools import ExploitTools
from .tool_validator import ToolValidator

class Arsenal:

    def __init__(self):
        self.recon = ReconTools()
        self.exploit = ExploitTools()
        self.validator = ToolValidator()

    # Optional unified access layer
    def run(self, tool, **kwargs):
        if hasattr(self.recon, tool):
            return getattr(self.recon, tool)(**kwargs)

        elif hasattr(self.execution, tool):
            return getattr(self.execution, tool)(**kwargs)

        else:
            return "Unknown tool"