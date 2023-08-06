import click

from .api import SentryApi


# The common_options idea is borrowed from https://github.com/pallets/click/issues/108
common_options = [
    click.option(
        "--auth-token",
        envvar="QSENTRY_AUTH_TOKEN",
        help="The auth token for invoke sentry apis. Can read from the QSENTRY_AUTH_TOKEN env variable.",
    ),
    click.option(
        "--host-url",
        envvar="QSENTRY_HOST_URL",
        default="https://sentry.io/",
        show_default=True,
        help="The host URL for the sentry service. Can read from the QSENTRY_HOST_URL env variable.",
    ),
    click.option(
        "--org",
        envvar="QSENTRY_ORG_SLUG",
        help="The organization slug. Can read from the QSENTRY_ORG_SLUG env variable.",
    ),
    click.option(
        "--count/--no-count",
        is_flag=True,
        default=False,
        help="Show the count of objects (members, teams and etc.)",
    ),
]


def add_common_options(options):
    def _add_common_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_common_options


@click.group(invoke_without_command=True)
def main(*args, **kwargs):
    pass


@main.command()
@add_common_options(common_options)
@click.option(
    "--team",
    envvar="QSENTRY_TEAM_SLUG",
    help="The team slug.",
)
@click.option(
    "--role", default="admin", show_default=True, help="The role of the member."
)
def members(**kwargs):
    """Show members of a team by their roles"""
    members = SentryApi(kwargs["host_url"], kwargs["auth_token"]).filter_by_role_name(
        org_slug=kwargs["org"],
        team_slug=kwargs["team"],
        role_name=kwargs["role"],
        attributes=["id", "name", "email"],
    )
    if kwargs["count"]:
        print(f"Count: {len(members)}")
    for member in members:
        print(f"{member['id']}, {member['name']}, {member['email']}")


@main.command()
@add_common_options(common_options)
def teams(**kwargs):
    teams = SentryApi(kwargs["host_url"], kwargs["auth_token"]).get_all_teams(
        org_slug=kwargs["org"],
    )
    if kwargs["count"]:
        print(f"Count: {len(teams)}")
    for team in teams:
        print(f"{team['slug']}")


if __name__ == "__main__":
    main()
