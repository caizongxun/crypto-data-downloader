"""
快速開始範例
演示如何使用 CryptoDataDownloader
"""

import sys
import pandas as pd
from pathlib import Path

# 確保能夠推統父目錄中的模組
sys.path.insert(0, str(Path(__file__).parent.parent))

from crypto_downloader import CryptoDataDownloader


def example_1_single_download():
    """
    例一：下載單一幣種的資料
    """
    print("\n" + "="*60)
    print("例一：下載單一幣種的資料")
    print("="*60)
    
    downloader = CryptoDataDownloader()
    
    # 下載 BTC 的 15 分鐘資料
    result = downloader.download_single_file('BTCUSDT', '15m')
    
    if result:
        print(f"\n下載成功！")
        print(f檔案位置: {result}")
        
        # 讀取 CSV 並沒有推靈
        df = pd.read_csv(result)
        print(f"\n資料統計：")
        print(f"  該檔案有 {len(df)} 行")
        print(f"  欄位： {', '.join(df.columns)}")
        print(f"\n前 5 行：")
        print(df.head())


def example_2_multiple_downloads():
    """
    例二：下載多個幣種
    """
    print("\n" + "="*60)
    print("例二：下載多個幣種")
    print("="*60)
    
    downloader = CryptoDataDownloader()
    
    # 下載多個幣種
    symbols = ['BTCUSDT', 'ETHUSDT']
    results = downloader.download_multiple_files(
        symbols,
        ['15m']  # 只下載 15 分鐘的資料
    )
    
    print(f"\n成功下載 {len(results)} 個檔案")
    for key, path in results.items():
        print(f"  - {key}: {path}")


def example_3_data_analysis():
    """
    例三：下載後的資料分析
    """
    print("\n" + "="*60)
    print("例三：資料分析")
    print("="*60)
    
    downloader = CryptoDataDownloader()
    
    # 獲取資料資訊
    info = downloader.get_data_info('BTCUSDT', '15m')
    
    if info:
        print(f"\n{info['symbol']} - {info['timeframe']} 資料資訊")
        print("-" * 60)
        for key, value in info.items():
            if key not in ['symbol', 'timeframe']:
                print(f"  {key:20s}: {value}")


def example_4_combine_data():
    """
    例四：合併同一幣種不同時間框架的資料
    """
    print("\n" + "="*60)
    print("例四：合併資料")
    print("="*60)
    
    downloader = CryptoDataDownloader()
    
    # 先確保資料已下載
    print("\n正在下載資料...")
    downloader.download_single_file('BTCUSDT', '15m')
    downloader.download_single_file('BTCUSDT', '1h')
    
    # 合併資料
    print("\n正在合併資料...")
    combined_path = downloader.combine_csv_files('BTCUSDT', ['15m', '1h'])
    
    if combined_path:
        print(f"\n合併成功！")
        
        # 讀取合併的資料
        df_combined = pd.read_csv(combined_path)
        print(f"\n合併後數據：")
        print(f"  總行數： {len(df_combined)}")
        print(f"  時間框架分佈：")
        print(df_combined['timeframe'].value_counts())
        print(f"\n時間範圍：")
        print(f"  上： {df_combined['timestamp'].min()}")
        print(f"  下： {df_combined['timestamp'].max()}")


def example_5_custom_analysis():
    """
    例五：自定義分析 - 計算收益率
    """
    print("\n" + "="*60)
    print("例五：自定義分析 - 計算收益率")
    print("="*60)
    
    downloader = CryptoDataDownloader()
    
    # 下載資料
    downloader.download_single_file('BTCUSDT', '15m')
    
    # 讀取資料
    df = pd.read_csv('crypto_data/BTCUSDT_15m.csv')
    
    # 計算收益率
    df['return'] = ((df['close'] - df['open']) / df['open'] * 100).round(4)
    
    print(f"\nBTC 15 分鐘資料分析：")
    print("-" * 60)
    print(f"  收益率統計")
    print(f"    平均： {df['return'].mean():.4f}%")
    print(f"    最大： {df['return'].max():.4f}%")
    print(f"    最小： {df['return'].min():.4f}%")
    print(f"    标准偏差： {df['return'].std():.4f}%")
    
    print(f"\n收益率分布（前乐10次）：")
    print(df[['timestamp', 'open', 'close', 'return']].head(10))


if __name__ == '__main__':
    """
    运行所有例子
    """
    
    try:
        # 例一：下載單一幣種
        example_1_single_download()
        
        # 例二：下載多個幣種
        # example_2_multiple_downloads()  # 解除注释以使用
        
        # 例三：資料資訊
        example_3_data_analysis()
        
        # 例四：合併資料
        # example_4_combine_data()  # 解除注释以使用
        
        # 例五：自定義分析
        example_5_custom_analysis()
        
        print("\n" + "="*60)
        print("所有例子完成！")
        print("="*60)
        
    except Exception as e:
        print(f"\n需爱。錯誤：{str(e)}")
        import traceback
        traceback.print_exc()
