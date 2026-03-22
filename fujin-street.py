import streamlit as st
import pandas as pd
import os

# ==================== 1. 页面基本设置 (开启宽屏自适应) ====================
st.set_page_config(
    page_title="湖映福津·合伙“邻”距离",
    page_icon="🏘️",
    layout="wide", # 关键：开启电脑端宽屏模式，手机端自动折叠
    initial_sidebar_state="collapsed"
)

# ==================== 2. 自定义页眉 (党建引领与社区名) ====================
# 使用 HTML 样式制作红底白字的党建页眉
st.markdown(
    """
    <div style="background-color:#E81123;padding:10px;border-radius:5px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;font-size:28px;margin:0;">
            ☭ 党建引领 · 湖光社区
        </h1>
        <p style="color:white;text-align:center;margin:5px 0 0 0;font-size:16px;">
            Huguang Community: Party-building Leadership
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.title("湖映福津·合伙“邻”距离 🏘️")

# --- 网站建设中公告 ---
st.warning("⚠️ **公告**：本网站当前处于【建设调试阶段】。部分商户信息、地图坐标及活动内容正在陆续完善中，仅供样板展示。")


# ==================== 3. 数据加载 (读取真实 fujin.xlsx) ====================
@st.cache_data # 添加缓存，提高加载速度
def load_data():
    file_path = "fujin.xlsx"
    if os.path.exists(file_path):
        try:
            # 尝试读取 Excel
            df = pd.read_excel(file_path)
            # 确保经纬度列是数字格式，防止报错
            df['lat'] = pd.to_numeric(df['lat'], errors='coerce')
            df['lon'] = pd.to_numeric(df['lon'], errors='coerce')
            # 移除没有坐标的行用于地图展示
            df_map = df.dropna(subset=['lat', 'lon'])
            return df, df_map
        except Exception as e:
            st.error(f"读取 Excel 文件出错: {e}")
            return None, None
    else:
        st.error("⚠️ 未找到 'fujin.xlsx' 文件。请确保该文件已上传到 GitHub 仓库的最外层。")
        return None, None

df_shops, df_for_map = load_data()


# ==================== 4. 建立顶部导航标签页 📑 ====================
tab1, tab2, tab3 = st.tabs(["🏪 街区商户与地图", "👴 老干部“四就近”", "📢 街铺招租区"])

# ==================== 标签页 1：商户与地图 (响应式布局) ====================
with tab1:
    if df_shops is not None:
        # 🟢 魔法：使用 st.columns 在电脑端分栏，手机端自动堆叠
        left_col, right_col = st.columns([1, 1]) # 比例 1:1

        with left_col:
            st.subheader("🏪 商户搜索与名录")
            
            # 搜索与筛选交互
            search_col, category_col = st.columns(2)
            with search_col:
                search_text = st.text_input("🔍 输入店名模糊搜索")
            with category_col:
                # 获取表格中所有的类型用于下拉菜单
                if '类型' in df_shops.columns:
                    available_types = ["全部"] + sorted(df_shops['类型'].dropna().unique().tolist())
                    category = st.selectbox("📁 按类型筛选", available_types)
                else:
                    category = "全部"
                    st.warning("Excel表格中缺少'类型'列")

            # 数据过滤逻辑
            filtered_df = df_shops.copy()
            if search_text:
                filtered_df = filtered_df[filtered_df["店名"].str.contains(search_text, na=False)]
            if category != "全部":
                filtered_df = filtered_df[filtered_df["类型"] == category]

            # 展示过滤后的表格
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
            st.caption(f"当前显示 {len(filtered_df)} 家商户")
            
        with right_col:
            st.subheader("📍 街区便民地图")
            # 地图只显示有坐标的数据
            if df_for_map is not None and not df_for_map.empty:
                # 再次过滤地图数据，使其与表格搜索同步
                map_filtered = df_for_map.copy()
                if search_text:
                    map_filtered = map_filtered[map_filtered["店名"].str.contains(search_text, na=False)]
                if category != "全部":
                    map_filtered = map_filtered[map_filtered["类型"] == category]
                
                if not map_filtered.empty:
                    st.map(map_filtered, use_container_width=True)
                else:
                    st.info("当前筛选条件下无地图坐标数据。")
            else:
                st.info("表格中未检测到有效经纬度(lat/lon)数据，无法显示地图。")

        # --- 明星店铺展示区 (占全宽) ---
        st.divider() 
        st.subheader("🌟 街区合伙人明星店铺展示")
        st.markdown("*(注：此部分内容当前为样板，后续将替换为真实店铺风采照片)*")
        showcase_col1, showcase_col2, showcase_col3 = st.columns(3)
        with showcase_col1:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo", caption="店铺招牌图样例")
            st.info("**福津包子铺**\n\n社区老字号，对老人有专属优惠！")
        with showcase_col2:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo", caption="店铺招牌图样例")
            st.success("**老李五金店**\n\n响应速度快，上门维修价格公道。")
        with showcase_col3:
            st.image("https://via.placeholder.com/300x200.png?text=Shop+Photo", caption="店铺招牌图样例")
            st.warning("**社区智慧微食堂**\n\n干净卫生，年轻人的共享厨房。")

# ==================== 标签页 2：老干部“四就近” (建设中) ====================
with tab2:
    st.header("👴 银发赋能·“四就近”活动台")
    st.markdown("就近学习、就近活动、就近得到关心照顾、就近发挥作用。")
    st.info("🚧 此模块主要内容正在建设中...")
    
    with st.expander("📚 [建设中] 就近学习：智能手机防诈骗讲座"):
        st.write("**拟定时间**：待定\n\n**地点**：湖光社区党群服务中心")
    with st.expander("🎨 [建设中] 就近活动：社区秋季书画展"):
        st.write("即将开展，敬请期待...")

# ==================== 标签页 3：招租与合作 (联系人更新) ====================
with tab3:
    st.header("📢 优质商铺招租")
    st.markdown("寻找社区合伙人，共同激发街区活力！(联系人已更新)")
    
    # 使用 st.error 和 st.warning 制作醒目的招租卡片
    rent_col1, rent_col2 = st.columns(2)
    
    with rent_col1:
        st.error(
            """
            🏠 **福津街 12 号 (原便利店)**
            
            - **面积**：50 平方米
            - **优势**：临近街口，人流量大。
            - **状态**：空置中
            - **意向联系人**：邓小姐 (13xxxxxxxxx)
            """
        )
        
    with rent_col2:
        st.warning(
            """
            🏠 **福津街 28 号二楼**
            
            - **面积**：120 平方米
            - **优势**：采光极佳，适合做工作室或活动室。
            - **状态**：空置中
            - **意向联系人**：邓小姐 (13xxxxxxxxx)
            """
        )

# ==================== 5. 自定义页脚 (网格员联系方式) ====================
st.divider() # 添加一条全宽分割线
st.markdown("### 🤝 社区合伙人招募")

footer_col1, footer_col2 = st.columns([2, 1]) # 文字占 2/3，图片占 1/3

with footer_col1:
    st.markdown(
        """
        <br>
        <p style="font-size: 18px; font-weight: bold; color: #333;">
            欢迎添加湖光社区网格员小郑微信，加入合伙人！
        </p>
        <p style="color: #666;">
            无论是商户入驻、活动开展，还是关于智慧街区的建议，都欢迎你随时联系。
        </p>
        """,
        unsafe_allow_html=True
    )

with footer_col2:
    # 尝试加载你上传的微信二维码图片
    qr_filename = "Screenshot_20260322_230743_com.tencent.mm_edit_4401257242557.jpg"
    if os.path.exists(qr_filename):
        st.image(qr_filename, caption="网格员小郑微信", width=200) # 设置宽度，防止图片过大
    else:
        st.caption("(⚠️ 未找到二维码图片文件，请确保文件名完全一致)")
