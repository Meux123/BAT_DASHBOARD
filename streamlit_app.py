import streamlit as st
import geojson
import pandas as pd
import plotly.express as px
import os

@st.cache_data
def create_la_geojson():
    with open('local_authority_geojson.geojson') as f:
        gj=geojson.load(f)
    example_la_data = []
    
    for i in range(len(gj["features"])):
        # Extract local authority name
        la = gj["features"][i]['properties']['LAD21NM']
        # Assign the local authority name to a new 'id' property for later linking to dataframe
        gj["features"][i]['id'] = la
        # While I'm at it, append local authority name to a list to make some dummy data to test, along with i for a value to test on map
        example_la_data.append([la,i])

    return gj
gj=create_la_geojson()

@st.cache_data
def create_raw_data_dataframes(variable_to_force_refresh):
    list_of_files=os.listdir('data_for_dashboard')
    list_of_files_no_file_type=[x.split('.')[0] for x in list_of_files]
    dataframes_list=[]
    non_metric_cols=['date','la21_name','la21_cd']
    list_of_metric_columns=[]
    index_list=[]
    for i in range(len(list_of_files)):
        df=pd.read_csv(f'data_for_dashboard/{list_of_files[i]}')
        metrics=[x for x in df.columns if x.lower() not in non_metric_cols]
        dataframes_list.append(df)
        list_of_metric_columns.append(metrics)
        index_list.append(i)
    return list_of_files_no_file_type,dataframes_list,list_of_metric_columns,index_list



list_of_dashboards,dataframe_list,list_of_metric_columns,index_list=create_raw_data_dataframes(2)


st.title("Local Authority Map")


with st.sidebar:

    selected_dataset=st.selectbox('Please select the dataset you want to use',options=index_list,format_func=lambda x:list_of_dashboards[x])
    metric_choice=st.selectbox('Please select Metric to Show',options=list_of_metric_columns[selected_dataset])
    year_of_dataset=st.selectbox('Please Select which year of data to use',options=dataframe_list[selected_dataset]['DATE'])
tab1,tab2=st.tabs(['Map','Other Graphs'])
with tab1:
    
    st.write('test')
    # st.dataframe(dataframe_list[selected_dataset].loc[dataframe_list[selected_dataset]['DATE']==year_of_dataset])
    fig = px.choropleth_mapbox(dataframe_list[selected_dataset].loc[dataframe_list[selected_dataset]['DATE']==year_of_dataset],
                           geojson=gj,
                           locations='LA21_CD',
                           color=metric_choice,
                           featureidkey="properties.LAD21CD",
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           center={"lat": 55.09621, "lon": -4.0286298},
                           zoom=4.2,
                           
                           hover_data=['LA21_CD','LA21_NAME']
                           )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


    event_details=st.plotly_chart(fig,on_select='rerun')
    
    if len(event_details['selection']['points'])>0:
        df_ind=dataframe_list[selected_dataset].loc[dataframe_list[selected_dataset]['LA21_CD']==event_details['selection']['points'][0]['location']].transpose()
        df_ind.columns=['Individual LA Details']
        st.dataframe(df_ind,use_container_width=True)

