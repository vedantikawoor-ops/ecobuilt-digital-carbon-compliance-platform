from flask import Flask, render_template

from routes.routes_analyse import analysis_bp


# ========================================
# Create Flask Application
# ========================================

app = Flask(__name__)


# ========================================
# Register API Routes
# ========================================

app.register_blueprint(analysis_bp)


# ========================================
# Frontend Route
# ========================================

@app.route("/")
def home():
    return render_template("index.html")


# ========================================
# Run Application
# ========================================

if __name__ == "__main__":
    app.run(
        debug=True
    )