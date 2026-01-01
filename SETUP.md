# 設置與使用指南

## 專案概述

**crypto-data-downloader** 是一個 Python 工具，用於從 HuggingFace Hub 下載加密貨幣 OHLCV 資料並轉換為 CSV 格式。

### 使用場景

- TradingView 無法匯出 CSV 時的替代方案
- 需要歷史加密貨幣價格資料進行分析
- 構建量化交易系統
- 進行技術分析研究
- 訓練機器學習模型

## 快速設置

### 步驟 1: 安裝 Python

確保已安裝 Python 3.7 或更高版本。

### 步驟 2: 克隆或下載專案

```bash
git clone https://github.com/caizongxun/crypto-data-downloader.git
cd crypto-data-downloader
```

### 步驟 3: 安裝依賴

```bash
pip install -r requirements.txt
```

如果使用 conda：

```bash
conda create -n crypto-downloader python=3.9
conda activate crypto-downloader
pip install -r requirements.txt
```

## 基本用法

### 方式 1: 直接運行範例

```bash
python examples/quickstart.py
```

### 方式 2: 在自己的 Python 腳本中使用

```python
from crypto_downloader import CryptoDataDownloader

# 初始化下載器
downloader = CryptoDataDownloader()

# 下載 BTC 15 分鐘資料
downloader.download_single_file('BTCUSDT', '15m')

# 輸出: crypto_data/BTCUSDT_15m.csv
```

## 支援的幣種與時間框架

### 時間框架

- **15m** - 15 分鐘
- **1h** - 1 小時

### 支援的幣種（範例）

| 幣種 | 符號 | 幣種 | 符號 |
|------|------|------|------|
| Bitcoin | BTCUSDT | Cardano | ADAUSDT |
| Ethereum | ETHUSDT | Solana | SOLUSDT |
| BNB | BNBUSDT | Ripple | XRPUSDT |
| XRP | XRPUSDT | Dogecoin | DOGEUSDT |
| Polkadot | DOTUSDT | Litecoin | LTCUSDT |

