import streamlit as st
from gpt_review_analysis import get_completion
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os
import datetime
from streamlit_star_rating import st_star_rating


_ = load_dotenv(find_dotenv())
#MONGODB_URI  = os.getenv('MONGODB_URI')
MONGODB_URI = "your mongodb database connection string"

# Get current date and time
current_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
current_date = str(datetime.date.today())

# Set main interface image banner and title
st.image("https://3c5239fcccdc41677a03-1135555c8dfc8b32dc5b4bc9765d8ae5.ssl.cf1.rackcdn.com/22-5-16-BANS-feedback%20customer%20reviews_EDT-1000x350.jpg", width=800)
st.title("USER REVIEW CLASSIFICATION")


####################################################### TRANSFER DATA TO MONGODB ATLAS ########################################
def userReviewToAtlas(MONGODB_URI, user_review_data):
    """ This function allows data tranfer to MongoDB Atlas database. It takes as 
    input MongoDB Atlas connection string and the data to be transfered to the database"""
    try:
        # Connect to MongoDB cluster with MongoClient
        client = MongoClient(MONGODB_URI)

        #print("Client Connected")
        # Get reference to the database
        db = client.products_review_db

        # Get reference to the database collection
        users_reviews_collection = db.users_reviews
        #print("Connected to Collection")

        # Write the expression that inserts the user review in our mongodb database collection.
        result = users_reviews_collection.insert_one(user_review_data)
        #print("Data Transfered")
        # Close the connection to the database
        client.close()
    except:
        print("Error During The Update")

def on_click():
    """ This function when called will automatically clear defined input fields"""
    st.session_state.user_first_name_key = ""
    st.session_state.user_last_name_key = ""
    st.session_state.user_email_address_key = ""
    st.session_state.user_location_key = ""
    st.session_state.user_phone_number_key = ""
    st.session_state.user_review_key = ""

# Declare a markdown to modify the sidebar
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #becaff;
    }
</style>
""", unsafe_allow_html=True)

# Define our sidebar
with st.sidebar:
    #st.write("Side bar")
    # Set a sidebar image obtained from https://www.creativefabrica.com/product/ecommerce-logo-design-2/
    st.image("https://www.creativefabrica.com/wp-content/uploads/2022/06/17/Ecommerce-Logo-Design-Graphics-32523051-1.jpg")
    st.header("About")
    st.info('Your best Ecommerce platform which provides an end-to-end solution that allows online retailers to manage their business with the respect of customers.\
            Affordable prices and fast delivery. Choose your item and we take care of the rest.')
    stars_rating = st_star_rating("Voted 5 Stars Best Ecommerce Platform", maxValue=5, defaultValue=5, key="start_rating", read_only = True)
    emoji_rating = st_star_rating(label = "Best Customer Experience", maxValue = 5, defaultValue = 5, key = "emoji_rating", emoticons = True, read_only = True)



with st.form("user_review_form", clear_on_submit=True):
    st.write("**In order to provide you with the best service and improve our customer experience, kindly fill the review form.**")
    select_category = st.selectbox("Kindly Select Your Item Category:",
                            ('Computer and Consumer Electronics', 'Toys and Games', 'Apparel', 
                             'Home Appliances', 'Beauty or Personal care', 'Household Products',
                             'Furniture', 'Auto and Parts', 'Office Equipment and Supplies', 'Book or Musics or Video'))
    user_first_name = st.text_input("Enter Your First and Middle Name", key="user_first_name_key")
    user_last_name = st.text_input("Enter Your Last Name", key="user_last_name_key")
    user_email_address = st.text_input("Enter Your Email Address", key="user_email_address_key")
    user_location = st.text_input("Enter Your Location", key="user_location_key")
    user_phone_number = st.text_input("Enter Your Phone Number", key="user_phone_number_key")
    user_review = st.text_area("Product Review Area", height=250, key="user_review_key")
    # Button for review submission
    submitted = st.form_submit_button("Submit") #, on_click=on_click)
    if submitted:
        # Define our prompt for chatgpt
        prompt = f"""
        Identify the following items from the review text: 
        - Sentiment (positive or negative or neutral)
        - Reviewer emotions
        - Item purchased by reviewer
        - Summarize the review

        The review is delimited with triple backticks. \
        Format your response as a python dictionary object with \
        "sentiment", "reviewer_emotions", "purchased_item" and "review_summary" as the keys.\
        Give only one emotion from the reviewer. \
        If the information isn't present, use "unknown" \
        as the value.
        Make your response as short as possible. Finaly the review's summary should \
        be concise and precise and only contains relevant information.

        Review text: '''{user_review}'''
        """
        response = get_completion(prompt)
        #print(response)

        dict_user_form = {'product_category': select_category,
                        'user_first_name': user_first_name,
                        'user_last_name':user_last_name,
                        'user_email_address': user_email_address,
                        'user_location': user_location,
                        'user_phone_number': user_phone_number,
                        'review_date': current_date,
                        'review_time': current_time,
                        "review_original": user_review
                        }
        dict_gpt_analysis = eval(response)
        final_data = {**dict_user_form, **dict_gpt_analysis}
        userReviewToAtlas(MONGODB_URI, final_data)
        #st.write(final_data)
        st.success('Thank you for your review!', icon="✅")
        

