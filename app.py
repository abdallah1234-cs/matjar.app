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
        return json.load(f)

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

# المجموعات والأقسام المعتمدة في النظام (تمت إضافة قسم حقائب)
AVAILABLE_CATEGORIES = ["ملابس", "اكسسوارات", "أحذية", "حقائب"]

# =========================================================
# 🎨 واجهة CSS3 المتقدمة لإضافة الطابع الاحترافي العصري للموقع
# =========================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stSidebar"], .stButton, div, h1, h2, h3, h4, p, label {
        font-family: 'Tajawal', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 15px;
    }
    div[data-testid="stRadio"] label {
        padding: 12px 24px !important;
        background: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        cursor: pointer !important;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #007bff !important;
        color: #ffffff !important;
        border-color: #007bff !important;
        border-radius: 0px !important; 
        box-shadow: 0 8px 15px rgba(0, 123, 255, 0.3) !important;
        transform: translateY(-2px);
    }
    
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    div.element-container:has(img) {
        border-radius: 12px;
        overflow: hidden;
    }
    
    .stButton>button[kind="primary"] {
        background: linear-gradient(45deg, #28a745, #218838) !important;
        border: none !important;
        box-shadow: 0 4px 10px rgba(40, 167, 69, 0.2) !important;
        transition: all 0.3s ease !important;
    }
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 6px 15px rgba(40, 167, 69, 0.4) !important;
        transform: scale(1.03);
    }
    </style>
