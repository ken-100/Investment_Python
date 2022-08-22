# https://hk29.hatenablog.jp/entry/2021/07/13/231356

import os
import pandas as pd

# 容量の表記フォーマットを変換する関数
def convert_format_size_func(file_size):
    # 表記フォーマットを辞書で作成
    bit = { "KB": 10, "MB": 20, "GB": 30, "TB": 40}
    # 辞書のキーと値をループで順次、取得する
    for unit, bit_shift in bit.items():
        # ビット変換
        val = file_size / float(1 << bit_shift)
        if val < 1000:
            break # 1000未満になったらループを抜ける
        
    return "{:,.1f}".format(val) + " " + unit


# フォルダ（ディレクトリ）の容量を抽出する関数
def get_dir_size_func(path='.'):
    sum = 0
    with os.scandir(path) as it:
        for entry in it:
            # ファイルがあった場合にファイルサイズを取得
            if entry.is_file():
                sum += entry.stat().st_size
            # サブフォルダを探索する場合
            elif entry.is_dir():
                sum += get_dir_size_func(entry.path)
    return sum


def main():
    # 指定パス以下のフォルダを探索して、容量をリストへ格納する
    dir_size_list = []
    for entry in os.scandir(my_path):
        if entry.is_file():
            pass
        else:
            my_size = get_dir_size_func(entry)
            dir_size_list.append([my_size, entry.path])

    # pandasデータフレーム形式にする
    df = pd.DataFrame(dir_size_list, columns = ['size', 'path'])
    # ファイルサイズでソート（並び替え）する
    df_s = df.sort_values(['size'], ascending=False)
    # ファイルサイズの列をリスト化する
    my_size_list = df_s['size'].to_list()
    
    # ファイルサイズの表記フォーマットを変換してリストに格納する
    my_new_size_list = []
    for my_size in my_size_list:
        my_new_size = convert_format_size_func(my_size)
        my_new_size_list.append(my_new_size)
    
    # 作成したリストをファイルサイズの列に上書きする
    df_s['size'] = my_new_size_list
    df_s['path'] = df_s['path'].replace(my_path, '', regex=True)
    print(df_s)
    
    # csvファイルに保存する   
    pd.DataFrame(df_s).to_csv('test.csv', encoding='utf_8_sig')
    
    
if __name__ == '__main__':
    my_path = "//localhost/C$/blp"
    
    main()
    print("finished")
