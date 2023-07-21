import streamlit as st
import pandas as pd


def main():
    st.title("データ分析アプリ")

    # ファイルのアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

    if uploaded_file is not None:
        # DataFrameへの読み込み
        df = pd.read_csv(uploaded_file)

        # データの先頭を表示
        st.subheader("データの先頭")
        st.write(df.head())

        # データの行数を表示
        num_rows = st.slider("表示する行数を選択してください", 1, len(df), len(df))

        # 選択された行数だけデータを表示
        st.subheader(f"データの先頭 {num_rows} 行")
        st.write(df.head(num_rows))


if __name__ == "__main__":
    main()
