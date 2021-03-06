from memoized import memoized

from corehq.pillows.cacheinvalidate import CacheInvalidateProcessor


@memoized
def _get_cache_processor():
    return CacheInvalidateProcessor()


def invalidate_document(document, deleted=False):
    """
    Invalidates a document in the cached_core caching framework.
    """
    _get_cache_processor().process_doc(document.to_json(), deleted)
