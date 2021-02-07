from datetime import datetime, timedelta

import requests

from match import Match


def get_upcoming_matches(*leagues, hours=24):
    LOLESPORTS_SCHEDULE_API_URL = "https://esports-api.lolesports.com/persisted/gw/getSchedule?hl=en-GB&leagueId=98767991302996019%2C98767991299243165%2C98767991310872058%2C98767991314006698"     # noqa
    headers = {
        "authority": "esports-api.lolesports.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36",    # noqa
        "x-api-key": "0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z",
        "accept": "*/*",
        "origin": "https://lolesports.com",
        "sec-fetch-site": "same-site",
        "sec-fetch-mode": "cors",
        "sec-fetch-dest": "empty",
        "referer": "https://lolesports.com/",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,sv;q=0.7,fr;q=0.6",
    }

    request = requests.get(LOLESPORTS_SCHEDULE_API_URL, headers=headers)

    events = request.json()["data"]["schedule"]["events"]
    matches = [Match(event_dict) for event_dict in events if event_dict["type"] == "match"]
    upcoming_matches = [match for match in matches if match.state == Match.STATE_UNSTARTED]

    latest_match_start_time = datetime.now() + timedelta(hours=hours)

    def passes_filter(match):
        """Return whether or not the given match passes the filter(s)."""
        return match.league in leagues and match.start_time <= latest_match_start_time

    filtered_upcoming_matches = [match for match in upcoming_matches if passes_filter(match)]

    return filtered_upcoming_matches
