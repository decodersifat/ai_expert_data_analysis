import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objs as go

st.set_page_config(page_title="AI Expert Challenge !!!", page_icon=":pencil2:", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center;'>Team: Coding Slug</h1>
    """,
    unsafe_allow_html=True
)
st.header("Level 3 ::black_nib:", divider=True)

hide_streamlit_style = """
<style>
.css-hi6a2p {padding-top: 0rem;}
div.block-container {padding-top: 1rem;}
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


st.subheader(":bar_chart: DataSet")
df = pd.read_csv('AI_Expert_Challenge/ecommerce_customer_behavior_dataset.csv')
st.dataframe(df)


st.subheader('Factors contribute most for a return customer',divider=True)

# Convert 'Return Customer' to numerical (1 for True, 0 for False)
df['Return Customer'] = df['Return Customer'].astype(int)

# Step 1: Correlation for numerical factors
# Select all numerical features except 'z-score-of-payment'
numerical_features = ['Age', 'Purchase Amount ($)', 'Time Spent on Website (min)', 
                      'Number of Items Purchased', 'Discount Availed', 'Review Score (1-5)', 
                      'Delivery Time (days)']
correlation_with_return_customer = df[numerical_features + ['Return Customer']].corr()['Return Customer'].sort_values(ascending=False)

# Create a DataFrame for correlation
correlation_df = correlation_with_return_customer.drop('Return Customer').reset_index()
correlation_df.columns = ['Feature', 'Correlation']

# Step 2: Visualization
# Correlation heatmap
x_values = correlation_df['Feature'].tolist()
y_values = ['Return Customer']
z_values = [correlation_df['Correlation'].values.tolist()]
annotation_text = [[f"{val:.2f}" for val in correlation_df['Correlation']]]

fig_heatmap = ff.create_annotated_heatmap(
    z=z_values,
    x=x_values,
    y=y_values,
    colorscale='Viridis',
    annotation_text=annotation_text,
    showscale=True
)
fig_heatmap.update_layout(
    xaxis_title="Feature",
    yaxis_title="",
    font=dict(size=12)
)

# Step 3: Return rate by location
return_rate_by_location = df.groupby('Location')['Return Customer'].mean() * 100
location_df = return_rate_by_location.reset_index()
location_df.columns = ['Location', 'Return Rate (%)']

fig_location = px.bar(
    location_df,
    x='Location',
    y='Return Rate (%)',
    title='Return Customer Rate by Location',
    color='Location',
    text='Return Rate (%)',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_location.update_layout(
    title=dict(text='Return Customer Rate by Location', font=dict(size=18), x=0.2)
)

# Step 4: Return rate by payment method
return_rate_by_payment_method = df.groupby('Payment Method')['Return Customer'].mean() * 100
payment_method_df = return_rate_by_payment_method.reset_index()
payment_method_df.columns = ['Payment Method', 'Return Rate (%)']

fig_payment_method = px.bar(
    payment_method_df,
    x='Payment Method',
    y='Return Rate (%)',
    title='Return Customer Rate by Payment Method',
    color='Payment Method',
    text='Return Rate (%)',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_payment_method.update_layout(
    title=dict(text='Return Customer Rate by Payment Method', font=dict(size=18), x=0.2)
)

# Step 5: Return rate by gender
return_rate_by_gender = df.groupby('Gender')['Return Customer'].mean() * 100
gender_df = return_rate_by_gender.reset_index()
gender_df.columns = ['Gender', 'Return Rate (%)']

fig_gender = px.bar(
    gender_df,
    x='Gender',
    y='Return Rate (%)',
    title='Return Customer Rate by Gender',
    color='Gender',
    text='Return Rate (%)',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_gender.update_layout(
    title=dict(text='Return Customer Rate by Gender', font=dict(size=18), x=0.2)
)



col1, col2 = st.columns(2)
with col1:
    st.subheader("Correlation Heatmap")
    st.write('Correlation of Numerical Features with Being a Return Customer')
    st.plotly_chart(fig_heatmap)
with col2:
    st.subheader("Return Rate by Location")
    st.plotly_chart(fig_location)

st.write("---")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Return Rate by Payment Method")
    st.plotly_chart(fig_payment_method)
with col4:
    st.subheader("Return Rate by Gender")
    st.plotly_chart(fig_gender)



st.subheader('Payment methods influence customer satisfaction and return rates',divider=True)

# Step 1: Map 'Customer Satisfaction' to numerical values for easier analysis
# Assuming 'High' = 3, 'Medium' = 2, 'Low' = 1
df['Satisfaction Score'] = df['Customer Satisfaction'].map({'High': 3, 'Medium': 2, 'Low': 1})

# Calculate average satisfaction score and return rate by payment method
avg_satisfaction_by_payment = df.groupby('Payment Method')['Satisfaction Score'].mean()
return_rate_by_payment = df.groupby('Payment Method')['Return Customer'].mean() * 100

# Create a DataFrame for analysis
payment_method_analysis = pd.DataFrame({
    'Average Satisfaction Score': avg_satisfaction_by_payment,
    'Return Rate (%)': return_rate_by_payment
})

# Print the analysis DataFrame
st.write("Analysis of Payment Methods Influence on Customer Satisfaction and Return Rates:")
st.dataframe(payment_method_analysis,use_container_width=True)

# Visualization: Bar chart for both satisfaction score and return rate
fig = go.Figure()

# Add bars for average satisfaction score
fig.add_trace(go.Bar(
    x=payment_method_analysis.index,
    y=payment_method_analysis['Average Satisfaction Score'],
    name='Average Satisfaction Score',
    marker_color='green'
))

# Add bars for return rate
fig.add_trace(go.Bar(
    x=payment_method_analysis.index,
    y=payment_method_analysis['Return Rate (%)'],
    name='Return Rate (%)',
    marker_color='yellow'
))

# Update layout for better appearance
fig.update_layout(
    title='Influence of Payment Methods on Customer Satisfaction and Return Rates',
    xaxis_title='Payment Method',
    yaxis_title='Scores / Rates',
    barmode='group',  # Group bars together
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    title_x=0.2,  # Center the title
    font=dict(size=14)
)

# Display the chart in Streamlit
st.plotly_chart(fig)







# Group by Location to calculate average purchase amount and delivery time
avg_purchase_by_location = df.groupby('Location')['Purchase Amount ($)'].mean()
avg_delivery_time_by_location = df.groupby('Location')['Delivery Time (days)'].mean()

# Create a DataFrame for analysis
location_analysis = pd.DataFrame({
    'Average Purchase Amount ($)': avg_purchase_by_location,
    'Average Delivery Time (Days)': avg_delivery_time_by_location
})

# Display the DataFrame in Streamlit
st.subheader("Analysis of Location's Influence on Purchase Amount and Delivery Time:",divider=True)
st.dataframe(location_analysis,use_container_width=True)

# Visualization: Bar chart for both average purchase amount and average delivery time
fig = go.Figure()

# Add bars for average purchase amount
fig.add_trace(go.Bar(
    x=location_analysis.index,
    y=location_analysis['Average Purchase Amount ($)'],
    name='Average Purchase Amount ($)',
    marker_color='skyblue'
))

# Add bars for average delivery time
fig.add_trace(go.Bar(
    x=location_analysis.index,
    y=location_analysis['Average Delivery Time (Days)'],
    name='Average Delivery Time (Days)',
    marker_color='yellow'
))

# Update layout for better appearance
fig.update_layout(
    title='Influence of Location on Purchase Amount and Delivery Time',
    xaxis_title='Location',
    yaxis_title='Value',
    barmode='group',  # Group bars together
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper background
    title_x=0.2,  # Center the title
    font=dict(size=14)
)

# Display the chart in Streamlit
st.plotly_chart(fig)




