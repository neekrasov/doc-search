python3.11 ../scripts/load_data_into_elastic.py --host http://elasticsearch:9200 --path ../sources/posts.csv
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000


