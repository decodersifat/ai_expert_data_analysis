import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


st.set_page_config(page_title="AI Expert Challenge !!!", page_icon=":pencil2:", layout="wide")


page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1501426026826-31c667bdf23d");
background-size: 180%;
background-position: top left;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""


st.markdown(page_bg_img, unsafe_allow_html=True)




st.markdown(
    """
    <h1 style='text-align: center;'>Team: Coding Slug</h1>
    """,
    unsafe_allow_html=True
)
st.header("Label 1 ::black_nib:",divider=True)

hide_streamlit_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
div.block-container {padding-top: 1rem;}
.css-1y0tads {padding-top: 0rem;}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


st.subheader(":bar_chart: DataSet")

df = pd.read_csv('AI_Expert_Challenge/ecommerce_customer_behavior_dataset.csv')
st.dataframe(df)

mean_mode_median_col, col2 = st.columns(2)

mean = df['Age'].mean()
median = df['Age'].median()
mode = df['Age'].mode()[0]
mean_mode_median = [mean, median, mode]
label = [f'Mean: {mean:.2f}', f'Median: {median:.2f}', f'Mode: {mode:.2f}']

with mean_mode_median_col:
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=label,
        values=mean_mode_median,
        hole=0.4,
        marker=dict(
            colors=['#FF9999', '#66B2FF', '#99FF99'],
            line=dict(color='black', width=3)
        ),
        textinfo='percent+label'
    ))

    fig.update_layout(
        title={
            'text': 'Mean, Median, and Mode Calculation on Age',
            'font': dict(size=15, color='white'),
            'x': 0.2
        },
        paper_bgcolor=None,
        plot_bgcolor='black',
        showlegend=True
    )
    st.plotly_chart(fig)

    # Divider
    st.subheader('Comparison of Variance and Standard Deviation',divider=True)

    # Calculate Variance and Standard Deviation
    variance = df['Purchase Amount ($)'].var()
    std_deviation = df['Purchase Amount ($)'].std()

    # CSS for card styling
    card_style = """
        <style>
        .card-var {
            background-color: #004d1a;
            border: 1px solid #33ff77;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 10px;
        }
        .card-std-div {
            background-color: #001a4d;
            border: 1px solid #3333ff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 10px;
        }

        .card-header {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .card-value-var {
            font-size: 24px;
            color: #33ff77;
        }

        .card-value-std-div {
            font-size: 24px;
            color: #1aa3ff;
        }
        </style>
    """

    # Inject custom CSS
    st.markdown(card_style, unsafe_allow_html=True)
    
    # Display cards using custom HTML and CSS
    col_var, col_std_dev = st.columns(2)
    
    with col_var:
        st.markdown(f"""
            <div class="card-var">
                <div class="card-header">Variance</div>
                <div class="card-value-var">{variance:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    with col_std_dev:
        st.markdown(f"""
            <div class="card-std-div">
                <div class="card-header">Standard Deviation</div>
                <div class="card-value-std-div">{std_deviation:.2f}</div>
            </div>
        """, unsafe_allow_html=True)

    # Display the Variance and Standard Deviation Chart
    metrics = ['Variance', 'Standard Deviation']
    values = [variance, std_deviation]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=values, y=metrics,
        mode='lines+markers',
        line=dict(color='gray', width=2),
        marker=dict(color=['#ff6347', '#4682b4'], size=12),
        name='Value'
    ))

    fig.update_layout(
        xaxis_title='Value',
        yaxis_title='Metric',
        plot_bgcolor=None,
        paper_bgcolor=None,
        font=dict(size=12)
    )

    # Show the plot
    st.plotly_chart(fig)

# Z-Score Analysis
with col2:
    # Calculate Z-scores
    new_df = df.copy()
    new_df['z-score-of-payment'] = (new_df['Purchase Amount ($)'] - new_df['Purchase Amount ($)'].mean()) / new_df['Purchase Amount ($)'].std()

    # Create histogram of Z-scores
    fig = px.histogram(new_df, x='z-score-of-payment', nbins=15, title='Histogram of Z-Scores for Purchase Amounts',
                       labels={'z-score-of-payment': 'Z-Score', 'count': 'Frequency'},
                       color_discrete_sequence=['skyblue'])

    # Add vertical line for Z=0
    fig.add_shape(type='line',
                  x0=0, x1=0,
                  y0=0, y1=new_df['z-score-of-payment'].count(),
                  line=dict(color='red', dash='dash'))

    # Display the histogram
    st.plotly_chart(fig)

    # Display the dataframe with Z-scores
    st.dataframe(new_df[['Purchase Amount ($)', 'z-score-of-payment']],use_container_width=True)



st.subheader('Top 3 Product Categories Based on Number of Purchases', divider=True)
# Create two columns inside col_top_cate
col_top_three_horizontal, con_top_three_vertical = st.columns(2)
# Prepare data for the charts
df_categories = df.groupby('Product Category')['Number of Items Purchased'].sum().reset_index()
df_categories = df_categories.sort_values(by='Number of Items Purchased', ascending=False)
top_three_products = df_categories.head(3)
# Horizontal bar chart
with col_top_three_horizontal:
    fig = px.bar(
        df_categories, 
        y='Product Category',  # Swap 'x' and 'y' for horizontal bar chart
        x='Number of Items Purchased',  # Use 'Number of Items Purchased' as the x-axis
        text='Number of Items Purchased',
        color='Product Category',  # Use different colors for each category
        color_discrete_sequence=px.colors.qualitative.Set2  # A visually appealing color scheme
    )
    # Customize the layout for a more appealing look
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(size=12), 
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',  
            title_text='Number of Items Purchased'
        ),
        yaxis=dict(
            showgrid=False,  # Remove gridlines for y-axis
            title_text='Product Category'
        ),
        margin=dict(l=50, r=50, t=70, b=50)  # Adjust margins
    )
    # Add text formatting for the bars
    fig.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside', 
        marker_line_color='black', 
        marker_line_width=1.5
    )
    st.plotly_chart(fig)

with con_top_three_vertical:
    fig = px.bar(
        top_three_products,
        x='Product Category',
        y='Number of Items Purchased',
        text='Number of Items Purchased',
        color='Product Category',  # Use different colors for each category
        color_discrete_sequence=px.colors.qualitative.Set2  # A visually appealing color scheme
    )
    # Customize the layout for a more appealing look
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        font=dict(size=12),  # General font size for the chart
        xaxis=dict(
            showgrid=False,  # Remove gridlines for x-axis
            title_text='Product Category'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',  # Light gray grid color for the y-axis
            title_text='Number of Items Purchased'
        ),
        margin=dict(l=50, r=50, t=70, b=50)  # Adjust margins
    )
    # Add text formatting for the bars
    fig.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside', 
        marker_line_color='black', 
        marker_line_width=1.5
    )
    # Display the chart in Streamlit
    st.plotly_chart(fig)


# Divider
st.divider()

# Create two columns for Return and Non-Return analysis
col_total_return, col_avg_review = st.columns(2)

with col_total_return:  

    return_non_return = {
            "Customer Type": ["Return Customers", "Non-Return Customers"],
            "Count": [
                df.loc[df['Return Customer'] == True, 'Return Customer'].count(),
                df.loc[df['Return Customer'] == False, 'Return Customer'].count()
            ]
        }

    df_return_non_return = pd.DataFrame(return_non_return)

    fig = px.bar(
        df_return_non_return, 
        x="Customer Type", 
        y="Count", 
        color="Customer Type",
        text="Count",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    # Customize layout
    fig.update_layout(
        title="Comparison of Return vs Non-Return Customers",
        xaxis_title="Customer Type",
        yaxis_title="Number of Customers",
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)'   # Transparent paper background
    )
    # Display the chart in Streamlit
    st.plotly_chart(fig)

with col_avg_review:
    # Calculate the average review score
    avg_rev_score = df['Review Score (1-5)'].mean()

    # Create a gauge chart for the average review score
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=avg_rev_score,
        gauge={
            'axis': {'range': [1, 5]},  # Review scores are between 1 and 5
            'bar': {'color': "green"},
            'steps': [
                {'range': [1, 2], 'color': "red"},
                {'range': [2, 3], 'color': "orange"},
                {'range': [3, 4], 'color': "yellow"},
                {'range': [4, 5], 'color': "lightgreen"}
            ],
        },
        title={'text': "Average Review Score"}
    ))

    # Customize layout
    fig.update_layout(
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)'   # Transparent paper background
    )

    # Display the gauge chart in Streamlit
    st.plotly_chart(fig)

st.divider()

col_avg_delivary, col_paid_users = st.columns(2)

with col_avg_delivary:
    # Calculate the average delivery time for each subscription status
    avg_delivery = df.groupby('Subscription Status')['Delivery Time (days)'].mean().reset_index()

    # Format the legend labels to include the average delivery time
    avg_delivery['Subscription Status'] = avg_delivery.apply(
        lambda row: f"{row['Subscription Status']} ({row['Delivery Time (days)']:.2f} days)", axis=1
    )

    # Create a donut chart for average delivery time by subscription status
    fig = px.pie(
        avg_delivery, 
        values='Delivery Time (days)', 
        names='Subscription Status', 
        hole=0.5,  # Increase the hole size for a better donut look
        color_discrete_sequence=['#66C2A5', '#FC8D62']  # Custom colors for the slices
    )

    # Customize the layout
    fig.update_traces(
        textinfo='percent+label',  # Show percentage and label on slices
        textfont_size=14,  # Font size for the text inside the chart
        marker=dict(
            line=dict(color='#000000', width=2)  # Black border line for each slice
        )
    )

    # Further customize layout for a polished look
    fig.update_layout(
        title=dict(
            text="Average Delivery Time by Subscription Status",
            font=dict(size=18, color='white'),
            x=0.2,  # Center the title
        ),
        annotations=[
            dict(
                text='Delivery<br>Time',  # Text in the center of the donut
                showarrow=False,
                font=dict(size=20, color='white')
            )
        ],
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        legend=dict(
            orientation='h',  # Horizontal legend at the bottom
            y=-0.5,
            font=dict(size=12)
        )
    )

    # Display the stylish donut chart in Streamlit
    st.plotly_chart(fig)

with col_paid_users:

    paid_customers = df.loc[df['Subscription Status']=='Premium','Subscription Status'].count()
    free_customers = df.loc[df['Subscription Status']=='Free','Subscription Status'].count()
    trail_customers = df.loc[df['Subscription Status']=='Trial','Subscription Status'].count()
    subscription_counts = {
        'Subscription Status': ['Premium', 'Free', 'Trial'],
        'Count': [paid_customers, free_customers, trail_customers]
    }

    legend_labels = [
        f"Premium ({paid_customers})",
        f"Free ({free_customers})",
        f"Trial ({trail_customers})"
    ]

    # Create a line graph
    fig = go.Figure()

    # Add trace for the line graph
    fig.add_trace(go.Scatter(
        x=subscription_counts['Subscription Status'],
        y=subscription_counts['Count'],
        mode='lines+markers',
        marker=dict(size=12, color=['#1f77b4', '#ff7f0e', '#2ca02c']),
        line=dict(width=3, dash='solid'),
        text=[f'{count}' for count in subscription_counts['Count']],  # Add the counts as text
        textposition='top center',  # Position the text above the markers
        name='Customer Count'  # Trace name for the legend
    ))

    # Customize layout for a polished look
    fig.update_layout(
        title=dict(
            text='Customer Count by Subscription Status',
            font=dict(size=18, color='white'),
            x=0.2  # Center the title
        ),
        xaxis=dict(
            title='Subscription Status',
            tickvals=subscription_counts['Subscription Status'],
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            title='Number of Customers',
            tickfont=dict(size=12)
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        legend=dict(
            orientation='h',  # Horizontal legend at the bottom
            y=-0.2,
            font=dict(size=12),
            title=dict(text='Subscription Status')
        )
    )

    # Update legend to include the counts
    for idx, trace in enumerate(fig.data):
        trace.name = legend_labels[idx]

    # Display the stylish line graph in Streamlit
    st.plotly_chart(fig)

st.divider()
col_avg_purchase , col_device = st.columns(2)


with col_device:
    percentage_mobile = ((df.loc[df[ 'Device Type'] == 'Mobile','Device Type'].count())/df['Device Type'].count())*100
    percentage_desktop = ((df.loc[df[ 'Device Type'] == 'Desktop','Device Type'].count())/df['Device Type'].count())*100
    percentage_tablet = ((df.loc[df[ 'Device Type'] == 'Tablet','Device Type'].count())/df['Device Type'].count())*100
    # Data for device type percentages
    device_types = [
        f'Mobile: {percentage_mobile:.2f}%',
        f'Desktop: {percentage_desktop:.2f}%',
        f'Tablet: {percentage_tablet:.2f}%'
    ]
    percentages = [percentage_mobile, percentage_desktop, percentage_tablet]

    # Create a pie chart
    fig = go.Figure(
        go.Pie(
            labels=device_types,
            values=percentages,
            hole=0.4,  # Donut shape
            marker=dict(
                colors=['#1f77b4', '#ff7f0e', '#2ca02c'],
                line=dict(color='black', width=2)
            ),
            textinfo='label',  # Show both label and percentage
            hoverinfo='label+percent+value',  # Display label, percentage, and value on hover
            textfont=dict(size=14)
        )
    )

    # Customize layout for a more stylish look
    fig.update_layout(
        title=dict(
            text='Device Type Usage for Purchases',
            font=dict(size=18, color='white'),
            x=0.2  # Center the title
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        legend=dict(
            orientation='h',  # Horizontal legend at the bottom
            font=dict(size=12)
        )
    )
    st.plotly_chart(fig)

with col_avg_purchase:
    # Data for average purchase amount
    avg_purchase_amount = df.groupby('Discount Availed')['Purchase Amount ($)'].mean().reset_index()

    # Create labels for availed and not availed
    avg_purchase_amount['Discount Availed'] = avg_purchase_amount['Discount Availed'].map({True: 'Discount Availed', False: 'No Discount'})

    fig = px.bar(
        avg_purchase_amount, 
        x='Discount Availed', 
        y='Purchase Amount ($)', 
        text='Purchase Amount ($)',
        color='Discount Availed', 
        color_discrete_sequence=['#66c2a5', '#fc8d62'],  # Custom color scheme
        title='Average Purchase Amount: Discount vs No Discount'
    )

    # Customize layout for a more stylish look
    fig.update_layout(
        title=dict(
            text='Average Purchase Amount for Discount vs No Discount',
            font=dict(size=18, color='white'),
            x=0.1  # Center the title
        ),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
        xaxis_title='Discount Status',
        yaxis_title='Average Purchase Amount ($)',
        font=dict(size=12)
    )

    # Add text formatting for the bars
    fig.update_traces(
        texttemplate='$%{text:.2f}', 
        textposition='outside', 
        marker_line_color='black', 
        marker_line_width=1.5
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

st.divider()

# Calculate the count for each payment method
payment_method_counts = df.groupby('Payment Method')['Payment Method'].count().reset_index(name='Count')

# Create a horizontal bar chart with dynamic colors
fig = px.bar(
    payment_method_counts, 
    y='Payment Method',  # Change to y for horizontal
    x='Count',          # Change to x for horizontal
    text='Count', 
    color='Payment Method',  # Different colors for each payment method
    title='Most Common Payment Methods',
    color_discrete_sequence=px.colors.qualitative.Plotly  # Dynamic color sequence
)

# Customize the layout for a stylish look
fig.update_layout(
    title=dict(
        text='Most Common Payment Methods Used by Customers',
        font=dict(size=18, color='white'),
        x=0.3  # Center the title
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    xaxis_title='Number of Customers',  # Label for the x-axis
    yaxis_title='Payment Method',        # Label for the y-axis
    font=dict(size=12)
)

# Add text formatting for the bars
fig.update_traces(
    texttemplate='%{text}', 
    textposition='outside', 
    marker_line_color='black', 
    marker_line_width=1.5
)

# Highlight the most common payment method
top_payment_method = payment_method_counts.loc[payment_method_counts['Count'].idxmax(), 'Payment Method']
highlight_color = '#FF8C00'  # Color for the top payment method
fig.for_each_trace(lambda t: t.update(marker_color=highlight_color if t.name == top_payment_method else None))
st.plotly_chart(fig)






