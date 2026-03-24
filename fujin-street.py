import streamlit as st
import pandas as pd
import os
import datetime

# ==================== 1. 页面基本设置与样式 ====================
st.set_page_config(
    page_title="湖映福津·合伙“邻”距离",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* 🚨 强力隐藏顶部导航条和基础页脚 */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    
    /* 🚨 强力隐藏右下角的云平台悬浮水印 (拦截所有指向官方的链接元素) */
    a[href^="https://streamlit.io"] {display: none !important;}
    div[class^="viewerBadge"] {display: none !important;}
    
    /* 🚨 微信排版修复：禁止微信自动放大字体，限制最大宽度防止横向溢出变形 */
    html, body, [class*="css"]  {
        -webkit-text-size-adjust: 100% !important; 
        text-size-adjust: 100% !important;
        max-width: 100vw;
        overflow-x: hidden;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
        background-color: #f7f8fa; 
    }
    
    .clean-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        color: #333333;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        border: none;
    }
    
    h4 { margin-top: 0; color: #1a1a1a; font-weight: 600; }
    ul { padding-left: 20px; color: #555555; font-size: 14px; }
    li { margin-bottom: 6px; }
    </style>
    """,
    unsafe_allow_html=True
)

# ==================== 2. 自定义页眉 ====================
st.markdown(
    """
    <div style="background-color:#E81123;padding:12px;border-radius:8px;margin-bottom:20px;box-shadow: 0 2px 8px rgba(232,17,35,0.2);">
        <h1 style="color:white;text-align:center;font-size:24px;margin:0;letter-spacing:1px;">
            ☭ 党建引领 · 湖光社区
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("湖映福津·合伙“邻”距离 🏘️")
st.info("⚠️ **公告**：本网站当前处于【建设调试阶段】。部分数据仅供样板展示。")

# ==================== 3. 主页 C 位：环境卫士行动 ====================
st.markdown(
    """
    <div style="background-color: #fff0f0; border-left: 6px solid #E81123; padding: 16px; border-radius: 8px; margin-bottom: 24px; box-shadow: 0 2px 6px rgba(232,17,35,0.1);">
        <h3 style="margin-top:0; color:#E81123; font-size: 20px;">📸 福津大街“环境卫士”行动</h3>
        <p style="color:#555; font-size:15px; margin-bottom: 16px;">发现垃圾落地、小广告等脏乱差现象？请拍下来发给我们，社区网格员将第一时间跟进处理！</p>
        <a href="https://wj.qq.com/s2/26097409/c8ed/" target="_self" style="display: block; text-align: center; background-color: #E81123; color: white; padding: 12px 15px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px;">👉 点击上传图片</a>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================== 4. 数据加载与时间魔法 ====================
def get_shop_status(hours_str):
    if pd.isna(hours_str) or str(hours_str).strip() == '':
        return "⚪ 未知"
    try:
        now = datetime.datetime.now().time()
        current_time_mins = now.hour * 60 + now.minute
        
        periods = str(hours_str).replace('，', ',').split(',')
        for p in periods:
            start_str, end_str = p.split('-')
            start_h, start_m = map(int, start_str.split(':'))
            end_h, end_m = map(int, end_str.split(':'))
            
            start_mins = start_h * 60 + start_m
            end_mins = end_h * 60 + end_m
            
            if start_mins <= current_time_mins <= end_mins:
                return "🟢 营业中"
        return "🔴 已休息"
    except Exception:
        return "⚠️ 格式错误"

@st.cache_data
def load_data():
    file_path = "fujin.xlsx"
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path)
            
            if '营业时间' in df.columns:
                df['当前状态'] = df['营业时间'].apply(get_shop_status)
                
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

# ==================== 5. 导航标签页 ====================
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

        st.divider() 
        st.subheader("🌟 街区合伙人明星店铺展示")
        showcase_col1, showcase_col2, showcase_col3 = st.columns(3)
        with showcase_col1:
            st.markdown('<div class="clean-card"><h4>🥟 福津包子铺</h4><p style="color:#666;font-size:14px;">社区老字号，对老人有专属优惠！</p></div>', unsafe_allow_html=True)
        with showcase_col2:
            st.markdown('<div class="clean-card"><h4>🔧 老李五金店</h4><p style="color:#666;font-size:14px;">响应速度快，上门维修价格公道。</p></div>', unsafe_allow_html=True)
        with showcase_col3:
            st.markdown('<div class="clean-card"><h4>🥗 社区智慧微食堂</h4><p style="color:#666;font-size:14px;">干净卫生，年轻人的共享厨房。</p></div>', unsafe_allow_html=True)

# --- 标签页 2：老干部“四就近” ---
with tab2:
    st.header("👴 银发赋能·“四就近”活动台")
    st.markdown('<div class="clean-card"><h4>📚 [建设中] 就近学习：智能手机防诈骗讲座</h4><ul><li><b>拟定时间</b>：待定</li><li><b>地点</b>：湖光社区党群服务中心</li></ul></div>', unsafe_allow_html=True)

# --- 标签页 3：招租与合作 ---
with tab3:
    st.header("📢 优质商铺招租")
    st.markdown("寻找社区合伙人，共同激发街区活力！*(此部分为样板，仅供展示)*")
    
    rent_col1, rent_col2 = st.columns(2)
    with rent_col1:
        st.markdown(
            """
            <div class="clean-card">
                <h4>🏠 福津街 12 号 (原便利店)</h4>
                <ul>
                    <li><b>面积</b>：50 平方米</li>
                    <li><b>优势</b>：临近街口，人流量大。</li>
                    <li><b>状态</b>：<span style="color:#E81123;font-weight:bold;">空置中</span></li>
                    <li><b>联系人</b>：邓小姐 (13xxxxxxxxx)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )
    with rent_col2:
        st.markdown(
            """
            <div class="clean-card">
                <h4>🏠 福津街 28 号二楼</h4>
                <ul>
                    <li><b>面积</b>：120 平方米</li>
                    <li><b>优势</b>：采光极佳，适合做工作室。</li>
                    <li><b>状态</b>：<span style="color:#E81123;font-weight:bold;">空置中</span></li>
                    <li><b>联系人</b>：邓小姐 (13xxxxxxxxx)</li>
                </ul>
            </div>
            """, unsafe_allow_html=True
        )

# ==================== 6. 自定义页脚 ====================
st.markdown("### 🤝 社区合伙人招募")
footer_col1, footer_col2 = st.columns([2, 1])

with footer_col1:
    st.markdown("<p style='font-size: 16px; color: #555; margin-top:20px;'>欢迎添加湖光社区网格员微信，加入街区合伙人共治计划！</p>", unsafe_allow_html=True)

with footer_col2:
    qr_filename = "Screenshot_20260322_230743_com.tencent.mm_edit_4401257242557.jpg"
    if os.path.exists(qr_filename):
        st.image(qr_filename, width=150)
