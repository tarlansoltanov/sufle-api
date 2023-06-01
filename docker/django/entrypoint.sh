#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate --noinput

# Compile translations if any
if [ -d "locale" ]; then
    echo "Compile translations"
    python manage.py compilemessages
fi

exec $cmd