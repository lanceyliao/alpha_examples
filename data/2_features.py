"""

"""
import os
import sys
from pathlib import Path

# 修改当前目录到上层目录，方便跨不同IDE中使用
pwd = str(Path(__file__).parents[1])
os.chdir(pwd)
sys.path.append(pwd)
print("pwd:", os.getcwd())
# ====================

import polars as pl

# 加载数据
df = pl.read_parquet('data/data.parquet')

# 生成特征
from codes.features import main

df = main(df)
print(df.tail())

# 保存
df.write_parquet('data/features.parquet')
