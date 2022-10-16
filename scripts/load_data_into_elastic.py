import argparse
import csv
import pathlib
from elasticsearch import Elasticsearch


def parse_args():
    parser = argparse.ArgumentParser(description="Load test data into elasticsearch")
    parser.add_argument(
        "--host", help="Elasticsearch host and port", default="http://localhost:9200"
    )

    return parser.parse_args()


def csv_to_json(csv_path: str) -> dict:
    json_data = []
    with open(csv_path, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            json_data.append(row)
    return json_data


def load_data_elastic(json_data, host):
    es = Elasticsearch(host)
    if es.indices.exists(index="posts"):
        print("INDEX ALREADY EXISTS")
    else:
        es.indices.create(
            index="posts",
            mappings={
                "properties": {
                    "text": {"type": "text"},
                    "created_date": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss", "store": False, "index": False},
                    "rubrics": {"type": "text", "store": False, "index": False },
                }
            },
        )
        for item in json_data:
            es.index(index="posts", document=item)

        print("INDEX CREATED")


def main():
    args = parse_args()

    csv_path = pathlib.Path.cwd() / "sources" / "posts.csv"

    json_data = csv_to_json(csv_path)

    load_data_elastic(json_data, args.host)


if __name__ == "__main__":
    main()
