import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
st.title("Hello Ahmed Abdelmaksoud ❤️")

st.title("🕒 تعديل عمود OrderDate +3 ساعات")

def add_3_hours(text):
    try:
        dt = datetime.strptime(str(text), '%m/%d/%Y %I:%M:%S %p')
        dt_plus3 = dt + timedelta(hours=3)
        return dt_plus3.strftime('%m/%d/%Y %I:%M:%S %p')
    except:
        return text

uploaded_file_order= st.file_uploader(" Choose Excel file ", type=['xlsx'])

if uploaded_file_order:
    try:
        st.write(uploaded_file_order.name)
        df = pd.read_excel(uploaded_file_order, engine="openpyxl")

        # 🟢 نخلي أسماء الأعمدة كلها lowercase علشان نقارن بسهولة
        df.columns = [col.lower() for col in df.columns]

        # 🔹 تعديل عمود التاريخ
        if 'orderdate' in df.columns:
            df['orderdate_plus3'] = df['orderdate'].apply(add_3_hours)

            # 🟢 عمود جديد فيه التاريخ فقط
            df['orderdate_dateonly'] = df['orderdate_plus3'].apply(
                lambda x: str(x).split(' ')[0] if isinstance(x, str) else x
            )

            st.success("✅ تم تعديل عمود OrderDate وإضافة عمود التاريخ فقط")
        else:
            st.warning("⚠️ الملف لا يحتوي على عمود OrderDate (بأي شكل من الحروف)")

        # 🔹 عمود جديد فيه Price * 3.75 (مهما كان اسمه capital أو small)
        price_col = [c for c in df.columns if 'price' in c]
        if price_col:
            df['price_x3.75'] = df[price_col[0]] * 3.75
            st.success(f"✅ تم إنشاء عمود price_x3.75 من العمود {price_col[0]}")
        else:
            st.warning("⚠️ الملف لا يحتوي على عمود Price")

        st.dataframe(df)
        daily_report_order = (df.groupby("orderdate_dateonly")
           .agg( عدد_الأوردرات=("orderdate_dateonly", "count"), 
                 إجمالي_السعر=("price_x3.75", "sum") )
                    .reset_index())
        st.subheader("📊 Daily Report")
        st.dataframe(daily_report_order)

        output_file = "OrderDate_updated.xlsx"
        df.to_excel(output_file, index=False)
        with open(output_file, "rb") as f:
            st.download_button(
                label="⬇️ تحميل النسخة المعدلة Excel",
                data=f,
                file_name="OrderDate_updated.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
     if "defaultColWidthPt" in str(e):
        st.error(
            "❌ الملف غير متوافق. برجاء فتحه في Excel ثم Save As ثم إعادة رفعه."
        )
     else:
        st.error(f"❌ حدث خطأ: {e}")


st.title("Daily Report")

uploaded_file = st.file_uploader(
    "Hello Ahmed please download your excel file ⬇️",
    type=["xlsx"]
)

if uploaded_file is not None:
    st.success("File Uploaded Successfully ✅")

    df = pd.read_excel(uploaded_file)
    df.columns = df.columns.str.strip()

    df["التاريخ/الوقت"] = pd.to_datetime(
        df["التاريخ/الوقت"],
        format="%d/%m/%Y, %H:%M:%S"
    )

    df["التاريخ/الوقت_بعد التعديل"] = (
        df["التاريخ/الوقت"] + pd.Timedelta(hours=1)
    )
    df['التاريخ بعد التعديل ']=df["التاريخ/الوقت_بعد التعديل"].dt.date
    df['سعر التكلفة']=df['سعر التكلفة'].astype(str).str.replace('ر.س',"",regex=False).str.strip().astype(float)
    st.write(df)  
    df["التاريخ بعد التعديل"] = df["التاريخ/الوقت_بعد التعديل"].dt.date  

    daily_report = (
    df.groupby("التاريخ بعد التعديل")
    .agg(
        عدد_الأوردرات=("التاريخ بعد التعديل", "count"),
        إجمالي_التكلفة=("سعر التكلفة", "sum")
    )
    .reset_index()
)
    st.dataframe(daily_report)

st.title("قائمة الطلبات ")
def Clean_price(df):
    df['price']=df['الإجمالي'].astype(str).str.replace("ر.س","",regex=False).str.strip().astype(float)
uploaded__file=st.file_uploader("choose ypur excel file",type=["xlsx"])
if uploaded__file:
    st.success("File Uploaded Successfully ✅")
    df=pd.read_excel(uploaded__file)
    df.columns=df.columns.str.strip()
    df['تاريخ الاضافة']=pd.to_datetime(df['تاريخ الاضافة'])
    df['date']=df['تاريخ الاضافة'].dt.date
    Clean_price(df)
    if st.button("عرض البيانات بعد التعديل"):
     st.write(df)
    report=df.groupby("date").agg(اجمالى_عدد_البطاقات=("عدد البطاقات","sum"),
                           اجمالى_السعر =("price","sum")).reset_index()
    report.rename(columns={"date":"التاريخ"},inplace=True)
    if st.button("عرض التقرير"):
       st.markdown("<h2 style='text-align:center;'>تقرير الطلبات</h2>",unsafe_allow_html=True)
       st.dataframe(report)

