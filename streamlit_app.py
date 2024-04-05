# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothei :cup_with_straw:")
st.write(
    """Choose the fruits you want in your cutsom Smoothei!
    """
)


name_on_order = st.text_input('Name on Smoothei :')
st.write('The name on your smoothei will be : ', name_on_order)



#option = st.selectbox(
#    'What is your favrouite fruit?',
#    ('Apple', 'Banana', 'Orange'))
#st.write('You selected:', option)

cnx=st.connection("snowflake")
session= cnx.session()
my_dataframe=session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.STOP()

#Convert the snowpark datafream to pandas datafream so we can use the LOC function

pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list=st.multiselect('Choose upto 5 ingredients :', my_dataframe)

if ingredients_list:
    ingredients_string=''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen +' '
        st.subheader(fruit_chosen+' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!' + name_on_order , icon="✅")



