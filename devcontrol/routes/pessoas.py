from flask import Blueprint, render_template

pessoas_bp = Blueprint(
    "pessoas",
    __name__,
    url_prefix="/pessoas"
)

@pessoas_bp.route("/")
def listar_pessoas():
    return render_template("pessoas/listar.html")