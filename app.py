import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
import calendar as pycalendar
from activities import get_activity_for_date
import db

def init():
    db.init_db()
    if "user" not in st.session_state:
        st.session_state.user = None
    if "completed_dates" not in st.session_state:
        st.session_state.completed_dates = set()
    if "selected_activity" not in st.session_state:
        st.session_state.selected_activity = None
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = None

def login_page():
    st.title("🎈 Kids Activity Helper")
    st.subheader("Login / Register")

    menu = ["Login", "Register"]
    choice = st.selectbox("Menu", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            if db.login_user(username, password):
                st.success(f"Welcome {username}")
                st.session_state.user = username
                st.session_state.completed_dates = db.get_user_completions(username)
                st.rerun()
            else:
                st.error("Incorrect Username/Password")

    elif choice == "Register":
        if st.button("Register"):
            if db.register_user(username, password):
                st.success("You have successfully created an account")
                st.info("Go to Login Menu to login")
            else:
                st.error("Username already exists")

def get_month_events(year, month):
    """Generates events for a specific month."""
    num_days = pycalendar.monthrange(year, month)[1]
    events = []
    
    for day in range(1, num_days + 1):
        activity = get_activity_for_date(day)
        date_str = f"{year}-{month:02d}-{day:02d}"

        # Check completion status
        is_done = date_str in st.session_state.completed_dates

        event = {
            "title": ("✅ " if is_done else "") + activity["title"],
            "start": date_str,
            "allDay": True,
            "backgroundColor": "#d4edda" if is_done else "#e2e3e5",
            "borderColor": "#c3e6cb" if is_done else "#d6d8db",
            "textColor": "#155724" if is_done else "#383d41",
        }
        events.append(event)
    return events

def main_app():
    st.set_page_config(page_title="Toddler Activity Calendar", page_icon="🎈")
    
    # Header with Logout
    col_h1, col_h2 = st.columns([4, 1])
    with col_h1:
        st.title("🎈 Toddler Activity Calendar")
    with col_h2:
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.completed_dates = set()
            st.rerun()

    # Calculate statistics
    today = date.today()
    current_year = today.year
    current_month = today.month
    
    events = []
    for m in range(1, 13):
        events.extend(get_month_events(current_year, m))

    completed_this_month = sum(
        1 for d in st.session_state.completed_dates
        if d.startswith(f"{current_year}-{current_month:02d}")
    )
    
    # Mobile-friendly layout: Stack the metric on top or use full width columns
    st.metric("Completed This Month", f"{completed_this_month}")
    st.caption("Click on a date to discover a fun activity for your 3-5 year old!")

    # Sidebar
    st.sidebar.header(f"Hi, {st.session_state.user}!")
    st.sidebar.info("Focusing on Toddler Group (3-5 years)")

    # Calendar options - Mobile friendly adjustments
    # Add view switching to list view for mobile
    calendar_options = {
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth,listMonth",
        },
        "initialView": "dayGridMonth",
        "height": "auto", # Let it grow
    }

    custom_css = """
        .fc-event-past {
            opacity: 0.8;
        }
        .fc-event-time {
            font-style: italic;
        }
        .fc-event-title {
            font-weight: 700;
            font-size: 0.8rem;
            white-space: normal;
        }
        .fc-toolbar-title {
            font-size: 1.5rem; /* Smaller title for mobile */
        }
        .fc-daygrid-event {
            white-space: normal !important;
            align-items: center;
        }
        /* Make toolbar buttons stack on very small screens if needed */
        @media (max-width: 500px) {
            .fc-header-toolbar {
                flex-direction: column;
                gap: 10px;
            }
        }
    """

    cal = calendar(events=events, options=calendar_options, custom_css=custom_css, key="calendar")

    # Handle callbacks
    if cal.get("callback") == "dateClick" or cal.get("callback") == "eventClick" or cal.get("callback") == "select":
        date_str = None
        if cal.get("callback") == "dateClick":
            date_str = cal["dateClick"]["date"]
        elif cal.get("callback") == "eventClick":
            date_str = cal["eventClick"]["event"]["start"]
        elif cal.get("callback") == "select":
             date_str = cal["select"]["start"]

        if date_str:
            if "T" in date_str:
                date_str = date_str.split("T")[0]

            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                day = date_obj.day

                st.session_state.selected_activity = get_activity_for_date(day)
                st.session_state.selected_date = date_str
            except Exception as e:
                st.error(f"Error parsing date: {e}")

    # Display the activity if one is selected
    if st.session_state.selected_activity and st.session_state.selected_date:
        st.markdown("---")
        st.header(f"📅 Activity for {st.session_state.selected_date}")
        
        with st.container():
            st.subheader(f"🎨 {st.session_state.selected_activity['title']}")
            st.write(st.session_state.selected_activity['description'])

            # Completion Checkbox
            is_completed = st.session_state.selected_date in st.session_state.completed_dates

            def toggle_completion():
                target_date = st.session_state.selected_date
                user = st.session_state.user

                # Update DB
                new_status = db.toggle_completion(user, target_date)

                # Update Session State
                if new_status:
                    st.session_state.completed_dates.add(target_date)
                else:
                    st.session_state.completed_dates.remove(target_date)

            st.checkbox(
                "Mark as Done",
                value=is_completed,
                key=f"done_{st.session_state.selected_date}",
                on_change=toggle_completion
            )

            if is_completed:
                st.success("Great job! Activity completed.")

    st.markdown("---")
    st.write("Built with Streamlit & Python 🐍")

if __name__ == "__main__":
    init()
    if st.session_state.user:
        main_app()
    else:
        login_page()
