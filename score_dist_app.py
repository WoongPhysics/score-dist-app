import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import numpy as np

def set_korean_font(font_path):
    if os.path.exists(font_path):
        fontprop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=fontprop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return fontprop.get_name()
    else:
        print("폰트 경로가 잘못됨:", font_path)
        return None
    
font_path = './fonts/PretendardVariable.ttf'
set_korean_font(font_path)

st.title("점수 분포 시각화 및 예측 프로그램")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    score_col = st.selectbox("점수 컬럼을 선택하세요", df.columns)
    cutoff = st.number_input("최소 점수(컷오프)", value=22)
    scores = df[df[score_col] >= cutoff][score_col]

    # --- 평균/중앙값, 등급컷 계산 ---
    mean_score = scores.mean()
    median_score = scores.median()
    cut_1 = np.percentile(scores, 100 - 8)   # 상위 8% (1등급)
    cut_2 = np.percentile(scores, 100 - 20)  # 상위 20% (2등급)
    cut_3 = np.percentile(scores, 100 - 50)  # 상위 50% (3등급)

    # --- 그래프 ---
    fig, ax = plt.subplots(figsize=(8,6))
    sns.histplot(scores, bins=25, color="#7DBAFF", alpha=0.6, edgecolor='k', stat='density', label='히스토그램', ax=ax)
    sns.kdeplot(scores, color="#FF96A2", linewidth=2, label='분포 곡선', ax=ax)
    ax.set_xlabel('점수')
    ax.set_ylabel('')
    ax.set_yticks([])
    ax.set_title("점수 분포")
    ax.legend()

    # 평균/중앙값 텍스트 (좌상단)
    textstr = f"평균: {mean_score:.2f}\n중앙값: {median_score:.2f}\n"
    ax.text(
        0.02, 0.98, textstr, transform=ax.transAxes,
        fontsize=13, va='top', ha='left',
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray')
    )

    # 등급컷 안내 (평균/중앙값 아래)
    cutstr = (
    f"상위 8% (1등급컷): {int(cut_1)}점\n"
    f"상위 20% (2등급컷): {int(cut_2)}점\n"
    f"상위 50% (3등급컷): {int(cut_3)}점"
)
    ax.text(
        0.02, 0.82, cutstr, transform=ax.transAxes,
        fontsize=13, va='top', ha='left',
        bbox=dict(facecolor='white', alpha=0.5, edgecolor='gray')
    )

    # 등급컷 라인 그리기
    ax.axvline(cut_1, color='#FFBB00', linestyle='--', linewidth=2, label='1등급컷')
    ax.axvline(cut_2, color='#FF8700', linestyle='--', linewidth=2, label='2등급컷')
    ax.axvline(cut_3, color='#FF2E00', linestyle='--', linewidth=2, label='3등급컷')
    ax.legend()

    st.pyplot(fig)

    # 표로도 안내
    st.markdown(f"""
    ### 📊 집단 상위 등급컷(%) [N수생 보정]  
    - **1등급**: {cut_1:.1f}점  
    - **2등급**: {cut_2:.1f}점  
    - **3등급**: {cut_3:.1f}점
    """)
    
    