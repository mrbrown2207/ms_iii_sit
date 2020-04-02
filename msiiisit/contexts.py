from flask import current_app
from . constants import ISSUE_STATUS

#@current_app.context_processor
def utility_contexts():
    print("Ok, got here")
    """
    def issue_is_entered(status):
        return (status == ISSUE_STATUS.get('entered'))

    def issue_is_viewed(status):
        return (status == ISSUE_STATUS.get('viewed'))

    def issue_is_resolved(status):
        return (status == ISSUE_STATUS.get('resolved'))

    return dict(issue_is_entered=issue_is_entered,
                issue_is_viewed=issue_is_viewed,
                issue_is_resolved=issue_is_resolved)
    """
    return True
