import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date, timedelta
import calendar as pycalendar
from activities import get_activity_for_date, get_milestones, get_random_activity
import db
import json

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
    if "age_group" not in st.session_state:
        st.session_state.age_group = "3"
    if "random_count" not in st.session_state:
        # Track random generations per day: { "YYYY-MM-DD": count }
        st.session_state.random_count = {}

    # Logic to ensure activity is loaded if date is selected (or default to today)
    if st.session_state.user:
        target_date = st.session_state.selected_date

        # If no date selected, default to today
        if target_date is None:
            target_date = date.today().strftime("%Y-%m-%d")
            st.session_state.selected_date = target_date

        # If no activity loaded for the selected date, load it
        if st.session_state.selected_activity is None:
            load_activity_for_date(target_date)

def load_activity_for_date(date_str):
    """Helper to load activity into session state for a given date string."""
    # Check for override
    override = db.get_activity_override(st.session_state.user, date_str)
    if override:
         st.session_state.selected_activity = override
    else:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            st.session_state.selected_activity = get_activity_for_date(date_obj.day, st.session_state.age_group)
        except Exception as e:
            # Fallback or error logging
            pass

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
                # Reset selection state to force fresh load in init() or right here
                st.session_state.selected_date = None
                st.session_state.selected_activity = None
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
    """Generates events for a specific month. Only shows dots for completed days."""
    num_days = pycalendar.monthrange(year, month)[1]
    events = []
    
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"

        # Check completion status
        if date_str in st.session_state.completed_dates:
            event = {
                "title": "", # No title
                "start": date_str,
                "display": "list-item", # Dot style
                "backgroundColor": "#28a745", # Green dot
                "borderColor": "#28a745",
            }
            events.append(event)

    return events

def get_previous_month_stats(current_date):
    """Calculates stats for previous months."""
    stats = []
    # Go back 3 months
    for i in range(1, 4):
        first_of_month = current_date.replace(day=1) - timedelta(days=1)
        if first_of_month.year < 2023: # Arbitrary cutoff
            break

        target_year = first_of_month.year
        target_month = first_of_month.month

        # Count completed
        count = sum(
            1 for d in st.session_state.completed_dates
            if d.startswith(f"{target_year}-{target_month:02d}")
        )

        month_name = pycalendar.month_name[target_month]
        stats.append({"month": month_name, "year": target_year, "count": count})

        current_date = first_of_month # Move back

    return stats

