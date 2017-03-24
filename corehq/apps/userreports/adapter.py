from __future__ import absolute_import
from dimagi.utils.decorators.memoized import memoized
from dimagi.utils.logging import notify_exception
from corehq.util.test_utils import unit_testing_only


class IndicatorAdapter(object):

    def __init__(self, config):
        self.config = config

    @memoized
    def get_table(self):
        raise NotImplementedError

    def rebuild_table(self):
        raise NotImplementedError

    def drop_table(self):
        raise NotImplementedError

    def refresh_table(self):
        raise NotImplementedError

    @unit_testing_only
    def clear_table(self):
        raise NotImplementedError

    def get_query_object(self):
        raise NotImplementedError

    def best_effort_save(self, doc):
        """
        Does a best-effort save of the document. Will fail silently if the save is not successful.

        For certain known, expected errors this will do no additional logging.
        For unexpected errors it will log them.
        """
        try:
            indicator_rows = self.get_all_values(doc)
        except Exception as e:
            self.handle_exception(doc, e)
        else:
            self.best_effort_save_rows(indicator_rows, doc)

    def best_effort_save_rows(self, rows, doc):
        """
        Like save_rows, but catches errors
        """
        raise NotImplementedError

    def handle_exception(self, doc, exception):
        notify_exception(
            None,
            u'unexpected error saving UCR doc: {}'.format(exception),
            details={
                'domain': self.config.domain,
                'doc_id': doc.get('_id', '<unknown>'),
                'table': '{} ({})'.format(self.config.display_name, self.config._id)
            }
        )

    def save(self, doc):
        """
        Saves the document. Should bubble up known errors.
        """
        indicator_rows = self.get_all_values(doc)
        self.save_rows(indicator_rows, doc)

    def get_all_values(self, doc):
        "Gets all the values from a document to save"
        return self.config.get_all_values(doc)

    def save_rows(self, rows, doc):
        "Saves rows to a data source"
        raise NotImplementedError

    def delete(self, doc):
        raise NotImplementedError

    @property
    def run_asynchronous(self):
        return self.config.asynchronous
