from api.authentication import router as router_auth
from api.users import router as router_users
from api.todos import router as router_todos

all_routers = [
    router_auth,
    router_users,
    router_todos
]
