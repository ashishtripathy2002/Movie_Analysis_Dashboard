import pandas as pd
from datetime import datetime
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import psycopg2
from services.metadata_service import MetadataService
from services.movie_service import MovieService

def conn_db():
    connection_params = {
        'dbname': 'movie_analysis_db',
        'user': 'postgres',
        'password': '123456',
        'host': 'localhost', 
        'port': '5432'}
    try:
        conn = psycopg2.connect(**connection_params)
        # print("Database connection successful!")
        return conn.cursor(), conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")

def fetch_mapping(col_nm):
    cur, conn = conn_db()
    cur.execute(f"SELECT * FROM {col_nm};")
    rows = cur.fetchall()
    map_dict = {row[1]: row[0] for row in rows}
    return map_dict

def movie_mgmt():
    # st.title("Manage Movie Info")
    # User login check
    # st.success(f'Welcome, {st.session_state["current_user"].get("role") == "admin"}!')
    # For navigation between pages
    if st.session_state["current_user"].get("role") == "admin":
        page = st.radio('Select Page', ['View Movies', 'Add/Update/Delete Movies'],horizontal=True)
    else:
        page = 'View Movies'

    if page == 'View Movies':
        st.header('Movies List')
        movies_data = MovieService.get_all_movies(per_page=0)
        movies_df = pd.DataFrame(movies_data['movies']) #pd.read_csv('movies.csv')
        search_term = st.text_input('Search Movies:', '')
        filtered_movies = movies_df[movies_df['title'].str.contains(search_term, case=False, na=False)]
        st.dataframe(filtered_movies)

    elif page == 'Add/Update/Delete Movies':
        st.header('Add, Update or Delete Movies')
        action = st.radio('Select Action', ['Insert', 'Update', 'Delete'],horizontal=True)
        movies_data = MovieService.get_all_movies(per_page=0)
        movies_df = pd.DataFrame(movies_data['movies'])
        if action == 'Update':
            st.subheader('Update Movie Information')
            
            search_id = st.number_input('Enter Movie ID:', 0 )
            if search_id!=0:
                try:
                    movie = movies_df[movies_df['movie_id'] == search_id].iloc[0]
                    movie_nm = movie['title']
                    #to update movie info
                    st.write(f"Selected Movie: {movie_nm}")
                    st.write('Cast: ', ", ".join(movie['actors']))
                    st.write('Directors: ', ", ".join(movie['directors']))
                    updated_runtime = st.number_input('Runtime', value=movie['runtime'])
                    updated_overview = st.text_input('Overview',value= movie['overview'])
                    updated_tagline = st.text_input('Tagline',value= movie['tagline'])
                    updated_budget = st.number_input('Budget', value=movie['budget'])
                    updated_revenue = st.number_input('Revenue', value=movie['revenue'])
                    data = {'runtime':updated_runtime,'overview':updated_overview,'tagline':updated_tagline,'budget':updated_budget,'revenue':updated_revenue}
                    # Button to save changes
                    if st.button('Save Changes'):
                        movies_df.loc[movies_df['movie_id'] == search_id, 'runtime'] = updated_runtime
                        movies_df.loc[movies_df['movie_id'] == search_id, 'overview'] = updated_overview
                        movies_df.loc[movies_df['movie_id'] == search_id, 'tagline'] = updated_tagline
                        movies_df.loc[movies_df['movie_id'] == search_id, 'budget'] = updated_budget
                        movies_df.loc[movies_df['movie_id'] == search_id, 'revenue'] = updated_revenue
                        response = MovieService.update_movie(search_id, data)
                        if "error" in response:
                            if response.get("status_code") == 404:
                                st.error(f"Error: Movie not found. Please check the movie ID.")
                            else:
                                st.error(f"Error updating movie: {response['error']}")
                    else:
                        st.toast("Movie updated successfully!")
                except Exception as e:
                    print("Enter correct movie id", e)
            

        elif action == 'Delete':
            st.subheader('Delete Movie')
            search_id = st.number_input('Enter Movie ID:', 0 )
            if search_id!=0:
                try:
                    movie = movies_df[movies_df['movie_id'] == search_id].iloc[0]
                    movie_nm = movie['title']
                    # Form to update movie info
                    st.write(f"Selected Movie: {movie_nm}")
                    if st.button('Delete Movie'):
                        # movies_df = movies_df[movies_df['id'] != movie_id]
                        response = MovieService.delete_movie(search_id)
                        movies_df = movies_df[movies_df['movie_id'] != search_id]
                        st.toast("Record deleted Successfully")
                except:
                    print("Enter correct movie id")
                    
        elif action == 'Insert':
            st.subheader('Add New Movie')
            st.write(f"New Movie id: {movies_df['movie_id'].max() + 1}")
            new_title = st.text_input('Original Title')
            dir_dict = fetch_mapping('directors')
            dir_list = list(dir_dict.keys())
            new_director = st.multiselect("Select Directors to add", options=dir_list, default=[])
            act_dict = fetch_mapping('actors')
            act_list = list(act_dict.keys())
            new_cast = st.multiselect("Select Actors to add", options=act_list, default=[])
            # new_cast = st.text_input('Cast')
            # genre_list = [genre['genre_name'] for genre in MetadataService.fetch_genres()] 
            genre_dict = fetch_mapping('genres')
            genre_list = list(genre_dict.keys())
            new_genres = st.multiselect("Select Genres to add", options=genre_list, default=[])
            new_runtime = st.number_input('Runtime',min_value=0)
            new_overview = st.text_area('Overview')
            new_budget = st.number_input('Budget',min_value=0)
            new_revenue = st.number_input('Revenue',min_value=0)
            new_release_date = st.date_input('Release Date', min_value=datetime(1900, 1, 1))
            new_rel_yr = new_release_date.year
            new_vote_cnt = st.number_input('Vote Count',min_value=0)
            new_vote_avg = st.number_input('Vote Average',format="%.2f")

            if st.button('Add New Movie'):
                if not new_title.strip():
                    st.warning("Title cannot be empty.")
                elif new_genres ==[]:
                    st.warning("Genre cannot be empty.")
                elif new_cast ==[]:
                    st.warning("Actors cannot be empty.")
                else:
                    new_movie = {
                        'movie_id': movies_df['movie_id'].max() + 1,  # Assign new id
                        'title': new_title,
                        'directors': new_director,
                        'actors': new_cast,
                        'genres': new_genres,
                        'runtime': new_runtime,
                        'overview': new_overview,
                        'release_date': new_release_date,
                        'budget': new_budget, 
                        'revenue': new_revenue, 
                        'release_year': new_rel_yr, 
                        'vote_count': new_vote_cnt, 
                        'vote_average': new_vote_avg
                    }
                    df =  pd.DataFrame([new_movie])
                    cmd_list = []
                    for index, row in df.iterrows():
                        cmd_list.append(f"""INSERT INTO movies (movie_id, popularity, budget, revenue, original_title, homepage, tagline, overview, runtime, release_date, vote_count, vote_average, release_year,budget_adj, revenue_adj) VALUES ({row['movie_id']}, {0},{row['budget']}, {row['revenue']}, '{row['title']}', '{''}', '{''}','{row['overview']}', {row['runtime']}, {row['release_date']}, {row['vote_count']}, {row['vote_average']}, {row['release_year']},{0}, {0}); """)
                    df1 = df.explode('actors')
                    for index, row in df1[['movie_id','actors']].iterrows():
                        a_id = act_dict[row['actors'].lower()]
                        cmd_list.append(f"insert into movie_actor values ({row['movie_id']}, {a_id});")

                    df1 = df.explode('genres')
                    df1[['movie_id','genres']]
                    for index, row in df1[['movie_id','genres']].iterrows():
                        g_id = genre_dict[row['genres'].lower()]
                        cmd_list.append(f"insert into movie_genre values ({row['movie_id']}, {g_id});")
                    
                    df1 = df.explode('directors')
                    df1[['movie_id','directors']]
                    for index, row in df1[['movie_id','directors']].iterrows():
                        d_id = dir_dict[row['directors'].lower()]
                        cmd_list.append(f"insert into movie_director values ({row['movie_id']}, {d_id});")
                    st.write(cmd_list)
                    for cmd in cmd_list:
                        cur, conn = conn_db()
                        cur.execute(cmd)
                        conn.commit()  
                    st.success(f'New movie "{new_title}" added successfully!')