更多幣種請查看 [HuggingFace 資料集](https://huggingface.co/datasets/zongowo111/v2-crypto-ohlcv-data)。

## 輸出文件說明

下載的 CSV 檔案包含以下欄位：

| 欄位 | 說明 | 例子 |
|------|------|------|
| timestamp | 時間戳 | 2024-01-15 10:30:00 |
| open | 開盤價 | 42150.50 |
| high | 最高價 | 42580.75 |
| low | 最低價 | 41950.25 |
| close | 收盤價 | 42300.00 |
| volume | 交易量 | 1234567.89 |

### 檔案存儲位置

所有下載的文件預設存儲在 `crypto_data/` 目錄中：

```
crypto_data/
├── BTCUSDT_15m.csv
├── BTCUSDT_1h.csv
├── ETHUSDT_15m.csv
└── ...
```

## 常見任務

### 任務 1: 下載單個幣種的數據

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()
downloader.download_single_file('BTCUSDT', '15m')
```

### 任務 2: 批量下載多個幣種

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()

symbols = ['BTCUSDT', 'ETHUSDT', 'ADAUSDT', 'DOGEUSDT']
downloader.download_multiple_files(symbols, ['15m', '1h'])
```

### 任務 3: 合併同一幣種的不同時間框架

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()

# 先下載數據
downloader.download_single_file('BTCUSDT', '15m')
downloader.download_single_file('BTCUSDT', '1h')

# 合併數據
downloader.combine_csv_files('BTCUSDT', ['15m', '1h'])
# 輸出: crypto_data/BTCUSDT_combined.csv
```

### 任務 4: 使用 Pandas 分析下載的數據

```python
import pandas as pd
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()
downloader.download_single_file('BTCUSDT', '15m')

# 讀取 CSV 文件
df = pd.read_csv('crypto_data/BTCUSDT_15m.csv')

# 數據分析
print(f"行數: {len(df)}")
print(f"時間範圍: {df['timestamp'].min()} 到 {df['timestamp'].max()}")
print(f"最高價: {df['high'].max()}")
print(f"最低價: {df['low'].min()}")
print(f"平均成交量: {df['volume'].mean()}")

# 計算日收益率
df['return'] = ((df['close'] - df['open']) / df['open'] * 100).round(4)
print(df[['timestamp', 'open', 'close', 'return']].head(10))
```

### 任務 5: 構建簡單的回測策略

```python
import pandas as pd
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()
downloader.download_single_file('BTCUSDT', '15m')

df = pd.read_csv('crypto_data/BTCUSDT_15m.csv')

# 計算簡單移動平均線
df['SMA_20'] = df['close'].rolling(window=20).mean()
df['SMA_50'] = df['close'].rolling(window=50).mean()

# 生成交易信號
df['signal'] = 0
df.loc[df['SMA_20'] > df['SMA_50'], 'signal'] = 1  # 買入
df.loc[df['SMA_20'] < df['SMA_50'], 'signal'] = -1  # 賣出

print(df[['timestamp', 'close', 'SMA_20', 'SMA_50', 'signal']].head(100))
```

## API 快速參考

### 初始化

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader(repo_id="zongowo111/v2-crypto-ohlcv-data")
```

### 方法

#### `download_single_file(symbol, timeframe='15m', output_format='csv')`

下載單個幣種的數據。

**參數：**
- `symbol` (str): 幣種符號，如 'BTCUSDT'
- `timeframe` (str): 時間框架，'15m' 或 '1h'
- `output_format` (str): 輸出格式，'csv' 或 'parquet'

**返回：** 輸出文件路徑 (str)

#### `download_multiple_files(symbols, timeframes=None, output_format='csv')`

批量下載多個幣種的數據。

**參數：**
- `symbols` (List[str]): 幣種列表
- `timeframes` (List[str]): 時間框架列表，預設 ['15m', '1h']
- `output_format` (str): 輸出格式

**返回：** {key: path} 字典

#### `combine_csv_files(symbol, timeframes, output_filename=None)`

合併同一幣種的不同時間框架。

**參數：**
- `symbol` (str): 幣種符號
- `timeframes` (List[str]): 時間框架列表
- `output_filename` (str): 輸出檔案名稱

**返回：** 輸出文件路徑 (str)

#### `get_data_info(symbol, timeframe='15m')`

獲取數據的基本統計信息。

**參數：**
- `symbol` (str): 幣種符號
- `timeframe` (str): 時間框架

**返回：** 包含統計信息的字典

## 性能提示

1. **緩存利用**：第一次下載後，HuggingFace Hub 會在本地緩存數據，後續下載會更快。

2. **批量下載**：當下載多個幣種時，使用 `download_multiple_files()` 比逐個下載更有效率。

3. **輸出格式**：
   - CSV：易於閱讀和共享，但文件較大
   - Parquet：壓縮效率更好，適合大型數據集

4. **時間框架選擇**：
   - 短期交易：使用 15m 數據
   - 中期分析：使用 1h 數據
   - 數據合併：合併多時間框架進行多角度分析

## 故障排除

### 問題 1: "ModuleNotFoundError: No module named 'huggingface_hub'"

**解決方案**：重新安裝依賴

```bash
pip install --upgrade -r requirements.txt
```

### 問題 2: "FileNotFoundError" 或 "下載失敗"

**原因**：
- 幣種符號不正確
- HuggingFace Hub 連接問題
- 該幣種沒有該時間框架的數據

**解決方案**：
1. 確認幣種符號（需要包含 USDT）
2. 檢查網絡連接
3. 查看 [HuggingFace 資料集](https://huggingface.co/datasets/zongowo111/v2-crypto-ohlcv-data) 確認幣種可用性

### 問題 3: 下載速度很慢

**原因**：
- 網絡連接不穩定
- HuggingFace Hub 伺服器響應慢
- 數據文件很大

**解決方案**：
- 重試下載
- 使用更好的網絡連接
- 一次只下載必要的數據

## 進階用法

### 自定義輸出目錄

```python
from crypto_downloader import CryptoDataDownloader
from pathlib import Path

downloader = CryptoDataDownloader()
downloader.output_dir = Path('my_custom_folder')
downloader.output_dir.mkdir(exist_ok=True)

downloader.download_single_file('BTCUSDT', '15m')
```

### 轉換為 Parquet 格式

```python
from crypto_downloader import CryptoDataDownloader

downloader = CryptoDataDownloader()
downloader.download_single_file('BTCUSDT', '15m', output_format='parquet')
# 輸出: crypto_data/BTCUSDT_15m.parquet
```

## 資源連結

- [HuggingFace 資料集](https://huggingface.co/datasets/zongowo111/v2-crypto-ohlcv-data)
- [Pandas 文檔](https://pandas.pydata.org/docs/)
- [Python 官方文檔](https://docs.python.org/3/)

## 許可證

MIT License

## 支援與反饋

如有問題或建議，歡迎提交 Issue 或 Pull Request。
