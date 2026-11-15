#!/bin/sh
set -e

echo "[entrypoint] waiting for database..."
until python - <<'PY'
import os, sys, psycopg
url = os.environ["DATABASE_URL"].replace("+psycopg", "")
try:
    psycopg.connect(url).close()
except Exception as e:
    print(f"  db not ready: {e}", file=sys.stderr)
    sys.exit(1)
PY
do
    sleep 1
done
echo "[entrypoint] database is up"

echo "[entrypoint] running migrations..."
alembic upgrade head

echo "[entrypoint] starting app: $*"
exec "$@"