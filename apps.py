from flask import Flask, render_template, jsonify, Response

from detector import (
    start_detector,
    get_traffic_data,
    generate_frames
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/traffic")
def traffic():
    data = get_traffic_data()
    return jsonify(data)


@app.route("/video_feed")
def video_feed():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


if __name__ == "__main__":

    print("Starting AI Smart Traffic Management System...")

    start_detector()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True
    )