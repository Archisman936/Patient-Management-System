import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Patient Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

PAGES = [
    {"key": "Dashboard",       "icon": "🏠", "label": "Dashboard"},
    {"key": "All Patients",    "icon": "📋", "label": "All Patients"},
    {"key": "Search Patient",  "icon": "🔍", "label": "Search"},
    {"key": "Add Patient",     "icon": "➕", "label": "Add"},
    {"key": "Update Patient",  "icon": "✏️", "label": "Update"},
    {"key": "Delete Patient",  "icon": "🗑️", "label": "Delete"},
    {"key": "Sort Patients",   "icon": "📊", "label": "Sort"},
]

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* Global */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* ── Hide the default sidebar completely ── */
    section[data-testid="stSidebar"],
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* ── Top Navbar ── */
    .top-navbar {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #4c1d95 100%);
        padding: 0;
        margin: -1rem -1rem 2rem -1rem;
        position: sticky;
        top: 0;
        z-index: 99999;
        box-shadow: 0 4px 24px rgba(30, 27, 75, 0.4);
        border-bottom: 2px solid rgba(102, 126, 234, 0.3);
    }
    .navbar-inner {
        max-width: 1400px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        padding: 0 1.5rem;
    }
    .navbar-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.85rem 0;
        margin-right: 2rem;
        text-decoration: none;
        flex-shrink: 0;
    }
    .navbar-brand-icon {
        font-size: 1.6rem;
    }
    .navbar-brand-text {
        font-size: 1.15rem;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.3px;
    }
    .navbar-links {
        display: flex;
        align-items: center;
        gap: 4px;
        flex-wrap: wrap;
    }
    .nav-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 0.55rem 1rem;
        border-radius: 10px;
        font-size: 0.88rem;
        font-weight: 500;
        color: #c7d2fe;
        text-decoration: none;
        transition: all 0.25s ease;
        cursor: pointer;
        border: 1px solid transparent;
        white-space: nowrap;
    }
    .nav-link:hover {
        background: rgba(255, 255, 255, 0.12);
        color: #ffffff;
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
    }
    .nav-link.active {
        background: rgba(102, 126, 234, 0.35);
        color: #ffffff;
        border-color: rgba(102, 126, 234, 0.5);
        box-shadow: 0 2px 12px rgba(102, 126, 234, 0.3);
        font-weight: 600;
    }
    .nav-link-icon {
        font-size: 1rem;
    }

    /* ── Hero header ── */
    .hero-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    .hero-header h1 {
        color: #ffffff;
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-header p {
        color: rgba(255,255,255,0.85);
        font-size: 1.05rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    /* ── Metric cards ── */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border: 1px solid rgba(255,255,255,0.6);
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }
    .metric-card .metric-value {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card .metric-label {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }

    /* Colored metric cards */
    .metric-green { background: linear-gradient(135deg, #e8f5e9 0%, #a5d6a7 100%); }
    .metric-green .metric-value { background: linear-gradient(135deg, #2e7d32, #1b5e20); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .metric-blue { background: linear-gradient(135deg, #e3f2fd 0%, #90caf9 100%); }
    .metric-blue .metric-value { background: linear-gradient(135deg, #1565c0, #0d47a1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .metric-orange { background: linear-gradient(135deg, #fff3e0 0%, #ffcc80 100%); }
    .metric-orange .metric-value { background: linear-gradient(135deg, #e65100, #bf360c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .metric-red { background: linear-gradient(135deg, #fce4ec 0%, #ef9a9a 100%); }
    .metric-red .metric-value { background: linear-gradient(135deg, #c62828, #b71c1c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

    /* ── Patient card ── */
    .patient-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 1.8rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 5px solid #667eea;
        transition: transform 0.2s ease;
    }
    .patient-card:hover {
        transform: translateX(4px);
    }
    .patient-card h3 {
        margin: 0 0 0.8rem 0;
        color: #1e293b;
        font-weight: 700;
    }
    .patient-card .detail {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 500;
        margin: 0.2rem;
    }

    /* Verdict badges */
    .badge-underweight { background: #fff3e0; color: #e65100; }
    .badge-normal { background: #e8f5e9; color: #2e7d32; }
    .badge-overweight { background: #fff8e1; color: #f57f17; }
    .badge-obese { background: #fce4ec; color: #c62828; }

    /* Info detail pill */
    .info-pill {
        display: inline-block;
        background: #f1f5f9;
        padding: 0.3rem 0.75rem;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #475569;
        margin: 0.15rem 0.1rem;
        font-weight: 500;
    }

    /* ── Success / Error boxes ── */
    .success-box {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 5px solid #2e7d32;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #1b5e20;
        font-weight: 500;
        margin: 1rem 0;
    }
    .error-box {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd0 100%);
        border-left: 5px solid #c62828;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #b71c1c;
        font-weight: 500;
        margin: 1rem 0;
    }

    /* Table styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* Section header */
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }

    /* Ensure nav buttons are fully visible at top */
    .block-container {
        padding-top: 0.5rem !important;
    }

    /* Remove Streamlit header bar gap */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Nav button row styling */
    .stApp > .main .block-container > div:first-child {
        margin-bottom: 1.5rem;
    }
</style>

""", unsafe_allow_html=True)



def get_verdict_badge(verdict: str) -> str:
    verdict_lower = verdict.lower()
    if verdict_lower == "underweight":
        return f'<span class="detail badge-underweight">⚠️ {verdict}</span>'
    elif verdict_lower == "normal":
        return f'<span class="detail badge-normal">✅ {verdict}</span>'
    elif verdict_lower == "overweight":
        return f'<span class="detail badge-overweight">⚡ {verdict}</span>'
    else:
        return f'<span class="detail badge-obese">🔴 {verdict}</span>'


def render_patient_card(patient_id: str, info: dict):
    verdict_badge = get_verdict_badge(info.get("verdict", "N/A"))
    gender_icon = "👩" if info.get("gender") == "female" else "👨"

    st.markdown(f"""
    <div class="patient-card">
        <h3>{gender_icon} {info.get('name', 'N/A')} <small style="color:#94a3b8; font-weight:400;">({patient_id})</small></h3>
        <div>
            <span class="info-pill">📍 {info.get('city', 'N/A')}</span>
            <span class="info-pill">🎂 {info.get('age', 'N/A')} yrs</span>
            <span class="info-pill">📏 {info.get('height', 'N/A')} m</span>
            <span class="info-pill">⚖️ {info.get('weight', 'N/A')} kg</span>
            <span class="info-pill">📊 BMI: {info.get('bmi', 'N/A')}</span>
            {verdict_badge}
        </div>
    </div>
    """, unsafe_allow_html=True)


def set_page(page_key):
    st.session_state.current_page = page_key

cols = st.columns(len(PAGES))
for i, p in enumerate(PAGES):
    with cols[i]:
        if st.button(f'{p["icon"]} {p["label"]}', key=f'nav_{p["key"]}', use_container_width=True):
            st.session_state.current_page = p["key"]
            st.rerun()


page = st.session_state.current_page


if page == "Dashboard":
    st.markdown("""
    <div class="hero-header">
        <h1>🏥 Patient Management System</h1>
        <p>A modern, full-featured interface for managing patient health records</p>
    </div>
    """, unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_URL}/view")
        if response.status_code == 200:
            data = response.json()
            total = len(data)

            ages = [v.get("age", 0) for v in data.values()]
            bmis = [v.get("bmi", 0) for v in data.values()]
            verdicts = [v.get("verdict", "").lower() for v in data.values()]

            avg_age = round(sum(ages) / total, 1) if total else 0
            avg_bmi = round(sum(bmis) / total, 1) if total else 0
            normal_count = verdicts.count("normal")
            obese_count = verdicts.count("obese")

            cols = st.columns(4)
            with cols[0]:
                st.markdown(f"""
                <div class="metric-card metric-blue">
                    <div class="metric-value">{total}</div>
                    <div class="metric-label">Total Patients</div>
                </div>""", unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div class="metric-card metric-green">
                    <div class="metric-value">{avg_age}</div>
                    <div class="metric-label">Average Age</div>
                </div>""", unsafe_allow_html=True)
            with cols[2]:
                st.markdown(f"""
                <div class="metric-card metric-orange">
                    <div class="metric-value">{avg_bmi}</div>
                    <div class="metric-label">Average BMI</div>
                </div>""", unsafe_allow_html=True)
            with cols[3]:
                st.markdown(f"""
                <div class="metric-card metric-red">
                    <div class="metric-value">{normal_count}/{total}</div>
                    <div class="metric-label">Normal BMI</div>
                </div>""", unsafe_allow_html=True)


        else:
            st.error("❌ Could not fetch data from the API.")
    except requests.exceptions.ConnectionError:
        st.markdown("""
        <div class="error-box">
            🔌 <strong>Connection Failed!</strong> — The FastAPI backend is not running.
            <br>Start it with: <code>uvicorn main:app --reload</code>
        </div>
        """, unsafe_allow_html=True)


elif page == "All Patients":
    st.markdown('<div class="section-header">📋 All Patient Records</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    try:
        response = requests.get(f"{API_URL}/view")
        if response.status_code == 200:
            data = response.json()
            if not data:
                st.info("No patients found in the system.")
            else:
                for pid, info in data.items():
                    render_patient_card(pid, info)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-header">📊 Table View</div>', unsafe_allow_html=True)
                rows = []
                for pid, info in data.items():
                    rows.append({
                        "ID": pid,
                        "Name": info.get("name"),
                        "City": info.get("city"),
                        "Age": info.get("age"),
                        "Gender": info.get("gender"),
                        "Height (m)": info.get("height"),
                        "Weight (kg)": info.get("weight"),
                        "BMI": info.get("bmi"),
                        "Verdict": info.get("verdict"),
                    })
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.error("❌ Failed to load patients.")
    except requests.exceptions.ConnectionError:
        st.error("🔌 Cannot connect to the API. Is the server running?")


elif page == "Search Patient":
    st.markdown('<div class="section-header">🔍 Search Patient by ID</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. P001", key="search_id")

    if st.button("🔎 Search", type="primary", use_container_width=True):
        if patient_id.strip():
            try:
                response = requests.get(f"{API_URL}/patient/{patient_id.strip()}")
                if response.status_code == 200:
                    info = response.json()
                    render_patient_card(patient_id, info)

                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("📏 Height", f"{info.get('height', 'N/A')} m")
                    with col2:
                        st.metric("⚖️ Weight", f"{info.get('weight', 'N/A')} kg")
                    with col3:
                        st.metric("📊 BMI", info.get("bmi", "N/A"))

                elif response.status_code == 404:
                    st.markdown('<div class="error-box">🚫 Patient not found. Check the ID and try again.</div>', unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {response.status_code}")
            except requests.exceptions.ConnectionError:
                st.error("🔌 Cannot connect to the API.")
        else:
            st.warning("⚠️ Please enter a patient ID.")


elif page == "Add Patient":
    st.markdown('<div class="section-header">➕ Add New Patient</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("add_patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            new_id = st.text_input("Patient ID *", placeholder="e.g. P006")
            new_name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma")
            new_city = st.text_input("City *", placeholder="e.g. Delhi")
            new_age = st.number_input("Age *", min_value=1, max_value=119, value=25)
        with col2:
            new_gender = st.selectbox("Gender *", options=["male", "female", "others"])
            new_height = st.number_input("Height (meters) *", min_value=0.1, max_value=3.0, value=1.70, step=0.01, format="%.2f")
            new_weight = st.number_input("Weight (kg) *", min_value=0.1, max_value=500.0, value=70.0, step=0.1, format="%.1f")

        submitted = st.form_submit_button("🚀 Create Patient", type="primary", use_container_width=True)

        if submitted:
            if not new_id.strip() or not new_name.strip() or not new_city.strip():
                st.warning("⚠️ Please fill in all required fields.")
            else:
                payload = {
                    "id": new_id.strip(),
                    "name": new_name.strip(),
                    "city": new_city.strip(),
                    "age": new_age,
                    "gender": new_gender,
                    "height": new_height,
                    "weight": new_weight,
                }
                try:
                    response = requests.post(f"{API_URL}/create", json=payload)
                    if response.status_code == 201:
                        st.markdown('<div class="success-box">✅ Patient created successfully!</div>', unsafe_allow_html=True)
                    elif response.status_code == 400:
                        st.markdown('<div class="error-box">⚠️ Patient with this ID already exists.</div>', unsafe_allow_html=True)
                    else:
                        st.error(f"API Error: {response.status_code} — {response.text}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Cannot connect to the API.")


elif page == "Update Patient":
    st.markdown('<div class="section-header">✏️ Update Patient Record</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    update_id = st.text_input("Patient ID to update", placeholder="e.g. P001", key="update_id")

    if update_id.strip():
        try:
            response = requests.get(f"{API_URL}/patient/{update_id.strip()}")
            if response.status_code == 200:
                current = response.json()
                st.markdown("##### Current Record")
                render_patient_card(update_id, current)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("##### ✏️ Edit Fields")
                st.caption("Leave a field empty to keep the current value.")

                with st.form("update_form"):
                    col1, col2 = st.columns(2)
                    with col1:
                        upd_name = st.text_input("Name", value=current.get("name", ""))
                        upd_city = st.text_input("City", value=current.get("city", ""))
                        upd_age = st.number_input("Age", min_value=1, max_value=119, value=current.get("age", 25))
                    with col2:
                        gender_options = ["male", "female"]
                        current_gender = current.get("gender", "male")
                        upd_gender = st.selectbox("Gender", options=gender_options, index=gender_options.index(current_gender) if current_gender in gender_options else 0)
                        upd_height = st.number_input("Height (m)", min_value=0.1, max_value=3.0, value=float(current.get("height", 1.70)), step=0.01, format="%.2f")
                        upd_weight = st.number_input("Weight (kg)", min_value=0.1, max_value=500.0, value=float(current.get("weight", 70.0)), step=0.1, format="%.1f")

                    update_submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

                    if update_submitted:
                        payload = {}
                        if upd_name != current.get("name"):
                            payload["name"] = upd_name
                        if upd_city != current.get("city"):
                            payload["city"] = upd_city
                        if upd_age != current.get("age"):
                            payload["age"] = upd_age
                        if upd_gender != current.get("gender"):
                            payload["gender"] = upd_gender
                        if upd_height != current.get("height"):
                            payload["height"] = upd_height
                        if upd_weight != current.get("weight"):
                            payload["weight"] = upd_weight

                        if not payload:
                            st.info("ℹ️ No changes detected.")
                        else:
                            try:
                                resp = requests.put(f"{API_URL}/edit/{update_id.strip()}", json=payload)
                                if resp.status_code == 200:
                                    st.markdown('<div class="success-box">✅ Patient updated successfully!</div>', unsafe_allow_html=True)
                                else:
                                    st.error(f"API Error: {resp.status_code} — {resp.text}")
                            except requests.exceptions.ConnectionError:
                                st.error("🔌 Cannot connect to the API.")

            elif response.status_code == 404:
                st.markdown('<div class="error-box">🚫 Patient not found.</div>', unsafe_allow_html=True)
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API.")


elif page == "Delete Patient":
    st.markdown('<div class="section-header">🗑️ Delete Patient</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    del_id = st.text_input("Patient ID to delete", placeholder="e.g. P001", key="delete_id")

    if del_id.strip():
        try:
            response = requests.get(f"{API_URL}/patient/{del_id.strip()}")
            if response.status_code == 200:
                info = response.json()
                st.markdown("##### 📋 Patient to Delete")
                render_patient_card(del_id, info)

                st.markdown("<br>", unsafe_allow_html=True)
                st.warning("⚠️ This action is **irreversible**. The patient record will be permanently removed.")

                col1, col2, _ = st.columns([1, 1, 2])
                with col1:
                    if st.button("🗑️ Confirm Delete", type="primary", use_container_width=True):
                        try:
                            resp = requests.delete(f"{API_URL}/delete/{del_id.strip()}")
                            if resp.status_code == 200:
                                st.markdown('<div class="success-box">✅ Patient deleted successfully!</div>', unsafe_allow_html=True)
                            else:
                                st.error(f"API Error: {resp.status_code}")
                        except requests.exceptions.ConnectionError:
                            st.error("🔌 Cannot connect to the API.")
            elif response.status_code == 404:
                st.markdown('<div class="error-box">🚫 No patient found with this ID.</div>', unsafe_allow_html=True)
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API.")


elif page == "Sort Patients":
    st.markdown('<div class="section-header">📊 Sort Patients</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        sort_by = st.selectbox("Sort by", ["height", "weight", "bmi"])
    with col2:
        order = st.selectbox("Order", ["asc", "desc"], format_func=lambda x: "Ascending ↑" if x == "asc" else "Descending ↓")

    if st.button("🔄 Sort", type="primary", use_container_width=True):
        try:
            response = requests.get(f"{API_URL}/sort", params={"sort_by": sort_by, "order": order})
            if response.status_code == 200:
                sorted_data = response.json()
                if sorted_data:
                    st.markdown(f"<br>", unsafe_allow_html=True)
                    st.markdown(f'<div class="section-header">Results — Sorted by {sort_by.upper()} ({order})</div>', unsafe_allow_html=True)

                    rows = []
                    for i, p in enumerate(sorted_data, 1):
                        rows.append({
                            "#": i,
                            "Name": p.get("name"),
                            "City": p.get("city"),
                            "Age": p.get("age"),
                            "Gender": p.get("gender"),
                            "Height (m)": p.get("height"),
                            "Weight (kg)": p.get("weight"),
                            "BMI": p.get("bmi"),
                            "Verdict": p.get("verdict"),
                        })
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                    # Visual chart
                    st.markdown("<br>", unsafe_allow_html=True)
                    chart_df = pd.DataFrame([
                        {"Patient": p.get("name", f"Patient {i}"), sort_by.capitalize(): p.get(sort_by, 0)}
                        for i, p in enumerate(sorted_data, 1)
                    ])
                    st.bar_chart(chart_df, x="Patient", y=sort_by.capitalize(), color="#667eea")
                else:
                    st.info("No data to display.")
            else:
                st.error(f"API Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("🔌 Cannot connect to the API.")