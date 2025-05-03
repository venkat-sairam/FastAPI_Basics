from datetime import datetime, timezone

def get_hour_key(user_id: str) -> str:
    current_hour = datetime.now(timezone.utc).strftime("%Y%m%d%H")
    return f"usage:{user_id}:hour:{current_hour}"

def get_day_key(user_id: str) -> str:
    current_day = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"usage:{user_id}:day:{current_day}"

def get_block_key(user_id: str) -> str:
    return f"blocked:{user_id}"

def get_role_limit_key(role: str) -> str:
    return f"limits:{role}"
