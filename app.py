import streamlit as st
import pandas as pd
from datetime import datetime

# إعدادات الصفحة الأساسية
st.set_page_config(page_title="متجر matjar.jo الإلكتروني", page_icon="🛍️", layout="wide")

# تصميم CSS مخصص لإصلاح أزرار الأقسام فقط دون التأثير على نصوص المتجر الأخرى
st.markdown("""
    <style>
    /* تحسين شكل وألوان أزرار الأقسام التفاعلية لتظهر بوضوح دائماً */
    .stRadio div[role="radiogroup"] label {
        background-color: #ffffff !important;
        color: #111111 !important; /* لون نص أسود واضح جداً داخل الزر الأبيض */
        border: 2px solid #dee2e6 !important;
        padding: 10px 20px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        margin-bottom: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة الجلسة لتخزين السلة والطلبات الواردة للتاجر
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'orders' not in st.session_state:
    st.session_state.orders = []

# قاعدة بيانات المنتجات التجريبية
products = [
    {"id": 1, "name": "قميص كاجوال فاخر", "category": "ملابس", "price": 25, "image": "👕"},
    {"id": 2, "name": "فستان صيفي أنيق", "category": "ملابس", "price": 40, "image": "👗"},
    {"id": 3, "name": "ساعة يد كلاسيكية", "category": "اكسسوارات", "price": 60, "image": "⌚"},
    {"id": 4, "name": "نظارة شمسية عصرية", "category": "اكسسوارات", "price": 15, "image": "🕶️"},
    {"id": 5, "name": "حذاء رياضي مريح", "category": "أحذية", "price": 35, "image": "👟"},
    {"id": 6, "name": "حقيبة جلدية فاخرة", "category": "حقائب", "price": 50, "image": "👜"}
]

# تقسيم التطبيق إلى صفحات رئيسية باستخدام Tabs
tab1, tab2 = st.tabs(["🛒 واجهة التسوق والسلة", "👨‍💼 لوحة تحكم التاجر"])

# ==================== 1️⃣ واجهة التسوق ====================
with tab1:
    st.title("🛍️ متجر matjar.jo الإلكتروني")
    st.write("أهلاً بك في تجربتك المتكاملة للتسوق")
    
    # تصفح حسب الأقسام
    st.subheader("📂 تصفح حسب الأقسام التفاعلية")
    categories = ["الكل", "ملابس", "اكسسوارات", "أحذية", "حقائب"]
    selected_category = st.radio("", categories, horizontal=True)
    
    # تصفية المنتجات بناءً على القسم المحدد
    if selected_category == "الكل":
        filtered_products = products
    else:
        filtered_products = [p for p in products if p["category"] == selected_category]
        
    # عرض المنتجات في أعمدة
    st.subheader(f"✨ منتجات قسم ({selected_category})")
    cols = st.columns(3)
    for i, prod in enumerate(filtered_products):
        with cols[i % 3]:
            st.markdown(f"### {prod['image']} {prod['name']}")
            st.write(f"**السعر:** {prod['price']} دينار")
            if st.button(f"إضافة للسلة 🛒", key=f"add_{prod['id']}"):
                st.session_state.cart.append(prod)
                st.toast(f"تمت إضافة {prod['name']} إلى السلة!")
                st.rerun()

    st.write("---")
    
    # قسم سلة المشتريات للمستخدم
    st.subheader("🛒 سلة المشتريات الخاصة بك")
    if not st.session_state.cart:
        st.info("سلتك فارغة حالياً. أضف بعض المنتجات للتسوق!")
    else:
        total_price = 0
        for item in st.session_state.cart:
            st.write(f"- {item['name']} | السعر: {item['price']} دينار")
            total_price += item['price']
            
        st.markdown(f"### 💰 الإجمالي الكلي: **{total_price} دينار**")
        
        # نموذج العميل لتأكيد الطلب
        st.write("### 📞 أدخل بياناتك لتأكيد الطلب:")
        customer_name = st.text_input("الاسم الكامل")
        customer_phone = st.text_input("رقم الهاتف")
        
        if st.button("✅ تأكيد وشراء الطلب الآن"):
            if customer_name and customer_phone:
                # إنشاء الطلب وإرساله إلى لوحة تحكم التاجر
                new_order = {
                    "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "الاسم": customer_name,
                    "الهاتف": customer_phone,
                    "المنتجات": ", ".join([item['name'] for item in st.session_state.cart]),
                    "المجموع": f"{total_price} دينار"
                }
                st.session_state.orders.append(new_order) # حفظ في قائمة طلبات التاجر
                st.session_state.cart = [] # تفريغ السلة بعد الشراء
                st.success("🎉 تم إرسال طلبك بنجاح إلى التاجر! شكراً لك.")
                st.rerun()
            else:
                st.warning("الرجاء ملء الاسم ورقم الهاتف لإتمام الطلب.")

# ==================== 2️⃣ لوحة تحكم التاجر ====================
with tab2:
    st.title("👨‍💼 لوحة الإدارة والتحكم الكاملة (التاجر)")
    st.write("هنا تظهر لك تفاصيل طلبات المستخدمين الواردة فوراً")
    
    if not st.session_state.orders:
        st.info("لا توجد طلبات واردة حتى الآن. بمجرد قيام أي مستخدم بالشراء ستظهر هنا فوراً.")
    else:
        # تحويل الطلبات إلى جدول DataFrame منظم وعرضه للتاجر
        df_orders = pd.DataFrame(st.session_state.orders)
        st.success(f"🔔 لديك حالياً {len(df_orders)} طلبات جديدة!")
        st.dataframe(df_orders, use_container_width=True)
        
        if st.button("🗑️ مسح جميع الطلبات المستلمة"):
            st.session_state.orders = []
            st.rerun()
