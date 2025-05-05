# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Zena's Amazing Athleisure Catalog")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("ZENAS_ATHLEISURE_DB.PRODUCTS.CATALOG_FOR_WEBSITE")

colors = my_dataframe.select(col('COLOR_OR_STYLE')).to_pandas()['COLOR_OR_STYLE'].tolist()

chosen_color = st.selectbox(
    label='Pick a sweatsuit color or style:',
    options=colors,
    index=None,
    placeholder="Select color"
)

if chosen_color:
    
    color_row = my_dataframe.filter(col("COLOR_OR_STYLE") == chosen_color).select(col("FILE_URL")).collect()
    price_row = my_dataframe.filter(col("COLOR_OR_STYLE") == chosen_color).select(col("PRICE")).collect()
    size_list_row = my_dataframe.filter(col("COLOR_OR_STYLE") == chosen_color).select(col("SIZE_LIST")).collect()
    consider_list = my_dataframe.filter(col("COLOR_OR_STYLE") == chosen_color).select(col("UPSELL_PRODUCT_DESC")).collect()

    st.image(color_row[0]['FILE_URL'], use_container_width=True)
    st.subheader(f"Price: {price_row[0]['PRICE']}")
    st.write(size_list_row[0]['SIZE_LIST'], use_container_width=True)
    st.write(consider_list[0]['UPSELL_PRODUCT_DESC'], use_container_width=True)
