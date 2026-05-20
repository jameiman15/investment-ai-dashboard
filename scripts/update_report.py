import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

# 台灣時區 UTC+8
taiwan_tz = timezone(timedelta(hours=8))
now = datetime.now(taiwan_tz)

report_path = Path("data/report.json")
portfolio_path = Path("data/portfolio.json")

with report_path.open("r", encoding="utf-8") as file:
    report = json.load(file)

with portfolio_path.open("r", encoding="utf-8") as file:
    portfolio = json.load(file)

# 讀取帳戶設定
accounts = portfolio.get("accounts", [])
holdings = portfolio.get("holdings", [])

# 統計每個帳戶有幾個投資商品
account_summary = []

for account in accounts:
    account_name = account["account"]
    account_holdings = [
        item for item in holdings
        if item.get("account") == account_name
    ]

    product_count = len(account_holdings)
    product_types = sorted(set(item.get("type", "未分類") for item in account_holdings))

    if account_name == "家庭":
        advice = "家庭帳戶優先保留現金與房貸預備金，不建議重壓高波動資產。"
    elif account_name == "小孩":
        advice = "小孩帳戶投資年限長，可偏長期成長，定期定額可持續。"
    elif account_name == "媽媽":
        advice = "媽媽帳戶建議以保守收益與低波動資產為主。"
    elif account_name == "老婆":
        advice = "老婆帳戶可維持穩健配置，ETF 與基金可續抱觀察。"
    else:
        advice = "自己帳戶可依市場狀況彈性調整，已有獲利標的可設定停利條件。"

    if product_count == 0:
        advice = "目前尚未建立投資商品，建議先補上持有標的。"

    account_summary.append({
        "name": account_name,
        "goal": account.get("goal", ""),
        "risk_profile": account.get("risk_profile", ""),
        "advice": advice
    })

# 找出需要注意的標的
watchlist = []

for item in holdings:
    item_type = item.get("type", "")
    name = item.get("name", "")
    account = item.get("account", "")
    purpose = item.get("purpose", "")
    strategy = item.get("strategy", "")

    if item_type == "現金":
        status = "資金預備"
        advice = strategy or "保留現金水位。"
    elif item_type == "基金":
        status = "需定期檢查績效與波動"
        advice = strategy or "定期定額續扣，單筆加碼等待回檔。"
    elif item_type == "ETF":
        status = "適合配置型追蹤"
        advice = strategy or "續抱，不追高。"
    elif item_type == "個股":
        status = "需檢查技術面與籌碼面"
        advice = strategy or "依照 MA20、RSI 與損益率判斷續抱或停利。"
    else:
        status = "待分類"
        advice = strategy or "請補充商品類型與投資目的。"

    watchlist.append({
        "type": item_type,
        "name": f"{name}（{account}）",
        "status": status,
        "advice": advice
    })

# 更新 report.json
report["updated_at"] = now.strftime("%Y-%m-%d %H:%M")

report["market"]["risk_level"] = "中等"
report["market"]["summary"] = "目前為自動化測試階段，市場資料尚未串接，先以投資清單健診為主。"
report["market"]["overall_advice"] = "自動讀取投資清單成功"

report["family_status"]["status"] = "已建立多帳戶"
report["family_status"]["summary"] = f"目前已建立 {len(accounts)} 個帳戶，共 {len(holdings)} 個投資商品。"

report["accounts"] = account_summary
report["watchlist"] = watchlist

with report_path.open("w", encoding="utf-8") as file:
    json.dump(report, file, ensure_ascii=False, indent=2)

print("report.json 已根據 portfolio.json 更新完成")
