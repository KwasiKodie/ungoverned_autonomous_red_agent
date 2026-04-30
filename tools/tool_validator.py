# tools/tool_validator.py

import shutil

class ToolValidator:

    REQUIRED_TOOLS = [
        "sqlmap",
        "commix",
        "nuclei",
        "gobuster",
        "curl",
        "searchsploit"
    ]

    def check_tool(self, tool_name):
        return shutil.which(tool_name) is not None

    def validate_all(self):
        missing = []
        for tool in self.REQUIRED_TOOLS:
            if not self.check_tool(tool):
                missing.append(tool)
        return missing