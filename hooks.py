from datetime import datetime

from humanize import naturaldelta

##
# Defined hook classes for framework independent integrations.
# At the moment only supports Django, but implementers can substitute
# their own mixins for different use cases.
##


class BaseHookMixin:
    """
    Base mixin supporting two break out methods for montiroing code execution
    within the selected context. Can be overridden depending on hook to provide
    enhanced functionality.
    """
    started = None
    time_take = None

    def enter_section_hook(self):
        self.started = datetime.now()
        return

    def exit_section_hook(self, default_kwargs):
        self.time_taken = naturaldelta(datetime.now() - self.started)

        default_kwargs['title'] = (
            f'Excecuted context in {self.time_taken}.'
        )

        return default_kwargs

##
# Set django as default hook if available.
# Use a basic generic mixin if not.
##


try:
    from django import db

    class DjangoHookMixin(BaseHookMixin):
        """
        Django specific hook, enhances the end flame graph with an output of
        total database queries.
        """

        def enter_section_hook(self):
            super().enter_section_hook()
            db.reset_queries()

        def exit_section_hook(self, default_kwargs):
            super().exit_section_hook(default_kwargs)
            num_sql_queries = len(db.connection.queries)

            default_kwargs['title'] = (
                f'Executed context in {self.time_taken}. '
                f'Made {num_sql_queries} SQL queries.'
            )

            return default_kwargs

    SetHookMixin = DjangoHookMixin

except ImportError:
    SetHookMixin = BaseHookMixin
