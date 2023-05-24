from flask import jsonify, request

from predictTags import getTags


def api_endpoints(app):
    @app.route("/api/predict-tags", methods=["POST"])
    def predictTags():
        try:
            data = request.get_json()
            title = data.get("title")
            post = data.get("post")
            tags = getTags(title, post)

        except Exception as e:
            status = {
                "status": "400",
                "message": e,
            }
            print(status)
            return jsonify({"status": status})
        status = {
            "status": "200",
            "message": "Success",
        }
        message = {"post": post, "tags": tags}
        return jsonify({"status": status, "message": message})
