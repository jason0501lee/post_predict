import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import time

# 設置頁面配置和效能優化
st.set_page_config(
    page_title="社群媒體貼文分析預測工具",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# 停用 Streamlit 的默認主題設定
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        .stToolbar {display:none;}
        .stSpinner > div > div {border-top-color: transparent;}
        .stApp > header {display:none;}
        .stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)

# 使用 st.cache_data 來快取數據
@st.cache_data(ttl=3600)
def get_preset_analyses():
    return PRESET_ANALYSES

@st.cache_data(ttl=3600)
def generate_trend_data(base_engagement):
    """生成未來7天的預測趨勢數據"""
    dates = pd.date_range(start=datetime.now(), periods=7, freq='D')
    trend = [base_engagement * (1 + random.uniform(-0.2, 0.3)) for _ in range(7)]
    return pd.DataFrame({
        '日期': dates,
        '預測互動率': trend
    })

@st.cache_data(ttl=3600)
def create_comparison_chart(original_metrics, optimized_metrics):
    """創建原始與優化後的比較圖表"""
    categories = ['互動率', '觀看數', '按讚數', '留言數', '分享數']
    
    fig = go.Figure(data=[
        go.Bar(name='原始貼文', x=categories, y=original_metrics, marker_color='lightblue'),
        go.Bar(name='優化後', x=categories, y=optimized_metrics, marker_color='lightgreen')
    ])
    
    fig.update_layout(
        barmode='group',
        title='貼文效果比較',
        xaxis_title='指標',
        yaxis_title='數值'
    )
    
    return fig

# 初始化 Faker
fake = Faker(['zh_TW'])

# 預設的分析結果
PRESET_ANALYSES = [
    {
        "engagement_rate": 4.8,
        "views": 15000,
        "likes": 720,
        "comments": 45,
        "shares": 25,
        "best_time": "晚上 8:00-9:00",
        "audience_age": "25-34歲 (45%), 18-24歲 (30%)",
        "audience_gender": "女性 (65%), 男性 (35%)",
        "favorite_content": ["生活風格", "美食分享", "旅遊探索"],
        "preferred_platforms": ["Instagram (65%)", "Facebook (25%)", "LINE (10%)"],
        "avg_reading_time": "1.5 分鐘",
        "audience_traits": ["重視生活品質", "喜歡分享", "追求新鮮體驗"],
        "recommended_tags": ["#生活日常", "#美食推薦", "#週末去哪玩"],
        "optimization_tips": [
            "建議在開頭加入更吸引人的鉤子",
            "可以加入更多相關的熱門標籤",
            "考慮在文末加入互動式問題"
        ],
        "sentiment": "正面"
    },
    {
        "engagement_rate": 3.9,
        "views": 12000,
        "likes": 580,
        "comments": 35,
        "shares": 18,
        "best_time": "下午 2:00-3:00",
        "audience_age": "18-24歲 (40%), 25-34歲 (35%)",
        "audience_gender": "男性 (55%), 女性 (45%)",
        "favorite_content": ["科技新知", "遊戲電競", "數位生活"],
        "preferred_platforms": ["YouTube (45%)", "Twitter (35%)", "Discord (20%)"],
        "avg_reading_time": "2.3 分鐘",
        "audience_traits": ["科技愛好者", "早期採用者", "喜歡深度內容"],
        "recommended_tags": ["#科技趨勢", "#數位生活", "#電競賽事"],
        "optimization_tips": [
            "建議增加更多視覺元素",
            "可以嘗試使用更簡潔的表達方式",
            "考慮加入當前熱門話題相關內容"
        ],
        "sentiment": "中性偏正面"
    },
    {
        "engagement_rate": 5.2,
        "views": 18000,
        "likes": 850,
        "comments": 62,
        "shares": 35,
        "best_time": "中午 12:00-1:00",
        "audience_age": "25-34歲 (50%), 35-44歲 (25%)",
        "audience_gender": "女性 (70%), 男性 (30%)",
        "favorite_content": ["時尚美妝", "健康養生", "心靈成長"],
        "preferred_platforms": ["Instagram (75%)", "Pinterest (15%)", "小紅書 (10%)"],
        "avg_reading_time": "1.8 分鐘",
        "audience_traits": ["注重外表", "追求健康", "樂於投資自我"],
        "recommended_tags": ["#穿搭分享", "#美妝保養", "#健康生活"],
        "optimization_tips": [
            "可以加入更多個人經驗分享",
            "建議使用更多表情符號增加親和力",
            "考慮製作系列內容增加追蹤度"
        ],
        "sentiment": "高度正面"
    },
    {
        "engagement_rate": 4.2,
        "views": 13500,
        "likes": 650,
        "comments": 40,
        "shares": 22,
        "best_time": "早上 10:00-11:00",
        "audience_age": "35-44歲 (40%), 25-34歲 (35%)",
        "audience_gender": "男性 (60%), 女性 (40%)",
        "favorite_content": ["財經投資", "職場發展", "產業分析"],
        "preferred_platforms": ["LinkedIn (50%)", "Facebook (30%)", "Twitter (20%)"],
        "avg_reading_time": "3.5 分鐘",
        "audience_traits": ["專業人士", "決策者", "注重效率"],
        "recommended_tags": ["#職場思維", "#投資理財", "#產業趨勢"],
        "optimization_tips": [
            "建議加入更多專業數據支持",
            "可以使用更多圖表說明",
            "考慮加入產業相關案例"
        ],
        "sentiment": "專業中性"
    },
    {
        "engagement_rate": 4.5,
        "views": 16000,
        "likes": 780,
        "comments": 52,
        "shares": 28,
        "best_time": "下午 5:00-6:00",
        "audience_age": "18-24歲 (45%), 25-34歲 (40%)",
        "audience_gender": "平均分配",
        "favorite_content": ["娛樂新聞", "音樂藝術", "生活娛樂"],
        "preferred_platforms": ["TikTok (55%)", "Instagram (35%)", "YouTube (10%)"],
        "avg_reading_time": "1.2 分鐘",
        "audience_traits": ["追求娛樂", "創意愛好者", "社交活躍"],
        "recommended_tags": ["#娛樂新聞", "#音樂分享", "#創意靈感"],
        "optimization_tips": [
            "可以加入更多趣味性元素",
            "建議使用更生動的描述方式",
            "考慮加入互動式投票或問卷"
        ],
        "sentiment": "活潑正面"
    }
]

