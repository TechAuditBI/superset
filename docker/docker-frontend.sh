#!/usr/bin/env bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
set -e
cd ./app/
npm install -g po2json
./scripts/po2json.sh

cd ./superset-frontend
npm install -g npm@7
# Packages needed for puppeteer:
apt update
apt install -y chromium

npm install -f --no-optional --global webpack webpack-cli
npm install -f --no-optional

echo "Running frontend"

if [ "$SUPERSET_ENV" == "production" ]; then
    npm run docker-server
else 
    npm run docker-server-dev
fi

