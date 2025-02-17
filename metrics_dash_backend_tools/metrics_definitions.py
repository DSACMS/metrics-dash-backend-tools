"""
Definitions of specific metrics for metricsLib
"""
from .metrics_data_structures import CustomMetric, parse_commits_by_month, RangeMetric
from .metrics_data_structures import GraphQLMetric, LengthMetric, ResourceMetric, BaseMetric
from .metrics_data_structures import ListMetric, parse_nadia_label_into_badge
from .metrics_data_structures import BaseMetric, LanguageMetric
from .constants import TOKEN, AUGUR_HOST

# The general procedure is to execute all metrics against all repos and orgs

SIMPLE_METRICS = []

# Weekly, monthly metrics.
PERIODIC_METRICS = []

# Classification metrics
ADVANCED_METRICS = []

# Metrics gathered by org instead of by repo
ORG_METRICS = []

# Metrics that save a resource to a file
RESOURCE_METRICS = []

# Predominant Languages Endpoint (ex. https://api.github.com/repos/chaoss/augur/languages)
LANGUAGE_ENDPOINT = "https://api.github.com/repos/{owner}/{repo}/languages"

REPO_GITHUB_GRAPHQL_QUERY = """
query ($repo: String!, $owner: String!) {
  repository(name: $repo, owner: $owner) {
    description,
    forkCount,
    forkingAllowed,
    stargazerCount,
    createdAt,
    
    pullRequests(first: 1)
    {
      totalCount
    },
    mergedPullRequests: pullRequests(first: 1, states: MERGED)
    {
      totalCount
    },
    closedPullRequests: pullRequests(first: 1, states: CLOSED)
    {
      totalCount
    },
    openPullRequests: pullRequests(first: 1, states: OPEN)
    {
      totalCount
    },
    issues(first: 1)
    {
      totalCount
    },
    openIssues: issues(first: 1, states: OPEN)
    {
      totalCount
    },
    closedIssues: issues(first: 1, states: CLOSED)
    {
      totalCount
    },
    watchers(first: 1)
    {
      totalCount
    }
    defaultBranchRef
    {
      name,
      target
      {
        ... on Commit
        {
          history(first: 1)
          {
            totalCount
          }
          
        }
      }
    }
  }
}
"""


github_graphql_simple_counts_metric_map = {
    "description": ["data", "repository", "description"],
    "commits_count": ["data", "repository", "defaultBranchRef", "target", "history", "totalCount"],
    "issues_count": ["data", "repository", "issues", "totalCount"],
    "open_issues_count": ["data", "repository", "openIssues", "totalCount"],
    "closed_issues_count": ["data", "repository", "closedIssues", "totalCount"],
    "pull_requests_count": ["data", "repository", "pullRequests", "totalCount"],
    "open_pull_requests_count": ["data", "repository", "openPullRequests", "totalCount"],
    "merged_pull_requests_count": ["data", "repository", "mergedPullRequests", "totalCount"],
    "closed_pull_requests_count": ["data", "repository", "closedPullRequests", "totalCount"],
    "forks_count": ["data", "repository", "forkCount"],
    "stargazers_count": ["data", "repository", "stargazerCount"],
    "watchers_count": ["data", "repository", "watchers", "totalCount"],
    "created_at": ["data", "repository", "createdAt"]
}
SIMPLE_METRICS.append(GraphQLMetric("githubGraphqlSimpleCounts", ["repo", "owner"],
                                    REPO_GITHUB_GRAPHQL_QUERY,
                                    github_graphql_simple_counts_metric_map, token=TOKEN))

SIMPLE_METRICS.append(RangeMetric("totalRepoLines",["repo_id"], AUGUR_HOST +
                                 "/complexity/project_lines?repo_id={repo_id}",
                                 {"total_project_lines": ["total_lines"],
                                 "average_project_lines": ["average_lines"]}))

SIMPLE_METRICS.append(RangeMetric("totalRepoCommentLines",["repo_id"], AUGUR_HOST +
                                 "/complexity/project_comment_lines?repo_id={repo_id}",
                                 {"total_project_comment_lines": ["comment_lines"],
                                 "average_project_comment_lines": ["avg_comment_lines"]}))

