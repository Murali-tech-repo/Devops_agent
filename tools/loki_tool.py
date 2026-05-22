import requests
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

class LokiLogTool:

    def __init__(self, base_url=os.getenv("LOKI_URL"), token=os.getenv("LOKI_TOKEN")):
        self.base_url = base_url
        self.token = token

    def get_last_15min_logs(self, query='{job="api/report-service"}', limit=500):

        end = datetime.now(timezone.utc)
        start = end - timedelta(minutes=15)

        params = {
            "query": query,
            "start": int(start.timestamp() * 1e9),
            "end": int(end.timestamp() * 1e9),
            "limit": limit
        }

        url = f"{self.base_url}/loki/api/v1/query_range"

        headers = {}

        # 🔐 AUTH TOKEN (IMPORTANT)
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=15
            )
            response.raise_for_status()

            data = response.json()

            logs = []

            for stream in data.get("data", {}).get("result", []):
                for value in stream.get("values", []):
                    timestamp, log_line = value
                    logs.append(f"{timestamp} | {log_line}")

            return "\n".join(logs)

        except Exception as e:
            return f"LOKI_FETCH_ERROR: {str(e)}"