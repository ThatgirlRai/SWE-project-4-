# urls.py

from django.urls import path
from .views import (
    CreateGameBySizeView,
    GameListView,
    GameDetailView,
    GameLeaderBoardView,
)

urlpatterns = [
    # Create a new game by grid size
    # Example: GET /game/4
    path("game/<int:size>/", CreateGameBySizeView.as_view(), name="create-game-by-size"),

    # List all games
    # Example: GET /games
    path("games/", GameListView.as_view(), name="game-list"),

    # Retrieve a specific game by UUID
    # Example: GET /games/550e8400-e29b-41d4-a716-446655440000
    path("games/<uuid:id>/", GameDetailView.as_view(), name="game-detail"),

    # Retrieve or submit leaderboard entries
    # Example:
    # GET  /games/{uuid}/leaderboard
    # POST /games/{uuid}/leaderboard
    path(
        "games/<uuid:id>/leaderboard/",
        GameLeaderBoardView.as_view(),
        name="game-leaderboard",
    ),
]