from datetime import datetime
 
log_path = r"S:\【1230】マルチ戦略運用U\30_業務用個人フォルダ\A1800401_山崎健\010_市場分析\000_News\004_Python\python_executed.log"
 
with open(log_path, "a", encoding="utf-8") as f:
    f.write(f"実行日時: {datetime.now()}\n")
