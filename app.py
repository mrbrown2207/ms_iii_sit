from ms_iii_sit import create_app
from . constants import ISSUE_STATUS

app = create_app()

# Set up some utility contexts
#ctx = utility_contexts()

#@current_app.context_processor
@app.context_processor
def utility_contexts():
    def issue_not_viewed(status):
        return (status == ISSUE_STATUS.get('notviewed'))

    def issue_viewed(status):
        return (status == ISSUE_STATUS.get('viewed'))

    def issue_resolved(status):
        return (status == ISSUE_STATUS.get('resolved'))

    def notviewed():
        return ISSUE_STATUS.get('notviewed')

    def viewed():
        return ISSUE_STATUS.get('viewed')

    def resolved():
        return ISSUE_STATUS.get('resolved')

    def testing():
        return app.config.get('TESTING')

    return dict(issue_viewed=issue_viewed,
                issue_not_viewed=issue_not_viewed,
                issue_resolved=issue_resolved,
                notviewed=notviewed,
                viewed=viewed,
                resolved=resolved,
                testing=testing)

if __name__ == '__main__':
    app.run(debug=True)
