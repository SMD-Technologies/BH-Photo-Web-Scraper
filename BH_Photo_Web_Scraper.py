# import streamlit as st
# import undetected_chromedriver as uc
# from bs4 import BeautifulSoup
# import pandas as pd
# import ipywidgets as widgets
# from IPython.display import display

# st.title("Web Scraping Data")

# # Input for user to provide the URL
# url_input = st.text_input("Enter the URL:", "")
# scrape_button = st.button("Scrape and Display")

# if scrape_button:
#     if url_input:
#         options = uc.ChromeOptions()
#         options.headless = True  # Run Chrome in headless mode

#         with uc.Chrome(options=options) as driver:
#             driver.get(url_input)
#             page_source = driver.page_source

#         soup = BeautifulSoup(page_source, 'html.parser')

#         title = soup.find('title')
#         title_text = title.text.strip()
#         price = soup.find('div', class_='price__9gLfjPSjp')
#         price_text = price.text.strip()

#         # Find the div elements that contain features
#         feature_groups = soup.find_all('div', class_='group_fDXOr6EpR9')

#         # Initialize a list to store the camera features
#         features = []

#         # Loop through each feature group and extract the labels and values
#         for group in feature_groups:
#             feature_label = group.find('div', class_='name_fDXOr6EpR9').text.strip()

#             feature_table = group.find('table', class_='table_fDXOr6EpR9')
#             feature_rows = feature_table.find_all('tr', class_='pair_KqJ3Q3GPKv')

#             feature_data = {}
#             for row in feature_rows:
#                 label = row.find('td', class_='label_KqJ3Q3GPKv').text.strip()
#                 value = row.find('td', class_='value_KqJ3Q3GPKv').text.strip()
#                 feature_data[label] = value

#             features.append({feature_label: feature_data})

#             # Create an empty dictionary to hold the data
#             data = {}

#             # Iterate through each item in the nested list
#             for item in features:
#                 for category, details in item.items():
#                     row = []
#                     for key, value in details.items():
#                         row.append(f"{key}: {value}")
#                     data[category] = ['\n'.join(row)]

#             df = pd.DataFrame(data)

#             pd.set_option('display.max_colwidth', None)

#             df.insert(0,'Price',price_text)
#             df.insert(0,'Title',title_text)

#         # Display the DataFrame
#         st.header("Features DataFrame:")
#         st.table(df)
#     else:
#         st.warning("Please enter a valid URL.")

import streamlit as st
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import pandas as pd
import json
import base64
from io import BytesIO
import streamlit as st
import pandas as pd
import base64
from io import BytesIO
# import locale
# locale.setlocale( locale.LC_ALL, 'en_ZA.ANSI' )
def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download Excel file</a>' # decode b'abc' => abc

st.set_page_config(layout="wide")
st.title("Web Scraping Data")

# Input for user to provide the URL
url_input = st.text_input("Enter the URL:", "")
scrape_button = st.button("Scrape and Display")

if scrape_button:
    if url_input:
        options = uc.ChromeOptions()
        options.headless = True  # Run Chrome in headless mode

        with uc.Chrome(options=options) as driver:
            driver.get(url_input)
            page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')


        # price = soup.find('div', class_='price__9gLfjPSjp')
        # price_text = price.text.strip()
        try:
            title = soup.find('title')
            title_text = title.text.strip()
            script_tag = soup.find('script', type='application/ld+json')
            json_data = script_tag.contents[0]
            data = json.loads(json_data)
            price = data['offers']['price']
            priceCurrency = data['offers']['priceCurrency']


            # Find the div elements that contain features
            feature_groups = soup.find_all('div', class_='group_fDXOr6EpR9')

            # Initialize a list to store the camera features
            features = []

            # Loop through each feature group and extract the labels and values
            for group in feature_groups:
                feature_label = group.find('div', class_='name_fDXOr6EpR9').text.strip()

                feature_table = group.find('table', class_='table_fDXOr6EpR9')
                feature_rows = feature_table.find_all('tr', class_='pair_KqJ3Q3GPKv')

                feature_data = {}
                for row in feature_rows:
                    label = row.find('td', class_='label_KqJ3Q3GPKv').text.strip()
                    value = row.find('td', class_='value_KqJ3Q3GPKv').text.strip()
                    feature_data[label] = value

                features.append({feature_label: feature_data})

            # Create an empty dictionary to hold the data
            data = {}

            # Iterate through each item in the nested list
            for item in features:
                for category, details in item.items():
                    row = []
                    for key, value in details.items():
                        row.append(f"{key}: {value}")
                    data[category] = ['\n'.join(row)]

            df = pd.DataFrame(data)
            df.insert(0,'Price Currency',priceCurrency)
            df.insert(0,'Price',price)
            df.insert(0,'Title',title_text)

            # Display the DataFrame
            st.header("Features Table:")
            st.table(df)
            df = df
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)


        except:
            st.write("Looks like B&H Photo has been scraped too many times. Please visit the URL to confirm you are human:")
            st. write(url_input)

    else:
        st.warning("Please enter a valid URL.")

