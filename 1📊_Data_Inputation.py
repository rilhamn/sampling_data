import streamlit as st
import pandas as pd
from supabase import create_client

# ===============================
# Supabase
# ===============================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ===============================
# Location → table mapping
# ===============================

LOCATION_TABLE_MAP = {
    "Well RD-I3": "sample_well_i3",
    "Well RD-N1": "sample_well_n1",
    "HP Separator": "sample_hp_separator",
    "LP 2nd Flash Separator": "sample_lp_2nd_flash_separator"
    "Well B1": "sample_well_b1"
}

# ===============================
# 📍 LOCATION SELECTOR (MAIN PAGE)
# ===============================

st.title("🧪 Sample Inputation")

location = st.selectbox(
    "📍 Select Location",
    list(LOCATION_TABLE_MAP.keys())
)

#TABLE = LOCATION_TABLE_MAP[location]


# ===============================
# ➕ ADD Sample
# ===============================

with st.form("add_sample"):

    st.subheader(f"➕ Add Sample – {location}")

    code_value = st.text_input("QR Code / Code Value")
    employee_name = st.text_input("Employee name")
    department = st.text_input("Department")
    company = st.text_input("Company")

    submitted = st.form_submit_button("Save")

    #if submitted:
        #if not code_value:
            #st.error("Code value is required")
        #else:
            #try:
                #supabase.table(TABLE).insert({
                    #"code_value": code_value.strip(),
                    #"employee_name": employee_name,
                    #"department": department,
                    #"company": company
                #}).execute()

                #st.success("Employee added")
                #st.rerun()

            #except Exception as e:
                #st.error(e)


# ===============================
# 📋 VIEW Sample
# ===============================

#st.divider()
#st.subheader(f"📋 Sample Data list – {location}")

#try:
    #res = (
        #supabase
        #.table(TABLE)
        #.select("*")
        #.order("employee_name")
        #.execute()
    #)

    #df = pd.DataFrame(res.data)

    #st.dataframe(df, use_container_width=True)

#except Exception as e:
    #st.error(e)
    #df = pd.DataFrame()


# ===============================
# 🗑 DELETE EMPLOYEE
# ===============================

#st.divider()
#st.subheader(f"🗑 Delete Sample Data – {location}")

#if not df.empty:

    #selected_code = st.selectbox(
        #"Select employee (by code_value)",
        #df["code_value"].tolist()
    #)

    #col1, col2 = st.columns([1, 3])

    #with col1:
        #delete_btn = st.button("Delete")

    #if delete_btn:
        #try:
            #supabase.table(TABLE)\
                #.delete()\
                #.eq("code_value", selected_code)\
                #.execute()

            #st.success(f"Deleted {selected_code}")
            #st.rerun()

        #except Exception as e:
            #st.error(e)

else:
    st.info("No employee data yet.")
