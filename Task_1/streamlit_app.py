
import streamlit as st
import requests
import pandas as pd

API = "http://127.0.0.1:5000/students"

st.set_page_config(
    page_title="NEXUS | Campus System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SUCCESS MESSAGE SYSTEM
if "success_message" not in st.session_state:
    st.session_state.success_message = ""

if "error_message" not in st.session_state:
    st.session_state.error_message = ""

# DESIGN AND ANIMATIONS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #e9dcff 0%, transparent 30%),
        radial-gradient(circle at 90% 80%, #fce4ee 0%, transparent 25%),
        #faf9ff;
    color: #211b35;
}

header {
    background: transparent !important;
}

.block-container {
    padding: 2rem 3rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #211832, #33204e);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 35px;
    border-radius: 25px;
    background: linear-gradient(115deg, #241634, #6743a4, #a36be2);
    color: white;
    box-shadow: 0 15px 40px rgba(87, 51, 137, 0.22);
    animation: appear 0.8s ease;
}

.hero h1 {
    color: white;
    font-size: 38px;
    font-weight: 900;
    margin: 0;
}

.hero p {
    color: #e8dafa;
}

.hero:after {
    content: "";
    position: absolute;
    width: 230px;
    height: 230px;
    right: -40px;
    top: -90px;
    border: 2px solid rgba(255,255,255,0.25);
    border-radius: 50%;
    box-shadow: 0 0 0 25px rgba(255,255,255,0.06),
                0 0 0 55px rgba(255,255,255,0.04);
    animation: rotate 15s linear infinite;
}

@keyframes rotate {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}

@keyframes appear {
    from { opacity: 0; transform: translateY(18px); }
    to { opacity: 1; transform: translateY(0); }
}

.metric-card {
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(15px);
    border: 1px solid #e9ddfa;
    border-radius: 19px;
    padding: 22px;
    min-height: 125px;
    box-shadow: 0 8px 25px rgba(75,40,120,0.07);
    animation: appear 0.8s ease;
    transition: all 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-7px);
    border-color: #a77aff;
    box-shadow: 0 15px 30px rgba(110,65,180,0.16);
}

.metric-label {
    color: #81748f;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
}

.metric-number {
    font-size: 35px;
    color: #6941a5;
    font-weight: 900;
    margin-top: 8px;
}

.section-heading {
    color: #302342;
    font-size: 22px;
    font-weight: 800;
    margin: 20px 0 10px;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.9);
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e7dafa;
    box-shadow: 0 10px 30px rgba(70,40,100,0.06);
}

