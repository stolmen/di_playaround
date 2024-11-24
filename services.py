import json
import statistics
import sqlite3
import requests


def create_http_client():
    return requests.Session()


def create_db_client(db_filename):
    return sqlite3.connect(db_filename)


class JsonFileStorageService:
    """store data as a JSON file"""

    def __init__(self, filename):
        self.filename = filename

    def store_data(self, data):
        with open(self.filename, "w") as f:
            f.write(json.dumps(data, indent=4))

    def get_data(
        self,
    ):
        with open(self.filename, "r") as f:
            data = f.read()
            if not data:
                raise ValueError("huh, no data?")
        return json.loads(data)


class Skip(Exception):
    pass


class DataService:
    """Responsible for querying for and storing persisted data"""

    def __init__(self, http_client, storage_service):
        # self.db_client = db_client
        self.http_client = http_client
        self.storage_service = storage_service

    def is_stale(self):
        # query database to check whether the data is stale, or not
        return False  # TODO: implement

    def refresh_data(self):
        bulk_data_url = "http://www.childcarseats.com.au/api/v1/child_car_seats/filter_data/retrieve?_format=json"
        response = self.http_client.get(bulk_data_url)
        seats = response.json()["seats"]
        filtered = [i for i in seats if i["type_ids"] == ["7", "500"]]
        data = []
        for seat in filtered:
            fine_data_url = f"http://www.childcarseats.com.au/api/v1/child_car_seats/seat_extra/retrieve/{seat['nid']}"
            response = self.http_client.get(fine_data_url)
            data.append(
                {
                    "general_info": seat,
                    "detailed_info": response.json(),
                }
            )
        self.storage_service.store_data(data)

    def render_data(self):
        # render a table. fields:
        # overall stars, then for each thing
        data = self.storage_service.get_data()
        from rich.table import Table
        from rich.console import Console

        table = Table(title="Seats")
        table.add_column("name")
        table.add_column("mean_score")
        table.add_column("median_score")
        table.add_column("min_score")
        table.add_column("ease_of_use_mean")
        # table.add_column("worst_scores_reasons")

        thinged_data = []
        for row in data:
            title = row["general_info"]["title"]
            try:
                score_info = self.extract_scores(
                    row["detailed_info"], test_type="protection"
                )
            except Skip:
                continue

            scores = [float(i[1]) for i in score_info]

            mean_score = statistics.mean(scores)
            median_score = statistics.median(scores)
            min_score = min(scores)

            # worst_scores_reasons = ",".join(
            #     [i[0] for i in sorted(score_info, key=lambda x: float(x[1]))][:3]
            # )

            ease_of_use_scores = self.extract_scores(
                row["detailed_info"], test_type="ease_of_use"
            )
            ease_of_use_mean = statistics.mean([i[1] for i in ease_of_use_scores])

            thinged_data.append(
                (
                    title,
                    "{0:.2f}".format(mean_score),
                    "{0:.2f}".format(median_score),
                    "{0:.2f}".format(min_score),
                    "{0:.2f}".format(ease_of_use_mean),
                )
            )

        thinged_data = sorted(thinged_data, key=lambda x: float(x[1]))[-20:]
        for row in thinged_data:
            table.add_row(*row)

        print(table)
        console = Console()
        console.print(table)

    @staticmethod
    def extract_scores(detailed_info, test_type, skip_shit=True):
        assert len(detailed_info["tests"].keys()) == 1
        first_key = list(detailed_info["tests"].keys())[0]
        # things = detailed_info["tests"]["1296"]
        things = detailed_info["tests"][first_key]

        test_types = [test_type]

        scores = []
        for k in ["500", "7"]:
            for test_type in test_types:
                blah = things[k][test_type]
                for test_name, ratings in blah.items():
                    if len(ratings) == 1:
                        assert len(ratings) == 1, ratings
                        score = ratings[0]["fraction"]  # score out of 1
                        print(ratings[0]["rating_scheme_id"])
                        if ratings[0]["rating_scheme_id"] != "1296" and skip_shit:
                            raise Skip()
                    elif len(ratings) == 2:
                        assert ratings[0] == ratings[1]
                        score = ratings[0]["fraction"]  # score out of 1
                        print(ratings[0]["rating_scheme_id"])
                        if ratings[0]["rating_scheme_id"] != "1296" and skip_shit:
                            raise Skip()

                    else:
                        assert False
                    scores.append((test_name, float(score)))

        return scores
