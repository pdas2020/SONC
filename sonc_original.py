import pandas as pd
from pathlib import Path


'''
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
'''
this_dir=Path(__file__).parent if '__file__' in locals( ) else Path.cwd()
wb_file_path = this_dir / 'SONC_project_data.xlsx'

df = pd.read_excel(
    io=wb_file_path,
    engine='openpyxl',
    sheet_name='Sheet',
    skiprows=0,
    usecols='B:R',
    nrows=2079
)

# Add 'hour' column to dataframe
data["hour"] = pd.to_datetime(data["Time"], format="%H:%M:%S").dt.hour


# Get unique values of each filter
cities = list(data["City"].unique())
customer_types = list(data["Customer_type"].unique())
genders = list(data["Gender"].unique())


layout = {
    "xaxis": {"title": ""},
    "yaxis": {"title": ""},
    "margin": {"l": 150},
}


def on_filter(state):
    if (
        len(state.cities) == 0
        or len(state.customer_types) == 0
        or len(state.genders) == 0
    ):
        notify(state, "Error", "No results found. Check the filters.")
        return

    state.data_filtered, state.sales_by_product_line, state.sales_by_hour = filter(
        state.cities, state.customer_types, state.genders
    )


def filter(cities, customer_types, genders):
    # Filter the data based on the user selections
    data_filtered = data[
        data["City"].isin(cities)
        & data["Customer_type"].isin(customer_types)
        & data["Gender"].isin(genders)
    ]

    # Calculate sales by product line, summing up the "Total" for each product line, and sorting the results
    sales_by_product_line = (
        data_filtered[["Product line", "Total"]]
        .groupby(by="Product line")
        .sum()
        .sort_values(by="Total", ascending=True)
        .reset_index()  # Converts the "Product line" index into a column
    )

    # Calculate sales by hour, summing up the "Total" for each hour
    sales_by_hour = (
        data_filtered[["hour", "Total"]]
        .groupby(by="hour")
        .sum()
        .reset_index()  # Converts the "hour" index into a column
    )

    # Return the filtered dataset, sales by product line, and sales by hour
    return data_filtered, sales_by_product_line, sales_by_hour


def to_text(value):
    return "{:,}".format(int(value))


with tgb.Page() as page:
    tgb.toggle(theme=True)
    tgb.text("SONC volunteer report", class_name="h1 text-center pb2")

    with tgb.layout("1 1 1", class_name="p1"):
        with tgb.part(class_name="card"):
            tgb.text("## Total Sales:", mode="md")
            tgb.text("US $ {to_text(data_filtered['Total'].sum())}", class_name="h4")

        with tgb.part(class_name="card"):
            tgb.text("## Average Sales:", mode="md")
            tgb.text("US $ {to_text(data_filtered['Total'].mean())}", class_name="h4")

        with tgb.part(class_name="card"):
            tgb.text("## Average Rating:", mode="md")
            tgb.text(
                "{round(data_filtered['Rating'].mean(), 1)}"
                + "{'⭐' * int(round(data_filtered['Rating'].mean()))}",
                class_name="h4",
            )

    with tgb.layout("1 1 1", class_name="p1"):
        tgb.selector(
            value="{cities}",
            lov=cities,
            dropdown=True,
            multiple=True,
            label="Select cities",
            class_name="fullwidth",
            on_change=on_filter,
        )
        tgb.selector(
            value="{customer_types}",
            lov=customer_types,
            dropdown=True,
            multiple=True,
            label="Select customer types",
            class_name="fullwidth",
            on_change=on_filter,
        )
        tgb.selector(
            value="{genders}",
            lov=genders,
            dropdown=True,
            multiple=True,
            label="Select genders",
            class_name="fullwidth",
            on_change=on_filter,
        )

    with tgb.layout("1 1"):
        tgb.chart(
            "{sales_by_hour}",
            x="hour",
            y="Total",
            type="bar",
            title="Sales by Hour",
            layout=layout,
        )
        tgb.chart(
            "{sales_by_product_line}",
            x="Total",
            y="Product line",
            type="bar",
            orientation="h",
            layout=layout,
            title="Sales by Product Line",
        )


if __name__ == "__main__":
    data_filtered, sales_by_product_line, sales_by_hour = filter(
        cities, customer_types, genders
    )
    Gui(page).run(
        title="SONC volunteer report",
        use_reloader=True,
        debug=True,
        watermark="",
        margin="4em",
        favicon="images/favicon-32x32.png"
    )
