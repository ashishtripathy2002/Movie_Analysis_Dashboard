# data_analytics.py component
import streamlit as st
import plotly.express as px
import pandas as pd
from services.metadata_service import MetadataService
from services.movie_service import MovieService
from services.analytics_service import AnalyticsService

import plotly.graph_objects as go

def plot_enhanced_profit_margin_chart(df):
    fig = go.Figure(
        data=[
            go.Bar(
                x=df['movie_title'],
                y=df['profit_margin'],
                text=df['profit_margin'],  
                marker=dict(
                    color=df['profit_margin'],  
                    colorscale="Viridis", 
                    colorbar=dict(title="Revenue to Budget Ratio")  
                ),
                texttemplate="%{text:.2f}", 
                textposition="outside",  
            )
        ]
    )

    fig.update_layout(
        title="Top Movies by Profit Margin",
        xaxis_title="Movie Titles",
        yaxis_title="Revenue to Budget Ratio",
        title_x=0.5,
        template="plotly_dark",
        showlegend=False,
        margin=dict(t=50, l=60, r=40, b=40), 
      )
    return fig

def plot_bar_chart(df, x, y, title, labels, color=None, color_scheme="Blues"):
    fig = px.bar(
        df,
        x=x,
        y=y,
        title=title,
        labels=labels,
        color=y, 
        color_continuous_scale=color_scheme,  
        template="plotly_white" 
    )

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=labels.get(x, x),
        yaxis_title=labels.get(y, y),
        coloraxis_colorbar=dict(title=labels.get(y, y)),
        margin=dict(l=40, r=40, t=60, b=40)
    )

    st.plotly_chart(fig, use_container_width=True)

