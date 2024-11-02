import streamlit as st
import streamlit_shadcn_ui as ui


def sample_data():

    st.title("Sample Data")
    st.write(f'Welcome *{st.session_state["name"]}*!')
    cols = st.columns(3)
    with cols[0]:
        ui.metric_card(title="Spending Score", content="5.33",
                       description="+5.5% from last month", key="card1")
    with cols[1]:
        ui.metric_card(title="Budget", content="$3,000",
                       description="#change your budget on the spending tracker tab", key="card2")
    with cols[2]:
        ui.metric_card(title="Budget Used", content="$1,342.45/$3,000",
                       description="+10.4% budget spending compared to the last month", key="card3")
    trigger_btn = ui.button(text="Trigger Button", key="trigger_btn")
    ui.alert_dialog(show=trigger_btn, title="Alert Dialog", description="This is an alert dialog",
                    confirm_label="OK", cancel_label="Cancel", key="alert_dialog1")

    dt = ui.date_picker(key="date_picker", label="Date Picker")
    st.write("Date:", dt)

    choice = ui.select(options=["Apple", "Banana", "Orange"])

    st.markdown(f"Current value: {choice}")

    with st.sidebar:
        st.write("Welcome to the your Dashboard!")
