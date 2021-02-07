from datetime import datetime


class Match:

    STATE_UNSTARTED = "unstarted"
    STATE_IN_PROGRESS = "inProgress"
    STATE_COMPLETED = "completed"

    def __init__(self, event_dict):
        self.league = event_dict["league"]["name"]
        self.id_ = event_dict["match"]["id"]
        event_type = event_dict["match"]["strategy"]["type"]
        if event_type != "bestOf":
            raise ValueError(f"Unknown event type '{event_type}'.")
        self.games = event_dict["match"]["strategy"]["count"]    # Best of x
        self.team1_codename = event_dict["match"]["teams"][0]["code"]
        self.team2_codename = event_dict["match"]["teams"][1]["code"]
        self.team1_fullname = event_dict["match"]["teams"][0]["name"]
        self.team2_fullname = event_dict["match"]["teams"][1]["name"]
        self.start_time = datetime.fromisoformat(event_dict["startTime"][:-1])    # Removing trailing "Z" and convert to datetime
        self.state = event_dict["state"]

    def __repr__(self):
        return f"[{self.league}] {self.start_time}: {self.team1_fullname} vs. {self.team2_fullname} (bo{self.games})"

    def print_debug(self):
        print(f"[{self.league}] {self.start_time} Best of {self.games} ({self.id_})\n"
              f"[{self.team1_codename}] {self.team1_fullname} vs. {self.team2_fullname} [{self.team2_codename}]\n"
              f"State: {self.state}")