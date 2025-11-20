# Chatbot Fix - Instructions for preserving uploaded image state

"""
PROBLEM: When chatbot uses st.rerun(), the uploaded image is lost and page returns to home.

SOLUTION: Store uploaded file in session state before any rerun happens.

Add this code to EACH analysis page (Crop Health, Pest, Weed, Irrigation, Unified):
"""

# At the top of the page, after imports:
# Initialize session state for uploaded file
if 'uploaded_file_data' not in st.session_state:
    st.session_state.uploaded_file_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None

# When file is uploaded:
uploaded_file = st.file_uploader("📸 Upload Image", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Store file data in session state
    if st.session_state.uploaded_file_data is None or uploaded_file.name != st.session_state.get('uploaded_file_name'):
        st.session_state.uploaded_file_data = uploaded_file.read()
        st.session_state.uploaded_file_name = uploaded_file.name
        uploaded_file.seek(0)  # Reset file pointer
    
    # Use the file
    image = Image.open(uploaded_file)
    
    # Run analysis and store results
    if st.button("Analyze"):
        results = run_analysis(image)
        st.session_state.analysis_results = results

# Display results from session state
if st.session_state.analysis_results is not None:
    results = st.session_state.analysis_results
    # Display tabs, chatbot, etc.
