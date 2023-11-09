from .settings import *

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
DATABASES['default']['NAME'] = 'test_mydatabase'
TEST_DATABASE_PREFIX = 'test_'
