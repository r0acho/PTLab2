from .settings import *

DATABASES['default']['ENGINE'] = 'django.db.backends.postgresql'
DATABASES['default']['NAME'] = ':memory:'
TEST_DATABASE_PREFIX = 'test_'
