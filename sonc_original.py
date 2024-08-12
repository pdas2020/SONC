import pandas as pd
import streamlit as st



st.title("This is SONC Volunteering Data Dashboard")
volunteers = pd.read_csv(r'C:\project\SONC_backup\SONC_project_data.csv')


# Filter only the required columns
df = volunteers.filter(items=["Job", "T-Shirt size", "Job Location"])


# Standardizing T-shirt size names
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
    "First-Aid Team": ["First Aid [password: Medical]"]
}

# Function to categorize jobs
def categorize_job(x):
    for key, values in job_categories.items():
        if x in values:
            return key
    return "Standard"

# Apply categorization
df['Job Category'] = df['Job'].apply(categorize_job)

# Specify the order of T-shirt sizes
size_order = ["S", "M", "L", "XL", "2XL", "3XL", "4XL"]

# Pivot table to count T-shirt sizes by job location, shift, and job category
# Include fill_value to handle NaNs and column order for proper sequence
pivot_table = df.pivot_table(index=["Job Location", "Job Category"],
                             columns="T-Shirt size",
                             aggfunc='size',
                             fill_value=0).reindex(size_order, axis=1)

# Adding a total column
pivot_table["Total"] = pivot_table.sum(axis=1)

# Display the table
st.dataframe(pivot_table)