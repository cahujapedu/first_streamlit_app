import streamlit as st
import pandas as pd
import numpy as np
import requests as rq
import snowflake.connector
from urllib.error import URLError

st.header('Breakfast Menu')
st.text('🍜 Omega 3 & Blueberry Oatmeal')
st.text('🍞 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')

st.header('🍌 Build Your Own Fruit Smoothie 🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)




# Create the reeatable code block
def   get_fruitvice_data(this_fruit_choice):
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# new section to display fruitivice api response
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    st.dataframe(back_from_function)

except URLError as e:
  st.error()
  
# don't do anything past this line
st.stop()

#my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT * from fruit_load_list")
#my_data_rows = my_cur.fetchall()
st.header("The fruit load list contains:")
# snowflake-relataed function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# add a button to load the fruit
if st.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    st.dataframe(my_data_rows)

add_my_fruit = st.multiselect("What fruit would you like to add?", list(my_fruit_list.index), ['Honeydew'])

st.write('Thanks for adding', add_my_fruit)
my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from streamlit')")

