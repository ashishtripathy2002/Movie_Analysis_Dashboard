
class ProductionCompanyService:
    def __init__(self, production_company_repository):
        self.production_company_repository = production_company_repository

    def get_top_production_companies(self, limit,start_year, end_year, genres=None, year=None):
        # Pass genres and year filters to the repository method
        return self.production_company_repository.get_top_production_companies_by_revenue(
            limit=limit, start_year=start_year, 
            end_year=end_year,  genres=genres
        )
