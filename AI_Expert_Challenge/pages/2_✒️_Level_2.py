import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go


st.set_page_config(page_title="AI Expert Challenge !!!", page_icon=":pencil2:", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center;'>Team: Coding Slug</h1>
    """,
    unsafe_allow_html=True
)
st.header("Level 2 ::black_nib:", divider=True)

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
df = pd.read_csv('/AI_Expert_Challenge/ecommerce_customer_behavior_dataset.csv')
st.dataframe(df)

col_avg_payment, col_co_rel_purchese = st.columns(2)



# Calculate the average review scores for each payment method
average_review_scores = df.groupby('Payment Method')['Review Score (1-5)'].mean().reset_index()
# Create a bar chart for average review scores
fig = px.bar(
    average_review_scores, 
    x='Payment Method', 
    y='Review Score (1-5)', 
    text='Review Score (1-5)', 
    color='Payment Method',  # Different colors for each payment method
    title='Average Review Scores by Payment Method',
    color_discrete_sequence=px.colors.qualitative.Plotly  # Dynamic color sequence
)
# Customize the layout for a stylish look
fig.update_layout(
    title=dict(
        text='Average Review Scores of Users by Payment Method',
        font=dict(size=18, color='white'),
        x=0.2  # Center the title
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    xaxis_title='Payment Method',
    yaxis_title='Average Review Score (1-5)',
    font=dict(size=12)
)
# Update the text on the bars to include both payment method and average score
average_review_scores['Label'] = average_review_scores.apply(lambda x: f"{x['Payment Method']}: {x['Review Score (1-5)']:.2f}", axis=1)
fig.update_traces(
    text=average_review_scores['Label'],
    textposition='outside', 
    marker_line_color='black', 
    marker_line_width=1.5
)
# Display the chart in Streamlit
st.plotly_chart(fig)

st.header("",divider=True)

satisfied_customers = df[df['Review Score (1-5)'] >= 4]
satisfied_return_customers = satisfied_customers[satisfied_customers['Return Customer'] == True]
total_customers = len(df)
satisfied_return_count = len(satisfied_return_customers)
non_satisfied_or_non_return_count = total_customers - satisfied_return_count
data = {
    'Customer Type': ['Satisfied & Return Customers', 'Other Customers'],
    'Count': [satisfied_return_count, non_satisfied_or_non_return_count]
}
df_pie = pd.DataFrame(data)
fig = px.pie(
    df_pie, 
    names='Customer Type', 
    values='Count', 
    color='Customer Type',
    title='Percentage of Satisfied & Return Customers vs. Other Customers',
    color_discrete_sequence=px.colors.qualitative.Set2  
)
fig.update_layout(
    title=dict(
        text='Percentage of Satisfied (Rating 4 or 5) & Return Customers',
        font=dict(size=18, color='white'),
        x = 0.25
    ),
    showlegend=True
)
fig.update_traces(
    textinfo='label+percent',
    marker=dict(line=dict(color='black', width=1.5))
)
st.plotly_chart(fig)








# Step 1: Correlation calculation
# Calculate correlation between 'Time Spent on Website (min)' and 'Purchase Amount ($)'
correlation_time_purchase = df['Time Spent on Website (min)'].corr(df['Purchase Amount ($)'])

# Calculate correlation between 'Time Spent on Website (min)' and 'Number of Items Purchased'
correlation_time_items = df['Time Spent on Website (min)'].corr(df['Number of Items Purchased'])

# Step 2: Visualization
# Scatter plot for 'Time Spent on Website (min)' vs 'Purchase Amount ($)'
fig_purchase = px.scatter(
    df,
    x='Time Spent on Website (min)',
    y='Purchase Amount ($)',
    trendline='ols',
    title=f"Correlation between Time Spent on Website and Purchase Amount: {correlation_time_purchase:.2f}",
    labels={'Time Spent on Website (min)': 'Time Spent on Website (minutes)', 'Purchase Amount ($)': 'Purchase Amount ($)'}
)

# Scatter plot for 'Time Spent on Website (min)' vs 'Number of Items Purchased'
fig_items = px.scatter(
    df,
    x='Time Spent on Website (min)',
    y='Number of Items Purchased',
    trendline='ols',
    title=f"Correlation between Time Spent on Website and Number of Items Purchased: {correlation_time_items:.2f}",
    labels={'Time Spent on Website (min)': 'Time Spent on Website (minutes)', 'Number of Items Purchased': 'Number of Items Purchased'}
)



col1, col2 = st.columns(2)
with col1:
    st.subheader("Time Spent vs. Purchase Amount",divider=True)
    st.plotly_chart(fig_purchase)
with col2:
    st.subheader("Time Spent vs. Number of Items Purchased",divider=True)
    st.plotly_chart(fig_items)


st.write(f"The correlation between time spent on the website and purchase amount is {correlation_time_purchase:.2f}.")
st.write(f"The correlation between time spent on the website and number of items purchased is {correlation_time_items:.2f}.")

st.write("---")







st.subheader('Analysis of Items Purchased vs. Customer Satisfaction',divider=True)


# Assuming 'Customer Satisfaction' is categorized as 'High', 'Medium', 'Low'
df['Satisfaction Numeric'] = df['Customer Satisfaction'].apply(lambda x: 1 if x == 'High' else 0 if x == 'Low' else 0.5)

# Calculate correlation
correlation = df['Number of Items Purchased'].corr(df['Satisfaction Numeric'])
st.status(f"Correlation between Number of Items Purchased and Customer Satisfaction: {correlation:.2f}",state='complete')
st.status("A value closer to 1 indicates a strong positive correlation, while closer to -1 indicates a strong negative correlation.",state='complete')

# Create a scatter plot with Plotly
fig = px.scatter(
    df, 
    x='Number of Items Purchased', 
    y='Satisfaction Numeric', 
    labels={
        'Number of Items Purchased': 'Number of Items Purchased',
        'Satisfaction Numeric': 'Customer Satisfaction (0: Low, 0.5: Medium, 1: High)'
    },
    trendline='ols',  # Add a trendline to show correlation
    color='Customer Satisfaction',  # Color by customer satisfaction level
    color_discrete_map={'High': 'green', 'Medium': 'orange', 'Low': 'red'}
)

# Customize layout for a stylish look
fig.update_layout(
    
    xaxis_title='Number of Items Purchased',
    yaxis_title='Customer Satisfaction (0: Low, 0.5: Medium, 1: High)',
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
)

# Display the scatter plot with trendline in Streamlit
st.plotly_chart(fig)

st.subheader('',divider=True)



# Assuming df is your DataFrame
# Calculate average purchase amount by location
LAP = df.groupby('Location')['Purchase Amount ($)'].mean()
sorted_LAP = LAP.sort_values(ascending=False)
second_highest_location = sorted_LAP.index[1]
second_highest_avg_purchase = sorted_LAP.iloc[1]
location_df = pd.DataFrame({
    'Location': sorted_LAP.index,
    'Average Purchase Amount': sorted_LAP.values
})
fig = px.bar(
    location_df,
    x='Location',
    y='Average Purchase Amount',
    title='Average Purchase Amount by Location',
    text='Average Purchase Amount',
    color='Location', 
    color_discrete_sequence=px.colors.qualitative.Plotly
)
# Highlight the bar for the second highest location
fig.update_traces(marker=dict(line=dict(width=2, color='black')))  # Add a border to all bars
fig.add_annotation(
    x=second_highest_location,
    y=second_highest_avg_purchase,
    text=f'Second Highest: ${second_highest_avg_purchase:.2f}',
    showarrow=True,
    arrowhead=2,
    ax=-40,
    ay=-40,
    font=dict(size=12, color='white'),
    bgcolor='green',
    bordercolor='white',
    borderwidth=1,
)
# Customize the layout for a stylish look
fig.update_layout(
    title=dict(
        text='Average Purchase Amount by Location',
        font=dict(size=18, color='white'),
        x=0.1  # Center the title
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent background
    paper_bgcolor='rgba(0, 0, 0, 0)',  # Transparent paper background
    xaxis_title='Location',
    yaxis_title='Average Purchase Amount ($)',
    font=dict(size=12)
)
# Display the chart in Streamlit
st.plotly_chart(fig)

