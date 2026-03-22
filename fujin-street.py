import streamlit as st
import pandas as pd
import os
import datetime # 提前准备好时间工具箱，我们马上要用到！

# ==================== 1. 页面基本设置与样式 ====================
st.set_page_config(
    page_title="湖映福津·合伙“邻”距离",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入自定义 CSS 样式 (清爽淡蓝风，并统一字体)
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Microsoft YaHei", sans-serif !important;
    }
    .blue-card {
        background-color: #F0F8FF;
        border: 1px solid #CCE5FF;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        color: #333333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== 2. 自定义页眉 ====================
st.markdown(
    """
    <div style="background-color:#E81123;padding:10px;border-radius:5px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;font-size:28px;margin:0;">
            ☭ 党建引领 · 湖光社区
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("湖映福津·合伙“邻”距离 🏘️")
st.warning("⚠️ **公告**：本网站当前处于【建设调试阶段】。部分商户信息、地图坐标及活动内容正在陆续完善中，仅供样板展示。")

# ==================== 3. 数据加载 ====================
@st.cache_data
def load_data():
    file_path = "fujin.xlsx"
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            df_map = df.dropna(subset=['lat', 'lon'])
            return df, df_map
        except Exception as e:
            st.error(f"读取 Excel 文件出错: {e}")
            return None, None
    else:
        st.error("⚠️ 未找到 'fujin.xlsx' 文件。")
        return None, None

df_shops, df_for_map = load_data()

# ==================== 4. 导航标签页 ====================
tab1, tab2, tab3 = st.tabs(["🏪 街区商户与地图", "👴 老干部“四就近”", "📢 街铺招租区"])

# --- 标签页 1：商户与地图 ---
with tab1:
    if df_shops is not None:
        left_col, right_col = st.columns([1, 1])

        with left_col:
            st.subheader("🏪 商户搜索与名录")
            search_text = st.text_input("🔍 输入店名模糊搜索")
            
            category = "全部"
            if '类型' in df_shops.columns:
                available_types = ["全部"] + sorted(df_shops['类型'].dropna().unique().tolist())
                category = st.selectbox("📁 按类型筛选", available_types)

            filtered_df = df_shops.copy()
            if search_text:
                filtered_df = filtered_df[filtered_df["店名"].str.contains(search_text, na=False)]
            if category != "全部":
                filtered_df = filtered_df[filtered_df["类型"] == category]

            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            
        with right_col:
            st.subheader("📍 街区便民地图")
            if df_for_map is not None and not df_for_map.empty:
                map_filtered = df_for_map.copy()
                if search_text:
                    map_filtered = map_filtered[map_filtered["店名"].str.contains(search_text, na=False)]
                if category != "全部":
                    map_filtered = map_filtered[map_filtered["类型"] == category]
                
                if not map_filtered.empty:
                    st.map(map_filtered, use_container_width=True)
                else:
                    st.info("当前筛选条件下无地图坐标数据。")

        # 明星店铺展示区 (已换上新衣服)
        st.divider() 
        st.subheader("🌟 街区合伙人明星店铺展示")
        showcase_col1, showcase_col2, showcase_col3 = st.columns(3)
        with showcase_col1:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo")
            st.markdown('<div class="blue-card"><b>福津包子铺</b><br>社区老字号，对老人有专属优惠！</div>', unsafe_allow_html=True)
        with showcase_col2:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo")
            st.markdown('<div class="blue-card"><b>老李五金店</b><br>响应速度快，上门维修价格公道。</div>', unsafe_allow_html=True)
        with showcase_col3:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo")
            st.markdown('<div class="blue-card"><b>社区智慧微食堂</b><br>干净卫生，年轻人的共享厨房。</div>', unsafe_allow_html=True)

# --- 标签页 2：老干部“四就近” ---
with tab2:
    st.header("👴 银发赋能·“四就近”活动台")
    st.info("🚧 此模块主要内容正在建设中...")
    with st.expander("📚 [建设中] 就近学习：智能手机防诈骗讲座"):
        st.write("**拟定时间**：待定\n\n**地点**：湖光社区党群服务中心")

# --- 标签页 3：招租与合作 (已换上新衣服并修改文字) ---
with tab3:
    st.header("📢 优质商铺招租")
    st.markdown("寻找社区合伙人，共同激发街区活力！*(此部分为样板，仅供展示)*")
    
    rent_col1, rent_col2 = st.columns(2)
    with rent_col1:
        st.markdown(
            """
            <div class="blue-card">
                <h4 style="margin-top:0;">🏠 福津街 12 号 (原便利店)</h4>
                <ul style="padding-left: 20px;">
                    <li><b>面积</b>：50 平方米</li>
                    <li><b>优势</b>：临近街口，人流量大。</li>
                    <li><b>状态</b>：空置中</li>
                    <li><b>联系人</b>：邓小姐 (13xxxxxxxxx)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )
    with rent_col2:
        st.markdown(
            """
            <div class="blue-card">
                <h4 style="margin-top:0;">🏠 福津街 28 号二楼</h4>
                <ul style="padding-left: 20px;">
                    <li><b>面积</b>：120 平方米</li>
                    <li><b>优势</b>：采光极佳，适合做工作室或活动室。</li>
                    <li><b>状态</b>：空置中</li>
                    <li><b>联系人</b>：邓小姐 (13xxxxxxxxx)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )

# ==================== 5. 自定义页脚 ====================
st.divider()
st.markdown("### 🤝 社区合伙人招募")
footer_col1, footer_col2 = st.columns([2, 1])

with footer_col1:
    st.markdown(
        """
        <br>
        <p style="font-size: 18px; font-weight: bold; color: #333;">
            欢迎添加湖光社区网格员小郑微信，加入合伙人！
        </p>
        """, unsafe_allow_html=True
    )

with footer_col2:
    qr_filename = "Screenshot_20260322_230743_com.tencent.mm_edit_4401257242557.jpg"
    if os.path.exists(qr_filename):
        st.image(qr_filename, caption="网格员小郑微信", width=200)
    else:
        st.caption("(⚠️ 未找到二维码图片)")