def main_app():
    st.set_page_config(page_title="Toddler Activity Calendar", page_icon="🎈", layout="wide")
    
    # Custom CSS for Mobile Friendliness & Dark Mode
    st.markdown("""
        <style>
        /* Increase base font size for better readability on mobile */
        html, body, [class*="css"]  {
            font-size: 16px;
        }

        /* Adjust header sizes */
        h1 { font-size: 2rem !important; }
        h2 { font-size: 1.5rem !important; }
        h3 { font-size: 1.25rem !important; }

        /* Calendar styling */
        .fc-toolbar-title {
            font-size: 1.2rem !important;
        }

        /* Button styling for better touch targets */
        .stButton > button {
            width: 100%;
            padding: 0.5rem 1rem;
            min-height: 44px; /* Apple Human Interface Guidelines */
        }

        /* Activity Detail Styling - Theme Aware */
        .activity-container {
            padding: 1rem;
            border-radius: 8px;
            /* Use slightly transparent background to work in both light/dark */
            background-color: rgba(128, 128, 128, 0.1);
            border: 1px solid rgba(128, 128, 128, 0.2);
            margin-bottom: 1rem;
        }

        .activity-title {
            color: #ff4b4b; /* Streamlit Red/Orange or similar for visibility */
            font-weight: bold;
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }

        .activity-meta {
            font-size: 0.9rem;
            opacity: 0.8;
            margin-bottom: 1rem;
        }

        </style>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header(f"Hi, {st.session_state.user}!")

        # Age Selection
        st.subheader("Child's Profile")
        age_options = ["2", "3", "4", "5"]
        selected_age = st.selectbox(
            "Select Age Group",
            age_options,
            index=age_options.index(st.session_state.age_group) if st.session_state.age_group in age_options else 1
        )

        if selected_age != st.session_state.age_group:
            st.session_state.age_group = selected_age
            # Force reload of activity
            if st.session_state.selected_date:
                load_activity_for_date(st.session_state.selected_date)
            st.rerun()

        st.info(f"Showing activities for {st.session_state.age_group} year olds.")

        st.divider()
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.completed_dates = set()
            st.session_state.random_count = {}
            st.rerun()

    # Main Layout

    # Top Section: Tabs (Activity, Milestones, Stats)
    tab_activity, tab_milestones, tab_stats = st.tabs(["🎯 Today's Activity", "🏆 Milestones", "📊 Progress"])

    with tab_activity:
        if st.session_state.selected_activity and st.session_state.selected_date:
            activity = st.session_state.selected_activity
            sel_date = st.session_state.selected_date

            # Use Streamlit markdown with classes for styling
            st.markdown(f"""
            <div class="activity-container">
                <div class="activity-title">{activity['title']}</div>
                <div class="activity-meta">📅 {sel_date}</div>
                <p><strong>📝 Description:</strong><br>{activity['description']}</p>
                <p><strong>🛠 Materials:</strong> {activity.get('materials', 'N/A')}</p>
                <p><strong>⏱ Duration:</strong> {activity.get('duration', 'N/A')}</p>
                <p><strong>💡 Benefits:</strong> {activity.get('benefits', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)

            col_act_1, col_act_2 = st.columns([1, 1])

            with col_act_1:
                # Completion Checkbox
                is_completed = sel_date in st.session_state.completed_dates

                def toggle_completion():
                    new_status = db.toggle_completion(st.session_state.user, sel_date)
                    if new_status:
                        st.session_state.completed_dates.add(sel_date)
                    else:
                        st.session_state.completed_dates.remove(sel_date)

                st.checkbox(
                    "Mark as Completed ✅",
                    value=is_completed,
                    key=f"done_{sel_date}",
                    on_change=toggle_completion
                )

            with col_act_2:
                # Random Activity Logic
                # Initialize count for this date if not exists
                if sel_date not in st.session_state.random_count:
                    st.session_state.random_count[sel_date] = 0

                remaining_swaps = 3 - st.session_state.random_count[sel_date]

                if remaining_swaps > 0:
                    if st.button(f"🎲 Pick Random ({remaining_swaps} left)", key="rnd_btn"):
                        st.session_state.random_count[sel_date] += 1

                        # Get new random activity
                        new_activity = get_random_activity(st.session_state.age_group, exclude_titles=[activity['title']])

                        # Save override to DB
                        db.save_activity_override(st.session_state.user, sel_date, new_activity)

                        # Update session state
                        st.session_state.selected_activity = new_activity
                        st.rerun()
                else:
                    st.caption("No more swaps for today.")

        else:
            st.info("Select a date below to see the activity.")

    with tab_milestones:
        st.header(f"Milestones: Age {st.session_state.age_group}")
        milestones = get_milestones(st.session_state.age_group)
        for m in milestones:
            st.markdown(f"- {m}")
        st.caption("These are general guidelines. Every child develops at their own pace.")

    with tab_stats:
        # Calculate statistics
        today = date.today()
        current_year = today.year
        current_month = today.month

        st.header("Your Progress")

        # Current Month
        completed_this_month = sum(
            1 for d in st.session_state.completed_dates
            if d.startswith(f"{current_year}-{current_month:02d}")
        )
        st.metric("This Month", completed_this_month)

        st.subheader("Previous Months")
        past_stats = get_previous_month_stats(today)
        if past_stats:
            for stat in past_stats:
                st.write(f"**{stat['month']} {stat['year']}**: {stat['count']} activities completed")
        else:
            st.write("No previous data yet.")

    st.divider()

    # Bottom Section: Calendar
    st.header("📅 Calendar Tracker")
    st.caption("Click a date to view or change the activity.")

    today = date.today()
    current_year = today.year

    events = []
    for m in range(1, 13):
        events.extend(get_month_events(current_year, m))

    calendar_options = {
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth",
        },
        "initialView": "dayGridMonth",
        "height": "auto",
    }

    cal = calendar(events=events, options=calendar_options, key="calendar")

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

            # Check if selection changed
            if date_str != st.session_state.selected_date:
                st.session_state.selected_date = date_str
                load_activity_for_date(date_str)
                st.rerun()

if __name__ == "__main__":
    init()
    if st.session_state.user:
        main_app()
    else:
        login_page()
