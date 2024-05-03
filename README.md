# Large Language Model Product Review Classification

# DESCRIPTION
The aim of this project is to use a large language model for customer product review.
Machine learning has been used for a while for images and texts classification, sentiment and emotion analysis. However, training an accurate machine learning model can be challenging. Here, we will replace the machine learning model with a large language model powered by gpt-3.5-turbo with custom prompt engineering.

# DEPENDENCIES
 - streamlit
 - pymongo
 - dotenv
 - os
 - datetime
 - streamlit_star_rating

# SYSTEM OVERVIEW
### PIPELINE
The system 
 - takes as input the user personal information (first and last name, email address, location, phone number) and his review.
 - Classify the review: positive, negative or neutral with gpt-3.5-turbo.
 - Classifiy the user emotion with gpt-3.5-turbo.
 - Generate the review summary with gpt-3.5-turbo. 
 - Tranfer the data to MongoDB Atlas.
![review_classification_system_overview](https://github.com/WENDGOUNDI/large_language_model_product_review_classification/assets/48753146/dbcddbf4-306f-41f2-9aa1-8eb0b4a67b46)


### STORING DATA ON MONGODB ATLAS
We used MongoDB Atlas, a NoSQL cloud database for storing the user and product review data. MongoDB Atlas offers a great flexibility in terms of document schema and allow building custom dashboards for realtime data monitoring.
The saved data contains:
 - Product Category
 - User First Name
 - User Last Name
 - User Email Address
 - User Location
 - User Phone Number
 - Reivew Date
 - Review Time
 - Review original
 - Sentiment
 - Reviewer Emotions
 - Purchases Item
 - Review Summary
![review_classification_database_mongodb](https://github.com/WENDGOUNDI/large_language_model_product_review_classification/assets/48753146/c32cb193-0798-40af-b1be-0b2a3e0f6d29)

# WEBAPP INTREFACE
The webapp interface has been implemented with Streamlit.
![interface](https://github.com/WENDGOUNDI/large_language_model_product_review_classification/assets/48753146/e96a0fa0-c902-4f6a-a4a9-bab41154bbb5)
