# this code is auto generated by the expr_codegen
# https://github.com/wukan1986/expr_codegen
# 此段代码由 expr_codegen 自动生成，欢迎提交 issue 或 pull request
import re

import numpy as np  # noqa
import pandas as pd  # noqa
import polars as pl  # noqa
import polars.selectors as cs  # noqa
from loguru import logger  # noqa

# ===================================
# 导入优先级，例如：ts_RSI在ta与talib中都出现了，优先使用ta
# 运行时，后导入覆盖前导入，但IDE智能提示是显示先导入的
_ = 0  # 只要之前出现了语句，之后的import位置不参与调整
from polars_ta.prefix.talib import *  # noqa
from polars_ta.prefix.tdx import *  # noqa
from polars_ta.prefix.ta import *  # noqa
from polars_ta.prefix.wq import *  # noqa
from polars_ta.prefix.cdl import *  # noqa

# ===================================

_ = (
    "OPEN",
    "HIGH",
    "LOW",
    "CLOSE",
    "DOJI",
    "RETURN_CC_1",
    "RETURN_CO_1",
    "NEXT_DOJI",
    "RETURN_OC_1",
    "RETURN_OO_1",
    "RETURN_OO_5",
)
(
    OPEN,
    HIGH,
    LOW,
    CLOSE,
    DOJI,
    RETURN_CC_1,
    RETURN_CO_1,
    NEXT_DOJI,
    RETURN_OC_1,
    RETURN_OO_1,
    RETURN_OO_5,
) = (pl.col(i) for i in _)

_ = (
    "_x_1",
    "_x_2",
    "_x_0",
    "DOJI",
    "RETURN_CC_1",
    "_x_3",
    "RETURN_CO_1",
    "RETURN_OC_1",
    "NEXT_DOJI",
    "RETURN_OO_1",
    "RETURN_OO_5",
    "LABEL_CC_1",
    "LABEL_CO_1",
    "LABEL_OC_1",
    "LABEL_OO_1",
    "LABEL_OO_5",
)
(
    _x_1,
    _x_2,
    _x_0,
    DOJI,
    RETURN_CC_1,
    _x_3,
    RETURN_CO_1,
    RETURN_OC_1,
    NEXT_DOJI,
    RETURN_OO_1,
    RETURN_OO_5,
    LABEL_CC_1,
    LABEL_CO_1,
    LABEL_OC_1,
    LABEL_OO_1,
    LABEL_OO_5,
) = (pl.col(i) for i in _)

_DATE_ = "date"
_ASSET_ = "asset"


def _expr_code():
    # 因子编辑区，可利用IDE的智能提示在此区域编辑因子

    # 这里用未复权的价格更合适
    # 今日涨停或跌停
    DOJI = four_price_doji(OPEN, HIGH, LOW, CLOSE)
    # 明日涨停或跌停
    NEXT_DOJI = ts_delay(DOJI, -1)

    # 远期收益率
    RETURN_CC_1 = ts_delay(CLOSE, -1) / CLOSE - 1
    RETURN_CO_1 = ts_delay(OPEN, -1) / CLOSE - 1
    RETURN_OC_1 = ts_delay(OPEN, -1) / ts_delay(CLOSE, -1) - 1
    RETURN_OO_1 = ts_delay(OPEN, -2) / ts_delay(OPEN, -1) - 1
    RETURN_OO_5 = ts_delay(OPEN, -6) / ts_delay(OPEN, -1) - 1

    # 标签
    LABEL_CC_1 = cs_label(DOJI, RETURN_CC_1, 20)
    LABEL_CO_1 = cs_label(DOJI, RETURN_CO_1, 20)
    LABEL_OC_1 = cs_label(NEXT_DOJI, RETURN_OC_1, 20)
    LABEL_OO_1 = cs_label(NEXT_DOJI, RETURN_OO_1, 20)
    LABEL_OO_5 = cs_label(NEXT_DOJI, RETURN_OO_5, 20)


def cs_label(cond, x, q=20):
    """表达式太长，可自己封装一下。tool.all中指定extra_codes可以自动复制到目标代码中

    注意：名字需要考虑是否设置前缀`ts_`、`cs_`
    内部函数前缀要统一，否则生成的代码混乱。
    如cs_label与内部的cs_bucket、cs_winsorize_quantile是统一的
    """
    return if_else(cond, None, cs_bucket(cs_winsorize_quantile(x, 0.01, 0.99), q))


def func_0_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        _x_1=ts_delay(CLOSE, -1),
        _x_2=ts_delay(OPEN, -1),
    )
    return df


def func_0_cl(df: pl.DataFrame) -> pl.DataFrame:
    # ========================================
    df = df.with_columns(
        _x_0=1 / CLOSE,
        DOJI=four_price_doji(OPEN, HIGH, LOW, CLOSE),
    )
    # ========================================
    df = df.with_columns(
        RETURN_CC_1=_x_0 * _x_1 - 1,
        _x_3=1 / _x_2,
        RETURN_CO_1=_x_0 * _x_2 - 1,
        RETURN_OC_1=(-_x_1 + _x_2) / _x_1,
    )
    return df


