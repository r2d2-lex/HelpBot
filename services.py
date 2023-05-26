from dataclasses import dataclass


@dataclass()
class UserState:
    user_id: int
    search_context: any or None
    search_continue: bool


users_context = dict()