def render_tab_movie_insights():
    st.markdown("Explore Top Movie Trends and Insights and Trends ", unsafe_allow_html=True)

    st.markdown("##### Correlation between Popularity and Box Office Revenue by Genre")
    data = AnalyticsService.get_genre_popularity_revenue_correlation()
    movie_data = MovieService.get_all_movies(per_page=0)
    movies_df = pd.DataFrame(movie_data["movies"])
    movies_df = movies_df.explode('genres')
    if "error" not in data:
        df = pd.DataFrame(data)
        col1, col2 = st.columns(2)
        with col1:
            # Compute the correlation between vote_average and revenue for each genre
            correlations = []
            for genre in movies_df['genres'].unique():
                genre_df = movies_df[movies_df['genres'] == genre]
                if len(genre_df) > 1: 
                    corr = genre_df['vote_average'].corr(genre_df['revenue'])
                    correlations.append({'genre_name': genre, 'correlation_coefficient': corr})

    
            correlation_df = pd.DataFrame(correlations)

            # Define the correlation coefficient bar chart
            genre_insights_bar_chart_placeholder = st.empty()
            fig1 = px.bar(
                correlation_df,
                x="genre_name",
                y="correlation_coefficient",
                title="Correlation Coefficient by Genre",
                labels={"genre_name": "Genre", "correlation_coefficient": "Correlation Coefficient"},
                color="correlation_coefficient",
                color_continuous_scale=[(0, 'red'), (0.5, 'white'), (1, px.colors.sequential.Blues[-1])]
            )
            fig1.update_layout(
                title_x=0.5,
                yaxis=dict(title="Correlation Coefficient"),
                xaxis=dict(title="Genre"),
                margin=dict(l=20, r=20, t=60, b=20),
                coloraxis_colorbar=dict(title="Correlation", tickvals=[-1, 0, 1], ticktext=["-1", "0", "1"]),
            )
            
            genre_insights_bar_chart_placeholder.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            genres = movies_df['genres'].unique()
            selected_genres = st.multiselect("Select Genre(s) to Filter", options=genres, default=genres[:2])
            filtered_data = ( movies_df[movies_df['genres'].isin(selected_genres)].groupby('genres').tail(200))
            # filtered_data = movies_df[movies_df['genres'].isin(selected_genres)]
            if not filtered_data.empty:
                fig = px.scatter(
                    filtered_data,
                    x='vote_average',  
                    y='revenue',
                    color='genres',
                    title="Popularity vs Revenue by Genre",
                    labels={"vote_average": "Popularity Score", "revenue": "Box Office Revenue"},
                    hover_data=['title', 'release_date'],
                    trendline="ols",
                 
                    log_y=True  # Apply log scale to y-axis
                )

                fig.update_traces(marker=dict(size=7, opacity=0.9), selector=dict(mode='markers'))
                fig.update_layout(showlegend=True)
                st.plotly_chart(fig, use_container_width=True)


            else:
                st.warning("No movies available for the selected genre(s).")

        # Most Profitable Sequels and Prequels by Genre
        st.markdown("##### Most Profitable Sequels and Prequels by Genre")                 
        all_keywords = ["sequel", "prequel"]
        default_keywords = ["sequel", "prequel"]
        selected_keywords = st.multiselect(
            "Select Keywords to Filter Movies",
            options=all_keywords,
            default=default_keywords
        )
        keywords_param = selected_keywords if selected_keywords else all_keywords
        data = AnalyticsService.get_most_profitable_genres_with_sequels_prequels(keywords=keywords_param)

        if isinstance(data, dict) and "error" in data:
            st.warning(f"Error: {data['error']}")
        elif isinstance(data, list) and len(data) == 0:
            st.info("No data available for the selected keywords.")
        else:
            df = pd.DataFrame(data)
            df = df.sort_values(by='total_profit', ascending=False) 
            color_map = {
                "sequel": {"positive": "rgb(8, 48, 107)", "negative": "rgb(111, 50, 47)"},
                "prequel": {"positive": "rgb(66, 146, 198)", "negative": "rgb(239, 83, 80)"}
            }
            df['color'] = df.apply(lambda row: color_map[row['keyword_name']]['positive'] if row['total_profit'] >= 0 
                                else color_map[row['keyword_name']]['negative'], axis=1)
                    
            df['color_label'] = df.apply(
                lambda row: f"{row['keyword_name']} (Positive)" if row['total_profit'] >= 0 else f"{row['keyword_name']} (Negative)",
                axis=1
            )
            fig = px.bar(
                df,
                x="genre_name",
                y="total_profit",
                color="color_label",
                barmode="group",
                title="Total Profit by Genre for Sequels and Prequels (Including Negative Profits)",
                labels={"total_profit": "Total Profit", "genre_name": "Genre", "keyword_name": "Type"},
                color_discrete_sequence=df['color'].unique()  
            )

            fig.update_layout(
                xaxis_title="Genre",
                yaxis_title="Total Profit",
                title_x=0.5,
                legend_title="Type",
                template="plotly_white",
                yaxis=dict(tickformat=".2s"),  
                margin=dict(t=60, b=40, l=20, r=20))

        # Display the chart in Streamlit
        st.plotly_chart(fig, use_container_width=True)


    min_year = 1950  
    max_year = 2023  
    st.markdown(f"##### Top Production Companies by Total Revenue across Genres")

    col1, col2, col3 = st.columns(3)
    with col1:
        top_n_companies = st.selectbox("Select number of production companies to display", options=[5, 10, 15], index=0)

    with col2:
        genre_list = [genre['genre_name'] for genre in MetadataService.fetch_genres()]  

        genres = st.multiselect("Filter by Genre", options=genre_list, default=genre_list[:3])

    with col3:
       
        selected_year_range = st.slider(
            "Filter by Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year)
        )

    data = AnalyticsService.get_top_production_companies_by_revenue(genres,start_year=selected_year_range[0], end_year=selected_year_range[1], limit=top_n_companies)
    if isinstance(data, dict) and "error" in data:
        st.warning(data["error"]) 
    elif isinstance(data, list) and len(data) == 0:
        st.info("No data available for the selected filters.")
    else:
        df = pd.DataFrame(data)
        if 'genre_name' in df.columns:
            df = df[df['genre_name'].isin(genres)]
        plot_bar_chart(df, x="company_name", y="total_revenue", title="Top Production Companies by Revenue",
                    labels={"company_name": "Company", "total_revenue": "Total Revenue"})
        
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Top Movies by Profit Margin")
        top_n_movies = st.selectbox("Select number of movies to display", options=[5, 10, 15], index=0)
        if top_n_movies:
            data = AnalyticsService.get_top_profit_margin_movies(limit=15)
            if "error" not in data:
                df = pd.DataFrame(data).head(top_n_movies)
                fig = plot_enhanced_profit_margin_chart(df)
                st.plotly_chart(fig, use_container_width=True)


