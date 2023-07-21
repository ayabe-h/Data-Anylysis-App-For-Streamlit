import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    st.title("データ分析アプリ")

    # ファイルのアップロード
    uploaded_file = st.file_uploader("CSVファイルをアップロードしてください", type=["csv"])

    if uploaded_file is not None:
        # DataFrameへの読み込み
        df = pd.read_csv(uploaded_file)

        # データの行数を取得
        num_rows = len(df)

        # データの先頭と行数を表示
        st.subheader(f"データの先頭")
        st.write(df.head())

        # データの総行数を表示
        st.write(f"### データの総行数 : {num_rows}")

        # 上限・下限の初期値を設定
        min_value = 0
        max_value = min(5, num_rows)

        # テキストボックスからの入力を受け取る
        min_input = st.text_input("最小行数を入力してください", min_value)
        max_input = st.text_input("最大行数を入力してください", max_value)

        # テキストボックスの入力を整数に変換して範囲内に制限
        try:
            min_input = int(min_input)
            min_value = max(min_input, 0)
        except ValueError:
            st.warning("最小行数には数字を入力してください。")

        try:
            max_input = int(max_input)
            max_value = min(max_input, num_rows)
        except ValueError:
            st.warning("最大行数には数字を入力してください。")

        # 選択された行数だけデータを表示
        st.subheader(f"データの先頭 {min_value} から {max_value} 行")
        st.write(df.iloc[min_value:max_value])

        # 列のカラム名を取得
        column_names = df.columns.tolist()
        # 列を選択するドロップダウンメニューを表示
        selected_column = st.selectbox("列を選択してください", column_names)

        st.subheader(f"{selected_column} の分布")
        fig, ax = plt.subplots()
        sns.histplot(df[selected_column], ax=ax)
        st.pyplot(fig)

        st.write(f"欠損値の数：{df[selected_column].isnull().sum()}")
        st.write(f"データの型：{df[selected_column].dtype}")

        try:
            # 選択した列が数値の場合のみ統計情報を表示
            if not df[selected_column].apply(lambda x: isinstance(x, str)).all():
                st.subheader(f"{selected_column} の統計情報")
                st.write(f"最小値：{df[selected_column].min()}")
                st.write(f"最大値：{df[selected_column].max()}")
                st.write(f"中央値：{df[selected_column].median()}")
                st.write(f"平均値：{df[selected_column].mean()}")
                st.write(f"最頻値：{df[selected_column].mode().iloc[0]}")

        except ValueError as e:
            # 数値に変換できなかった場合はエラーメッセージを表示
            st.write(f"エラー：{e}")

        # 列を2つ選択するドロップダウンメニューを表示
        selected_columns = st.multiselect("## 列を2つ選択してください", column_names)

        if len(selected_columns) == 2:
            try:
                # 選択した2つの列の要素が数値の場合には散布図を表示
                if (
                    not df[selected_columns]
                    .apply(lambda x: isinstance(x, str))
                    .any()
                    .any()
                ):
                    st.subheader("散布図")
                    fig, ax = plt.subplots()
                    sns.scatterplot(
                        data=df, x=selected_columns[0], y=selected_columns[1], ax=ax
                    )
                    st.pyplot(fig)
                    # 選択した2つの列の相関係数を計算し、表示
                    st.subheader("相関係数")
                    correlation_coefficient = df[selected_columns].corr().iloc[0, 1]
                    st.write(
                        f"{selected_columns[0]} と {selected_columns[1]} の相関係数：{correlation_coefficient}"
                    )
                else:
                    st.write("選択した列の要素は数値ではありません。数値の列を2つ選択してください。")
            except ValueError:
                st.warning("数値データではありません")
        else:
            st.write("2つの列を選択してください。")


if __name__ == "__main__":
    main()
