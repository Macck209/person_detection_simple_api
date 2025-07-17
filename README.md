# Person detection simple API

Excerpt from a small uni project (thus no commit history).

Project uses YOLO model for detection, Flask for API endpoints and sqlite3 for very simple queuing. 
Most endpoints return the number of people detected in the photo.

API lacks a lot of features, so I wouldn't recommend using it in any major/public projects (do it at your own risk).

## Setup:

- pull this branch
- install dependencies: `pip install -r requirements.txt --upgrade`
- download YOLOv3-608 cfg and weights from https://pjreddie.com/darknet/yolo/ (put those in root)
- run: `request_handler.py`
- run one (or more): `worker.py`

Params of `insert_task`:
status, path_or_url, result, return_id=False, save_processed_img=False, save_to_path=\''

`1000_tasks_test.py` is pretty self-explanatory. Used to test queuing.