SIMPLE_METRICS.append(RangeMetric("totalRepoBlankLines",["repo_id"], AUGUR_HOST +
                                 "/complexity/project_blank_lines?repo_id={repo_id}",
                                 {"total_project_blank_lines": ["blank_lines"],
                                 "average_blank_lines": ["avg_blank_lines"]}))

SIMPLE_METRICS.append(LanguageMetric("repositoryLanguages", 
                                     ["owner", "repo"], 
                                     LANGUAGE_ENDPOINT, 
                                     token=TOKEN))

SIMPLE_METRICS.append(GraphQLMetric("githubGraphqlSimpleCounts", ["repo", "owner"],
                                    REPO_GITHUB_GRAPHQL_QUERY,
                                    github_graphql_simple_counts_metric_map, token=TOKEN))

REPOMETRICS_ENDPOINT = "https://raw.githubusercontent.com/{owner}/{repo}/main/code.json"
repometrics_values = {"projectType": "projectType", "userInput": "userInput", "fismaLevel": "fismaLevel", 
                      "group": "group", "subsetInHealthcare": "subsetInHealthcare", "userType": "userType", 
                      "repositoryHost": "repositoryHost", "maturityModelTier": "maturityModelTier"}
SIMPLE_METRICS.append(BaseMetric("repometrics", ['owner', 'repo'], REPOMETRICS_ENDPOINT, repometrics_values, token=TOKEN))

ORG_METRICS.append(ListMetric("topCommitters", ["repo_group_id"],
                              AUGUR_HOST +
                              "/repo-groups/{repo_group_id}/top-committers",
                              {"top_committers": ["email", "commits"]}))

ORG_METRICS.append(ListMetric("orgLibyears", ["repo_group_id"],
                              AUGUR_HOST +
                              "/repo-groups/{repo_group_id}/libyear",
                              {"dependency_libyear_list": [
                                "repo_name", "name","libyear","most_recent_collection"
                                ]
                              }))


CONTRIBS_LABEL_LAST_MONTH = "new_commit_contributors_by_day_over_last_month"
PERIODIC_METRICS.append(ListMetric("newContributorsofCommitsWeekly",
                                   ["repo_id", "period", "begin_week", "end_date"],
                                   AUGUR_HOST + "/repos/{repo_id}" +
                                   "/pull-requests-merge-contributor-new" +
                                   "?period={period}&begin_date={begin_week}&end_date={end_date}",
                                   {
                                    CONTRIBS_LABEL_LAST_MONTH: ["commit_date", "count"]
                                    }))

sixMonthsParams = ["repo_id", "period", "begin_month", "end_date"]
LABEL = "new_commit_contributors_by_day_over_last_six_months"
PERIODIC_METRICS.append(ListMetric("newContributorsofCommitsMonthly", sixMonthsParams,
                                   AUGUR_HOST +
                                   "/repos/{repo_id}/pull-requests-merge-contributor-new" +
                                   "?period={period}&begin_date={begin_month}&end_date={end_date}",
                                   {LABEL: ["commit_date", "count"]}))

PERIODIC_METRICS.append(ListMetric("issuesNewWeekly", ["repo_id","period","begin_week","end_date"],
                                   AUGUR_HOST +
                                   "/repos/{repo_id}/issues-new" +
                                   "?period={period}&begin_date={begin_week}&end_date={end_date}",
                                   {"new_issues_by_day_over_last_month": ["date", "issues"]}))

PERIODIC_METRICS.append(ListMetric("issuesNewMonthly", sixMonthsParams,
                                   AUGUR_HOST +
                                   "/repos/{repo_id}/issues-new?" +
                                   "period={period}&begin_date={begin_month}&end_date={end_date}",
                                   {"new_issues_by_day_over_last_six_months": ["date", "issues"]}))

