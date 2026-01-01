# Crypto Data Downloader

從 HuggingFace Hub 下載加密貨幣 OHLCV 資料並轉換為 CSV 的幼年工具。

## 功能特性

- 一次性下載單一或多個幣種的 OHLCV 資料
- 自動從 Parquet 轉換為 CSV 格式
- 支持多個時間框架 (15分鐘、母小時等)
- 合併同一幣種不同時間框架的資料
- 提供資料统計信息

## 安裝

### 先使用条件

- Python 3.7+
- pip 或 conda

### 安裝步驟

1. 克隆此倉庫
```bash
git clone https://github.com/caizongxun/crypto-data-downloader.git
cd crypto-data-downloader
```

2. 安裝依賶污
```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 下載單一幣種的資料

```python
from crypto_downloader import CryptoDataDownloader

# 初始化下載器
downloader = CryptoDataDownloader()

# 下載 BTC 的 15 分鐘資料
downloader.download_single_file('BTCUSDT', '15m')

# 輸出位置: crypto_data/BTCUSDT_15m.csv
```

### 2. 下載多個幣種

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()

# 下載多個幣種的資料
symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT']
downloader.download_multiple_files(
    symbols,
    ['15m', '1h']  # 下載两種時間框架
)
```

### 3. 查看資料資訊

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()

# 獲取資料資訊
info = downloader.get_data_info('BTCUSDT', '15m')
print(info)
# 輸出示例：
# {
#     'symbol': 'BTCUSDT',
#     'timeframe': '15m',
#     'rows': 45678,
#     'columns': ['timestamp', 'open', 'high', 'low', 'close', 'volume'],
#     'memory_usage_mb': 2.45,
#     'date_range': '2023-01-01 12:00:00 - 2024-01-01 18:30:00',
#     'price_range': '28500.50 - 68900.75'
# }
```

### 4. 合併同一幣種不同時間框架的資料

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()

# 先下載資料
downloader.download_single_file('BTCUSDT', '15m')
downloader.download_single_file('BTCUSDT', '1h')

# 合併資料
downloader.combine_csv_files('BTCUSDT', ['15m', '1h'])
# 輸出: crypto_data/BTCUSDT_combined.csv
```

## 例子腳本

### 完整的希洛腳本

```python
from crypto_downloader import CryptoDataDownloader
import pandas as pd

def download_and_analyze():
    downloader = CryptoDataDownloader()
    
    # 下載 BTC 和 ETH 的 15 分鐘資料
    symbols = ['BTCUSDT', 'ETHUSDT']
    downloader.download_multiple_files(symbols, ['15m'])
    
    # 分析資料
    for symbol in symbols:
        df = pd.read_csv(f'crypto_data/{symbol}_15m.csv')
        print(f"\n{symbol} 資料統計")
        print(f"  行數: {len(df)}")
        print(f"  低價: {df['low'].min():.2f}")
        print(f"  高價: {df['high'].max():.2f}")
        print(f"  平均成交量: {df['volume'].mean():.2f}")

if __name__ == '__main__':
    download_and_analyze()
```

## 資料來源

資料來自 HuggingFace Hub 的 [zongowo111/v2-crypto-ohlcv-data](https://huggingface.co/datasets/zongowo111/v2-crypto-ohlcv-data) 資料集。

- **資料根目錄**: `klines/`
- **幣種案例**: BTCUSDT, ETHUSDT, ADAUSDT, 等等
- **時間框架**: 15分鐘 (15m)、母小時 (1h)
- **檔案格式**: Parquet (自動轉換為 CSV)

## API 參考

### CryptoDataDownloader

#### `download_single_file(symbol: str, timeframe: str = "15m", output_format: str = "csv") -> Optional[str]`

下載單一幣種的資料。

**參數：**
- `symbol`: 幣種符號（例子：'BTCUSDT'）
- `timeframe`: 時間框架（'15m' 或 '1h'）
- `output_format`: 輸出格式（'csv' 或 'parquet'）

**回傳：** 輸出檔案路徑

#### `download_multiple_files(symbols: List[str], timeframes: Optional[List[str]] = None, output_format: str = "csv") -> dict`

下載多個幣種的資料。

**參數：**
- `symbols`: 幣種列表
- `timeframes`: 時間框架列表（預設: ['15m', '1h']）
- `output_format`: 輸出格式

**回傳：** 成功下載的檔案字典

#### `combine_csv_files(symbol: str, timeframes: List[str], output_filename: Optional[str] = None) -> Optional[str]`

合併同一幣種不同時間框架的 CSV 檔案。

**參数：**
- `symbol`: 幣種符號
- `timeframes`: 時間框架列表
- `output_filename`: 輸出檔案名稱

**回傳：** 合併後檔案的路徑

#### `get_data_info(symbol: str, timeframe: str = "15m") -> Optional[dict]`

獲取資料的基本資訊。

**參数：**
- `symbol`: 幣種符號
- `timeframe`: 時間框架

**回傳：** 包含資料統計信息的字典

## 故障排查

### 問題 1: "檔案不存在" 錯誤

**原因**: HuggingFace 資料集中没有該幣種的資料

**解決**: 確保幣種符號正確（需併USDT），例如 'BTCUSDT'、'ETHUSDT' 等。

### 問題 2: 該就是每次下載都很慢

**原因**: 首次下載需要网絡下載、缑存和轉換

**解決**: 后次下載現有資料會採用本地缑存。

### 問題 3: Parquet 第一次不和 CSV 一樣

**原因**: Parquet 副文檔比 CSV 更有效，數浮數精度可能不同

**解決**: 在使用 CSV 前稍輸出前指定數值精度（例如 `.round(2)`）

## 所沙简因影響的目錄結構

```
crypto-data-downloader/
├── crypto_downloader.py      # 主要下載器
├── requirements.txt          # Python 依賶
├── README.md                 # 文檔
├── examples/                 # 例子腳本
│   └── example.py
└── crypto_data/              # 輸出資料目錄
    ├── BTCUSDT_15m.csv
    └── ETHUSDT_1h.csv
```

## 效能提示

- 輸出的 CSV 檔案比 Parquet 相對較大，但更容易可読。
- 大批量下載開展毋靫時間情形下，可但輈專沙横帶上並列处理算待採考龚。
- 採用 `pyarrow` 作為 Parquet 引擎可獲得更佳效能。

## 貨幣符號列表

HuggingFace 資料集中供提的貨幣符號有数十种（空纊基上）：

- BTC: BTCUSDT
- ETH: ETHUSDT
- ADA: ADAUSDT
- DOGE: DOGEUSDT
- SOL: SOLUSDT
- ...(更多)

## 貨敌錄 / 貨甚

如你継发創主貨畊慢終了，請汇報訊聯系我们。

## 授权

MIT License - 詳請那當使用

## 特佐
從 HuggingFace Hub 上的 [zongowo111/v2-crypto-ohlcv-data](https://huggingface.co/datasets/zongowo111/v2-crypto-ohlcv-data) 資料集改此還了所擁的資料。
