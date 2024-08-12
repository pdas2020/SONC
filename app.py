import pandas as pd
import streamlit as st

st.title("SONC Volunteering Data Analysis")

st.markdown("""
This Dashboard allows you to upload a file and provides data insights!
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2020, 2025))))

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Check if essential columns exist in the DataFrame
    expected_columns = ["Job", "T-Shirt size", "Job Location"]
    if not all(column in df.columns for column in expected_columns):
        st.error("Uploaded CSV does not contain all the required columns.")
        st.stop()

    # Filter only the required columns
    df = df.filter(items=expected_columns)

    # Standardizing T-Shirt size names
    size_mapping = {
        's': 'S', 'small': 'S', 'Small': 'S',
        'm': 'M', 'medium': 'M', 'Medium': 'M',
        'l': 'L', 'large': 'L', 'Large': 'L',
        'xl': 'XL', 'extra large': 'XL', 'Extra Large': 'XL', 'x-large': 'XL', 'X-Large': 'XL',
        '2xl': '2XL', 'xxl': '2XL', 'XXL': '2XL', 'double xl': '2XL', 'Double XL': '2XL',
        '3xl': '3XL', 'xxxl': '3XL', 'XXXL': '3XL', 'triple xl': '3XL', 'Triple XL': '3XL',
        '4xl': '4XL', 'xxxxl': '4XL', 'XXXXL': '4XL', 'quadruple xl': '4XL', 'Quadruple XL': '4XL'
    }

    # Apply the size mapping
    df['T-Shirt size'] = df['T-Shirt size'].map(size_mapping).fillna(df['T-Shirt size'])

    # Define categories for grouping
    job_categories = {
        "Venue Welcome Team": ["Station Manager", "Usher", "Venue Assistant", "Venue Welcome Team", "Venue Welcome-Access Control", "Venue Welcome-Transportation", "Volunteer Check-In/Venue Assistant"],
        "Power Team": ["Power Team"],
        "First-Aid Team": ["First Aid"]
    }

    # Function to categorize jobs
    def categorize_job(x):
        for key, values in job_categories.items():
            if x in values:
                return key
        return "Standard"

    # Apply categorization
    df['Job Category'] = df['Job'].apply(categorize_job)

    # Specify the order of T-Shirt sizes
    size_order = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]

    # Pivot table to count T-Shirt sizes by job location and job category
    pivot_table = df.pivot_table(index=["Job Location", "Job Category"],
                                 columns="T-Shirt size",
                                 aggfunc='size',
                                 fill_value=0).reindex(size_order, axis=1)

    # Adding a total column
    pivot_table["Total"] = pivot_table.sum(axis=1)


# Sidebar - Job Category Selection
    job_category_choices = list(job_categories.keys()) + ['Standard']  # Including 'Standard' for uncategorized jobs
    selected_job_category = st.sidebar.multiselect('Select Job Category', job_category_choices, default=job_category_choices)

    # Filtering data by job category
    if selected_job_category:
        filtered_data = pivot_table.loc[pivot_table.index.get_level_values('Job Category').isin(selected_job_category)]
    else:
        filtered_data = pivot_table  # If no specific selection, show all

    # Display the filtered data
    st.subheader("Filtered Table by Job Category")
    st.dataframe(filtered_data)

# Sidebar - T-shirt Size selection
    st.subheader("Filtered Table by T-Shirt size")
    selected_size = st.sidebar.multiselect('Select T-Shirt size to filter by', size_order, default=size_order)
    if selected_size:
        filtered_data = pivot_table[pivot_table.columns.intersection(selected_size + ["Total"])]
        st.dataframe(filtered_data)

 # Sidebar - Job Location selection
    job_locations = df['Job Location'].unique()
    selected_job_locations = st.sidebar.multiselect('Job Location', job_locations, default=job_locations)

    # Filtering data by selected job locations
    df_filtered = df[df['Job Location'].isin(selected_job_locations)]

    # Displaying filtered data
    st.subheader("Filtered Table by Job Location")
    st.dataframe(df_filtered)       

else:
    st.write("Waiting on file upload...")
