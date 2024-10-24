import streamlit as st
import geojson
import pandas as pd
import plotly.express as px

@st.cache_data
def create_la_geojson():
    with open('Local_Authority_Districts.geojson') as f:
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

fig = px.choropleth_mapbox(test_df,
                           geojson=gj,
                           locations='Local_Authority',
                           color='Value',
                           featureidkey="properties.LAD21NM",
                           color_continuous_scale="Viridis",
                           mapbox_style="carto-positron",
                           center={"lat": 55.09621, "lon": -4.0286298},
                           zoom=4.2,
                           labels={'val':'value'})

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.title("Example Local Authority Map")
st.plotly_chart(fig)
