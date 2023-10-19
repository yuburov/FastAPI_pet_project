from src.api.authentication import router as router_auth
from src.api.users import router as router_users
from src.api.todos import router as router_todos

all_routers = [
    router_auth,
    router_users,
    router_todos
]
