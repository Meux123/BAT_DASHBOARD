import streamlit as st
import geojson
import pandas as pd
import plotly.express as px

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
    
    test_df=pd.DataFrame(example_la_data)
    test_df.columns=['Local_Authority','Value']
    return gj,test_df
gj,test_df=create_la_geojson()

english_prof_table=pd.read_csv('census_english_prof.csv')
english_prof_table['Main_Language_English%']=(english_prof_table["MAIN_LANGUAGE_ENGLISH"]/english_prof_table['TOTAL_RESIDENTS'])*100


fig = px.choropleth_mapbox(english_prof_table,
                           geojson=gj,
                           locations='GEOGRAPHY_CODE',
                           color='Main_Language_English%',
                           featureidkey="properties.LAD21CD",
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           center={"lat": 55.09621, "lon": -4.0286298},
                           zoom=4.2,
                           labels={'val':'TOTAL_RESIDENTS'},
                           hoverdata=['GEOGRAPHY_CODE']
                           )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.title("Example Local Authority Map")
st.plotly_chart(fig)
