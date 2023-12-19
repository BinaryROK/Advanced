from datetime import datetime as dt 
import subprocess
import os
import pandas as pd
import numpy as np
import joblib

import cr


if __name__ == '__main__':
    today_date_str = dt.today().strftime('%Y-%m-%d')

    # zaraData crawl
    farm =1
    TargetDay = today_date_str
    cr.gen(TargetDay,farm)




        # Git 저장소 경로
    repo_path = "D:\Advanced"
    # 변경사항을 스테이징 영역에 추가
    subprocess.run(["git", "add", "Data"], cwd=repo_path)

    # 변경 내용 커밋
    commit_message = "Add ZaraData" + dt.now().strftime("%Y-%m-%d %H:%M:%S")
    subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path)

    # 변경 내용 푸시
    subprocess.run(["git", "push", "origin", "main"], cwd=repo_path)


