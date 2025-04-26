from app.domain.interfaces.RatingServiceProtocol import RatingServiceProtocol

# héritage de RatingServiceProtocol qui est l'interface
class RatingService:
    def __init__(self, rating_repository: RatingServiceProtocol):
        self.rating_repository = rating_repository


    def sort_users_category_by_rating(self, category: str):
        # recuperation des utilisateurs par categorie
        users = self.rating_repository.get_users_by_category(category)
        # tri des utilisateurs par note
        return sorted(users, key=lambda user: user.note, reverse=True)
