import os
import uuid
from task_scheduler import Scheduler
from flask import Flask, request, jsonify, render_template, session

app = Flask(__name__)


@app.route('/')
def view_form():
    return render_template('testing_form.html')


@app.route('/get_people_disk', methods=['GET'])
def get_people_disk():
    path = request.args.get('path')
    if not path:
        return jsonify({"error": "Path parameter is required"}), 400

    save = session.get('save', False)
    p = session.get('path', None)

    task_id = scheduler.insert_task('pending', path, 0,
                                    True,
                                    save,
                                    p)

    return jsonify(task_id)


@app.route('/get_people_url', methods=['GET'])
def get_people_url():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    save = session.get('save', False)
    p = session.get('path', None)

    task_id = scheduler.insert_task('pending', url, 0,
                                    True,
                                    save,
                                    p)

    return jsonify(task_id)


@app.route('/handle_post', methods=['POST'])
def handle_post():
    if 'image' not in request.files:
        return jsonify({'error': 'Image is required'}), 400

    img = request.files['image']

    if img.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    file_ext = os.path.splitext(img.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    # TODO Ask if we should delete imgs after processing
    img.save(file_path)

    save = session.get('save', False)
    p = session.get('path', None)
    print(file_path)

    task_id = scheduler.insert_task('pending', file_path, 0,
                                    True,
                                    save,
                                    p)

    return jsonify(task_id)


@app.route('/get_task_status_by_id', methods=['GET'])
def get_task_status_by_id():
    task_id = request.args.get('task_id')
    if not task_id:
        return jsonify({"error": "Id parameter is required"}), 400

    return jsonify(scheduler.task_status_by_id(task_id))


@app.route('/get_queue_status', methods=['GET'])
def get_queue_status():
    return jsonify(scheduler.check_status())


@app.route('/handle_saving', methods=['GET'])
def handle_saving():
    save_checkbox = 'save' in request.args
    save_value = request.args.get('save')
    save = save_checkbox and save_value == 'on'
    path = request.args.get('path')

    if save and not path:
        return jsonify({"error": "Change save path or disable saving"}), 400

    session['save'] = save
    session['path'] = path

    return jsonify({"message": "Settings updated", "save": save, "path": path}), 200


if __name__ == "__main__":
    UPLOAD_FOLDER = 'uploaded_images'
    app.secret_key = 'human_detect_secret_api_key'  # incredibly secret :O
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    scheduler = Scheduler()
    app.run(debug=True)
