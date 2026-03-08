from Engines import cache
from fastapi import Request, HTTPException, status

redis_client= cache.redis_client

X= "FIXED WINDOW ALGORITHM"

def fixed_window_rate_limit(key: str,limit: int,window: int):
    current = redis_client.get(key)

    if current is None:
        redis_client.setex(key, window, 1)
        return True

    if int(current) >= limit:
        return False

    redis_client.incr(key)
    return True

def get_client_ip(request: Request):
    
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"

def rate_limit(request: Request,key_prefix: str,limit: int,window: int):
    ip = get_client_ip(request)
    key = f"rate:{key_prefix}:ip:{ip}"

    allowed = fixed_window_rate_limit(key, limit, window)

    if not allowed:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS,detail="Too many requests")
    
def rate_limit_user_and_ip(request: Request, user_id: int):
    ip = get_client_ip(request)

    key_user = f"rate:user:{user_id}"
    key_ip = f"rate:ip:{ip}"

    if not fixed_window_rate_limit(key_user, 10, 60):
        raise HTTPException(429, "Too many requests (user)")

    if not fixed_window_rate_limit(key_ip, 30, 60):
        raise HTTPException(429, "Too many requests (ip)")
    
def rate_limit_user(user_id, key_prefix, limit, window):
    key = f"rate:{key_prefix}:user:{user_id}"

    allowed = fixed_window_rate_limit(key, limit, window)

    if not allowed:
        raise HTTPException(status_code=429,detail="Rate limit exceeded") 
    
# =====================================================================================================

X= "SLIDING WINDOW ALGORITHM"

import time
import uuid
from fastapi import HTTPException, status

def sliding_window_rate_limit(key: str, limit: int, window: int):
    now = time.time()
    window_start = now - window

    # Remove old requests
    redis_client.zremrangebyscore(key, 0, window_start)

    # Count current requests in window
    current_count = redis_client.zcard(key)

    if current_count >= limit:
        return False

    # Add new request
    redis_client.zadd(key, {str(uuid.uuid4()): now})

    # Set expiry so Redis auto-cleans key
    redis_client.expire(key, window)

    return True

def rate_limit_sliding(request: Request, key_prefix: str, limit: int, window: int):
    ip = get_client_ip(request)
    key = f"rate:{key_prefix}:ip:{ip}"

    allowed = sliding_window_rate_limit(key, limit, window)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )

# =====================================================================================================

X= "TOKEN BUCKET ALGORITHM"

import time

def token_bucket_rate_limit(key: str, capacity: int, refill_rate: float):
    now = time.time()

    bucket = redis_client.hgetall(key)

    if not bucket:
        tokens = capacity
        last_refill = now
    else:
        tokens = float(bucket["tokens"])
        last_refill = float(bucket["last_refill"])

    time_passed = now - last_refill
    tokens += time_passed * refill_rate

    tokens = min(capacity, tokens)

    if tokens < 1:
        return False

    tokens -= 1

    redis_client.hset(key, mapping={
        "tokens": tokens,
        "last_refill": now
    })

    redis_client.expire(key, 60)

    return True

from fastapi import Request, HTTPException, status

def token_bucket_limit(request: Request, key_prefix: str, capacity: int, refill_rate: float):

    ip = request.client.host
    key = f"rate:{key_prefix}:ip:{ip}"

    allowed = token_bucket_rate_limit(key, capacity, refill_rate)

    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests"
        )
    


    
