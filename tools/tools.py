
from crewai_tools import FileReadTool
from tools.loki_tool import LokiLogTool

# TOOL: Read Log Files
log_reader_tool = FileReadTool()
loki_tool = LokiLogTool()
