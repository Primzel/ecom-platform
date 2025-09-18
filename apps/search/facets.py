from oscar.apps.search.facets import *


def base_sqs():
    """
    Return the base SearchQuerySet for Haystack searches.
    """
    sqs = SearchQuerySet()
    for facet in settings.OSCAR_SEARCH_FACETS["fields"].values():
        options = facet.get("options", {})
        sqs = sqs.facet(facet["field"], **options)
    for facet in settings.OSCAR_SEARCH_FACETS["queries"].values():
        for query in facet["queries"]:
            sqs = sqs.query_facet(facet["field"], query[1])

    sqs = sqs.all()
    return sqs

