import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
import numpy as np
import os
import io
import chardet

def set_korean_font(font_path):
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rc('font', family=font_name)
        plt.rcParams['axes.unicode_minus'] = False
        return font_name
    else:
        st.warning(f"⚠️ 폰트 경로가 잘못됨: {font_path}")
        return None

font_path = 'PretendardVariable.ttf'
set_korean_font(font_path)

st.title("점수 분포 시각화 및 예측 프로그램")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

def read_csv_auto_encoding(file):
    raw = file.read()
    enc = chardet.detect(raw)['encoding']
    file.seek(0)
    return pd.read_csv(io.BytesIO(raw), encoding=enc)

if uploaded_file is not None:
    df = read_csv_auto_encoding(uploaded_file)
    score_col = st.selectbox("점수 컬럼을 선택하세요", df.columns)
    cutoff = st.number_input("최소 점수(컷오프)", value=22)
    # --- 결측치/문자/이상값 제거 ---
    df[score_col] = pd.to_numeric(df[score_col], errors='coerce')
    scores = df[score_col].dropna()
    scores = scores[(scores >= cutoff) & (scores <= 50)]
    scores = scores.astype(int)

    mean_score = scores.mean()
    median_score = scores.median()
    cut_1 = np.percentile(scores, 100 - 8)
    cut_2 = np.percentile(scores, 100 - 20)
    cut_3 = np.percentile(scores, 100 - 50)

    st.markdown(f"""
    ### 📊 현장 수강생 기반 등급컷 예상 [N수생 보정]  
    - **예상 1등급 컷**: {cut_1:.1f}점  
    - **예상 2등급 컷**: {cut_2:.1f}점  
    - **예상 3등급 컷**: {cut_3:.1f}점
    """)

    fig, ax = plt.subplots(figsize=(8,6))
    sns.histplot(scores, bins=25, color="#7DBAFF", alpha=0.6, edgecolor='k', stat='density', label='히스토그램', ax=ax)
    sns.kdeplot(scores, color="#FF96A2", linewidth=2, label='분포 곡선', ax=ax)
    ax.set_xlabel('점수')
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_title("점수 분포")
    ax.legend()

    textstr = f"평균: {mean_score:.2f}\n중앙값: {median_score:.2f}\n"
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=13, va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))
"""
    cutstr = (
        f"예상 1등급컷: {int(cut_1)}점\n"
        f"예상 2등급컷: {int(cut_2)}점\n"
        f"예상 3등급컷: {int(cut_3)}점"
    )
    ax.text(0.02, 0.82, cutstr, transform=ax.transAxes, fontsize=13, va='top', ha='left',
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray'))
    ax.axvline(cut_1, color='#FFBB00', linestyle='--', linewidth=2, label='1등급컷')
    ax.axvline(cut_2, color='#FF8700', linestyle='--', linewidth=2, label='2등급컷')
    ax.axvline(cut_3, color='#FF2E00', linestyle='--', linewidth=2, label='3등급컷')
    ax.legend()
"""
    st.pyplot(fig)
