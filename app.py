import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime, date
import calendar as pycalendar
from activities import get_activity_for_date

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

def main():
    st.set_page_config(page_title="Toddler Activity Calendar", page_icon="🎈")
    
    st.title("🎈 Toddler Activity Calendar")

    # Initialize session state for completion
    if "completed_dates" not in st.session_state:
        st.session_state.completed_dates = set()
    if "selected_activity" not in st.session_state:
        st.session_state.selected_activity = None
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = None

    # Calculate statistics for the current month (based on today or selected view?)
    # For simplicity, we'll use the real-world current month to display the "This Month" stat
    # unless we can easily get the calendar's view.
    # Let's use today's month as the default context.
    today = date.today()
    current_year = today.year
    current_month = today.month
    
    # We will generate events for the current year to ensure navigation works nicely.
    # In a real app, we might want to do this dynamically based on view range.
    events = []
    for m in range(1, 13):
        events.extend(get_month_events(current_year, m))

    # Calculate completed in current month
    completed_this_month = sum(
        1 for d in st.session_state.completed_dates
        if d.startswith(f"{current_year}-{current_month:02d}")
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("Click on a date to discover a fun activity for your 3-5 year old!")
    with col2:
        st.metric("Completed This Month", f"{completed_this_month}")
    
    # Sidebar inputs
    st.sidebar.header("Settings")
    st.sidebar.info("Focusing on Toddler Group (3-5 years)")

    # Calendar options
    calendar_options = {
        "editable": False,
        "selectable": True,
        "headerToolbar": {
            "left": "today prev,next",
            "center": "title",
            "right": "dayGridMonth",
        },
        "initialView": "dayGridMonth",
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
            font-size: 2rem;
        }
        .fc-daygrid-event {
            white-space: normal !important;
            align-items: center;
        }
    """

    cal = calendar(events=events, options=calendar_options, custom_css=custom_css, key="calendar")

    # Handle callbacks
    if cal.get("callback") == "dateClick" or cal.get("callback") == "eventClick" or cal.get("callback") == "select":
        # Determine the date
        date_str = None
        if cal.get("callback") == "dateClick":
            date_str = cal["dateClick"]["date"]
        elif cal.get("callback") == "eventClick":
            # If they click the event (the title), we still want to show details
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
        
        # Details container
        with st.container():
            st.subheader(f"🎨 {st.session_state.selected_activity['title']}")
            st.write(st.session_state.selected_activity['description'])

            # Completion Checkbox
            # We use a key based on the date so it's unique per day
            is_completed = st.session_state.selected_date in st.session_state.completed_dates

            def toggle_completion():
                target_date = st.session_state.selected_date
                if target_date in st.session_state.completed_dates:
                    st.session_state.completed_dates.remove(target_date)
                else:
                    st.session_state.completed_dates.add(target_date)

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
    main()
