from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import time

# Import your models
import body_model_2
import arm_model_home
import hand_model_home
import hand_model_center

app = Flask(__name__)
CORS(app)

@app.route('/start_exercise/<mode>/<child_id>/<exercise_name>', methods=['GET'])
def start_exercise(mode, child_id, exercise_name):
    side = request.args.get('side', None)  # Optional query param

    if mode == 'body':
        return Response(start_body_v1(child_id, exercise_name), mimetype='multipart/x-mixed-replace; boundary=frame')

    elif mode == 'arm':
            return Response(start_arm(child_id, exercise_name , side), mimetype='multipart/x-mixed-replace; boundary=frame')

    elif mode == 'hand':
        return Response(start_hand(child_id , exercise_name , side), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    elif mode == 'center':
        return Response(start_center(exercise_name), mimetype='multipart/x-mixed-replace; boundary=frame')

    else:
        return jsonify({"error": "Invalid mode"}), 400


def start_body_v1(child_id, exercise_name):
    body_model_2.exercise = exercise_name
    body_model_2.child_id = child_id
    body_model_2.start_time = time.time()
    body_model_2.distance_threshold_close, body_model_2.distance_threshold_far = body_model_2.exercises[exercise_name].values()
    
    return body_model_2.generate_video_feed()


def start_arm(child_id, exercise_name , side=None):
    arm_model_home.exercise = exercise_name
    arm_model_home.child_id = child_id
    arm_model_home.start_time = time.time()
    if side:
        arm_model_home.side = side  # Only set if side param is provided
    return arm_model_home.generate_video_feed()


def start_hand(child_id , exercise_name , side = None):
    hand_model_home.exercise = exercise_name
    hand_model_home.child_id = child_id
    hand_model_home.start_time = time.time()
    hand_model_home.exercise_active = False
    hand_model_home.max_duration = 120
    return hand_model_home.generate_video_feed()

def start_center( exercise_name):
    hand_model_center.exercise = exercise_name
    #hand_model_center.start_time = time.time()
    hand_model_center.exercise_active = False
    #hand_model_center.max_duration = 120
    return hand_model_center.generate_video_feed()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
