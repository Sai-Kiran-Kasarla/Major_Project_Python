import random
import time
from datetime import date

import streamlit as st
import pandas as pd
import numpy as np

from lms import LMS
from question_bank import QUESTION_BANK
from mail_services import send_otp_email


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="LearnHub LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==================================================
# LMS OBJECT
# ==================================================

lms = LMS()


# ==================================================
# SESSION STATE
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "user_id" not in st.session_state:
    st.session_state.user_id = ""

if "user_name" not in st.session_state:
    st.session_state.user_name = ""

if "user_email" not in st.session_state:
    st.session_state.user_email = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"

if "login_otp" not in st.session_state:
    st.session_state.login_otp = ""

if "login_otp_time" not in st.session_state:
    st.session_state.login_otp_time = 0

if "registration_otp" not in st.session_state:
    st.session_state.registration_otp = ""

if "registration_otp_time" not in st.session_state:
    st.session_state.registration_otp_time = 0

if "admin_page" not in st.session_state:
    st.session_state.admin_page = "Dashboard"

# ==================================================
# EXAM SESSION STATE
# ==================================================

if "exam_id" not in st.session_state:
    st.session_state.exam_id = None

if "exam_questions" not in st.session_state:
    st.session_state.exam_questions = []

if "exam_current_index" not in st.session_state:
    st.session_state.exam_current_index = 0

if "exam_answers" not in st.session_state:
    st.session_state.exam_answers = {}

if "exam_deadline" not in st.session_state:
    st.session_state.exam_deadline = 0

if "exam_started" not in st.session_state:
    st.session_state.exam_started = False

if "exam_finished" not in st.session_state:
    st.session_state.exam_finished = False

if "exam_score" not in st.session_state:
    st.session_state.exam_score = 0


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
<style>

/* =========================================================
   LEARNHUB PREMIUM UI
   Visual-only styling: existing layout and functionality kept
   ========================================================= */

#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(37,99,235,.08), transparent 28%),
        radial-gradient(circle at 90% 12%, rgba(99,102,241,.07), transparent 26%),
        #f5f7fb;
    color: #172554;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ---------- Brand / hero ---------- */
.hero {
    background: linear-gradient(135deg, #111f55 0%, #1d4ed8 58%, #2563eb 100%);
    padding: 45px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 18px 45px rgba(15,23,42,.16);
    border: 1px solid rgba(255,255,255,.12);
    position: relative;
    overflow: hidden;
}

.hero::after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    right: -80px;
    top: -120px;
    border-radius: 50%;
    background: rgba(255,255,255,.08);
}

.hero {
    text-align: center;
    padding: 48px 30px;
    margin-left: auto;
    margin-right: auto;
}

.hero-brand {
    font-size: 54px;
    line-height: 1.1;
    letter-spacing: -1.5px;
    font-weight: 900;
    color: #ffffff;
    text-shadow: 0 3px 12px rgba(0,0,0,.18);
}

.hero-subtitle {
    margin-top: 12px;
    font-size: 19px;
    font-weight: 500;
    letter-spacing: .2px;
    color: rgba(255,255,255,.92);
}

/* Center the main content while preserving the existing layout. */
.main .block-container {
    margin-left: auto;
    margin-right: auto;
}

.profile-card, .admin-hero {
    text-align: center;
}

.profile-card h1, .profile-card h2, .profile-card p,
.admin-hero .admin-title, .admin-hero .admin-subtitle {
    text-align: center;
}

/* Center major page headings without changing navigation or functionality. */
.main h1, .main h2, .main h3 {
    text-align: center;
}

/* Keep forms and data tables readable rather than stretching edge-to-edge. */
.main .stDataFrame, .main [data-testid="stMetric"] {
    margin-left: auto;
    margin-right: auto;
}

@media (max-width: 700px) {
    .hero-brand {
        font-size: 40px;
    }
    .hero-subtitle {
        font-size: 16px;
    }
}

/* ---------- Cards ---------- */
.card {
    background: rgba(255,255,255,.96);
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #e4e8f0;
    box-shadow: 0 10px 30px rgba(15,23,42,.07);
    margin-bottom: 20px;
    transition: box-shadow .2s ease, transform .2s ease;
}

.card:hover {
    box-shadow: 0 14px 34px rgba(15,23,42,.10);
}

.metric-card {
    background: rgba(255,255,255,.98);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #e4e8f0;
    text-align: center;
    box-shadow: 0 8px 25px rgba(15,23,42,.06);
}

.metric-number {
    font-size: 32px;
    font-weight: 800;
    color: #2563eb;
}

.metric-label {
    color: #64748b;
    font-size: 15px;
}

/* ---------- Login / registration ---------- */
.login-box {
    max-width: 650px;
    margin: 40px auto;
    background: rgba(255,255,255,.98);
    padding: 40px;
    border-radius: 25px;
    box-shadow: 0 18px 55px rgba(15,23,42,.11);
    border: 1px solid #e2e8f0;
}

.brand {
    text-align: center;
    font-size: 42px;
    font-weight: 850;
    color: #172554;
    letter-spacing: -1.2px;
}

.subtitle {
    text-align: center;
    color: #64748b;
    margin-bottom: 30px;
    font-size: 17px;
}

