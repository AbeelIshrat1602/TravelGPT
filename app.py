import streamlit as st
from TravelAgents import guide_expert, location_expert, planner_expert, chatgpt_llm
from TravelTasks import location_task, guide_task, planner_task
from crewai import Crew

st.title("AI Travel Planner")

# First, verify the API key is working
with st.sidebar:
    st.subheader("OpenAI API Test")
    if st.button("Test API Connection"):
        try:
            response = chatgpt_llm.invoke("Hello, this is a test message.")
            st.success("✅ OpenAI API connection successful!")
        except Exception as e:
            st.error(f"❌ API Error: {str(e)}")

# Input form
with st.form("travel_form"):
    from_city = st.text_input("Departure City", "New York")
    destination_city = st.text_input("Destination City", "Paris")
    date_from = st.date_input("Arrival Date")
    date_to = st.date_input("Departure Date")
    interests = st.text_area("Your Interests", "art, cuisine, history")
    
    submit_button = st.form_submit_button("Plan My Trip")

if submit_button:
    # Display a progress bar/status area
    progress_area = st.empty()
    progress_area.info("Starting your travel planning process...")
    
    try:
        # Convert date objects to strings for the task functions
        date_from_str = date_from.strftime('%Y-%m-%d')
        date_to_str = date_to.strftime('%Y-%m-%d')
        
        # Try a more direct approach - just use the planner
        progress_area.info("Creating your travel plan...")
        
        # Create the planner task directly
        plan_task = planner_task(
            None, planner_expert, destination_city, interests, date_from_str, date_to_str
        )
        
        # Create a crew with just the planner
        planner_crew = Crew(
            agents=[planner_expert],
            tasks=[plan_task],
            verbose=True,
        )
        
        # Execute the task
        final_plan = planner_crew.kickoff()
        
        # Display results
        progress_area.success("Your travel plan is ready!")
        st.subheader("Your Travel Plan")
        st.markdown(final_plan)
        
        # Provide download links for the output files
        try:
            with open('travel_plan.md', 'r') as f:
                st.download_button(
                    label="Download Travel Plan",
                    data=f.read(),
                    file_name="travel_plan.md",
                    mime="text/markdown"
                )
        except FileNotFoundError:
            st.warning("Travel plan file not found. The content is displayed above.")
            
    except Exception as e:
        progress_area.error(f"Error during planning: {str(e)}")
        st.error(f"Error type: {type(e)}")
        import traceback
        st.error(traceback.format_exc())