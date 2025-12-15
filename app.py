import streamlit as st
from streamlit_calendar import calendar
from datetime import datetime
from activities import get_activity_for_date

def main():
    st.set_page_config(page_title="Toddler Activity Calendar", page_icon="🎈")
    
    st.title("🎈 Toddler Activity Calendar")
    st.write("Click on a date to discover a fun activity for your 3-5 year old!")
    
    # Sidebar inputs
    st.sidebar.header("Settings")
    st.sidebar.info("Focusing on Toddler Group (3-5 years)")

    if "selected_activity" not in st.session_state:
        st.session_state.selected_activity = None
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = None

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
        }
        .fc-toolbar-title {
            font-size: 2rem;
        }
    """

    cal = calendar(events=[], options=calendar_options, custom_css=custom_css)
    
    if cal.get("callback") == "dateClick":
        date_str = cal["dateClick"]["date"]
        if "T" in date_str:
            date_str = date_str.split("T")[0]

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        day = date_obj.day
        
        st.session_state.selected_activity = get_activity_for_date(day)
        st.session_state.selected_date = date_str

    elif cal.get("callback") == "select":
        start_str = cal["select"]["start"]
        try:
            date_str = start_str[:10]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            day = date_obj.day

            st.session_state.selected_activity = get_activity_for_date(day)
            st.session_state.selected_date = date_str
        except Exception as e:
            st.error(f"Could not load activity: {e}")

    # Display the activity if one is selected
    if st.session_state.selected_activity and st.session_state.selected_date:
        st.markdown("---")
        st.header(f"📅 Activity for {st.session_state.selected_date}")
        st.subheader(f"🎨 {st.session_state.selected_activity['title']}")
        st.write(st.session_state.selected_activity['description'])

    st.markdown("---")
    st.write("Built with Streamlit & Python 🐍")

if __name__ == "__main__":
    main()