.stButton > button,
.stFormSubmitButton > button {
    background: linear-gradient(100deg, #7046ad, #a16cdb);
    color: white;
    border: none;
    border-radius: 11px;
    min-height: 45px;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background: linear-gradient(100deg, #48276f, #8050bd);
    color: white;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(110,65,180,0.3);
}

div[data-testid="stDataFrame"] {
    border: 1px solid #e9ddfa;
    border-radius: 15px;
    overflow: hidden;
}

.stTextInput input, .stNumberInput input {
    border-radius: 10px;
}

.footer {
    text-align: center;
    color: #887c98;
    font-size: 11px;
    padding: 20px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# DATABASE FUNCTIONS
def get_students():
    try:
        response = requests.get(API, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        st.error("Flask API is not responding. Start app.py first.")
        return []


def show_messages():
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = ""

    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = ""


# SIDEBAR
st.sidebar.markdown("""
<div style="text-align:center;padding:20px 5px;">
    <div style="font-size:45px;">🎓</div>
    <div style="font-size:25px;font-weight:900;letter-spacing:3px;">
        NEXUS
    </div>
    <div style="font-size:10px;letter-spacing:3px;color:#d6bafa;">
        CAMPUS INTELLIGENCE
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Add Student",
        "Update Student",
        "Delete Student"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("""
<div style="padding:15px;background:#ffffff15;border-radius:14px;">
    <div style="font-size:12px;color:#d6bafa;">SYSTEM STATUS</div>
    <div style="font-size:15px;font-weight:800;margin-top:7px;">
        🟢 ONLINE
    </div>
    <div style="font-size:10px;color:#d6bafa;">
        Student database management
    </div>
</div>
""", unsafe_allow_html=True)


# HERO HEADER
st.markdown("""
<div class="hero">
    <div style="color:#f5c5dc;font-size:11px;letter-spacing:3px;font-weight:800;">
        NEXT GENERATION UNIVERSITY SYSTEM
    </div>
    <h1>NEXUS CAMPUS</h1>
    <p>One platform. Every student. Smarter management.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

# SHOW SUCCESS OR ERROR MESSAGES AFTER REFRESH
show_messages()

# GET LATEST DATABASE RECORDS
students = get_students()


# DASHBOARD
if page == "Dashboard":

    st.markdown(
        '<div class="section-heading">◈ Overview Dashboard</div>',
        unsafe_allow_html=True
    )

    total = len(students)
    departments = len(set(s["department"] for s in students))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">TOTAL STUDENTS</div>
            <div class="metric-number">{total}</div>
            <div style="color:#887c98;font-size:12px;">Registered records</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">DEPARTMENTS</div>
            <div class="metric-number">{departments}</div>
            <div style="color:#887c98;font-size:12px;">Academic departments</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">DATABASE STATUS</div>
            <div class="metric-number" style="font-size:27px;">ONLINE</div>
            <div style="color:#198754;font-size:12px;">● Connected</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-heading">◈ Student Directory</div>',
        unsafe_allow_html=True
    )

    if students:
        st.dataframe(
            pd.DataFrame(students),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No student records found.")


# ADD STUDENT
elif page == "Add Student":

    st.markdown(
        '<div class="section-heading">✚ Create Student Profile</div>',
        unsafe_allow_html=True
    )

    st.caption("Register a new student in the university database.")

    with st.form("add_student", clear_on_submit=True):

        col1, col2 = st.columns(2)

        with col1:
            student_id = st.number_input(
                "Student ID", min_value=1, step=1
            )
            name = st.text_input("Full Name")

        with col2:
            department = st.text_input("Department")
            email = st.text_input("Email Address")

        submit = st.form_submit_button(
            "✚ CREATE STUDENT",
            use_container_width=True
        )

        if submit:

            if not name.strip() or not department.strip() or not email.strip():
                st.warning("Please fill all fields.")

            else:
                try:
                    response = requests.post(
                        API,
                        json={
                            "id": int(student_id),
                            "name": name.strip(),
                            "department": department.strip(),
                            "email": email.strip()
                        },
                        timeout=5
                    )

                    if response.status_code == 201:
                        st.session_state.success_message = "🎉 Student Added Successfully!"
                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "message", "Unable to add student."
                            )
                        )

                except requests.RequestException:
                    st.error("Flask API is not responding.")


# UPDATE STUDENT
elif page == "Update Student":

    st.markdown(
        '<div class="section-heading">✎ Edit Student Profile</div>',
        unsafe_allow_html=True
    )

    if students:

        ids = [s["id"] for s in students]

        selected_id = st.selectbox(
            "Select Student ID",
            ids
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        with st.form("update_student"):

            new_name = st.text_input(
                "Full Name",
                value=selected["name"]
            )

            new_department = st.text_input(
                "Department",
                value=selected["department"]
            )

            new_email = st.text_input(
                "Email Address",
                value=selected["email"]
            )

            submit = st.form_submit_button(
                "SAVE CHANGES",
                use_container_width=True
            )

            if submit:

                if not new_name.strip() or not new_department.strip() or not new_email.strip():
                    st.warning("All fields are required.")

                else:
                    try:
                        response = requests.put(
                            f"{API}/{selected_id}",
                            json={
                                "name": new_name.strip(),
                                "department": new_department.strip(),
                                "email": new_email.strip()
                            },
                            timeout=5
                        )

                        if response.status_code == 200:
                            st.session_state.success_message = "🎉 Student Updated Successfully!"
                            st.rerun()

                        else:
                            st.error(
                                response.json().get(
                                    "message", "Update failed."
                                )
                            )

                    except requests.RequestException:
                        st.error("Flask API is not responding.")

    else:
        st.info("No student records available to update.")


# DELETE STUDENT
elif page == "Delete Student":

    st.markdown(
        '<div class="section-heading">✕ Remove Student</div>',
        unsafe_allow_html=True
    )

    if students:

        selected_id = st.selectbox(
            "Select Student",
            [s["id"] for s in students],
            format_func=lambda x: next(
                s["name"] + " (ID: " + str(s["id"]) + ")"
                for s in students if s["id"] == x
            )
        )

        selected = next(
            s for s in students if s["id"] == selected_id
        )

        st.warning(
            f"Selected Student: {selected['name']} | {selected['department']}"
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this student."
        )

        if st.button(
            "✕ DELETE STUDENT",
            use_container_width=True
        ):

            if not confirm:
                st.warning("Please confirm before deleting.")

            else:
                try:
                    response = requests.delete(
                        f"{API}/{selected_id}",
                        timeout=5
                    )

                    if response.status_code == 200:
                        st.session_state.success_message = "🗑️ Student Deleted Successfully!"
                        st.rerun()

                    else:
                        st.error(
                            response.json().get(
                                "message", "Delete failed."
                            )
                        )

                except requests.RequestException:
                    st.error("Flask API is not responding.")

    else:
        st.info("No student records available to delete.")


# FOOTER
st.markdown("""
<div class="footer">
    NEXUS CAMPUS MANAGEMENT SYSTEM<br>
    POWERED BY FLASK • SQLITE • STREAMLIT
</div>
""", unsafe_allow_html=True)