def main():
    st.title("📊 AI 社群媒體貼文分析預測工具")
    
    # 使用 spinner 來提供更好的加載體驗
    with st.spinner('載入中...'):
        # 輸入區域
        with st.container():
            st.subheader("✍️ 請輸入要分析的貼文內容")
            post_content = st.text_area(
                "貼文內容",
                height=150,
                placeholder="在此輸入您想要分析的貼文內容..."
            )
            
            if st.button("開始分析", type="primary"):
                if post_content:
                    # 添加短暫延遲以避免過快重新導向
                    time.sleep(0.5)
                    
                    # 從快取中獲取分析結果
                    analysis = random.choice(get_preset_analyses())
                    
                    # 顯示分析結果
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("預測互動率", f"{analysis['engagement_rate']}%")
                    with col2:
                        st.metric("預測觀看數", f"{analysis['views']:,}")
                    with col3:
                        st.metric("預測按讚數", f"{analysis['likes']:,}")
                    with col4:
                        st.metric("預測留言數", f"{analysis['comments']:,}")
                    
                    # 使用快取的數據生成圖表
                    st.subheader("📈 未來7天互動率預測")
                    trend_data = generate_trend_data(analysis['engagement_rate'])
                    fig = px.line(trend_data, x='日期', y='預測互動率')
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # 比較圖
                    st.subheader("📊 優化效果比較")
                    original_metrics = [
                        analysis['engagement_rate'],
                        analysis['views'],
                        analysis['likes'],
                        analysis['comments'],
                        analysis['shares']
                    ]
                    optimized_metrics = [x * 1.2 for x in original_metrics]
                    comparison_fig = create_comparison_chart(original_metrics, optimized_metrics)
                    st.plotly_chart(comparison_fig, use_container_width=True)
                    
                    # 詳細分析報告
                    st.subheader("📝 詳細分析報告")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("### 📊 受眾分析")
                        st.write(f"**年齡分布：** {analysis['audience_age']}")
                        st.write(f"**性別分布：** {analysis['audience_gender']}")
                        st.write(f"**最佳發文時間：** {analysis['best_time']}")
                        st.write(f"**平均閱讀時間：** {analysis['avg_reading_time']}")
                        
                        st.markdown("#### 🎯 受眾特性")
                        st.write("**喜好文章類型：**")
                        for content_type in analysis['favorite_content']:
                            st.write(f"• {content_type}")
                            
                        st.write("**最常使用平台：**")
                        for platform in analysis['preferred_platforms']:
                            st.write(f"• {platform}")
                            
                        st.write("**受眾特性分布：**")
                        for trait in analysis['audience_traits']:
                            st.write(f"• {trait}")
                            
                        st.markdown("#### 🏷️ 建議標籤")
                        for tag in analysis['recommended_tags']:
                            st.write(f"• {tag}")
                        
                    with col2:
                        st.markdown("### 💡 優化建議")
                        for tip in analysis['optimization_tips']:
                            st.write(f"• {tip}")
                    
                    # 情感分析
                    st.subheader("🎯 內容情感分析")
                    st.write(f"整體情感傾向：**{analysis['sentiment']}**")
                    
                else:
                    st.warning("請輸入貼文內容後再進行分析")

if __name__ == "__main__":
    main() 