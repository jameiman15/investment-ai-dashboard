import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 台灣時區 UTC+8
taiwan_tz = timezone(timedelta(hours=8))
now = datetime.now(taiwan_tz)

report_path = Path("data/report.json")

with report_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

data["updated_at"] = now.strftime("%Y-%m-%d %H:%M")
data["market"]["risk_level"] = "中等"
data["market"]["summary"] = "這是由 GitHub Actions 自動更新的測試內容。"
data["market"]["overall_advice"] = "自動化測試成功，先觀察。"

with report_path.open("w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

print("report.json 已更新")
