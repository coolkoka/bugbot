from os import environ
from jira import JIRA


class Jira:
    auth_jira = None
    project = None
    url = None

    def __init__(self):
        self.url = environ.get('JIRA_URL')
        self.auth_jira = JIRA({'server': self.url},
                              basic_auth=(
                                  environ.get('JIRA_LOGIN'),
                                  environ.get('JIRA_PASSWORD'))
                              )
        self.project = environ.get('JIRA_PROJECT')
        self.jira_users = {
            '@lexx_v': 'Lexx',
            '@rainbowdash593': 'rainbowdash593',
            '@seniyaeclair': 'Kosheleva.yuliya.mmf',
            '@nezzl': 'Nezzl'
        }

    def search_issues_by_description(self, search):
        issues = self.auth_jira.search_issues('project = {project} AND description ~ {search}'.format(
            project=self.project,
            search=search
        ))
        return list(self._generate_url_to_issue(issue) for issue in issues)

    def create_issue(self, summary, responsible_user, description=''):
        issue = self.auth_jira.create_issue(project=self.project,
                                            summary=summary,
                                            description=description,
                                            issuetype={'name': 'Баг из телеги'})
        if responsible_user in self.jira_users:
            self.auth_jira.assign_issue(issue.key, self.jira_users[responsible_user])
        return self._generate_url_to_issue(issue)

    def _generate_url_to_issue(self, issue):
        return self.url + '/browse/' + issue.key
