from flask import jsonify
from .blueprint import bp


@bp.route("/hello", methods=["GET"])
async def search():
    return jsonify(message="Search"), 200
