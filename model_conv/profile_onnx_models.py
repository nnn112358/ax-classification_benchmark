import os
import glob
import re
import pandas as pd

def extract_macs_from_file(file_path):
    """テキストファイルからTotal MACsの値を抽出する"""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Total行を探す
        total_match = re.search(r'Total\s+_\s+([\d,]+)\s+100%', content)
        if total_match:
            # カンマを取り除いて数値に変換
            macs_str = total_match.group(1).replace(',', '')
            try:
                return float(macs_str)
            except ValueError:
                print(f"警告: {file_path} で数値変換エラー: {macs_str}")
                return None
        else:
            print(f"警告: {file_path} でTotal行が見つかりませんでした")
            return None
    except Exception as e:
        print(f"エラー ({file_path}): {str(e)}")
        return None

def collect_macs_from_txt_files(directory_path):
    """指定ディレクトリ内のすべてのテキストファイルからMACsを収集する"""
    # .txtファイルの一覧を取得
    txt_files = glob.glob(os.path.join(directory_path, "*.txt"))
    
    if not txt_files:
        print(f"指定されたディレクトリ '{directory_path}' にテキストファイルが見つかりませんでした。")
        return
    
    results = []
    
    for txt_file in txt_files:
        base_name = os.path.basename(txt_file)
        model_name = base_name.replace('.txt', '.onnx')
        
        # ファイルからMACsを抽出
        macs = extract_macs_from_file(txt_file)
        
        # 結果を保存
        results.append({
            'model_name': model_name,
            'forward_macs': macs
        })
    
    # 結果をDataFrameに変換
    df = pd.DataFrame(results)
    
    # CSVファイルに保存
    csv_path = os.path.join(directory_path, "onnx_models_macs_summary.csv")
    df.to_csv(csv_path, index=False)
    print(f"\n結果が {csv_path} に保存されました。")
    
    # 結果をコンソールに表示
    print("\nモデル別MACsの概要:")
    for idx, row in df.iterrows():
        macs_str = f"{row['forward_macs']:,.0f}" if pd.notna(row['forward_macs']) else "N/A"
        tops_str = f"{row['forward_macs'] * 2 / 1e12:.2f}" if pd.notna(row['forward_macs']) else "N/A"
        print(f"{row['model_name']}: {macs_str} MACs ({tops_str} TOPS @ 1秒)")
    
    return df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        directory_path = sys.argv[1]
    else:
        directory_path = "models"  # デフォルトのディレクトリパス
    
    collect_macs_from_txt_files(directory_path)