def func_1_ts__asset(df: pl.DataFrame) -> pl.DataFrame:
    df = df.sort(by=[_DATE_])
    # ========================================
    df = df.with_columns(
        NEXT_DOJI=ts_delay(DOJI, -1),
    )
    # ========================================
    df = df.with_columns(
        RETURN_OO_1=_x_3 * ts_delay(OPEN, -2) - 1,
        RETURN_OO_5=_x_3 * ts_delay(OPEN, -6) - 1,
    )
    return df


def func_2_cs__date(df: pl.DataFrame) -> pl.DataFrame:
    # ========================================
    df = df.with_columns(
        LABEL_CC_1=cs_label(DOJI, RETURN_CC_1, 20),
        LABEL_CO_1=cs_label(DOJI, RETURN_CO_1, 20),
        LABEL_OC_1=cs_label(NEXT_DOJI, RETURN_OC_1, 20),
    )
    # ========================================
    df = df.with_columns(
        LABEL_OO_1=cs_label(NEXT_DOJI, RETURN_OO_1, 20),
        LABEL_OO_5=cs_label(NEXT_DOJI, RETURN_OO_5, 20),
    )
    return df


"""
#========================================func_0_ts__asset
_x_1 = ts_delay(CLOSE, -1)
_x_2 = ts_delay(OPEN, -1)
#========================================func_0_cl
_x_0 = 1/CLOSE
DOJI = four_price_doji(OPEN, HIGH, LOW, CLOSE)
#========================================func_0_cl
RETURN_CC_1 = _x_0*_x_1 - 1
_x_3 = 1/_x_2
RETURN_CO_1 = _x_0*_x_2 - 1
RETURN_OC_1 = (-_x_1 + _x_2)/_x_1
#========================================func_1_ts__asset
NEXT_DOJI = ts_delay(DOJI, -1)
#========================================func_1_ts__asset
RETURN_OO_1 = _x_3*ts_delay(OPEN, -2) - 1
RETURN_OO_5 = _x_3*ts_delay(OPEN, -6) - 1
#========================================func_2_cs__date
LABEL_CC_1 = cs_label(DOJI, RETURN_CC_1, 20)
LABEL_CO_1 = cs_label(DOJI, RETURN_CO_1, 20)
LABEL_OC_1 = cs_label(NEXT_DOJI, RETURN_OC_1, 20)
#========================================func_2_cs__date
LABEL_OO_1 = cs_label(NEXT_DOJI, RETURN_OO_1, 20)
LABEL_OO_5 = cs_label(NEXT_DOJI, RETURN_OO_5, 20)
"""

"""
DOJI = four_price_doji(OPEN, HIGH, LOW, CLOSE)
NEXT_DOJI = ts_delay(DOJI, -1)
RETURN_CC_1 = -1 + ts_delay(CLOSE, -1)/CLOSE
RETURN_CO_1 = -1 + ts_delay(OPEN, -1)/CLOSE
RETURN_OC_1 = -1 + ts_delay(OPEN, -1)/ts_delay(CLOSE, -1)
RETURN_OO_1 = ts_delay(OPEN, -2)/ts_delay(OPEN, -1) - 1
RETURN_OO_5 = ts_delay(OPEN, -6)/ts_delay(OPEN, -1) - 1
LABEL_CC_1 = cs_label(DOJI, RETURN_CC_1, 20)
LABEL_CO_1 = cs_label(DOJI, RETURN_CO_1, 20)
LABEL_OC_1 = cs_label(NEXT_DOJI, RETURN_OC_1, 20)
LABEL_OO_1 = cs_label(NEXT_DOJI, RETURN_OO_1, 20)
LABEL_OO_5 = cs_label(NEXT_DOJI, RETURN_OO_5, 20)
"""


def main(df: pl.DataFrame):
    # logger.info("start...")

    df = df.sort(by=[_DATE_, _ASSET_])
    df = df.group_by(by=[_ASSET_]).map_groups(func_0_ts__asset)
    df = func_0_cl(df)
    df = df.group_by(by=[_ASSET_]).map_groups(func_1_ts__asset)
    df = df.group_by(by=[_DATE_]).map_groups(func_2_cs__date)

    # drop intermediate columns
    df = df.drop(columns=list(filter(lambda x: re.search(r"^_x_\d+", x), df.columns)))

    # shrink
    df = df.select(cs.all().shrink_dtype())
    df = df.shrink_to_fit()

    # logger.info('done')

    # save
    # df.write_parquet('output.parquet', compression='zstd')

    return df


if __name__ in ("__main__", "builtins"):
    # TODO: 数据加载或外部传入
    df_output = main(df_input)
