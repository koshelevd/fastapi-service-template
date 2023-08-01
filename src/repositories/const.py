from enum import Enum

from sqlalchemy import asc as sa_asc
from sqlalchemy import desc as sa_desc


class SortingType(Enum):
    asc = sa_asc
    desc = sa_desc
