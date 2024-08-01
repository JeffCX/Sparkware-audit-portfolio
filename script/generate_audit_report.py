import requests
import datetime
import os

GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_KEY_CTF_SEC")  # Save your GitHub Token in an environment variable
HEADERS = {'Authorization': 'token ' + GITHUB_TOKEN}

report_name = "GMX_Audit_Report"
REPO_OWNER = 'ctf-sec'
REPO_NAME = '2023-04-gmx-shadow-force-auditing'

def get_issues(repo_owner, repo_name):
    url = f'https://api.github.com/repos/{repo_owner}/{repo_name}/issues'
    issues = requests.get(url, headers=HEADERS).json()
    return issues

def generate_report(report_name, issues):
    report = f'# Audit Report - {report_name}\n\n'
    report += '|             |                                                                           |\n'
    report += '| ----------- | ------------------------------------------------------------------------- |\n'
    report += f'| **Date**    | {datetime.datetime.now().strftime("%B %Y")}                                                          |\n'
    report += '| **Auditor** | xxxxx                          |\n'
    report += '| **Status**  | **Final**                                                                 |\n\n'
    report += '## Findings\n\n'
    count = 1

    for issue in issues:
        for label in issue['labels']:
            if label['name'].lower() in ['critical', 'high', 'medium', 'low']:
                report += f'### {label["name"].capitalize()} - {count}. {issue["title"]}\n\n'
                report += f'**Link:** [{issue["html_url"]}]({issue["html_url"]})\n\n'
                report += issue["body"].replace("\n", "")
                count += 1

    now = datetime.datetime.now()
    with open(f'{now.strftime("%Y_%m")}_{report_name}.md', 'w') as f:
        f.write(report)

issues = get_issues(REPO_OWNER, REPO_NAME)
generate_report(report_name, issues)