RESOURCE_METRICS.append(ResourceMetric("firstResponseForClosedPR", sixMonthsParams,
                                AUGUR_HOST + "/pull_request_reports/PR_time_to_first_response/" +
                                "?repo_id={repo_id}&start_date={begin_month}&end_date={end_date}"))

ORG_GITHUB_GRAPHQL_QUERY = """
query ($org_login: String!) {
  organization(login: $org_login) {
    createdAt,
    avatarUrl,
    description,
    email,
    isVerified,
    location,
    twitterUsername
    repositories(first: 1)
    {
      totalCount
    }
  }
}
"""
ORG_METRICS.append(GraphQLMetric("githubGraphqlOrgSimple", ["org_login"], ORG_GITHUB_GRAPHQL_QUERY,
                                 {"timestampCreatedAt": ["data", "organization", "createdAt"],
                                 "avatar_url": ["data", "organization", "avatarUrl"],
                                  "description": ["data", "organization", "description"],
                                  "email": ["data", "organization", "email"],
                                  "is_verified": ["data", "organization", "isVerified"],
                                  "location": ["data", "organization", "location"],
                                  "twitter_username": ["data", "organization", "twitterUsername"],
                                  "repo_count": ["data","organization","repositories","totalCount"]
                                  }, token=TOKEN))

FOLLOWERS_ENDPOINT = "https://api.github.com/users/{org_login}/followers"
ORG_METRICS.append(
    LengthMetric("orgFollowers", ["org_login"],
              FOLLOWERS_ENDPOINT, "followers_count", token=TOKEN)
)

ORG_METRICS.append(ListMetric("issueNewWeekly", ["repo_group_id","period","begin_week","end_date"],
                              AUGUR_HOST +
                              "/repo-groups/{repo_group_id}/issues-new" +
                              "?period={period}&begin_date={begin_week}&end_date={end_date}",
                              {"new_issues_by_day_over_last_month": ["date", "issues"]}))

ORG_METRICS.append(ListMetric("issueNewMonthly",["repo_group_id","period","begin_month","end_date"],
                              AUGUR_HOST +
                              "/repo-groups/{repo_group_id}/issues-new" +
                              "?period={period}&begin_date={begin_month}&end_date={end_date}",
                              {"new_issues_by_day_over_last_six_months": ["date", "issues"]}))

COMMITS_ENDPOINT = "https://api.github.com/repos/{owner}/{repo}/commits"
SIMPLE_METRICS.append(CustomMetric("getCommitsByMonth", [
                      'owner', 'repo'], COMMITS_ENDPOINT, parse_commits_by_month, token=TOKEN))


NADIA_ENDPOINT = AUGUR_HOST + "/repos/{repo_id}/nadia-project-labeling-badge/"
ADVANCED_METRICS.append(CustomMetric("getNadiaBadgeURL",[
  "repo_id"],NADIA_ENDPOINT, parse_nadia_label_into_badge))

REPO_LIBYEAR_ENDPOINT = AUGUR_HOST + "/repo-groups/{repo_group_id}/repos/{repo_id}/libyear"
ADVANCED_METRICS.append(ListMetric(
  "repoLibyears",
  ["repo_group_id","repo_id"],
  REPO_LIBYEAR_ENDPOINT,
  {
    "repo_dependency_libyear_list" : [
                                "name","libyear","most_recent_collection"
                                ]
  }
  )
)

SIMPLE_METRICS.append(ListMetric("averageIssueResolutionTime", sixMonthsParams, AUGUR_HOST + "/repos/" + "{repo_id}" + "/average-issue-resolution-time", {"average_issue_resolution_time": ["repo_name", "avg_issue_resolution_time"]}))

# Metric for Average Commit Counts per PR
# TODO: - Currently not working because of something wrong on Augur's end. Develop a solution here (hacky) or fix upstream.

# RESOURCE_METRICS.append(ResourceMetric("averageCommitsPerPR", sixMonthsParams,
#                                 AUGUR_HOST + "/pull_request_reports/average_commits_per_PR/" +
#                                 "?repo_id={repo_id}&start_date={begin_month}&end_date={end_date}"))
