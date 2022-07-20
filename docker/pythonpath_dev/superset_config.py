# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#
import logging
import os
from datetime import timedelta
from typing import Optional
from superset.superset_typing import CacheConfig
from cachelib.file import FileSystemCache
from celery.schedules import crontab


logger = logging.getLogger()
def get_env_variable(var_name: str, default: Optional[str] = None) -> str:
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)
SESSION_COOKIE_SAMESITE = "Lax"

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI", 'postgres://superset:superset@localhost:5432/superset')
DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
DATABASE_USER = get_env_variable("DATABASE_USER")
DATABASE_PASSWORD = get_env_variable("DATABASE_PASSWORD")
DATABASE_HOST = get_env_variable("DATABASE_HOST")
DATABASE_PORT = get_env_variable("DATABASE_PORT")
DATABASE_DB = get_env_variable("DATABASE_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%s/%s" % (
    DATABASE_DIALECT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_DB,
)

CACHE_REDIS_URL = os.environ.get("CACHE_REDIS_URL", "redis://redis:6379/0")
# Default cache for Superset objects
CACHE_CONFIG: CacheConfig = {
        "CACHE_TYPE": "redis",
        "CACHE_REDIS_PORT": "6379",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_KEY_PREFIX":"superset_13",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}

# Cache for datasource metadata and query results
DATA_CACHE_CONFIG: CacheConfig = {
        "CACHE_TYPE": "redis",
        "CACHE_DEFAULT_TIMEOUT": 3600,
        "CACHE_REDIS_PORT": "6379",
        "CACHE_KEY_PREFIX":"superset_13_data",
        "CACHE_REDIS_URL": CACHE_REDIS_URL
}
WTF_CSRF_ENABLED = False

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://0.0.0.0:8088/"
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

SQLLAB_CTAS_NO_LIMIT = True
LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}
