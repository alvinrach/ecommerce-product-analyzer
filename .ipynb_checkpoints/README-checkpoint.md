# Ecommerce Product Analyzer

Go to enhanceyourgifts.streamlit.app :)

For merchants, this apps can give you insights & add your product value, here you can:  
1. See 3 most similar competitor of your product
2. Make your product description better using AI

For engineer/data team, this apps works by 3 steps:
1. Get dataset. By parsing data from Tokopedia
2. Find similar product using cosine similarity
3. Using generative AI to make your description better

More explanation in main.ipynb, where we will done several experimente before we create this app!

For engineer/data team to run app:

pip install -r requirements.txt
streamlit run app.py

will be run in port 8501

Next development (if i have more time I will):
-Create backend
-Deploy on docker
-Improve precision