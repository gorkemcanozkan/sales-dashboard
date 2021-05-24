### region ---------Library Imports---------
import streamlit as st
import pandas as pd
import sys
import datetime
import numpy as np
import plotly.express as px
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

###endregion

###region -----------Data Import-------------
dataset=pd.read_csv("dataset.csv")
###endregion

# region -------------------Streamlit-------------------------
#Loading the logo here
st.image('logo.png', use_column_width=True)

#Generating Headers for main page and sidebar
st.header("Sales Dashboard")
st.sidebar.header('Sales Dashboard')

def user_input_features():
    radio_selection=st.sidebar.radio("Please Choose a Chart Type",('Bubble Chart',"Bar Chart","Tree Chart","Map Chart"))
    if radio_selection=="Bubble Chart":
        st.write("Comparison of stores according to Net Sales and Gross Profits:")
        xmin=float(dataset["Gross Profit %"].min())
        xmax=float(dataset["Gross Profit %"].max())
        ymin=float(dataset["Net Profit %"].min())
        ymax=float(dataset["Net Profit %"].max())
        net_profit=dataset["Net Profit"]/dataset["Net Sales"]
        fig=px.scatter(dataset, x="Gross Profit %",y=net_profit,
                       animation_group="Store Name",
                       size="Net Sales",color="Net Sales",
                       hover_name="Store Name",animation_frame="Month",
                       log_x=True, range_x=[xmin,xmax], range_y=[-1,ymax])
        st.plotly_chart(fig,use_container_width=True)


    if radio_selection=="Bar Chart":
        bar_radio = st.sidebar.radio('Please Choose A Criteria', ('Gross Sales', 'Net Profit', 'Operating Expenses'))
        if bar_radio=='Gross Sales':
            dataset2 = pd.pivot_table(dataset, values='Net Sales', index=['Store Name'], aggfunc=np.sum)
            dataset2.reset_index(inplace=True)
            dataset2.sort_values(by=["Net Sales"], ascending=False, inplace=True)
            dataset2 = dataset2.reset_index()
            dataset2 = dataset2.drop(columns=["index"])
            dataset2 = dataset2.head(10)
            fig1 = px.bar(dataset2, x='Store Name', y='Net Sales',color='Net Sales')
            st.write("Top 10 Stores:")
            st.plotly_chart(fig1,use_container_width=True)

            dataset3 = pd.pivot_table(dataset, values='Net Sales', index=['Store Name'], aggfunc=np.sum)
            dataset3.reset_index(inplace=True)
            dataset3.sort_values(by=["Net Sales"], ascending=True, inplace=True)
            dataset3 = dataset3.reset_index()
            dataset3 = dataset3.drop(columns=["index"])
            dataset3 = dataset3.head(10)
            fig2 = px.bar(dataset3, x='Store Name', y='Net Sales',color='Net Sales')
            st.write("Bottom 10 Stores:")
            st.plotly_chart(fig2,use_container_width=True)
        if bar_radio=='Net Profit':
            dataset2 = pd.pivot_table(dataset, values='Net Profit %', index=['Store Name'], aggfunc=np.sum)
            dataset2.reset_index(inplace=True)
            dataset2.sort_values(by=["Net Profit %"], ascending=False, inplace=True)
            dataset2 = dataset2.reset_index()
            dataset2 = dataset2.drop(columns=["index"])
            dataset2 = dataset2.head(10)
            fig1 = px.bar(dataset2, x='Store Name', y='Net Profit %',color='Net Profit %')
            st.write("Top 10 Stores:")
            st.plotly_chart(fig1,use_container_width=True)

            dataset3 = pd.pivot_table(dataset, values='Net Profit %', index=['Store Name'], aggfunc=np.sum)
            dataset3.reset_index(inplace=True)
            dataset3.sort_values(by=["Net Profit %"], ascending=True, inplace=True)
            dataset3 = dataset3.reset_index()
            dataset3 = dataset3.drop(columns=["index"])
            dataset3 = dataset3.head(10)
            fig2 = px.bar(dataset3, x='Store Name', y='Net Profit %',color='Net Profit %')
            st.write("Bottom 10 Stores:")
            st.plotly_chart(fig2,use_container_width=True)

        if bar_radio=='Operating Expenses':
            dataset2 = pd.pivot_table(dataset, values='Operating Expenses', index=['Store Name'], aggfunc=np.sum)
            dataset2.reset_index(inplace=True)
            dataset2.sort_values(by=["Operating Expenses"], ascending=False, inplace=True)
            dataset2 = dataset2.reset_index()
            dataset2 = dataset2.drop(columns=["index"])
            dataset2 = dataset2.head(10)
            fig1 = px.bar(dataset2, x='Store Name', y='Operating Expenses',color='Operating Expenses')
            st.write("10 Stores with the most operating expenses:")
            st.plotly_chart(fig1,use_container_width=True)

            dataset3 = pd.pivot_table(dataset, values='Operating Expenses', index=['Store Name'], aggfunc=np.sum)
            dataset3.reset_index(inplace=True)
            dataset3.sort_values(by=["Operating Expenses"], ascending=True, inplace=True)
            dataset3 = dataset3.reset_index()
            dataset3 = dataset3.drop(columns=["index"])
            dataset3 = dataset3.head(10)
            fig2 = px.bar(dataset3, x='Store Name', y='Operating Expenses',color='Operating Expenses')
            st.write("10 Stores with the least operating expenses:")
            st.plotly_chart(fig2,use_container_width=True)

    if radio_selection == "Tree Chart":
        month_selection = st.sidebar.selectbox('Please Choose a Month', dataset['Month'].unique())
        criteria_selection=st.sidebar.selectbox('Please choose a criteria', ('Store Type','Sales Person','Territory Manager'))
        dataset2 = dataset[dataset["Month"] == month_selection]
        net_profit=dataset2["Net Profit"]/dataset2["Net Sales"]
        if criteria_selection=='Store Type':
            dataset2=dataset[dataset["Month"]==month_selection]
            fig3 = px.treemap(dataset2, path=[px.Constant(f'Stores - {month_selection}'), 'Store Type', 'Store Name'], values='Net Sales',
                             color=net_profit,color_continuous_scale='RdBu')
            st.plotly_chart(fig3,use_container_width=True)
        if criteria_selection=="Sales Person":
            fig3 = px.treemap(dataset2, path=[px.Constant(f'Stores - {month_selection}'), 'Sales Person', 'Store Name'],
                              values='Net Sales',
                              color='Net Profit %', color_continuous_scale='RdBu')
            st.plotly_chart(fig3, use_container_width=True)
        if criteria_selection=='Territory Manager':
            fig3 = px.treemap(dataset2, path=[px.Constant(f'Stores - {month_selection}'), 'Territory Manager', 'Store Name'],
                              values='Net Sales',
                              color='Net Profit %', color_continuous_scale='RdBu')
            st.plotly_chart(fig3, use_container_width=True)
    if radio_selection == "Map Chart":
        month_selection = st.sidebar.selectbox('Please Choose a Month', dataset['Month'].unique())
        dataset4 = dataset[dataset["Month"] == month_selection]
        net_profit=dataset4["Net Profit"]/dataset4["Net Sales"]
        fig3 = px.scatter_mapbox(dataset4, lat="Latitude", lon="Longitude", color=net_profit, size="Net Sales",
                                color_continuous_scale="RdYlGn", size_max=40,zoom=4,
                                mapbox_style="carto-positron",opacity=1,hover_name="Store Name")
        st.plotly_chart(fig3, use_container_width=True)
user_input_features()

### endregion  UI