.welcome-bar {
    max-width: 650px;
    margin: 32px auto 18px auto;
    background: linear-gradient(135deg, #ffffff, #f8faff);
    min-height: 64px;
    padding: 0 28px;
    border-radius: 20px;
    border: 1px solid #dfe5ef;
    box-shadow: 0 12px 32px rgba(15,23,42,.08);
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.welcome-title {
    font-size: 30px;
    line-height: 1.2;
    font-weight: 750;
    color: #172554;
    letter-spacing: -.5px;
}

.section-title {
    font-size: 28px;
    font-weight: 750;
    color: #172554;
    margin-bottom: 20px;
}

.profile-card {
    background: linear-gradient(135deg, #111f55 0%, #1e40af 52%, #2563eb 100%);
    color: white;
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 25px;
    box-shadow: 0 14px 36px rgba(30,64,175,.18);
    border: 1px solid rgba(255,255,255,.10);
}

/* ---------- Streamlit controls ---------- */
.stButton > button {
    border-radius: 11px;
    min-height: 45px;
    font-weight: 650;
    border: 1px solid #d7deea;
    background: #ffffff;
    color: #172554;
    transition: all .18s ease;
    box-shadow: 0 2px 8px rgba(15,23,42,.04);
}

.stButton > button:hover {
    border-color: #2563eb;
    color: #1d4ed8;
    box-shadow: 0 7px 18px rgba(37,99,235,.12);
    transform: translateY(-1px);
}

.stButton > button:focus {
    box-shadow: 0 0 0 3px rgba(37,99,235,.15);
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    border-radius: 11px;
    border: 1px solid #dbe2ec;
    background: #f8fafc;
    min-height: 45px;
    color: #172554;
    transition: all .18s ease;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus,
.stDateInput input:focus,
.stTimeInput input:focus {
    border-color: #2563eb;
    background: #ffffff;
    box-shadow: 0 0 0 3px rgba(37,99,235,.10);
}

[data-baseweb="select"] > div {
    border-radius: 11px;
    border-color: #dbe2ec;
    background: #f8fafc;
}

[data-baseweb="select"] > div:focus-within {
    border-color: #2563eb;
    box-shadow: 0 0 0 3px rgba(37,99,235,.10);
}

.stRadio label,
.stCheckbox label {
    font-weight: 500;
}

/* ---------- Metrics ---------- */
[data-testid="stMetric"] {
    background: rgba(255,255,255,.98);
    border: 1px solid #e4e8f0;
    padding: 15px;
    border-radius: 15px;
    box-shadow: 0 8px 24px rgba(15,23,42,.05);
}

[data-testid="stMetricValue"] {
    color: #172554;
    font-weight: 750;
}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {
    border: 1px solid #e1e7f0;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 24px rgba(15,23,42,.05);
}

/* ---------- Alerts ---------- */
.stAlert {
    border-radius: 12px;
    border: 1px solid rgba(148,163,184,.25);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8faff 0%, #eef3fb 100%);
    border-right: 1px solid #e1e7f0;
}

section[data-testid="stSidebar"] .stRadio label {
    padding: 8px 10px;
    border-radius: 9px;
}

/* ---------- Headings ---------- */
h1, h2, h3 {
    color: #172554;
    letter-spacing: -.4px;
}

hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 1.2rem 0;
}

/* ---------- Mobile polish ---------- */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero { padding: 30px; }
    .hero h1 { font-size: 34px; }
    .login-box { padding: 28px; }
    .brand { font-size: 36px; }
    .welcome-title { font-size: 26px; }
}

</style>
""",
    unsafe_allow_html=True
)


# ==================================================
# FUNCTIONS
# ==================================================

def generate_otp():

    return str(
        random.randint(
            100000,
            999999
        )
    )


def otp_valid(otp_time):

    if otp_time == 0:
        return False

    return (
        time.time() - otp_time
    ) <= 300


def logout():

    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.user_id = ""
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.page = "Login"

    st.rerun()


def show_header():

    st.markdown(
        """
        <div class="hero">
            <div class="hero-brand">🎓 LearnHub</div>
            <div class="hero-subtitle">Modern Learning Management System</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# LOGIN PAGE
# ==================================================

def login_page():

    # Upper branding section - rendered as HTML, not displayed as code
    st.markdown(
        """
        <div class="login-box">
            <div class="brand">🎓 LearnHub</div>
            <div class="subtitle">Learning Management System</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Welcome message is intentionally placed in the existing white bar
    # between the LearnHub branding and the login form.
    st.markdown(
        """
        <div class="welcome-bar">
            <div class="welcome-title">Welcome Back 👋</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        role = st.radio(
            "Login as",
            [
                "Student",
                "Instructor",
                "Admin"
            ],
            horizontal=True
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Sign In",
                use_container_width=True
            ):

                if email.strip() == "":
                    st.error(
                        "Please enter your email."
                    )

                elif password.strip() == "":
                    st.error(
                        "Please enter your password."
                    )

                else:

                    user = lms.login_user(
                        email,
                        password,
                        role
                    )

                    if user is None:

                        st.error(
                            "Invalid email or password."
                        )

                    else:

                        if role != "Admin":

                            approved = (
                                str(
                                    user["Approved"]
                                ).lower()
                                == "true"
                            )

                            if not approved:

                                st.warning(
                                    "Your account is waiting for admin approval."
                                )

                                return

                        st.session_state.logged_in = True
                        st.session_state.role = role

                        st.session_state.user_id = str(
                            user["ID"]
                        )

                        st.session_state.user_name = str(
                            user["Name"]
                        )

                        st.session_state.user_email = str(
                            user["Email"]
                        )

                        st.session_state.page = "Dashboard"

                        st.success(
                            "Login successful."
                        )

                        st.rerun()

        with col2:

            if st.button(
                "Login with OTP",
                use_container_width=True
            ):

                if role == "Admin":

                    st.error(
                        "Admin uses email and password login."
                    )

                elif email.strip() == "":

                    st.error(
                        "Enter your email first."
                    )

                else:

                    user = lms.get_user(
                        email,
                        role
                    )

                    if user is None:

                        st.error(
                            "Account not found. Please register."
                        )

                    else:

                        otp = generate_otp()

                        sent = send_otp_email(
                            email,
                            otp
                        )

                        if sent:

                            st.session_state.login_otp = otp

                            st.session_state.login_otp_time = time.time()

                            st.success(
                                "OTP sent to your email."
                            )

                        else:

                            st.error(
                                "OTP could not be sent. Check SMTP settings."
                            )

        if (
            st.session_state.login_otp
            != ""
        ):

            st.markdown("---")

            st.subheader(
                "Verify Login OTP"
            )

            entered_otp = st.text_input(
                "Enter 6-digit OTP",
                type="password",
                max_chars=6
            )

            if st.button(
                "Verify OTP",
                use_container_width=True
            ):

                if not otp_valid(
                    st.session_state.login_otp_time
                ):

                    st.error(
                        "OTP expired. Please request a new OTP."
                    )

                    st.session_state.login_otp = ""

                elif (
                    entered_otp
                    == st.session_state.login_otp
                ):

                    user = lms.get_user(
                        email,
                        role
                    )

                    if user is not None:

                        approved = True

                        if role == "Instructor":
                            approved = (
                                str(
                                    user["Approved"]
                                ).lower()
                                == "true"
                            )

                        if not approved:

                            st.warning(
                                "Your account is waiting for admin approval."
                            )

                        else:

                            st.session_state.logged_in = True

                            st.session_state.role = role

                            st.session_state.user_id = str(
                                user["ID"]
                            )

                            st.session_state.user_name = str(
                                user["Name"]
                            )

                            st.session_state.user_email = str(
                                user["Email"]
                            )

                            st.session_state.login_otp = ""

                            st.session_state.page = "Dashboard"

                            st.success(
                                "OTP login successful."
                            )

                            st.rerun()

                else:

                    st.error(
                        "Invalid OTP."
                    )

        st.markdown("---")

        st.write(
            "Don't have an account?"
        )

        if st.button(
            "Create New Account",
            use_container_width=True
        ):

            st.session_state.page = "Register"

            st.rerun()



# ==================================================
# REGISTRATION
# ==================================================

def register_page():

    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            "## Create Your LearnHub Account"
        )

        st.write(
            "Register as a Student or Instructor."
        )

        role = st.radio(
            "Account Type",
            [
                "Student",
                "Instructor"
            ],
            horizontal=True
        )

        name = st.text_input(
            "Full Name",
            placeholder="Enter your full name"
        )

        email = st.text_input(
            "Email Address",
            placeholder="Enter your email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Create password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm password"
        )

        if st.button(
            "Send Registration OTP",
            use_container_width=True
        ):

            if name.strip() == "":

                st.error(
                    "Enter your name."
                )

            elif email.strip() == "":

                st.error(
                    "Enter your email."
                )

            elif password.strip() == "":

                st.error(
                    "Enter a password."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must contain at least 6 characters."
                )

            elif (
                email.lower()
                == lms.ADMIN_EMAIL.lower()
            ):

                st.error(
                    "This email is reserved for the administrator."
                )

            else:

                existing = lms.get_user(
                    email,
                    role
                )

                if existing is not None:

                    st.error(
                        "This email is already registered."
                    )

                else:

                    otp = generate_otp()

                    sent = send_otp_email(
                        email,
                        otp
                    )

                    if sent:

                        st.session_state.registration_otp = otp

                        st.session_state.registration_otp_time = time.time()

                        st.session_state.registration_name = name

                        st.session_state.registration_email = email

                        st.session_state.registration_password = password

                        st.session_state.registration_role = role

                        st.success(
                            "Registration OTP sent."
                        )

                    else:

                        st.error(
                            "Unable to send OTP. Check SMTP settings."
                        )

        if (
            st.session_state.registration_otp
            != ""
        ):

            st.markdown("---")

            st.subheader(
                "Verify Email"
            )

            otp = st.text_input(
                "Registration OTP",
                type="password",
                max_chars=6
            )

            if st.button(
                "Verify & Create Account",
                use_container_width=True
            ):

                if not otp_valid(
                    st.session_state.registration_otp_time
                ):

                    st.error(
                        "OTP expired."
                    )

                elif (
                    otp
                    == st.session_state.registration_otp
                ):

                    success, result = lms.register_user(
                        st.session_state.registration_name,
                        st.session_state.registration_email,
                        st.session_state.registration_password,
                        st.session_state.registration_role
                    )

                    if success:

                        st.success(
                            "Account created successfully."
                        )

                        if st.session_state.registration_role == "Instructor":
                            st.info(
                                "Instructor account is waiting for admin approval."
                            )
                        else:
                            st.info(
                                "Student account is active. You can login now."
                            )

                        st.session_state.registration_otp = ""

                    else:

                        st.error(
                            result
                        )

                else:

                    st.error(
                        "Invalid OTP."
                    )

        st.markdown("---")

        if st.button(
            "← Back to Login",
            use_container_width=True
        ):

            st.session_state.page = "Login"

            st.rerun()

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ==================================================
# ADMIN DASHBOARD
# ==================================================

def admin_dashboard():

    # Admin navigation is shown on the page, not as a dropdown/sidebar.
    selected = st.session_state.admin_page

    if selected == "Dashboard":
        admin_home()
        return

    st.markdown("## Administrator Workspace")

    if st.button("← Back to Dashboard", use_container_width=False):
        st.session_state.admin_page = "Dashboard"
        st.rerun()

    if selected == "Approve Students":
        admin_approve("Student")
    elif selected == "Approve Instructors":
        admin_approve("Instructor")
    elif selected == "Manage Courses":
        admin_courses()
    elif selected == "Manage Enrollments":
        admin_enrollments()
    elif selected == "Attendance":
        admin_attendance()
    elif selected == "All Students":
        admin_students()
    elif selected == "All Instructors":
        admin_instructors()
    elif selected == "All Courses":
        admin_all_courses()
    elif selected == "Statistics":
        admin_statistics()
    elif selected == "Excel Data":
        admin_excel()
    elif selected == "Logout":
        logout()


# ==================================================
# ADMIN HOME
# ==================================================

def admin_home():

    show_header()

    st.markdown(
        """
        <div class="admin-hero">
            <div class="admin-kicker">ADMINISTRATION</div>
            <div class="admin-title">Welcome, Administrator 👋</div>
            <div class="admin-subtitle">Manage students, instructors, courses, attendance and platform analytics.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    stats = lms.get_statistics()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👨‍🎓 Students", stats["students"])
    c2.metric("📚 Courses", stats["courses"])
    c3.metric("📝 Enrollments", stats["enrollments"])
    c4.metric("📊 Attendance", str(stats["attendance"]) + "%")

    st.markdown("## Administration")
    st.caption("Choose a management area")

    cards = [
        ("👨‍🎓", "Approve Students", "Review student registrations."),
        ("👨‍🏫", "Approve Instructors", "Review instructor registrations."),
        ("📚", "Manage Courses", "Create courses, fees, duration and instructors."),
        ("📝", "Manage Enrollments", "Review enrollment and payment status."),
        ("📅", "Attendance", "Monitor student attendance."),
        ("👥", "All Students", "View registered students."),
        ("👨‍🏫", "All Instructors", "View instructors."),
        ("📖", "All Courses", "View the course catalogue."),
        ("📈", "Statistics", "View charts and platform analytics."),
        ("📊", "Excel Data", "View safe, non-password data."),
    ]

    for row_start in range(0, len(cards), 3):
        cols = st.columns(3)
        for col, card in zip(cols, cards[row_start:row_start + 3]):
            icon, title, text = card
            with col:
                st.markdown(
                    f"""<div class="admin-card"><div class="admin-icon">{icon}</div><div class="admin-card-title">{title}</div><div class="admin-card-text">{text}</div></div>""",
                    unsafe_allow_html=True
                )
                if st.button("Open", key="admin_open_" + title, use_container_width=True):
                    st.session_state.admin_page = title
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Logout", use_container_width=True):
        logout()


# ==================================================
# APPROVAL
# ==================================================

def admin_approve(role):

    st.markdown(
        f"## Approve {role}s"
    )

    data = lms.get_pending_users(
        role
    )

    if data.empty:

        st.success(
            f"No pending {role.lower()} approvals."
        )

        return

    for _, row in data.iterrows():

        with st.container():

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            c1, c2, c3, c4 = st.columns(
                [2, 3, 2, 1]
            )

            with c1:
                st.write(
                    "**Name**"
                )
                st.write(
                    row["Name"]
                )

            with c2:
                st.write(
                    "**Email**"
                )
                st.write(
                    row["Email"]
                )

            with c3:
                st.write(
                    "**ID**"
                )
                st.write(
                    row["ID"]
                )

            with c4:

                if st.button(
                    "Approve",
                    key="approve_" + str(
                        row["ID"]
                    )
                ):

                    lms.approve_user(
                        row["ID"]
                    )

                    st.success(
                        "Approved."
                    )

                    st.rerun()

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


# ==================================================
# ADMIN COURSES
# ==================================================

def admin_courses():

    st.markdown(
        "## Course Management"
    )

    tab1, tab2 = st.tabs(
        [
            "Create Course",
            "Assign Instructor"
        ]
    )

    with tab1:

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        title = st.text_input(
            "Course Title"
        )

        description = st.text_area(
            "Course Description"
        )

        fee = st.number_input(
            "Course Fee",
            min_value=0.0,
            step=500.0
        )

        days = st.number_input(
            "Number of Days",
            min_value=1,
            step=1
        )

        if st.button(
            "Create Course",
            use_container_width=True
        ):

            if title.strip() == "":

                st.error(
                    "Enter course title."
                )

            else:

                course_id = lms.create_course(
                    title,
                    description,
                    fee,
                    days
                )

                st.success(
                    "Course created: "
                    + course_id
                )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    with tab2:

        courses = lms.get_courses()

        instructors = lms.get_instructors()

        if courses.empty:

            st.info(
                "Create a course first."
            )

            return

        if instructors.empty:

            st.warning(
                "No approved instructors available."
            )

            return

        course_options = {}

        for _, row in courses.iterrows():

            course_options[
                row["Title"]
                + " ("
                + str(row["CourseID"])
                + ")"
            ] = row["CourseID"]

        instructor_options = {}

        for _, row in instructors.iterrows():

            instructor_options[
                row["Name"]
                + " ("
                + str(row["ID"])
                + ")"
            ] = row["ID"]

        selected_course = st.selectbox(
            "Select Course",
            course_options.keys()
        )

        selected_instructor = st.selectbox(
            "Assign Instructor",
            instructor_options.keys()
        )

        if st.button(
            "Assign Instructor",
            use_container_width=True
        ):

            lms.assign_instructor(
                course_options[
                    selected_course
                ],
                instructor_options[
                    selected_instructor
                ]
            )

            st.success(
                "Instructor assigned successfully."
            )


# ==================================================
# ADMIN ENROLLMENTS
# ==================================================

def admin_enrollments():

    st.markdown(
        "## Enrollment Management"
    )

    data = lms.read_sheet(
        "Enrollments"
    )

    if data.empty:

        st.info(
            "No enrollment requests."
        )

        return

    for _, row in data.iterrows():

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.write(
            "**Enrollment:** "
            + str(row["EnrollmentID"])
        )

        st.write(
            "Student: "
            + str(row["StudentID"])
        )

        st.write(
            "Course: "
            + str(row["CourseID"])
        )

        st.write(
            "Academic Percentage: "
            + str(row["Percentage"])
            + "%"
        )

        st.write(
            "Discount: "
            + str(row["Discount"])
            + "%"
        )

        st.write(
            "Final Fee: ₹"
            + str(row["FinalFee"])
        )

        st.write(
            "Status: "
            + str(row["Status"])
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ==================================================
# ADMIN ATTENDANCE
# ==================================================

def admin_attendance():

    st.markdown(
        "## Student Attendance"
    )

    data = lms.get_attendance()

    if data.empty:

        st.info(
            "No attendance records."
        )

        return

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# ADMIN STUDENTS
# ==================================================

def admin_students():

    st.markdown(
        "## Students"
    )

    data = lms.read_sheet(
        "Users"
    )

    if data.empty:
        return

    data = data[
        data["Role"] == "Student"
    ]

    if not data.empty:

        display = data[
            [
                "ID",
                "Name",
                "Email",
                "Role",
                "Approved"
            ]
        ]

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# ADMIN INSTRUCTORS
# ==================================================

def admin_instructors():

    st.markdown(
        "## Instructors"
    )

    data = lms.read_sheet(
        "Users"
    )

    if data.empty:
        return

    data = data[
        data["Role"] == "Instructor"
    ]

    if not data.empty:

        display = data[
            [
                "ID",
                "Name",
                "Email",
                "Role",
                "Approved"
            ]
        ]

        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# ADMIN COURSES VIEW
# ==================================================

def admin_all_courses():

    st.markdown(
        "## All Courses"
    )

    data = lms.get_courses()

    if data.empty:

        st.info(
            "No courses created."
        )

        return

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# ADMIN STATISTICS
# ==================================================

def admin_statistics():

    st.markdown(
        "## Platform Statistics"
    )

    stats = lms.get_statistics()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Students",
        stats["students"]
    )

    c2.metric(
        "Courses",
        stats["courses"]
    )

    c3.metric(
        "Enrollments",
        stats["enrollments"]
    )

    c4.metric(
        "Attendance",
        str(
            stats["attendance"]
        ) + "%"
    )

    st.markdown("---")

    chart_data = lms.attendance_chart_data()

    if (
        chart_data["Count"].sum()
        > 0
    ):

        st.subheader(
            "Attendance Distribution"
        )

        st.pyplot(
            create_pie_chart(
                chart_data
            )
        )


# ==================================================
# PIE CHART
# ==================================================

def create_pie_chart(data):

    import matplotlib.pyplot as plt

    values = np.array(
        data["Count"]
    )

    labels = list(
        data["Status"]
    )

    fig, ax = plt.subplots()

    ax.pie(
        values,
        labels=labels,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.set_title(
        "Student Attendance"
    )

    return fig


# ==================================================
# EXCEL DATA
# ==================================================

def admin_excel():

    st.markdown(
        "## Excel Data"
    )

    sheets = [
        "Users",
        "Courses",
        "Enrollments",
        "Modules",
        "Tasks",
        "Assignments",
        "AssignmentScores",
        "Exams",
        "Questions",
        "ExamResults",
        "Attendance",
        "Progress"
    ]

    selected_sheet = st.selectbox(
        "Select Data",
        sheets
    )

    data = lms.read_sheet(
        selected_sheet
    )

    if selected_sheet == "Users":

        if not data.empty:

            data = data[
                [
                    "ID",
                    "Name",
                    "Email",
                    "Role",
                    "Approved"
                ]
            ]

    if data.empty:

        st.info(
            "No data available."
        )

    else:

        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# INSTRUCTOR DASHBOARD
# ==================================================

def instructor_dashboard():

    # Keep instructor navigation separate from the Admin panel.
    # Nothing in the Admin dashboard is changed here.
    if "instructor_page" not in st.session_state:
        st.session_state.instructor_page = "Dashboard"

    show_header()

    # ------------------------------------------------
    # INSTRUCTOR WELCOME
    # ------------------------------------------------

    st.markdown(
        f"""
        <div class="profile-card">
            <div style="font-size:14px; opacity:.85; font-weight:700; letter-spacing:1px;">
                INSTRUCTOR PORTAL
            </div>
            <h1 style="margin:8px 0 8px 0; color:white;">
                Welcome, {st.session_state.user_name} 👋
            </h1>
            <p style="margin:0; font-size:17px; color:white; opacity:.92;">
                Manage your courses, students, learning content and attendance from one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------
    # INSTRUCTOR STATISTICS
    # ------------------------------------------------

    courses = get_my_courses()

    enrollments = lms.read_sheet("Enrollments")

    if courses.empty:
        course_ids = []
    else:
        course_ids = courses["CourseID"].astype(str).tolist()

    if enrollments.empty or not course_ids:
        my_enrollments = pd.DataFrame()
    else:
        my_enrollments = enrollments[
            enrollments["CourseID"].astype(str).isin(course_ids)
        ]

    pending_count = 0
    assigned_count = 0

    if not my_enrollments.empty and "Status" in my_enrollments.columns:
        pending_count = len(
            my_enrollments[
                my_enrollments["Status"].astype(str) == "Pending"
            ]
        )
        assigned_count = len(
            my_enrollments[
                my_enrollments["Status"].astype(str) == "Assigned"
            ]
        )

    attendance = lms.read_sheet("Attendance")

    if attendance.empty or not course_ids:
        attendance_percentage = 0
    else:
        my_attendance = attendance[
            attendance["CourseID"].astype(str).isin(course_ids)
        ]
        if my_attendance.empty:
            attendance_percentage = 0
        else:
            attendance_percentage = round(
                (
                    len(
                        my_attendance[
                            my_attendance["Status"].astype(str) == "Present"
                        ]
                    ) / len(my_attendance)
                ) * 100,
                1
            )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📚 My Courses", len(courses))
    c2.metric("⏳ Pending Requests", pending_count)
    c3.metric("👨‍🎓 Assigned Students", assigned_count)
    c4.metric("📅 Attendance", str(attendance_percentage) + "%")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------
    # PROFESSIONAL NAVIGATION
    # ------------------------------------------------

    st.markdown("## Instructor Workspace")
    st.caption("Choose an area to continue.")

    pages = [
        ("🏠", "Dashboard"),
        ("📚", "My Courses"),
        ("👨‍🎓", "Assign Students"),
        ("📖", "Modules"),
        ("✅", "Tasks"),
        ("📝", "Assignments"),
        ("🎯", "Exams"),
        ("📅", "Attendance"),
        ("👥", "Students"),
        ("📊", "Results"),
    ]

    for row_start in range(0, len(pages), 5):
        cols = st.columns(5)
        for col, item in zip(cols, pages[row_start:row_start + 5]):
            icon, page_name = item
            with col:
                if st.button(
                    icon + "  " + page_name,
                    key="instructor_nav_" + page_name.replace(" ", "_") ,
                    use_container_width=True
                ):
                    st.session_state.instructor_page = page_name
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------------------------------------
    # PAGE CONTENT
    # ------------------------------------------------

    selected = st.session_state.instructor_page

    if selected == "Dashboard":

        st.markdown("## Quick Overview")

        if courses.empty:
            st.info(
                "No course has been assigned to you yet. "
                "Ask the administrator to assign a course."
            )
        else:
            left, right = st.columns(2)

            with left:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("📚 Your Courses")
                for _, row in courses.iterrows():
                    st.write(
                        "**" + str(row["Title"]) + "** — "
                        + str(row["Days"]) + " days"
                    )
                    st.caption(
                        "Course ID: " + str(row["CourseID"])
                    )
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("🔔 Enrollment Requests")

                if pending_count == 0:
                    st.success("No pending enrollment requests.")
                else:
                    st.warning(
                        str(pending_count)
                        + " student enrollment request(s) need your attention."
                    )
                    if st.button(
                        "Review Requests",
                        key="review_requests",
                        use_container_width=True
                    ):
                        st.session_state.instructor_page = "Assign Students"
                        st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    elif selected == "My Courses":
        instructor_courses()

    elif selected == "Assign Students":
        instructor_assign_students()

    elif selected == "Modules":
        instructor_modules()

    elif selected == "Tasks":
        instructor_tasks()

    elif selected == "Assignments":
        instructor_assignments()

    elif selected == "Exams":
        instructor_exams()

    elif selected == "Attendance":
        instructor_attendance()

    elif selected == "Students":
        instructor_students()

    elif selected == "Results":
        instructor_results()

    # ------------------------------------------------
    # LOGOUT
    # ------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    if st.button(
        "🚪 Logout",
        key="instructor_logout",
        use_container_width=True
    ):
        logout()


# ==================================================
# INSTRUCTOR HOME - KEPT FOR COMPATIBILITY
# ==================================================

def instructor_home():
    instructor_dashboard()


# ==================================================
# INSTRUCTOR COURSES
# ==================================================

def instructor_courses():

    st.markdown("## 📚 My Courses")
    st.caption("Courses assigned to you by the administrator.")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses have been assigned to you yet.")
        return

    for _, row in courses.iterrows():

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader(str(row["Title"]))

        st.write(str(row["Description"]))

        c1, c2, c3 = st.columns(3)
        c1.write("**Course ID**")
        c1.write(str(row["CourseID"]))
        c2.write("**Duration**")
        c2.write(str(row["Days"]) + " days")
        c3.write("**Fee**")
        c3.write("₹" + str(row["Fee"]))

        st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# INSTRUCTOR ASSIGN STUDENTS
# ==================================================

def instructor_assign_students():

    st.markdown("## 👨‍🎓 Assign Students")
    st.caption("Review pending enrollment requests and assign students to your courses.")

    courses = get_my_courses()

    if courses.empty:
        st.warning("No courses are assigned to you.")
        return

    enrollments = lms.read_sheet("Enrollments")

    if enrollments.empty:
        st.info("No enrollment requests yet.")
        return

    my_enrollments = enrollments[
        enrollments["CourseID"].astype(str).isin(
            courses["CourseID"].astype(str).tolist()
        )
    ]

    if my_enrollments.empty:
        st.info("No enrollment requests for your courses.")
        return

    pending = my_enrollments[
        my_enrollments["Status"].astype(str) == "Pending"
    ]

    if pending.empty:
        st.success("There are no pending enrollment requests.")
        return

    students = lms.read_sheet("Users")

    for _, row in pending.iterrows():

        student_name = str(row["StudentID"])

        if not students.empty and "ID" in students.columns:
            found = students[
                students["ID"].astype(str) == str(row["StudentID"])
            ]
            if not found.empty:
                student_name = str(found.iloc[0]["Name"])

        course_title = str(row["CourseID"])
        found_course = courses[
            courses["CourseID"].astype(str) == str(row["CourseID"])
        ]
        if not found_course.empty:
            course_title = str(found_course.iloc[0]["Title"])

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.subheader("👤 " + student_name)
        st.write("**Course:** " + course_title)
        st.write("**Student ID:** " + str(row["StudentID"]))
        st.write("**Academic Percentage:** " + str(row["Percentage"]) + "%")
        st.write("**Academic Discount:** " + str(row["Discount"]) + "%")
        st.write("**Final Fee:** ₹" + str(row["FinalFee"]))

        if st.button(
            "✅ Assign Student",
            key="assign_" + str(row["EnrollmentID"]),
            use_container_width=True
        ):
            lms.update_enrollment_status(
                row["EnrollmentID"],
                "Assigned"
            )
            st.success("Student assigned successfully.")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# HELPER
# ==================================================

def get_my_courses():

    courses = lms.get_courses()

    if courses.empty:
        return courses

    if "InstructorID" not in courses.columns:
        return pd.DataFrame()

    return courses[
        courses["InstructorID"].astype(str)
        == str(st.session_state.user_id)
    ]


# ==================================================
# MODULES
# ==================================================

def instructor_modules():

    st.markdown("## 📖 Course Modules")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    course_options = {}
    for _, row in courses.iterrows():
        course_options[str(row["Title"])] = str(row["CourseID"])

    course_title = st.selectbox(
        "Select Course",
        list(course_options.keys()),
        key="module_course"
    )

    title = st.text_input("Module Title", key="module_title")
    description = st.text_area("Module Description", key="module_description")
    link = st.text_input(
        "🔗 Module Video / Learning Link",
        placeholder="https://www.youtube.com/watch?v=...",
        key="module_link"
    )

    st.caption("Add a YouTube, Google Drive, website, PDF or other learning URL. Students will use this link to watch/study the module.")

    if st.button("➕ Add Module", use_container_width=True):
        if not title.strip():
            st.error("Enter a module title.")
        elif not link.strip():
            st.error("Enter the module learning link.")
        elif not (link.strip().startswith("http://") or link.strip().startswith("https://")):
            st.error("Please enter a valid link starting with http:// or https://")
        else:
            lms.add_module(
                course_options[course_title],
                title.strip(),
                description.strip(),
                link.strip()
            )
            st.success("Module and learning link added successfully.")
            st.rerun()

    st.divider()
    st.markdown("### 📚 Existing Modules")

    modules = lms.get_modules(course_options[course_title])

    if modules.empty:
        st.info("No modules created for this course yet.")
    else:
        for _, module in modules.iterrows():
            module_title = str(module.get("Title", "Module"))
            module_description = str(module.get("Description", ""))
            module_link = str(module.get("Link", "")).strip()

            with st.container(border=True):
                st.markdown(f"### 📖 {module_title}")
                if module_description:
                    st.write(module_description)
                if module_link and module_link.lower() != "nan":
                    st.link_button("▶️ Open Learning Link", module_link, use_container_width=True)
                else:
                    st.warning("No learning link added.")


# ==================================================
# TASKS
# ==================================================

def instructor_tasks():

    st.markdown("## ✅ Course Tasks")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    course_options = {}
    for _, row in courses.iterrows():
        course_options[str(row["Title"])] = str(row["CourseID"])

    course_title = st.selectbox(
        "Select Course",
        list(course_options.keys()),
        key="task_course"
    )

    modules = lms.get_modules(course_options[course_title])

    if modules.empty:
        st.warning("Add a module before adding a task.")
        return

    module_options = {}
    for _, row in modules.iterrows():
        module_options[str(row["Title"])] = str(row["ModuleID"])

    module_title = st.selectbox(
        "Select Module",
        list(module_options.keys()),
        key="task_module"
    )

    task_title = st.text_input("Task Title", key="task_title")
    description = st.text_area("Task Description", key="task_description")

    if st.button("➕ Add Task", use_container_width=True):
        if not task_title.strip():
            st.error("Enter a task title.")
        else:
            lms.add_task(
                module_options[module_title],
                task_title.strip(),
                description.strip()
            )
            st.success("Task added successfully.")


# ==================================================
# ASSIGNMENTS
# ==================================================

def instructor_assignments():

    st.markdown("## 📝 Assignments")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    options = {}
    for _, row in courses.iterrows():
        options[str(row["Title"])] = str(row["CourseID"])

    course = st.selectbox(
        "Select Course",
        list(options.keys()),
        key="assignment_course"
    )

    title = st.text_input("Assignment Title", key="assignment_title")
    description = st.text_area("Description", key="assignment_description")
    total_marks = st.number_input(
        "Total Marks",
        min_value=1,
        value=100,
        step=1,
        key="assignment_marks"
    )

    if st.button("➕ Create Assignment", use_container_width=True):
        if not title.strip():
            st.error("Enter an assignment title.")
        else:
            lms.add_assignment(
                options[course],
                title.strip(),
                description.strip(),
                total_marks
            )
            st.success("Assignment created successfully.")


# ==================================================
# EXAMS
# ==================================================

def _question_bank_items():
    """Return question-bank questions in one simple format.

    Supports the current subject-based QUESTION_BANK and the older
    flat question-bank format, so old data does not break the UI.
    """
    items = []

    if isinstance(QUESTION_BANK, dict):
        for subject, questions in QUESTION_BANK.items():
            if not isinstance(questions, (list, tuple)):
                continue

            for question in questions:
                if not isinstance(question, dict):
                    continue

                text = question.get("q", question.get("question", ""))
                options = question.get("options")

                if options and len(options) >= 4:
                    option_a = options[0]
                    option_b = options[1]
                    option_c = options[2]
                    option_d = options[3]
                else:
                    option_a = question.get("a", question.get("OptionA", ""))
                    option_b = question.get("b", question.get("OptionB", ""))
                    option_c = question.get("c", question.get("OptionC", ""))
                    option_d = question.get("d", question.get("OptionD", ""))

                answer = question.get("answer", question.get("Answer", ""))

                if str(text).strip():
                    items.append({
                        "subject": str(subject),
                        "question": str(text),
                        "a": str(option_a),
                        "b": str(option_b),
                        "c": str(option_c),
                        "d": str(option_d),
                        "answer": str(answer).upper().strip()
                    })

    elif isinstance(QUESTION_BANK, (list, tuple)):
        for question in QUESTION_BANK:
            if not isinstance(question, dict):
                continue

            text = question.get("q", question.get("question", ""))
            options = question.get("options")

            if options and len(options) >= 4:
                option_a = options[0]
                option_b = options[1]
                option_c = options[2]
                option_d = options[3]
            else:
                option_a = question.get("a", question.get("OptionA", ""))
                option_b = question.get("b", question.get("OptionB", ""))
                option_c = question.get("c", question.get("OptionC", ""))
                option_d = question.get("d", question.get("OptionD", ""))

            answer = question.get("answer", question.get("Answer", ""))

            if str(text).strip():
                items.append({
                    "subject": str(question.get("subject", "General")),
                    "question": str(text),
                    "a": str(option_a),
                    "b": str(option_b),
                    "c": str(option_c),
                    "d": str(option_d),
                    "answer": str(answer).upper().strip()
                })

    return items


def instructor_exams():
    st.markdown("## 🎯 Exams")
    st.caption("Create an exam by selecting subjects and the number of questions from each subject.")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    course_options = {}
    for _, row in courses.iterrows():
        course_options[str(row["Title"])] = str(row["CourseID"])

    course_title = st.selectbox(
        "📚 Select Course",
        list(course_options.keys()),
        key="exam_course"
    )
    course_id = course_options[course_title]

    st.divider()
    st.markdown("### 📝 Create Exam")

    exam_title = st.text_input(
        "Exam Title",
        placeholder="Example: Python Assessment",
        key="exam_title"
    )

    bank_items = _question_bank_items()

    if not bank_items:
        st.error("Question bank is empty or has an invalid format.")
        return

    subjects = []
    for item in bank_items:
        if item["subject"] not in subjects:
            subjects.append(item["subject"])

    st.markdown("### 📚 Select Subjects")
    st.caption("Choose how many questions should come from each subject.")

    selected_counts = {}
    total_questions = 0

    for subject in subjects:
        available = 0
        for item in bank_items:
            if item["subject"] == subject:
                available += 1

        c1, c2, c3 = st.columns([2, 1, 1])

        with c1:
            selected = st.checkbox(
                subject,
                key="exam_subject_" + subject.replace(" ", "_")
            )

        with c2:
            st.write("Available: " + str(available))

        with c3:
            if selected:
                count = st.number_input(
                    "Questions",
                    min_value=1,
                    max_value=available,
                    value=1,
                    step=1,
                    key="exam_count_" + subject.replace(" ", "_")
                )
                selected_counts[subject] = int(count)
                total_questions += int(count)
            else:
                st.write("-")

    total_marks = total_questions

    st.divider()
    c1, c2, c3 = st.columns(3)
    c1.metric("Subjects", len(selected_counts))
    c2.metric("Total Questions", total_questions)
    c3.metric("Total Marks", total_marks)

    if selected_counts:
        st.markdown("### 📊 Question Distribution")
        for subject, count in selected_counts.items():
            st.write("• " + subject + " → " + str(count) + " question(s)")

    if st.button(
        "🚀 Create Exam",
        use_container_width=True,
        type="primary",
        key="create_subject_exam"
    ):
        if not exam_title.strip():
            st.error("Enter an exam title.")
            return

        if not selected_counts:
            st.error("Select at least one subject.")
            return

        selected_questions = []

        for subject, count in selected_counts.items():
            available_questions = []
            for item in bank_items:
                if item["subject"] == subject:
                    available_questions.append(item)

            if count > len(available_questions):
                st.error(
                    "Not enough questions in " + subject + "."
                )
                return

            selected_questions.extend(
                random.sample(available_questions, count)
            )

        random.shuffle(selected_questions)

        exam_id = lms.create_exam(
            course_id,
            exam_title.strip(),
            total_marks
        )

        added_count = 0

        for item in selected_questions:
            added = lms.add_question(
                exam_id,
                item["question"],
                item["a"],
                item["b"],
                item["c"],
                item["d"],
                item["answer"]
            )

            if added:
                added_count += 1

        st.success("🎉 Exam created successfully!")
        st.write("**Exam ID:** " + str(exam_id))
        st.write("**Questions Added:** " + str(added_count))
        st.write("**Total Marks:** " + str(total_marks))

        for subject, count in selected_counts.items():
            st.write("• " + subject + ": " + str(count))

    st.divider()
    st.markdown("### 📋 Existing Exams")

    exams = lms.read_sheet("Exams")

    if exams.empty:
        st.info("No exams have been created for this course.")
        return

    if "CourseID" in exams.columns:
        exams = exams[
            exams["CourseID"].astype(str) == str(course_id)
        ]

    if exams.empty:
        st.info("No exams have been created for this course.")
        return

    for _, row in exams.iterrows():
        exam_id = str(row.get("ExamID", ""))
        title = str(row.get("Title", "Exam"))
        questions = lms.get_questions(exam_id)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader(title)
        st.write("Exam ID: " + exam_id)
        st.write("Questions: " + str(len(questions)))
        st.write("Marks: " + str(row.get("TotalMarks", len(questions))))
        st.markdown('</div>', unsafe_allow_html=True)

# ==================================================
# ATTENDANCE
# ==================================================

def instructor_attendance():

    st.markdown("## 📅 Mark Student Attendance")
    st.caption("Mark attendance for students assigned to your courses.")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    options = {}
    for _, row in courses.iterrows():
        options[str(row["Title"])] = str(row["CourseID"])

    course_title = st.selectbox(
        "Select Course",
        list(options.keys()),
        key="attendance_course"
    )

    course_id = options[course_title]

    enrollments = lms.get_course_enrollments(course_id)

    if enrollments.empty:
        st.info("No students have requested this course yet.")
        return

    enrollments = enrollments[
        enrollments["Status"].astype(str) == "Assigned"
    ]

    if enrollments.empty:
        st.info("No students are assigned to this course yet.")
        return

    selected_date = st.date_input(
        "Attendance Date",
        value=date.today(),
        key="attendance_date"
    )

    users = lms.read_sheet("Users")

    for _, row in enrollments.iterrows():

        student_id = str(row["StudentID"])
        name = student_id

        if not users.empty and "ID" in users.columns:
            student = users[
                users["ID"].astype(str) == student_id
            ]
            if not student.empty:
                name = str(student.iloc[0]["Name"])

        st.markdown('<div class="card">', unsafe_allow_html=True)

        st.write("**" + name + "**")
        st.caption("Student ID: " + student_id)

        status = st.radio(
            "Attendance",
            ["Present", "Absent"],
            horizontal=True,
            key="attendance_status_" + student_id
        )

        if st.button(
            "💾 Save Attendance",
            key="save_attendance_" + student_id,
            use_container_width=True
        ):
            lms.mark_attendance(
                course_id,
                student_id,
                str(selected_date),
                status
            )
            st.success("Attendance saved for " + name + ".")

        st.markdown('</div>', unsafe_allow_html=True)


# ==================================================
# INSTRUCTOR STUDENTS
# ==================================================

def instructor_students():

    st.markdown("## 👥 My Students")

    courses = get_my_courses()

    if courses.empty:
        st.info("No courses are assigned to you.")
        return

    enrollments = lms.read_sheet("Enrollments")

    if enrollments.empty:
        st.info("No students have enrolled yet.")
        return

    my = enrollments[
        enrollments["CourseID"].astype(str).isin(
            courses["CourseID"].astype(str).tolist()
        )
    ]

    my = my[
        my["Status"].astype(str) == "Assigned"
    ]

    if my.empty:
        st.info("No students are assigned to your courses yet.")
        return

    users = lms.read_sheet("Users")
    result = []

    for _, row in my.iterrows():
        student = users[
            users["ID"].astype(str) == str(row["StudentID"])
        ] if not users.empty else pd.DataFrame()

        name = str(row["StudentID"])
        email = ""

        if not student.empty:
            name = str(student.iloc[0]["Name"])
            if "Email" in student.columns:
                email = str(student.iloc[0]["Email"])

        course_name = str(row["CourseID"])
        found = courses[
            courses["CourseID"].astype(str) == str(row["CourseID"])
        ]
        if not found.empty:
            course_name = str(found.iloc[0]["Title"])

        result.append(
            {
                "Student ID": str(row["StudentID"]),
                "Name": name,
                "Email": email,
                "Course": course_name,
                "Academic %": row["Percentage"],
                "Status": row["Status"]
            }
        )

    if result:
        st.dataframe(
            pd.DataFrame(result),
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# INSTRUCTOR RESULTS
# ==================================================

def instructor_results():

    st.markdown("## 📊 Student Results")

    courses = get_my_courses()
    course_ids = [] if courses.empty else courses["CourseID"].astype(str).tolist()

    results = lms.get_exam_results()

    if not results.empty and course_ids and "CourseID" in results.columns:
        results = results[
            results["CourseID"].astype(str).isin(course_ids)
        ]

    if results.empty:
        st.info("No exam results are available for your courses.")
    else:
        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

    scores = lms.read_sheet("AssignmentScores")

    if not scores.empty and course_ids and "CourseID" in scores.columns:
        scores = scores[
            scores["CourseID"].astype(str).isin(course_ids)
        ]

    if not scores.empty:
        st.subheader("Assignment Scores")
        st.dataframe(
            scores,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# STUDENT DASHBOARD
# ==================================================

def student_dashboard():

    show_header()

    st.markdown(
        f"""
        <div class="profile-card">
            <div style="font-size:14px; opacity:.85; font-weight:700; letter-spacing:1px;">
                STUDENT PORTAL
            </div>
            <h1 style="margin:8px 0 8px 0; color:white;">
                Welcome back, {st.session_state.user_name} 👋
            </h1>
            <p style="margin:0; font-size:17px; color:white; opacity:.92;">
                Learn, track your progress, attend classes and complete your courses.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Student navigation is displayed on the page.
    # No dropdown navigation is used.
    pages = [
        ("🏠", "Dashboard"),
        ("📚", "Courses"),
        ("🎓", "My Courses"),
        ("📖", "Modules"),
        ("📈", "Progress"),
        ("📅", "Attendance"),
        ("📝", "Assignments"),
        ("🎯", "Exams"),
        ("📊", "Results"),
        ("🏆", "Certificate"),
        ("👤", "Profile")
    ]

    if "student_page" not in st.session_state:
        st.session_state.student_page = "Dashboard"

    st.markdown("## Student Workspace")
    st.caption("Choose an area to continue.")

    for row_start in range(0, len(pages), 5):
        cols = st.columns(5)
        for col, item in zip(cols, pages[row_start:row_start + 5]):
            icon, page_name = item
            with col:
                if st.button(
                    icon + "  " + page_name,
                    key="student_nav_" + page_name.replace(" ", "_"),
                    use_container_width=True
                ):
                    st.session_state.student_page = page_name
                    st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    selected = st.session_state.student_page

    if selected == "Dashboard":
        student_home()
    elif selected == "Courses":
        student_courses()
    elif selected == "My Courses":
        student_my_courses()
    elif selected == "Modules":
        student_modules()
    elif selected == "Progress":
        student_progress()
    elif selected == "Attendance":
        student_attendance()
    elif selected == "Assignments":
        student_assignments()
    elif selected == "Exams":
        student_exams()
    elif selected == "Results":
        student_results()
    elif selected == "Certificate":
        student_certificate()
    elif selected == "Profile":
        student_profile()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    if st.button(
        "🚪 Logout",
        key="student_logout",
        use_container_width=True
    ):
        logout()

# ==================================================
# STUDENT HOME
# ==================================================

def student_home():

    # Header and welcome section are rendered once by student_dashboard().
    # Keeping them out of this function prevents duplicate dashboard UI.
    enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    if enrollments.empty:

        count = 0

    else:

        count = len(
            enrollments[
                enrollments["Status"]
                == "Assigned"
            ]
        )

    attendance = lms.get_attendance(
        st.session_state.user_id
    )

    if attendance.empty:

        attendance_rate = 0

    else:

        attendance_rate = (
            len(
                attendance[
                    attendance["Status"]
                    == "Present"
                ]
            )
            /
            len(attendance)
        ) * 100

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "My Courses",
        count
    )

    c2.metric(
        "Attendance",
        str(
            round(
                attendance_rate,
                1
            )
        )
        + "%"
    )

    results = lms.get_exam_results(
        st.session_state.user_id
    )

    c3.metric(
        "Exams Completed",
        len(results)
    )


# ==================================================
# STUDENT COURSES
# ==================================================

def student_courses():

    st.markdown(
        "## Available Courses"
    )

    courses = lms.get_courses()

    if courses.empty:

        st.info(
            "No courses available."
        )

        return

    for _, row in courses.iterrows():

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader(
            str(row["Title"])
        )

        st.write(
            row["Description"]
        )

        c1, c2, c3 = st.columns(3)

        c1.write(
            "**Fee:** ₹"
            + str(row["Fee"])
        )

        c2.write(
            "**Duration:** "
            + str(row["Days"])
            + " days"
        )

        c3.write(
            "**Course ID:** "
            + str(row["CourseID"])
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader(
        "Request Course Enrollment"
    )

    options = {}

    for _, row in courses.iterrows():

        options[
            row["Title"]
        ] = row["CourseID"]

    course = st.selectbox(
        "Select Course",
        options.keys()
    )

    percentage = st.number_input(
        "Academic Percentage",
        min_value=0.0,
        max_value=100.0,
        value=50.0,
        step=0.5
    )

    discount = lms.calculate_discount(
        percentage
    )

    course_data = courses[
        courses["CourseID"].astype(str)
        == str(
            options[course]
        )
    ]

    fee = float(
        course_data.iloc[0]["Fee"]
    )

    final_fee = fee - (
        fee * discount / 100
    )

    st.info(
        "Academic Discount: "
        + str(discount)
        + "% | Final Fee: ₹"
        + str(
            round(
                final_fee,
                2
            )
        )
    )

    existing_enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    already_enrolled = False
    already_pending = False

    if not existing_enrollments.empty and "CourseID" in existing_enrollments.columns:
        same_course = existing_enrollments[
            existing_enrollments["CourseID"].astype(str)
            == str(options[course])
        ]

        if not same_course.empty:
            already_enrolled = str(
                same_course.iloc[0].get("Status", "")
            ).lower() == "assigned"
            already_pending = not already_enrolled

    if already_enrolled:
        st.success("You are already enrolled in this course.")
    elif already_pending:
        st.warning("You already have a pending request for this course.")
    elif st.button(
        "Request Enrollment",
        use_container_width=True
    ):

        success, result = lms.request_enrollment(
            st.session_state.user_id,
            options[course],
            percentage
        )

        if success:

            st.success(
                "Enrollment request sent to instructor."
            )

        else:

            st.error(
                result
            )


# ==================================================
# STUDENT MY COURSES
# ==================================================

def student_my_courses():

    st.markdown(
        "## My Courses"
    )

    enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    if enrollments.empty:

        st.info(
            "You have not enrolled in any course."
        )

        return

    assigned = enrollments[
        enrollments["Status"]
        == "Assigned"
    ]

    if assigned.empty:

        st.info(
            "Your enrollment requests are waiting for instructor assignment."
        )

        return

    courses = lms.get_courses()

    for _, enrollment in assigned.iterrows():

        course = courses[
            courses["CourseID"].astype(str)
            == str(
                enrollment["CourseID"]
            )
        ]

        if course.empty:
            continue

        row = course.iloc[0]

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader(
            row["Title"]
        )

        st.write(
            row["Description"]
        )

        st.write(
            "Academic Percentage: "
            + str(
                enrollment["Percentage"]
            )
            + "%"
        )

        st.write(
            "Discount: "
            + str(
                enrollment["Discount"]
            )
            + "%"
        )

        st.write(
            "Final Fee: ₹"
            + str(
                enrollment["FinalFee"]
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ==================================================
# STUDENT MODULES
# ==================================================

def student_modules():

    st.markdown("## 📖 Course Modules")
    st.caption("Watch your instructor's learning material and mark each module as completed.")

    enrollments = lms.get_student_enrollments(st.session_state.user_id)

    if enrollments.empty:
        st.info("You are not enrolled in any course yet.")
        return

    assigned = enrollments[
        enrollments["Status"].astype(str).str.lower() == "assigned"
    ]

    if assigned.empty:
        st.info("Your course enrollment must be assigned before modules are available.")
        return

    courses = lms.get_courses()
    course_options = {}

    for _, enrollment in assigned.iterrows():
        course_id = str(enrollment["CourseID"])
        course = courses[courses["CourseID"].astype(str) == course_id]
        if not course.empty:
            course_options[str(course.iloc[0]["Title"])] = course_id

    if not course_options:
        st.info("No assigned courses found.")
        return

    selected_course = st.selectbox(
        "📚 Select Course",
        list(course_options.keys()),
        key="student_module_course"
    )

    course_id = course_options[selected_course]
    modules = lms.get_modules(course_id)

    if modules.empty:
        st.info("Your instructor has not added any modules yet.")
        return

    progress = lms.read_sheet("Progress")

    completed_count = 0

    for _, module in modules.iterrows():

        module_id = str(module.get("ModuleID", ""))
        module_title = str(module.get("Title", "Module"))
        description = str(module.get("Description", ""))
        link = str(module.get("Link", "")).strip()

        if link.lower() == "nan":
            link = ""

        completed = False

        if not progress.empty and "ModuleID" in progress.columns:
            matches = progress[
                (progress["StudentID"].astype(str) == str(st.session_state.user_id))
                & (progress["CourseID"].astype(str) == str(course_id))
                & (progress["ModuleID"].astype(str) == module_id)
            ]

            if not matches.empty:
                completed = str(matches.iloc[-1].get("Completed", "")).lower() in ["true", "1", "yes", "completed"]

        if completed:
            completed_count += 1

        with st.container(border=True):
            status_text = "✅ Completed" if completed else "⏳ Not completed"
            st.markdown(f"### {status_text} &nbsp; {module_title}", unsafe_allow_html=True)

            if description and description.lower() != "nan":
                st.write(description)

            if link:
                st.link_button(
                    "▶️ Watch / Open Module",
                    link,
                    use_container_width=True
                )

                if not completed:
                    if st.button(
                        "✅ Mark Module as Watched / Completed",
                        key="complete_module_" + module_id,
                        use_container_width=True
                    ):
                        lms.save_progress(
                            st.session_state.user_id,
                            course_id,
                            module_id,
                            True
                        )
                        st.success("Module marked as completed.")
                        st.rerun()
                else:
                    st.success("You have completed this module.")
            else:
                st.warning("Your instructor has not added a learning link yet.")

    total_modules = len(modules)
    percentage = (completed_count / total_modules * 100) if total_modules else 0

    st.divider()
    st.metric(
        "Module Progress",
        f"{completed_count}/{total_modules} completed"
    )
    st.progress(min(max(percentage / 100, 0.0), 1.0))


# ==================================================
# STUDENT PROGRESS
# ==================================================

def student_progress():

    st.markdown(
        "## My Learning Progress"
    )

    enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    assigned = enrollments[
        enrollments["Status"]
        == "Assigned"
    ]

    if assigned.empty:

        st.info(
            "No assigned courses."
        )

        return

    courses = lms.get_courses()

    for _, enrollment in assigned.iterrows():

        course_id = enrollment[
            "CourseID"
        ]

        course = courses[
            courses["CourseID"].astype(str)
            == str(course_id)
        ]

        if course.empty:
            continue

        title = course.iloc[0][
            "Title"
        ]

        st.subheader(
            title
        )

        modules = lms.get_modules(
            course_id
        )

        if modules.empty:

            st.info(
                "No modules yet."
            )

            continue

        progress = lms.get_progress(
            st.session_state.user_id,
            course_id
        )

        total = len(
            modules
        )

        completed = 0

        if not progress.empty:

            completed = len(
                progress[
                    progress["Completed"]
                    == True
                ]
            )

        percentage = 0

        if total > 0:

            percentage = (
                completed / total
            )

        st.progress(
            percentage
        )

        st.write(
            str(
                round(
                    percentage * 100,
                    1
                )
            )
            + "% completed"
        )

        for _, module in modules.iterrows():

            checked = False

            if not progress.empty:

                existing = progress[
                    progress["ModuleID"].astype(str)
                    == str(
                        module["ModuleID"]
                    )
                ]

                if not existing.empty:

                    checked = (
                        str(
                            existing.iloc[0][
                                "Completed"
                            ]
                        ).lower()
                        == "true"
                    )

            new_value = st.checkbox(
                module["Title"],
                value=checked,
                key=(
                    "module_"
                    + str(
                        module["ModuleID"]
                    )
                )
            )

            if new_value != checked:

                lms.save_progress(
                    st.session_state.user_id,
                    course_id,
                    module["ModuleID"],
                    new_value
                )

                st.rerun()


# ==================================================
# STUDENT ATTENDANCE
# ==================================================

def student_attendance():

    st.markdown(
        "## My Attendance"
    )

    data = lms.get_attendance(
        st.session_state.user_id
    )

    if data.empty:

        st.info(
            "No attendance records."
        )

        return

    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    total = len(data)

    present = len(
        data[
            data["Status"]
            == "Present"
        ]
    )

    percentage = 0

    if total > 0:

        percentage = (
            present / total
        ) * 100

    st.metric(
        "Attendance Percentage",
        str(
            round(
                percentage,
                2
            )
        )
        + "%"
    )


# ==================================================
# STUDENT ASSIGNMENTS
# ==================================================

def student_assignments():

    st.markdown(
        "## My Assignments"
    )

    enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    assigned = enrollments[
        enrollments["Status"]
        == "Assigned"
    ]

    if assigned.empty:

        st.info(
            "No assigned courses."
        )

        return

    assignments = lms.read_sheet(
        "Assignments"
    )

    if assignments.empty:

        st.info(
            "No assignments available."
        )

        return

    assignments = assignments[
        assignments["CourseID"].isin(
            assigned["CourseID"]
        )
    ]

    if assignments.empty:

        st.info(
            "No assignments available."
        )

        return

    for _, row in assignments.iterrows():

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.subheader(
            row["Title"]
        )

        st.write(
            row["Description"]
        )

        st.write(
            "Total Marks: "
            + str(
                row["TotalMarks"]
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ==================================================
# STUDENT EXAMS
# ==================================================

def student_exams():

    QUESTION_TIME = 30
    MARKS_PER_CORRECT = 1

    st.markdown("## 🎯 Online Exams")
    st.caption("Each question has 30 seconds. Correct answer = 1 mark.")

    # --------------------------------------------------
    # GET STUDENT COURSES
    # --------------------------------------------------

    enrollments = lms.get_student_enrollments(
        st.session_state.user_id
    )

    if enrollments.empty:
        st.info("You are not enrolled in any course yet.")
        return

    assigned = enrollments[
        enrollments["Status"].astype(str).str.lower() == "assigned"
    ]

    if assigned.empty:
        st.info("No approved/assigned courses are available for exams.")
        return

    exams = lms.read_sheet("Exams")

    if exams.empty:
        st.info("No exams are available yet.")
        return

    exams["CourseID"] = exams["CourseID"].astype(str)
    assigned_ids = assigned["CourseID"].astype(str).tolist()

    exams = exams[exams["CourseID"].isin(assigned_ids)]

    if exams.empty:
        st.info("No exams are available for your courses.")
        return

    # --------------------------------------------------
    # RESET OLD EXAM WHEN NOT RUNNING
    # --------------------------------------------------

    if not st.session_state.exam_started:

        exam_options = {}

        for _, row in exams.iterrows():

            title = str(row.get("Title", "Exam"))
            exam_id = str(row.get("ExamID", ""))

            course_id = str(row.get("CourseID", ""))

            exam_options[
                f"{title} | {course_id}"
            ] = exam_id

        selected_exam = st.selectbox(
            "📚 Select Exam",
            list(exam_options.keys()),
            key="student_exam_select"
        )

        selected_exam_id = exam_options[selected_exam]

        questions = lms.get_questions(selected_exam_id)

        if questions.empty:
            st.warning("This exam does not have any questions yet.")
            return

        # Exam information
        selected_row = exams[
            exams["ExamID"].astype(str) == str(selected_exam_id)
        ].iloc[0]

        total_questions = len(questions)
        total_marks = total_questions * MARKS_PER_CORRECT

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Questions", total_questions)

        with col2:
            st.metric("Time / Question", "30 sec")

        with col3:
            st.metric("Maximum Marks", total_marks)

        st.info(
            "⏱️ Every question gets 30 seconds. "
            "If you do not answer before time ends, the question is skipped automatically."
        )

        if st.button(
            "🚀 Start Exam",
            use_container_width=True,
            type="primary"
        ):

            # Convert questions to a simple list.
            question_list = []

            for _, row in questions.iterrows():
                question_list.append({
                    "QuestionID": str(row["QuestionID"]),
                    "Question": str(row["Question"]),
                    "OptionA": str(row["OptionA"]),
                    "OptionB": str(row["OptionB"]),
                    "OptionC": str(row["OptionC"]),
                    "OptionD": str(row["OptionD"]),
                    "Answer": str(row["Answer"]).upper().strip()
                })

            st.session_state.exam_id = selected_exam_id
            st.session_state.exam_questions = question_list
            st.session_state.exam_current_index = 0
            st.session_state.exam_answers = {}
            st.session_state.exam_deadline = time.time() + QUESTION_TIME
            st.session_state.exam_started = True
            st.session_state.exam_finished = False
            st.session_state.exam_score = 0

            st.rerun()

        return

    # --------------------------------------------------
    # FINISHED EXAM
    # --------------------------------------------------

    if st.session_state.exam_finished:

        questions = st.session_state.exam_questions
        total = len(questions)
        score = st.session_state.exam_score
        skipped = sum(
            1
            for q in questions
            if st.session_state.exam_answers.get(q["QuestionID"]) is None
        )
        wrong = total - score - skipped

        st.success("🎉 Exam completed successfully!")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Score", f"{score} / {total}")

        with col2:
            st.metric("Correct", score)

        with col3:
            st.metric("Wrong", wrong)

        with col4:
            st.metric("Skipped", skipped)

        percentage = (score / total * 100) if total else 0

        st.progress(
            min(max(percentage / 100, 0.0), 1.0)
        )

        st.write(
            f"### Final Result: {score}/{total} ({percentage:.2f}%)"
        )

        if st.button(
            "↩️ Back to Exams",
            use_container_width=True
        ):

            st.session_state.exam_id = None
            st.session_state.exam_questions = []
            st.session_state.exam_current_index = 0
            st.session_state.exam_answers = {}
            st.session_state.exam_deadline = 0
            st.session_state.exam_started = False
            st.session_state.exam_finished = False
            st.session_state.exam_score = 0
            st.rerun()

        return

    # --------------------------------------------------
    # RUNNING EXAM
    # --------------------------------------------------

    questions = st.session_state.exam_questions

    if not questions:
        return

    if st.session_state.exam_current_index >= len(questions):
        return

    # --------------------------------------------------
    # FINISH EXAM FUNCTION
    # --------------------------------------------------

    def finish_exam():

        score = 0

        for q in st.session_state.exam_questions:

            selected = st.session_state.exam_answers.get(
                q["QuestionID"]
            )

            if selected is not None:

                if str(selected).upper() == str(q["Answer"]).upper():
                    score += MARKS_PER_CORRECT

        total = len(st.session_state.exam_questions)

        lms.save_exam_result(
            st.session_state.exam_id,
            st.session_state.user_id,
            score,
            total
        )

        st.session_state.exam_score = score
        st.session_state.exam_finished = True
        st.session_state.exam_started = False

    # --------------------------------------------------
    # AUTOMATIC 30 SECOND TIMER
    # --------------------------------------------------

    # st.fragment refreshes only the exam area every second.
    # This keeps the rest of the website stable.
    @st.fragment(run_every="1s")
    def exam_question_area():

        # Read these values inside the fragment so the next question
        # is displayed immediately after the timer or Next button.
        questions = st.session_state.exam_questions
        current_index = st.session_state.exam_current_index

        if not questions or current_index >= len(questions):
            return

        current = questions[current_index]
        question_id = current["QuestionID"]

        remaining = int(
            max(
                0,
                st.session_state.exam_deadline - time.time()
            )
        )

        total_questions = len(
            st.session_state.exam_questions
        )

        answered_count = len(
            st.session_state.exam_answers
        )

        # ------------------------------------------------
        # HEADER
        # ------------------------------------------------

        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(
                f"### Question {current_index + 1} of {total_questions}"
            )

        with col2:
            st.metric(
                "⏱️ Time Left",
                f"{remaining} sec"
            )

        with col3:
            st.metric(
                "Answered",
                f"{answered_count}/{total_questions}"
            )

        # Progress
        progress = (current_index + 1) / total_questions

        st.progress(progress)

        # ------------------------------------------------
        # TIMER DISPLAY
        # ------------------------------------------------

        if remaining <= 10:
            timer_text = "🔴 Hurry!"
        elif remaining <= 20:
            timer_text = "🟠 Time running"
        else:
            timer_text = "🟢 Time remaining"

        st.markdown(
            f"<div style='text-align:center; font-size:22px; "
            f"font-weight:700; padding:12px; border-radius:12px; "
            f"background:#f1f5f9;'>"
            f"{timer_text} — {remaining} seconds</div>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        # ------------------------------------------------
        # QUESTION
        # ------------------------------------------------

        st.markdown(
            f"### {current_index + 1}. {current['Question']}"
        )

        options = {
            "A": current["OptionA"],
            "B": current["OptionB"],
            "C": current["OptionC"],
            "D": current["OptionD"]
        }

        labels = [
            f"A. {options['A']}",
            f"B. {options['B']}",
            f"C. {options['C']}",
            f"D. {options['D']}"
        ]

        old_answer = st.session_state.exam_answers.get(
            question_id
        )

        old_index = None

        if old_answer in ["A", "B", "C", "D"]:
            old_index = ["A", "B", "C", "D"].index(old_answer)

        selected_label = st.radio(
            "Select your answer",
            labels,
            index=old_index,
            key=f"exam_answer_{question_id}"
        )

        if selected_label:
            selected_answer = selected_label[0]
            st.session_state.exam_answers[question_id] = selected_answer

        # ------------------------------------------------
        # TIMEOUT
        # ------------------------------------------------

        if remaining <= 0:

            # No answer means skipped.
            if question_id not in st.session_state.exam_answers:
                st.session_state.exam_answers[question_id] = None

            if current_index + 1 >= total_questions:
                finish_exam()
                st.rerun()
                return

            st.session_state.exam_current_index += 1
            st.session_state.exam_deadline = (
                time.time() + QUESTION_TIME
            )

            st.rerun(scope="fragment")
            return

        # ------------------------------------------------
        # NEXT / SUBMIT
        # ------------------------------------------------

        is_last = current_index == total_questions - 1

        button_text = (
            "🏁 Submit Exam"
            if is_last
            else "Next Question ➜"
        )

        if st.button(
            button_text,
            use_container_width=True,
            type="primary",
            key=f"next_{question_id}"
        ):

            if question_id not in st.session_state.exam_answers:
                st.session_state.exam_answers[question_id] = None

            if is_last:
                finish_exam()
                st.rerun()
                return

            st.session_state.exam_current_index += 1
            st.session_state.exam_deadline = (
                time.time() + QUESTION_TIME
            )

            st.rerun(scope="fragment")

    exam_question_area()


# ==================================================
# STUDENT RESULTS
# ==================================================

def student_results():

    st.markdown(
        "## My Results"
    )

    results = lms.get_exam_results(
        st.session_state.user_id
    )

    if results.empty:

        st.info(
            "No exam results."
        )

    else:

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

    scores = lms.get_assignment_scores(
        st.session_state.user_id
    )

    if not scores.empty:

        st.subheader(
            "Assignment Scores"
        )

        st.dataframe(
            scores,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# CERTIFICATE
# ==================================================

def student_certificate():

    st.markdown(
        "## Certificate Eligibility"
    )

    attendance = lms.get_attendance(
        st.session_state.user_id
    )

    results = lms.get_exam_results(
        st.session_state.user_id
    )

    attendance_percentage = 0
    exam_percentage = 0

    if not attendance.empty:

        attendance_percentage = (
            len(
                attendance[
                    attendance["Status"]
                    == "Present"
                ]
            )
            /
            len(attendance)
        ) * 100

    if not results.empty:

        marks = results["Marks"].sum()

        total = results[
            "TotalMarks"
        ].sum()

        if total > 0:

            exam_percentage = (
                marks / total
            ) * 100

    st.metric(
        "Attendance",
        str(
            round(
                attendance_percentage,
                2
            )
        )
        + "%"
    )

    st.metric(
        "Exam Performance",
        str(
            round(
                exam_percentage,
                2
            )
        )
        + "%"
    )

    if (
        attendance_percentage >= 75
        and exam_percentage >= 50
    ):

        st.success(
            "🎓 Congratulations! You are eligible for a certificate."
        )

    else:

        st.warning(
            "Certificate eligibility requirements are not completed yet."
        )


# ==================================================
# PROFILE
# ==================================================

def student_profile():

    st.markdown(
        "## My Profile"
    )

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.write(
        "**Student ID:** "
        + st.session_state.user_id
    )

    st.write(
        "**Name:** "
        + st.session_state.user_name
    )

    st.write(
        "**Email:** "
        + st.session_state.user_email
    )

    st.write(
        "**Role:** Student"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ==================================================
# MAIN APPLICATION
# ==================================================

if not st.session_state.logged_in:

    if st.session_state.page == "Register":

        register_page()

    else:

        login_page()

else:

    if st.session_state.role == "Admin":

        admin_dashboard()

    elif st.session_state.role == "Instructor":

        instructor_dashboard()

    elif st.session_state.role == "Student":

        student_dashboard()