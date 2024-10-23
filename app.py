import streamlit as st 
from utils import Stockfetch

st.set_page_config(page_title="Stock Price Project", page_icon="📈")

@st.cache_resource
def get_stock_client(api_key):
    return Stockfetch(api_key = api_key)

api_key = st.secrets["API_KEY"]
client = get_stock_client(api_key)

@st.cache_data(ttl=3600)
def search_stock(company):
    return client.symbol_search(company)

@st.cache_data(ttl=3600)
def plot_chart(symbol):
    return client.plot_chart(symbol)

if __name__ == "__main__":
    # Adding title to the app
    st.title("Stock Project Streamlit")

    # Add Subheading below
    st.subheader("By Anjali Takale")

    # Take company as text input from user
    company = st.text_input("Please provide company :")

    # After pressing enter giving company name
    if company:
        search_data = search_stock(company)
        if search_data:
            options = st.selectbox("Select company Symbol",list(search_data.keys()))
            symbol_data = search_data.get(options)
            st.success(f"Company Name : {symbol_data[0]}")
            st.success(f"Type : {symbol_data[1]}")
            st.success(f"Region : {symbol_data[2]}")

            if st.button("Submit"):
                fig = plot_chart(symbol = options)
                st.plotly_chart(fig)

        else:
            st.error("Company name not found")