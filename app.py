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

def get_month_events(year, month, age_group):
    """Generates events for a specific month."""
    num_days = pycalendar.monthrange(year, month)[1]
    events = []
    
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"

        # Check for overrides
        override = db.get_activity_override(st.session_state.user, date_str)

        if override:
            activity = override
        else:
            activity = get_activity_for_date(day, age_group)

        # Check completion status
        is_done = date_str in st.session_state.completed_dates

        event = {
            "title": ("✅ " if is_done else "") + activity["title"],
            "start": date_str,
            "allDay": True,
            "backgroundColor": "#d4edda" if is_done else "#ffffff",
            "borderColor": "#c3e6cb" if is_done else "#dee2e6",
            "textColor": "#155724" if is_done else "#212529",
            # Store activity data in extendedProps for easier access (optional, but helpful if calendar supports it)
            # Actually streamlit_calendar might not pass it back easily, stick to looking it up on click
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
    
    # Custom CSS for Mobile Friendliness
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
        .fc-event-title {
            font-weight: 600;
            font-size: 0.85rem;
            white-space: normal !important;
            overflow: visible !important;
        }

        .fc-toolbar-title {
            font-size: 1.2rem !important;
        }

        /* Button styling for better touch targets */
        .stButton > button {
            width: 100%;
            padding: 0.5rem 1rem;
            min-height: 44px; /* Apple Human Interface Guidelines */
        }

        /* Card-like look for activity detail */
        .activity-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
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
            st.rerun() # Refresh to update calendar content

        st.info(f"Showing activities for {st.session_state.age_group} year olds.")

        st.divider()
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.completed_dates = set()
            st.session_state.random_count = {}
            st.rerun()

    # Main Layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("📅 Activity Calendar")

        # Calculate statistics
        today = date.today()
        current_year = today.year
        current_month = today.month

        events = []
        # Load events for current month view primarily, but maybe neighbors too
        # Calendar component handles navigation, but we need to supply events.
        # Supplying full year is safest for navigation.
        for m in range(1, 13):
            events.extend(get_month_events(current_year, m, st.session_state.age_group))

        # Calendar options - Removed listMonth
        calendar_options = {
            "editable": False,
            "selectable": True,
            "headerToolbar": {
                "left": "prev,next today",
                "center": "title",
                "right": "dayGridMonth", # Removed listMonth
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

                st.session_state.selected_date = date_str

                # Fetch activity (check override first)
                override = db.get_activity_override(st.session_state.user, date_str)
                if override:
                     st.session_state.selected_activity = override
                else:
                    try:
                        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                        st.session_state.selected_activity = get_activity_for_date(date_obj.day, st.session_state.age_group)
                    except Exception as e:
                        st.error(f"Error parsing date: {e}")


    with col2:
        # TABS for Milestones vs Activity Detail
        tab_activity, tab_milestones, tab_stats = st.tabs(["🎯 Today's Activity", "🏆 Milestones", "📊 Progress"])

        with tab_activity:
            if st.session_state.selected_activity and st.session_state.selected_date:
                activity = st.session_state.selected_activity
                sel_date = st.session_state.selected_date

                st.markdown(f"""
                <div class="activity-card">
                    <h3>{activity['title']}</h3>
                    <p style="color: #666; font-size: 0.9em;">{sel_date}</p>
                    <p><strong>📝 Description:</strong><br>{activity['description']}</p>
                    <p><strong>🛠 Materials:</strong> {activity.get('materials', 'N/A')}</p>
                    <p><strong>⏱ Duration:</strong> {activity.get('duration', 'N/A')}</p>
                    <p><strong>💡 Benefits:</strong> {activity.get('benefits', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

                st.write("") # Spacer

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

                st.divider()

                # Random Activity Logic
                st.subheader("🎲 Not feeling it?")

                # Initialize count for this date if not exists
                if sel_date not in st.session_state.random_count:
                    st.session_state.random_count[sel_date] = 0

                remaining_swaps = 3 - st.session_state.random_count[sel_date]

                if remaining_swaps > 0:
                    if st.button(f"Get Random Activity ({remaining_swaps} left)"):
                        st.session_state.random_count[sel_date] += 1

                        # Get new random activity
                        new_activity = get_random_activity(st.session_state.age_group, exclude_titles=[activity['title']])

                        # Save override to DB
                        db.save_activity_override(st.session_state.user, sel_date, new_activity)

                        # Update session state
                        st.session_state.selected_activity = new_activity
                        st.rerun()
                else:
                    st.caption("You've used all your random swaps for this date!")

            else:
                st.info("👈 Select a date on the calendar to see the activity.")

        with tab_milestones:
            st.header(f"Milestones: Age {st.session_state.age_group}")
            milestones = get_milestones(st.session_state.age_group)
            for m in milestones:
                st.markdown(f"- {m}")
            st.caption("These are general guidelines. Every child develops at their own pace.")

        with tab_stats:
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

if __name__ == "__main__":
    init()
    if st.session_state.user:
        main_app()
    else:
        login_page()
