
import streamlit as st

import pandas as pd

import plotly.express as px
import joblib
import sqlite3
from sqlite3 import Error
from datetime import datetime



# Create tabs for Volunteer and Donation
tabs = st.sidebar.radio("FOOD DRIVE APP", ["Journey Overview"])

if tabs == "Journey Overview":

  # Load the dataset with a specified encoding
  data = pd.read_csv('clean_data.csv', encoding='latin1')

  # Page 1: Dashboard
  def dashboard():
      st.image('/content/logo_.png', use_column_width=True)

      st.subheader("💡 Abstract:")

      inspiration = '''
       This project draws inspiration from a collective desire to bridge gaps in food donation systems, driven by compassion for those in need. Empowering communities through organized efforts, it aspires to bring hope, nourishment, and dignity to every doorstep, fostering a sense of unity and care.


      '''

      st.write(inspiration)

      st.subheader("👨🏻‍💻 What our Project Does?")

      what_it_does = '''
    The Edmonton Food Drive Enhancement Project, involving various phases like data collection, cleaning, analysis, machine learning modeling, geospatial mapping, application development and stakeholder engagement will significantly improve the food donation process by improving resource allocation for timely donation collection and minimal logistical. And, during all this process we got invaluable field experience.

      '''

      st.write(what_it_does)


  # Page 2: Exploratory Data Analysis (EDA)
  def exploratory_data_analysis():
      st.title("Exploratory Data Analysis")
      # Rename columns for clarity
      data_cleaned = data.rename(columns={
          'Drop Off Location': 'Location',
          'Stake': 'Stake',
          '# of Adult Volunteers in this route': '# of Adult Volunteers',
          '# of Youth Volunteers in this route': '# of Youth Volunteers',
          '# of Donation Bags Collected/Route': 'Donation Bags Collected',
          'Time to Complete (in minutes) pick up of bags /route': 'Time to Complete (min)',
          'Number of routes completed': 'Routes Completed',
          '# of Doors in Route': 'Doors in Route'
        })

      # Visualize the distribution of numerical features using Plotly
      fig = px.histogram(data_cleaned, x='# of Adult Volunteers', nbins=20, labels={'# of Adult Volunteers': 'Adult Volunteers'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='# of Youth Volunteers', nbins=20, labels={'# of Youth Volunteers': 'Youth Volunteers'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='Donation Bags Collected', nbins=20, labels={'Donation Bags Collected': 'Donation Bags Collected'})
      st.plotly_chart(fig)

      fig = px.histogram(data_cleaned, x='Time to Complete (min)', nbins=20, labels={'Time to Complete (min)': 'Time to Complete'})
      st.plotly_chart(fig)

  # Page 3: Machine Learning Modeling
  def machine_learning_modeling():
      st.title("Machine Learning Modeling")
      st.write("Enter the details to predict donation bags:")

      # Mapping of options to their equivalent data
      options_data = {
      "Londonderry Chapel": 29.59322034,
      "Gateway Stake Centre": 30.29457364,
      "Bearspaw Chapel": 25.03571429,
      "Bonnie Doon Stake Centre": 22.5,
      "Coronation Park Chapel": 32.02380952,
      "North Stake Centre": 30.20930233,
      "Riverbend Stake Centre": 42.69444444,
      "Parkland (Spruce Grove/Stony Plain)": 45.14285714,
      "Morinville" : 52.5,
      "Onoway" : 10.0
      }

      # Create a dropdown list
      selected_option = st.selectbox(
      "Drop Off Locations:",
      list(options_data.keys())
      )


      # Display the equivalent data for the selected option
      if selected_option in options_data:
        selected_data = options_data[selected_option]
        st.write(f"Data for '{selected_option}': {selected_data}")
      else:
        st.write("No data available for the selected option.")

      # Mapping of options to their equivalent data
      options_data_stake = {
      "Bonnie Doon Stake": 27.515625,
      "Gateway Stake": 28.72251309,
      "Edmonton North Stake": 31.57723577,
      "Riverbend Stake": 42.69444444,
      "YSA Stake": 50.0
      }

      # Create a dropdown list
      selected_option_stake = st.selectbox(
      "Stake:",
      list(options_data_stake.keys())
      )


      # Display the equivalent data for the selected option
      if selected_option_stake in options_data_stake:
        selected_data_stake = options_data_stake[selected_option_stake]
        st.write(f"Data for '{selected_option_stake}': {selected_data_stake}")
      else:
        st.write("No data available for the selected option.")


      routes_completed = st.slider("Routes Completed", 1, 10, 5)
      time_spent = st.slider("Time Spent (minutes)", 10, 300, 60)
      adult_volunteers = st.slider("Number of Adult Volunteers", 1, 50, 10)
      doors_in_route = st.slider("Number of Doors in Route", 10, 500, 100)
      youth_volunteers = st.slider("Number of Youth Volunteers", 1, 50, 10)


    # Predict button
      if st.button("Predict"):

         # Load the trained model
         model = joblib.load('/content/random_forest_regressor_model.pkl')

          # Prepare input data for prediction
         input_data = [[selected_data, selected_data_stake,  routes_completed, time_spent, adult_volunteers, doors_in_route, youth_volunteers]]

          # Make prediction
         prediction = model.predict(input_data)

          # Display the prediction
         st.success(f"Predicted Donation Bags: {prediction[0]}")

          # You can add additional information or actions based on the prediction if needed
    # Page 4: Neighbourhood Mapping
    # Read geospatial data
  geodata = pd.read_csv("/content/merged_data.csv")

  def neighbourhood_mapping():
      st.title("Neighbourhood Mapping")

      # Get user input for neighborhood
      user_neighbourhood = st.text_input("Enter the neighborhood:")

    # Check if user provided input
      if user_neighbourhood:
          # Filter the dataset based on the user input
          filtered_data = geodata[geodata['Neighbourhood'] == user_neighbourhood]

          # Check if the filtered data is empty, if so, return a message indicating no data found
          if filtered_data.empty:
              st.write("No data found for the specified neighborhood.")
          else:
              # Create the map using the filtered data
              fig = px.scatter_mapbox(filtered_data,
                                      lat='Latitude',
                                      lon='Longitude',
                                      hover_name='Neighbourhood',
                                      zoom=12)

              # Update map layout to use OpenStreetMap style
              fig.update_layout(mapbox_style='open-street-map')

              # Show the map
              st.plotly_chart(fig)
      else:
           st.write("Please enter a neighborhood to generate the map.")


# Page 5: Data Collection
  def data_collection():
      st.title("Google Drive Data Collection")
      st.write("Please fill out the Google form to contribute to our Food Drive!")
      google_form_url = "https://forms.gle/Sif2hH3zV5fG2Q7P8"#YOUR_GOOGLE_FORM_URL_HERE
      st.markdown(f"[Fill out the form]({google_form_url})")

  # Main App Logic
  def main():
      st.sidebar.title("ML Journey")
      app_page = st.sidebar.radio("Select a Page", ["Dashboard", "EDA", "ML Modeling", "Neighbourhood Mapping", "Data Collection"])

      if app_page == "Dashboard":
          dashboard()
      elif app_page == "EDA":
          exploratory_data_analysis()
      elif app_page == "ML Modeling":
          machine_learning_modeling()
      elif app_page == "Neighbourhood Mapping":
          neighbourhood_mapping()
      elif app_page == "Data Collection":
          data_collection()

  if __name__ == "__main__":
     main()
