import streamlit as st
import pandas as pd

# 1. 页面基本设置：加入了 layout="wide" 开启宽屏自适应模式！
st.set_page_config(page_title="湖映福津", page_icon="🏘️", layout="wide")
st.title("湖映福津·合伙“邻”距离 🏘️")
st.markdown("欢迎来到湖光社区智慧街区展示平台！")

# 2. 模拟数据准备区
shop_data = {
    "店名": ["福津包子铺", "老李五金店", "社区卫生服务站"],
    "门牌号": ["福津街1号", "福津街15号", "福津街8号"],
    "类型": ["餐饮", "五金", "医疗"],
    "状态": ["营业中", "营业中", "营业中"],
    "lat": [39.9042, 39.9055, 39.9035], 
    "lon": [116.4074, 116.4085, 116.4065] 
}
df_shops = pd.DataFrame(shop_data)

# 3. 建立顶部导航标签页 📑
tab1, tab2, tab3 = st.tabs(["🏪 街区商户与地图", "👴 老干部“四就近”", "📢 街铺招租区"])

# ==================== 标签页 1：商户与地图 ====================
with tab1:
    # 核心魔法：将这里分成左右两列
    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("🏪 商户搜索与名录")
        # 搜索框也进行小分栏
        search_col, category_col = st.columns(2)
        with search_col:
            search_text = st.text_input("🔍 搜索店名 (如: 包子)")
        with category_col:
            category = st.selectbox("📁 按类型", ["全部", "餐饮", "五金", "医疗"])

        filtered_df = df_shops.copy()
        if search_text:
            filtered_df = filtered_df[filtered_df["店名"].str.contains(search_text)]
        if category != "全部":
            filtered_df = filtered_df[filtered_df["类型"] == category]

        st.dataframe(filtered_df, use_container_width=True)
        
    with right_col:
        st.subheader("📍 街区便民地图")
        st.map(filtered_df)

    # 明星店铺展示区放在下方，占满全宽
    st.divider() 
    st.subheader("🌟 明星店铺展示")
    showcase_col1, showcase_col2 = st.columns(2)
    with showcase_col1:
        st.info("🥟 **福津包子铺**\n\n社区老字号，每天早上6点准时出炉新鲜肉包。对老人有专属八折优惠！")
    with showcase_col2:
        st.success("🛠️ **老李五金店**\n\n承接各类日常维修，提供上门换锁、修水管服务。响应速度快，价格公道。")

# ==================== 标签页 2：老干部“四就近” ====================
with tab2:
    st.header("👴 银发赋能·“四就近”活动台")
    st.markdown("就近学习、就近活动、就近得到关心照顾、就近发挥作用。")
    with st.expander("📚 本周就近学习：智能手机防诈骗讲座"):
        st.write("**时间**：本周五下午 2:00\n\n**地点**：湖光社区党群服务中心二楼\n\n**内容**：帮助老同志识别新型网络骗局，守护养老钱。")
    with st.expander("🎨 本周就近活动：社区秋季书画展"):
        st.write("**时间**：全天开放\n\n**地点**：福津街文化长廊\n\n**内容**：展示辖区内老干部、老党员的优秀书画作品。")
    with st.expander("❤️ 就近发挥作用：银发志愿巡逻队招募"):
        st.write("诚邀身体健康、热心公益的老同志加入街区平安巡逻，发挥余热，共建美好家园。")

# ==================== 标签页 3：招租与合作 ====================
with tab3:
    st.header("📢 优质商铺招租")
    st.markdown("寻找社区合伙人，共同激发街区活力！")
    st.error("🏠 **福津街 12 号 (原便利店)**\n\n- **面积**：50 平方米\n- **优势**：临近街口，人流量大，适合做生鲜或便民服务。\n- **联系人**：王主任 (社区办公室)")
    st.warning("🏠 **福津街 28 号二楼**\n\n- **面积**：120 平方米\n- **优势**：采光极佳，适合做教培机构或社区活动室。\n- **联系人**：李书记 (社区办公室)")
