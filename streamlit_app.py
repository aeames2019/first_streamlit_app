import streamlit
import pandas
import requests

streamlit.title('My Mom\'s New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# let's put a pick list here so they can pick the fruits they want to include 
fruits_selected = streamlit.multiselect("pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table on a page
streamlit.dataframe(fruits_to_show)

# new section to display fruitvice api
streamlit.header('Fruityvice Fruit Adivce')
fruit_choice = streamlit.text_input('What fruits would you like more information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

fruitvice_reponse = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# take the json format and normalize it
fruityvice_normalized = pandas.json_normalize(fruitvice_reponse.json())
# output it to the screen as table
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector 

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT current_user(), current_account(), current_region()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
