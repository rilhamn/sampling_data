import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from supabase import create_client

# ===============================
# 🔐 AUTH
# ===============================

config = {
    "credentials": {
        "usernames": {
            user: dict(st.secrets["credentials"]["usernames"][user])
            for user in st.secrets["credentials"]["usernames"]
        }
    },
    "cookie": dict(st.secrets["cookie"]),
}

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

# Only admin can manage employee
if st.session_state.get("username") != "admin":
    st.error("🚫 Admin only")
    st.stop()


# ===============================
# Supabase
# ===============================

supabase = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"]
)

# ===============================
# Location → table mapping
# ===============================

LOCATION_TABLE_MAP = {
    "Well RD-I3": "sample_well_i3",
    "Well RD-N1": "sample_well_n1",
    "HP Separator": "sample_hp_separator",
    "LP 2nd Flash Separator": "sample_lp_2nd_flash_separator",
    "Well B1": "sample_well_b1",
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

    date = st.text_input("QR Code / Code Value")
    
    st.markdown("Upstream")
    upstream_wellhead_pressure = st.text_input("Wellhead Pressure")
    upstream_miniseparator_pressure = st.text_input("Mini Separator Pressure")
    upstream_miniseparator_temperature = st.text_input("Mini Separator Temperature")

    st.markdown("Downstream")
    downstream_wellhead_pressure = st.text_input("Wellhead Pressure")
    downstream_miniseparator_pressure = st.text_input("Mini Separator Pressure")
    downstream_miniseparator_temperature = st.text_input("Mini Separator Temperature")

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

st.divider()
st.subheader(f"📋 Sample Data list – {location}")

try:
    res = (
        supabase
        .table(TABLE)
        .select("*")
        .order("employee_name")
        .execute()
    )

    df = pd.DataFrame(res.data)

    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(e)
    df = pd.DataFrame()


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

#else:
    #st.info("No employee data yet.")
