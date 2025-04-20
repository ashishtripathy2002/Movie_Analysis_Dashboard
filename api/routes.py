from flask_restful import Api

from actors.actor_resource import ActorsHighestAvgVoteResource, ActorsGenreRatingDifferenceResource, \
    ActorsHighRatedAppearancesResource
from actors.actor_service import ActorService
from actors.auth_repository import ActorRepository
from auth.auth_resource import RegisterResource, LoginResource
from auth.auth_service import AuthService
from database import PostgresqlDB
from directors.director_repository import DirectorRepository
from directors.director_resource import TopGrossingDirectorsResource, TopDirectorsResource, \
    DirectorActorCollaborationResource
from directors.director_service import DirectorService
from genres.genre_repository import GenreRepository
from genres.genre_resource import GenrePopularityRevenueCorrelationResource, GenreProfitableMoviesResource, \
    GenreResource, GenreProfitMarginResource
from genres.genre_service import GenreService
from keywords.keywords_repository import KeywordsRepository
from keywords.keywords_resource import KeywordsResource
from keywords.keywords_service import KeywordsService
from movies.SummaryStatisticsResource import SummaryStatisticsResource
from movies.movie_repository import MovieRepository
from movies.movie_resource import MovieResource, TopRatedMoviesByYearResource
from movies.movie_service import MovieService
from production_companies.company_repository import ProductionCompanyRepository
from production_companies.company_resource import TopProductionCompaniesResource
from production_companies.company_service import ProductionCompanyService
from user.user_repository import UserRepository


class Routes:
    def __init__(self, app):
        # Initialize the API
        api = Api(app)

        # Initialize PostgresqlDB instance
        db_instance = PostgresqlDB(
            user_name=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            db_name=app.config['DB_NAME']
        )

        # Initialize repositories
        user_repository = UserRepository(db_instance)
        movie_repository = MovieRepository(db_instance)

        user_service = AuthService(user_repository)
        movie_service = MovieService(movie_repository)

        director_repository = DirectorRepository(db_instance)
        director_service = DirectorService(director_repository)

        genre_repository = GenreRepository(db_instance)
        genre_service = GenreService(genre_repository)

        production_company_repository = ProductionCompanyRepository(db_instance)
        production_company_service = ProductionCompanyService(production_company_repository)

        # Register resources with dependencies
        api.add_resource(RegisterResource, '/auth/register', resource_class_kwargs={'user_service': user_service})
        api.add_resource(LoginResource, '/auth/login', resource_class_kwargs={'user_service': user_service})

        api.add_resource(TopDirectorsResource, '/directors',
                         resource_class_kwargs={'director_service': director_service})
        api.add_resource(TopGrossingDirectorsResource, '/directors/top_grossing',
                         resource_class_kwargs={'director_service': director_service})
        api.add_resource(DirectorActorCollaborationResource, '/directors/collaborations',
                         resource_class_kwargs={'director_service': director_service})
        # Register movie resources

        api.add_resource(MovieResource, '/movies','/movies/<int:movie_id>',
                         resource_class_kwargs={'movie_service': movie_service})
        api.add_resource(TopRatedMoviesByYearResource, '/movies/top_rated_by_year',
                         resource_class_kwargs={'movie_service': movie_service})

        # Return app with routes registered
        actor_repository = ActorRepository(db_instance)
        actor_service = ActorService(actor_repository)
        # Register the actor-related resources
        api.add_resource(  ActorsHighestAvgVoteResource,'/actors',
            resource_class_kwargs={'actor_service': actor_service}
        )
        api.add_resource(ActorsGenreRatingDifferenceResource, '/actors/genre_rating_difference',
            resource_class_kwargs={'actor_service': actor_service}
        )
        api.add_resource( ActorsHighRatedAppearancesResource,'/actors/high_rated_appearances',
            resource_class_kwargs={'actor_service': actor_service}
        )

       ##GENRE RESOURCES
        # Register resources with dependencies
        api.add_resource(GenreResource, '/genres',
                         resource_class_kwargs={'genre_service': genre_service}
                         )
        api.add_resource(GenrePopularityRevenueCorrelationResource,'/genres/popularity_revenue_correlation',
            resource_class_kwargs={'genre_service': genre_service}
        )
        api.add_resource(GenreProfitableMoviesResource,'/genres/profitable_movies',
            resource_class_kwargs={'genre_service': genre_service}
        )
        api.add_resource(GenreProfitMarginResource, '/genres/profit_margin',
                         resource_class_kwargs={'genre_service': genre_service})

        #PRODUCTION COMPANIES
        api.add_resource(TopProductionCompaniesResource,'/production_companies',
            resource_class_kwargs={'production_company_service': production_company_service}
        )

        keywords_repository = KeywordsRepository(db_instance)
        keywords_service = KeywordsService(keywords_repository)
        api.add_resource(KeywordsResource, '/keywords',
                         resource_class_kwargs={'keywords_service': keywords_service}
                         )
        api.add_resource(SummaryStatisticsResource, '/summary',
                         resource_class_kwargs={'movie_service': movie_service})
        self.app = app
    def get_app(self):
        return self.app