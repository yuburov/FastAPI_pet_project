from src.api.authentication import router as router_auth
from src.api.users import router as router_users

all_routers = [
    router_auth,
    router_users
]
