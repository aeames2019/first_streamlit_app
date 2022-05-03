import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

def get_fruitvice_data(this_fruit_choice):
    fruitvice_reponse = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruitvice_reponse.json())
    return fruityvice_normalized  
try:
  fruit_choice = streamlit.text_input('What fruits would you like more information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruitvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
#Snowflake-realted function

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")
            return my_cur.fetchall()
        
# Add a button to load the fruit data
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_row = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

#add_my_fruit = streamlit.text_input('What fruits would you like to add?', 'Jackfruit')
#streamlit.write('Thanks for adding', add_my_fruit)
