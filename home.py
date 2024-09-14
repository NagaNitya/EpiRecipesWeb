import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

data=pd.read_csv('epi_r.csv')
recipes=pd.read_json('full_format_recipes.json')
pd.set_option('display.max_colwidth', None)


def prepData():
    data.sort_values(by='rating', ascending=False, inplace=True)
    data.reset_index(drop=True, inplace=True)


def home():
    st.title('Epic Recipe Ideas')
    st.write("Here are some of the top rated recipes from the Epic Recipe Ideas website:")
    for i in range(10):
        st.write("####", str(i+1)+".", data['title'][i])
        st.write("Rating:", str(data['rating'][i]), "\n", "Calorie Count:", str(data['calories'][i]))


def search():
    st.title('Search for a Recipe')
    st.write("Enter the name of a recipe to search for:")
    recipe_name=st.text_input("Recipe Name")+" "
    if recipe_name in data['title'].values:
        st.write("### Recipe found! Here are the details:")
        st.write("Rating:", data.loc[data['title']==recipe_name]["rating"].to_string(index=False))
        st.write("Calorie count:", data.loc[data['title']==recipe_name]["calories"].to_string(index=False)) 

        ing=recipes[recipes['title']==recipe_name]["ingredients"].to_string(index=False)[1:-1].split(",")
        st.write("#### Ingredients:")
        for i in range(len(ing)):
            st.write(str(i+1)+".", ing[i])
            
        st.write("#### Directions:\n", recipes[recipes['title']==recipe_name]["directions"].to_string(index=False)[1:-1])

    elif recipe_name==" ":
        st.write("Please enter a recipe name")
    else:
        st.write("### Recipe not found. Please try again.")  


def stats():
    st.title('Recipe Stats')
    st.write("#### Here are some statistics about the recipes:")
    st.write("Average rating:", str(data['rating'].mean()))
    st.write("Average calorie count:", str(data['calories'].mean()))
    st.write("Average protein count:", str(data['protein'].mean()))
    st.write("Average fat count:", str(data['fat'].mean()))
    st.write("Average sodium count:", str(data['sodium'].mean()))

    st.write("#### Visualisations:")
    rating_count=data['rating'].round().value_counts().reset_index()
    rating_count.columns=['rating', 'number of recipes']
    fig=px.pie(rating_count, names='rating', values='number of recipes', hole=0.3, title='Distribution of ratings', width=800, height=600)
    st.plotly_chart(fig)

    tags=data.drop(columns=['title', 'rating', 'calories', 'protein', 'fat', 'sodium'])
    tag_count=tags.sum().sort_values(ascending=False).reset_index()
    tag_count.columns=['tag', 'number of recipes']
    tag_count=tag_count[tag_count['number of recipes']>4000]
    fig=px.scatter(tag_count, x='tag', y='number of recipes', title='Number of recipes by tag', width=800, height=600)
    st.plotly_chart(fig)
    

def main():
    prepData()
    p1, p2, p3= st.tabs(["Home", "Search for a Recipe", "Stats"])
    with p1:
        home()
    with p2:
        search()
    with p3:
        stats()    
   

if __name__ == '__main__':
    main() 