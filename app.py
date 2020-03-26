from ms_iii_sit import create_app
from flask_login import current_user
from . constants import ISSUE_STATUS, USER_LEVEL

app = create_app()

# Set up some utility contexts
#ctx = utility_contexts()

#@current_app.context_processor  <- Couldn't get that to work and got impatient. And yes, I imported current_app ˘L˘
@app.context_processor
def utility_contexts():
    def issue_not_viewed(status):
        return (status == ISSUE_STATUS['notviewed']['id'])

    def issue_viewed(status):
        return (status == ISSUE_STATUS['viewed']['id'])

    def issue_resolved(status):
        return (status == ISSUE_STATUS['resolved']['id'])

    def notviewed():
        return ISSUE_STATUS['notviewed']['id']

    def viewed():
        return ISSUE_STATUS['viewed']['id']

    def resolved():
        return ISSUE_STATUS['resolved']['id']

    def testing():
        return app.config.get('TESTING')

    def is_superuser():
        return current_user.is_superuser()

    return dict(issue_viewed=issue_viewed,
                issue_not_viewed=issue_not_viewed,
                issue_resolved=issue_resolved,
                notviewed=notviewed,
                viewed=viewed,
                resolved=resolved,
                testing=testing,
                is_superuser=is_superuser)

if __name__ == '__main__':
    app.run(debug=True)