""", unsafe_allow_html=True)

current_users = load_users()

# ==========================================
# 🔑 واجهة الحسابات (تسجيل الدخول / إنشاء حساب)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align: center; color: #1e293b; margin-top: 50px;'>👋 مرحباً بك في matjar.jo المطور</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b;'>نظام التجارة الإلكترونية السريع والآمن</p>", unsafe_allow_html=True)
    st.write("")
    
    _, col_auth, _ = st.columns([1, 1.5, 1])
    
    with col_auth:
        if st.session_state.auth_mode == "login":
            with st.container(border=True):
                st.markdown("<h3 style='text-align: center; color: #0f172a;'>🔒 تسجيل الدخول إلى حسابك</h3>", unsafe_allow_html=True)
                login_email = st.text_input("البريد الإلكتروني", placeholder="example@matjar.jo", key="l_email")
                login_password = st.text_input("كلمة السر", type="password", placeholder="******", key="l_pass")
                
                if st.button("🚀 دخول النظام", type="primary", use_container_width=True):
                    if login_email in current_users and current_users[login_email] == login_password:
                        st.session_state.logged_in = True
                        st.session_state.user_email = login_email
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ البريد الإلكتروني أو كلمة السر غير صحيحة.")
                
                st.markdown("---")
                st.write("ليس لديك حساب؟")
                if st.button("✨ إنشاء حساب جديد", use_container_width=True):
                    st.session_state.auth_mode = "signup"
                    st.rerun()
                    
        elif st.session_state.auth_mode == "signup":
            with st.container(border=True):
                st.markdown("<h3 style='text-align: center; color: #0f172a;'>✨ تسجيل مستخدم جديد</h3>", unsafe_allow_html=True)
                new_email = st.text_input("البريد الإلكتروني الجديد", placeholder="user@matjar.jo", key="n_email")
                new_password = st.text_input("اختر كلمة السر", type="password", placeholder="******", key="n_pass")
                confirm_password = st.text_input("تأكيد كلمة السر", type="password", placeholder="******", key="c_pass")
                
                if st.button("➕ تسجيل الحساب الجديد", type="primary", use_container_width=True):
                    if not new_email or not new_password:
                        st.error("الرجاء تعبئة جميع الخانات المطلوبة.")
                    elif new_password != confirm_password:
                        st.error("❌ كلمات السر غير متطابقة.")
                    elif new_email in current_users:
                        st.error("⚠️ هذا البريد الإلكتروني مسجل مسبقاً في النظام!")
                    else:
                        save_user(new_email, new_password)
                        st.success("🎉 تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                
                st.markdown("---")
                st.write("لديك حساب بالفعل؟")
                if st.button("🔙 العودة لتسجيل الدخول", use_container_width=True):
                    st.session_state.auth_mode = "login"
                    st.rerun()
else:
    # ==========================================
    # 🛍️ واجهة المتجر الأساسية بعد الدخول
    # ==========================================
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.markdown("<h1 style='color: #0f172a;'>🛍️ متجر matjar.jo الإلكتروني</h1>", unsafe_allow_html=True)
        if st.session_state.user_email == "admin@matjar.jo":
            st.markdown("<span style='background-color:#eff6ff; color:#1d4ed8; padding:4px 12px; border-radius:20px; font-weight:bold; font-size:14px;'>👨‍💼 لوحة الإدارة والتحكم الكاملة (التاجر)</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: #475569;'>👋 أهلاً بك متصفحاً في متجرنا: <b>{st.session_state.user_email}</b></p>", unsafe_allow_html=True)
            
    with col_logout:
        st.write("") 
        if st.button("🚪 تسجيل الخروج", type="secondary", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.cart = {}
            st.rerun()
            
    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.user_email == "admin@matjar.jo":
        tab1, tab2, tab3 = st.tabs(["🛒 واجهة التسوق والسلة", "⚙️ لوحة تحكم التاجر", "📦 إدارة الطلبات الواردة"])
    else:
        tab1, = st.tabs(["🛒 واجهة التسوق والسلة"])

    # ==========================================
    # 🛒 التبويب الأول: واجهة التسوق والأقسام
    # ==========================================
    with tab1:
        st.markdown('<h3 style="color: #1e293b; margin-bottom:15px;">🗂️ تصفح حسب الأقسام التفاعلية</h3>', unsafe_allow_html=True)
        
        cat_options = ["الكل"] + AVAILABLE_CATEGORIES
        selected_cat = st.radio("اختر القسم لفلترة المنتجات فوراً:", cat_options, horizontal=True, label_visibility="collapsed")
        
        st.markdown("<hr style='border-top: 1px solid #cbd5e1;'>", unsafe_allow_html=True)
        
        col_products, col_cart = st.columns([2.2, 1])
        
        with col_products:
            st.markdown(f"<h3 style='color: #0f172a;'>🛍️ منتجات قسم ({selected_cat})</h3>", unsafe_allow_html=True)
            
            filtered_products = [p for p in st.session_state.products if selected_cat == "الكل" or p.get('category') == selected_cat]
                
            if not filtered_products:
                st.info("لا توجد منتجات معروضة حالياً في هذا القسم.")
            else:
                prod_cols = st.columns(2)
                for idx, p in enumerate(filtered_products):
                    with prod_cols[idx % 2]:
                        with st.container(border=True):
                            if p.get('image') and p['image'].strip() != "":
                                st.image(p['image'], use_container_width=True)
                            else:
                                st.image("https://via.placeholder.com/150?text=No+Image", use_container_width=True)
                                
                            st.markdown(f"<h3 style='margin-top:10px; color:#1e293b;'>{p['name']}</h3>", unsafe_allow_html=True)
                            st.markdown(f"**القسم:** <span style='color:#2563eb;'>{p.get('category', 'عام')}</span>", unsafe_allow_html=True)
                            st.markdown(f"**السعر:** <span style='font-size:18px; font-weight:bold; color:#10b981;'>{p['price']} دينار أردني</span>", unsafe_allow_html=True)
                            st.markdown(f"<p style='color:#64748b; font-size:14px;'>{p['desc']}</p>", unsafe_allow_html=True)
                            
                            if st.button(f"➕ إضافة إلى السلة", key=f"add_{p['id']}", use_container_width=True):
                                p_id = str(p['id'])
                                if p_id in st.session_state.cart:
                                    st.session_state.cart[p_id] += 1
                                else:
                                    st.session_state.cart[p_id] = 1
                                st.toast(f"تمت إضافة {p['name']} إلى السلة!")
                                st.rerun()

        with col_cart:
            st.markdown("<h3 style='color: #0f172a;'>🛒 سلة المشتريات</h3>", unsafe_allow_html=True)
            if not st.session_state.cart:
                st.write("السلة فارغة حالياً. اضف بعض المنتجات لتبدأ التسوق!")
            else:
                total_price = 0
                cart_items_to_del = []
                
                for p_id, qty in list(st.session_state.cart.items()):
                    product = next((p for p in st.session_state.products if str(p['id']) == p_id), None)
                    if product:
                        item_total = product['price'] * qty
                        total_price += item_total
                        st.markdown(f"**{product['name']}** (الكمية: {qty}) <br> <span style='color:#10b981;'>{item_total} دينار</span>", unsafe_allow_html=True)
                        
                        if st.button("❌ حذف", key=f"del_cart_{p_id}", type="secondary"):
                            del st.session_state.cart[p_id]
                            st.rerun()
                        st.markdown("---")
                    else:
                        cart_items_to_del.append(p_id)
                
                for p_id in cart_items_to_del:
                    del st.session_state.cart[p_id]

                st.markdown(f"<h3 style='color:#1e293b;'>💰 الحساب الإجمالي: <span style='color:#10b981;'>{total_price} دينار</span></h3>", unsafe_allow_html=True)
                st.markdown("---")
                
                st.markdown("<h4 style='color: #0f172a;'>👤 تفاصيل هاتف وعنوان التوصيل</h4>", unsafe_allow_html=True)
                customer_name = st.text_input("اسم العميل المستلم بالكامل", key="c_name")
                customer_phone = st.text_input("رقم الهاتف الفعال", key="c_phone")
                customer_address = st.text_input("المحافظة والعنوان بالتفصيل", key="c_address")
                
                if st.button("✅ تأكيد وشحن الطلب الآن", type="primary", use_container_width=True):
                    if customer_name and customer_phone and customer_address:
                        orders = load_orders()
                        new_order = {
                            "order_id": len(orders) + 1,
                            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "customer": customer_name,
                            "phone": customer_phone,
                            "address": customer_address,
                            "total": total_price,
                            "details": [
                                {"product": next(p['name'] for p in st.session_state.products if str(p['id']) == pid), "qty": q}
                                for pid, q in st.session_state.cart.items()
                            ]
                        }
                        orders.append(new_order)
                        save_orders(orders)
                        
                        st.session_state.cart = {}
                        st.success("🎉 تم تسجيل طلبك بنجاح وسُجل في جدول الإدارة!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("الرجاء تعبئة جميع خانات معلومات الشحن لإتمام الطلب.")

    # ==========================================
    # ⚙️ التبويب الثاني: لوحة تحكم التاجر (للأدمن)
    # ==========================================
    if st.session_state.user_email == "admin@matjar.jo":
        with tab2:
            st.subheader("🛠️ إدارة المنتجات المعروضة والأقسام والأسعار")
            col_add, col_list = st.columns([1, 1])
            
            with col_add:
                if st.session_state.editing_product_id is not None:
                    st.markdown("### 📝 تعديل بيانات المنتج والسعر")
                    edit_id = st.session_state.editing_product_id
                    prod_to_edit = next((p for p in st.session_state.products if p['id'] == edit_id), None)
                    
                    if prod_to_edit:
                        e_name = st.text_input("تعديل اسم المنتج", value=prod_to_edit['name'])
                        e_cat = st.selectbox("تعديل القسم", AVAILABLE_CATEGORIES, index=AVAILABLE_CATEGORIES.index(prod_to_edit.get('category', 'ملابس')))
                        e_price = st.number_input("تعديل السعر الجديد (دينار)", value=float(prod_to_edit['price']), min_value=0.1)
                        
                        # ميزة اختيار رفع صورة أو رابط بالتعديل
                        img_source_e = st.radio("مصدر صورة التعديل:", ["رفع ملف من الجهاز", "رابط من الإنترنت (URL)"], horizontal=True)
                        final_edit_img = prod_to_edit.get('image', '')
                        
                        if img_source_e == "رفع ملف من الجهاز":
                            uploaded_file_e = st.file_uploader("اختر صورة المنتج الجديدة من جهازك", type=["png", "jpg", "jpeg"], key="edit_file_up")
                            if uploaded_file_e:
                                final_edit_img = convert_image_to_base64(uploaded_file_e)
                        else:
                            final_edit_img = st.text_input("تعديل رابط الصورة (URL)", value=prod_to_edit.get('image', ''))
                            
                        e_desc = st.text_area("تعديل وصف المنتج", value=prod_to_edit['desc'])
                        
                        col_e_btns = st.columns(2)
                        with col_e_btns[0]:
                            if st.button("💾 حفظ التعديلات الجديدة", type="primary", use_container_width=True):
                                prod_to_edit['name'] = e_name
                                prod_to_edit['category'] = e_cat
                                prod_to_edit['price'] = e_price
                                prod_to_edit['image'] = final_edit_img
                                prod_to_edit['desc'] = e_desc
                                save_data(st.session_state.products)
                                st.session_state.editing_product_id = None
                                st.success("تم تعديل المنتج والأسعار بنجاح!")
                                st.rerun()
                        with col_e_btns[1]:
                            if st.button("❌ إلغاء التعديل", use_container_width=True):
                                st.session_state.editing_product_id = None
                                st.rerun()
                else:
                    st.markdown("### ➕ إضافة منتج جديد للسيستم")
                    p_name = st.text_input("اسم المنتج الجديد")
                    p_cat = st.selectbox("حدد قسم المنتج", AVAILABLE_CATEGORIES)
                    p_price = st.number_input("السعر المعروض (بالدينار الأردني)", min_value=0.0, step=0.5)
                    
                    # 🛠️ إضافة خيار تحديد نوع الرفع (ملف أو رابط)
                    img_source = st.radio("طريقة إضافة صورة المنتج:", ["رفع صورة من الجهاز 💻", "إدخال رابط إنترنت (URL) 🌐"], horizontal=True)
                    p_image = ""
                    
                    if img_source == "رفع صورة من الجهاز 💻":
                        uploaded_file = st.file_uploader("اختر ملف الصورة من كمبيوترك أو هاتفك", type=["png", "jpg", "jpeg"])
                        if uploaded_file is not None:
                            p_image = convert_image_to_base64(uploaded_file)
                    else:
                        p_image = st.text_input("رابط صورة المنتج من الإنترنت (URL)", placeholder="https://example.com/image.jpg")
                        
                    p_desc = st.text_area("وصف ومواصفات المنتج بالتفصيل")
                    
                    if st.button("✨ إدخل المنتج للمتجر الآن", use_container_width=True):
                        if p_name and p_price > 0 and p_image != "":
                            new_id = max([p['id'] for p in st.session_state.products], default=0) + 1
                            new_prod = {
                                "id": new_id, 
                                "name": p_name, 
                                "category": p_cat, 
                                "price": p_price, 
                                "image": p_image,
                                "desc": p_desc
                            }
                            st.session_state.products.append(new_prod)
                            save_data(st.session_state.products)
                            st.success(f"تمت إضافة المنتج بنجاح لقسم {p_cat}!")
                            st.rerun()
                        elif p_image == "":
                            st.error("⚠️ يرجى رفع صورة أو وضع رابط صورة لإكمال العملية.")
                        else:
                            st.error("الرجاء كتابة اسم منتج وسعر صالحين.")

            with col_list:
                st.markdown("### 📋 قائمة المنتجات والأسعار الحالية المعروضة")
                for p in st.session_state.products:
                    with st.container(border=True):
                        st.write(f"**{p['name']}** | القسم: {p.get('category', 'ملابس')} | :moneybag: {p['price']} دينار")
                        col_row_btns = st.columns(2)
                        with col_row_btns[0]:
                            if st.button("📝 تعديل البيانات", key=f"edit_trigger_{p['id']}", type="secondary", use_container_width=True):
                                st.session_state.editing_product_id = p['id']
                                st.rerun()
                        with col_row_btns[1]:
                            if st.button("🗑️ حذف نهائي", key=f"delete_trigger_{p['id']}", type="primary", use_container_width=True):
                                st.session_state.products = [prod for prod in st.session_state.products if prod['id'] != p['id']]
                                save_data(st.session_state.products)
                                st.success("تم الحذف من قاعدة البيانات.")
                                st.rerun()

        # ==========================================
        # 📦 التبويب الثالث: جدول الطلبات المستلمة (للأدمن)
        # ==========================================
        with tab3:
            st.subheader("📋 جدول الطلبات المستلمة التفصيلي الوارد للتاجر")
            saved_orders = load_orders()
            
            if not saved_orders:
                st.info("⚠️ لا توجد طلبات واردة بعد.")
            else:
                flat_orders = []
                for o in saved_orders:
                    items_summary = " + ".join([f"{item['product']} (عدد: {item['qty']})" for item in o['details']])
                    flat_orders.append({
                        "رقم الطلب": o['order_id'],
                        "تاريخ الطلب": o['date'],
                        "اسم الزبون": o['customer'],
                        "رقم هاتف الزبون": o['phone'],
                        "عنوان التوصيل": o['address'],
                        "تفاصيل المنتجات المطلوبة": items_summary,
                        "إجمالي الحساب": f"{o['total']} دينار"
                    })
                
                df_orders = pd.DataFrame(flat_orders)
                st.dataframe(df_orders, use_container_width=True)
                
                csv_data = df_orders.to_csv(index=False).encode('utf-8-sig')
                st.download_button(
                    label="📥 تحميل الجدول بالكامل لملف Excel",
                    data=csv_data,
                    file_name=f"طلبات_متجر_جو_{datetime.now().strftime('%Y-%m-%d')}.csv",
                    mime='text/csv',
                    use_container_width=True
                )