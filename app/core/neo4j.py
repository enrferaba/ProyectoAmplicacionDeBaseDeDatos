from functools import lru_cache
from typing import Any, Dict, Iterable

from django.conf import settings
from neo4j import GraphDatabase


@lru_cache(maxsize=1)
def get_driver():
    return GraphDatabase.driver(
        settings.NEO4J_URI,
        auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
    )


def run_query(query: str, parameters: Dict[str, Any] | None = None) -> Iterable[Dict[str, Any]]:
    with get_driver().session() as session:
        result = session.run(query, parameters or {})
        for record in result:
            yield record.data()