def render_tab_director_insights():
    st.markdown("Get Insights on director performance ", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    # Top directors by number of movies directed
    with col1:
        st.markdown("##### Top Directors by Number of Movies Directed")
        top_n_directors = st.selectbox("Select number of top directors to display", options=[5, 10, 15], index=0)
        top_directors_placeholder = st.empty()
        data = AnalyticsService.get_top_directors(limit=top_n_directors)
        if "error" not in data:
            df = pd.DataFrame(data)
            fig = go.Figure(
                data=[go.Bar(
                    x=df["director_name"],
                    y=df["number_of_directed_movies"],
                    text=df["number_of_directed_movies"],
                    marker=dict(
                        color=df["number_of_directed_movies"],
                        colorscale="Viridis",  
                        colorbar=dict(title="Movies Directed")
                    ),
                    texttemplate="%{text}",
                    textposition="outside",
                )]
            )

            fig.update_layout(
                title=f"Top {top_n_directors} Directors by Movies Directed",
                xaxis_title="Director",
                yaxis_title="Number of Movies",
                title_x=0.5,
                template="plotly_white",
                showlegend=False,
            )
            top_directors_placeholder.plotly_chart(fig, use_container_width=True)

    # Directors with most movies in the top 100 grossing films
    with col2:
        st.markdown("##### Directors with Most Movies in Top 100 Grossing Films")
        top_grossing_placeholder = st.empty()
        data = AnalyticsService.get_directors_top_grossing(limit=100)
        if "error" not in data:
            df = pd.DataFrame(data)
            df = df.sort_values(by=["num_movies", "films_gross"], ascending=[False, False])
            df = df.rename(columns={"director_name": "Director","num_movies": "Number of Movies in Top 100","films_gross": "Total Gross"})
            df["Total Gross"] = pd.to_numeric(df["Total Gross"], errors='coerce')
            df["Total Gross"].fillna(0, inplace=True)
            top_n = st.selectbox("Select number of top directors to display", options=[5, 10, 15, 20], index=0)
            # top_grossing_placeholder.dataframe(df, use_container_width=True)
            directors_aggregated_df = df.groupby('Director', as_index=False).agg({'Number of Movies in Top 100': 'sum'})
            top_directors_df = directors_aggregated_df.nlargest(top_n, 'Number of Movies in Top 100')
            directors_fig = px.bar(top_directors_df, x='Director', y='Number of Movies in Top 100',
                                title=f'Top {top_n} Directors by Number of Movies Directed',
                                labels={'Number of Movies in Top 100': 'Number of Movies'},
                                color='Number of Movies in Top 100',
                                color_continuous_scale=px.colors.sequential.Viridis)

            st.plotly_chart(directors_fig)
    
    # Director-Actor Collaborations with Highest-Grossing Movie
    st.markdown("##### Top Director-Actor Collaborations by Collaboration Count")
    director_actor_collaboration_placeholder = st.empty()
    data = AnalyticsService.get_director_actor_collaborations()
    if "error" not in data:
        # st.write(data)
        top_n = st.selectbox("Select number of top director-actor collab to display", options=[5, 10, 15, 20], index=0)
        df = pd.DataFrame(data)
        top_da_df = df.nlargest(top_n, 'collaboration_count') 
        fig = px.bar(
                    top_da_df, 
                    y='director_name',            
                    x='collaboration_count',      
                    color='actor_name',           
                    hover_data={'revenue': True}, 
                    title='Top Director-Actor Collaborations by Collaboration Count',
                    labels={'collaboration_count': 'Collaboration Count', 'actor_name': 'Actor'},
                    orientation='h'              
                )
        
        # Update layout for axis labels
        fig.update_layout(xaxis_title="Collaboration Count", yaxis_title="Director", legend_title="Actor")

        st.plotly_chart(fig)
    else:
        st.write(data)


def render_tab_actor_insights():
    st.markdown("Insights into the most popular actors ", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    # Actors with Highest Average Vote in Sci-Fi
    with col1:
        st.markdown(f"##### Actors with Highest Average Vote in Selected Genre")
        col3, col4 = st.columns(2)
        with col3:
            top_n_actors = st.selectbox("Select number of top actors by average vote", options=[5, 10, 15], index=0)

        with col4:
            genre_list = [genre['genre_name'] for genre in MetadataService.fetch_genres()]  # Fetch genres dynamically

            default_index = genre_list.index("science fiction") if "science fiction" in genre_list else 0
            selected_genre = st.selectbox("Select a genre", options=[""] + genre_list, index=(default_index + 1))

        data = AnalyticsService.get_highest_avg_vote_actors_by_genre(genre=selected_genre, limit=top_n_actors)
        if "error" not in data and data:
            df = pd.DataFrame(data)
            plot_bar_chart(df, x="actor_name", y="avg_vote", title=f"Top {selected_genre.capitalize()} Actors by Average Vote",
                            labels={"actor_name": "Actor", "avg_vote": "Average Vote"}, color_scheme="Cividis")
        else:
            st.warning("No data available or error in API response.")
   
    # Actors with Most Appearances in High-Rated Movies
    with col2:
        st.markdown("##### Actors with Most Appearances in High-Rated Movies")
        
        col5, col6 = st.columns(2)
        with col5:
            limit = st.selectbox("Select number of actors to display", options=[5, 10, 15], index=0)
        with col6:
            min_rating = st.slider("Select Minimum Rating Threshold", min_value=5, max_value=10, value=8, step=1)
        data = AnalyticsService.get_actors_with_high_rated_appearances(limit, min_rating=min_rating)
        if "error" not in data and data:
            df = pd.DataFrame(data)
            plot_bar_chart(df, x="actor_name", y="high_rated_appearances",title="Actors with High-Rated Appearances",
                            labels={"actor_name": "Actor", "high_rated_appearances": "Appearances"}, color_scheme="Viridis")
            
    # Actors with Highest Rating Difference Between Two Genres
    st.markdown("##### Actors with Highest Difference in Average Ratings Between Two Genres")
    col1, col2 = st.columns(2)
    with col1:
        genre1 = st.selectbox("Select First Genre", options=genre_list, index=genre_list.index("drama"))
    with col2:
        genre2 = st.selectbox("Select Second Genre", options=[g for g in genre_list if g != genre1],
                                index=genre_list.index("comedy") - 1)
    if genre1 and genre2:
        data = AnalyticsService.get_highest_rating_diff_actors_between_2_genres(genre1=genre1, genre2=genre2)
        if "error" not in data and data:
            df = pd.DataFrame(data)
            plot_bar_chart(df, x="actor_name", y="rating_difference", title=f"Rating Difference Between {genre1.capitalize()} and {genre2.capitalize()}",
                            labels={"actor_name": "Actor", "rating_difference": "Rating Difference"}, color_scheme="Blues")
    
# Main Dashboard Layout
def render_analytics_dashboard():
    
    tab1, tab2, tab3 = st.tabs([ 
        "🎬 Movie Insights",
        "🎥 Director Insights",
        "🎭 Actor Insights"
    ])
    
    with tab1:
       render_tab_movie_insights()
    
    with tab2: 
       render_tab_director_insights()

    with tab3:
       render_tab_actor_insights()