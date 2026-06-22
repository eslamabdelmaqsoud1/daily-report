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
        st.write(df.head())

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


