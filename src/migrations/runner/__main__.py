import sys

from migrations.runner.composite import alembic_runner

alembic_runner(*sys.argv[1:])
