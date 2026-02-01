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

    st.subheader(f"Add Sample - {location}")

    date = st.date_input("Date")
    fcv = st.text_input("FCV Opening")
    wellhead_pressure = st.text_input("Wellhead Pressure")
    
    st.markdown("##### Operation Data")
    upstream_line_pressure = st.text_input("Line Pressure (Upstream)")
    upstream_line_temperature = st.text_input("Line Temperature (Upstream)")
    upstream_miniseparator_pressure = st.text_input("Mini Separator Pressure (Upstream)")
    upstream_miniseparator_temperature = st.text_input("Mini Separator Temperature (Upstream)")
    downstream_line_pressure = st.text_input("Line Pressure (Downstream)")
    downstream_line_temperature = st.text_input("Line Temperature (Downstream)")
    downstream_miniseparator_pressure = st.text_input("Mini Separator Pressure (Downstream)")
    downstream_miniseparator_temperature = st.text_input("Mini Separator Temperature (Downstream)")
    st.markdown("##### chemistry Data")
    upstream_ph = st.text_input("pH (Upstream)")
    upstream_ec = st.text_input("EC (Upstream)")
    upstream_temperature = st.text_input("Temperature (Upstream)")
    downstream_ph = st.text_input("pH (Downstream)")
    downstream_ec = st.text_input("EC (Downstream)")
    downstream_temperature = st.text_input("Temperature (Downstream)")
    
    submitted = st.form_submit_button("Save")

    if submitted:
        if not date:
            st.error("Date is required")
        else:
            try:
                supabase.table(TABLE).upsert({
                    "Date": date,
                    "FCV": fcv,
                    "wellhead_pressure": wellhead_pressure,
                    "upstream_line_pressure":  upstream_line_pressure,
                    "upstream_line_temperature": upstream_line_temperature,
                    "upstream_miniseparator_pressure":  upstream_miniseparator_pressure,
                    "upstream_miniseparator_temperature": upstream_miniseparator_temperature,
                    "downstream_line_pressure":  downstream_line_pressure,
                    "downstream_line_temperature": downstream_line_temperature,
                    "downstream_miniseparator_pressure":  downstream_miniseparator_pressure,
                    "downstream_miniseparator_temperature": downstream_miniseparator_temperature,
                    "upstream_ph": upstream_ph,
                    "upstream_ec": upstream_ec,
                    "upstream_temperature": upstream_temperature,
                    "downstream_ph": downstream_ph,
                    "downstream_ec": downstream_ec,
                    "downstream_temperature": downstream_temperature,
                }).execute()

                st.success("Employee added")
                st.rerun()

            except Exception as e:
                st.error(e)


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
