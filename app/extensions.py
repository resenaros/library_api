from flask_caching import Cache
from flask_limiter import Limiter
from flask_marshmallow import Marshmallow 
from flask_limiter.util import get_remote_address

ma = Marshmallow()
limiter=Limiter(key_func=get_remote_address) # creating an instance of Limiter
cache=Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300}) # creating an instance of Cache