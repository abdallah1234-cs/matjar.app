import streamlit as st
import pandas as pd
import os
import json
import base64
from datetime import datetime

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="matjar.jo | المتجر المطور الفاخر",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# دالة ذكية لتحويل الصورة المرفوعة من الجهاز إلى نص Base64 ليتم حفظها في ملف الـ JSON
def convert_image_to_base64(image_file):
    if image_file is not None:
        return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
    return None

# دالات النظام (تحميل وحفظ البيانات)
def load_users():
    if not os.path.exists('users.json'):
        default_users = {"admin@matjar.jo": "123456"}
        with open('users.json', 'w', encoding='utf-8') as f:
            json.dump(default_users, f, ensure_ascii=False, indent=4)
    with open('users.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_user(email, password):
    users = load_users()
    users[email] = password
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def load_data():
    has_data = False
    if os.path.exists('products.json') and os.path.getsize('products.json') > 0:
        with open('products.json', 'r', encoding='utf-8') as f:
            try:
                content = json.load(f)
                if isinstance(content, list) and len(content) > 0:
                    has_data = True
            except:
                has_data = False

    if not has_data:
        demo_products = [
            {
                "id": 1,
                "name": "هودي شتوي كاجوال مريح",
                "category": "ملابس",
                "price": 18.5,
                "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&q=80",
                "desc": "هودي قطني مريح وعالي الجودة مناسب للأجواء اليومية والشتوية."
            },
            {
                "id": 2,
                "name": "تيشيرت صيفي قطن 100%",
                "category": "ملابس",
                "price": 10.0,
                "image": "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&q=80",
                "desc": "تيشيرت صيفي ناعم ومريح متوفر بجميع المقاسات والألوان."
            },
            {
                "id": 3,
                "name": "ساعة يد كلاسيكية فاخرة",
                "category": "اكسسوارات",
                "price": 45.0,
                "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&q=80",
                "desc": "ساعة يد أنيقة بسير جلدي مقاوم للماء، تناسب جميع المناسبات الرسمية."
            },
            {
                "id": 4,
                "name": "حقيبة ظهر مقاومة للماء مع منفذ لابتوب",
                "category": "حقائب",
                "price": 22.0,
                "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&q=80",
                "desc": "حقيبة ظهر عملية وممتازة للجامعة أو العمل لحماية اللابتوب والأغراض اليومية."
            },
            {
                "id": 5,
                "name": "حذاء رياضي مريح للجري والتمارين",
                "category": "أحذية",
                "price": 28.0,
                "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&q=80",
                "desc": "حذاء رياضي خفيف الوزن ومصمم لدعم القدم أثناء المشي والجري لمسافات طويلة."
            }
        ]
        with open('products.json', 'w', encoding='utf-8') as f:
            json.dump(demo_products, f, ensure_ascii=False, indent=4)
        return demo_products
        
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_orders():
    if not os.path.exists('orders.json'):
        with open('orders.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
    with open('orders.json', 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_orders(orders):
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=4)

# تهيئة المنتجات تلقائياً في الجلسة لضمان التحميل الفوري
st.session_state.products = load_data()

if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'editing_product_id' not in st.session_state:
    st.session_state.editing_product_id = None
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = "login"

# المجموعات والأقسام المعتمدة في النظام
AVAILABLE_CATEGORIES = ["ملابس", "اكسسوارات", "أحذية", "حقائب"]

# =========================================================
# 🎨 واجهة CSS3 المتقدمة لإضافة الطابع الاحترافي العصري للموقع
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght=400;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stButton, div, h1, h2, h3, h4, p, label {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    /* تحسين أزرار الراديو (الأقسام) لتبدو بارزة وواضحة جداً */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 15px;
    }
    div[data-testid="stRadio"] label {
        padding: 12px 24px !important;
        background: #ffffff !important;
        color: #111111 !important;
        border: 2px solid #dee2e6 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #007bff !important;
        color: #ffffff !important;
        border-color: #007bff !important;
        box-shadow: 0 8px 15px rgba(0, 123, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    div.element-container:has(img) {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# تقسيم التطبيق إلى صفحات رئيسية باستخدام Tabs
tab1, tab2 = st.tabs(["🛒 واجهة التسوق والسلة", "👨‍💼 لوحة تحكم التاجر"])

# ==================== 1️⃣ واجهة التسوق والسلة ====================
with tab1:
    st.title("🛍️ متجر matjar.jo الإلكتروني")
    st.write("أهلاً بك في منصة التسوق الفاخرة")
    
    st.subheader("📂 تصفح حسب الأقسام التفاعلية")
    categories_options = ["الكل"] + AVAILABLE_CATEGORIES
    selected_category = st.radio("", categories_options, horizontal=True)
    
    # تصفية المنتجات
    if selected_category == "الكل":
        display_products = st.session_state.products
    else:
        display_products = [p for p in st.session_state.products if p.get("category") == selected_category]
        
    # عرض المنتجات
    st.subheader(f"✨ منتجات قسم ({selected_category})")
    if not display_products:
        st.info("لا توجد منتجات في هذا القسم حالياً.")
    else:
        cols = st.columns(3)
        for i, prod in enumerate(display_products):
            with cols[i % 3]:
                if prod.get("image"):
                    st.image(prod["image"], use_container_width=True)
                st.markdown(f"### {prod.get('name', 'منتج غير مسمى')}")
                st.write(prod.get("desc", ""))
                st.markdown(f"💰 **السعر:** {prod.get('price', 0)} دينار أردني")
                
                prod_id = str(prod.get("id"))
                if st.button(f"إضافة إلى السلة 🛒", key=f"buy_{prod_id}"):
                    if prod_id in st.session_state.cart:
                        st.session_state.cart[prod_id] += 1
                    else:
                        st.session_state.cart[prod_id] = 1
                    st.toast(f"تمت إضافة {prod.get('name')} إلى سلتك!")
                    st.rerun()

    st.markdown("---")
    
    # سلة المشتريات التفاعلية للمستخدم
    st.subheader("🛒 سلة المشتريات الخاصة بك")
    if not st.session_state.cart:
        st.info("سلتك فارغة حالياً. تسوق الآن وأضف المنتجات!")
    else:
        total_bill = 0
        order_items_text = []
        
        for p_id, qty in list(st.session_state.cart.items()):
            product_info = next((p for p in st.session_state.products if str(p.get("id")) == p_id), None)
            if product_info:
                item_total = product_info.get("price", 0) * qty
                total_bill += item_total
                order_items_text.append(f"{product_info.get('name')} (العدد: {qty})")
                
                c_item1, c_item2, c_item3 = st.columns([3, 1, 1])
                with c_item1:
                    st.write(f"**{product_info.get('name')}** - الكمية: {qty}")
                with c_item2:
                    st.write(f"الإجمالي: {item_total} دينار")
                with c_item3:
                    if st.button("حذف 🗑️", key=f"del_{p_id}"):
                        del st.session_state.cart[p_id]
                        st.rerun()
                        
        st.markdown(f"### 💵 إجمالي الحساب النهائي: **{total_bill} دينار أردني**")
        
        # نموذج إرسال الطلب وحفظه للتاجر
        st.write("### 📞 أدخل بياناتك لشحن وتأكيد الطلب:")
        c_name = st.text_input("اسمك الكامل", key="order_name")
        c_phone = st.text_input("رقم الهاتف الفعال", key="order_phone")
        
        if st.button("✅ إتمام عملية الشراء وإرسال الطلب"):
            if c_name and c_phone:
                all_orders = load_orders()
                new_order_data = {
                    "الوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "الاسم": c_name,
                    "الهاتف": c_phone,
                    "المنتجات الواردة": ", ".join(order_items_text),
                    "المجموع الإجمالي": f"{total_bill} دينار"
                }
                all_orders.append(new_order_data)
                save_orders(all_orders)
                st.session_state.cart = {}
                st.success("🎉 تم إرسال طلبك بنجاح إلى إدارة المتجر! شكرًا لتسوقك معنا.")
                st.rerun()
            else:
                st.warning("الرجاء تعبئة الاسم ورقم الهاتف لتتمكن من الشراء.")

# ==================== 2️⃣ لوحة تحكم التاجر ====================
with tab2:
    st.title("👨‍💼 لوحة الإدارة والتحكم (التاجر)")
    
    if not st.session_state.logged_in:
        st.subheader("🔒 يرجى تسجيل الدخول للوصول للوحة التحكم")
        users_db = load_users()
        
        login_email = st.text_input("البريد الإلكتروني للتاجر")
        login_password = st.text_input("كلمة المرور", type="password")
        
        if st.button("تسجيل الدخول 🔑"):
            if login_email in users_db and users_db[login_email] == login_password:
                st.session_state.logged_in = True
                st.session_state.user_email = login_email
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("بيانات الدخول خاطئة! يرجى المحاولة مجدداً.")
    else:
        st.write(f"مرحباً بك مجدداً: `{st.session_state.user_email}`")
        if st.button("تسجيل الخروج 🚪"):
            st.session_state.logged_in = False
            st.rerun()
            
        st.write("---")
        
        # قسم الطلبات الواردة
        st.subheader("🔔 الطلبات الواردة من المستخدمين حالياً")
        current_orders = load_orders()
        if not current_orders:
            st.info("لا توجد طلبات جديدة مستلمة حتى اللحظة.")
        else:
            df_orders = pd.DataFrame(current_orders)
            st.dataframe(df_orders, use_container_width=True)
            if st.button("🗑️ تفريغ ومسح سجل الطلبات المستلمة"):
                save_orders([])
                st.rerun()
                
        st.write("---")
        
        # نظام إدارة وإضافة المنتجات
        st.subheader("🛠️ إدارة المنتجات المعروضة")
        with st.form("add_new_product_form", clear_on_submit=True):
            st.write("➕ **إضافة منتج جديد للمتجر**")
            new_name = st.text_input("اسم المنتج الجديد")
            new_category = st.selectbox("قسم المنتج", AVAILABLE_CATEGORIES)
            new_price = st.number_input("السعر (دينار)", min_value=0.0, step=0.5)
            new_desc = st.text_area("وصف وتفاصيل المنتج")
            new_img_file = st.file_uploader("ارفع صورة المنتج من جهازك", type=["jpg", "png", "jpeg"])
            
            if st.form_submit_button("حفظ وإضافة المنتج الجديد ✨"):
                if new_name and new_price > 0:
                    img_url = convert_image_to_base64(new_img_file) if new_img_file else "https://via.placeholder.com/500"
                    
                    new_id = max([p.get("id", 0) for p in st.session_state.products]) + 1 if st.session_state.products else 1
                    new_prod = {
                        "id": new_id,
                        "name": new_name,
                        "category": new_category,
                        "price": new_price,
                        "image": img_url,
                        "desc": new_desc
                    }
                    st.session_state.products.append(new_prod)
                    save_data(st.session_state.products)
                    st.success(f"تمت إضافة منتج ({new_name}) بنجاح!")
                    st.rerun()
                else:
                    st.error("الرجاء كتابة اسم المنتج وتحديد سعر صحيح.")
