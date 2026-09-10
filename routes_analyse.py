from flask import Blueprint, request, jsonify

from services.pagespeed_ import (
    analyze_website,
    extract_metrics
)

from services.html_Service import analyze_html

from services.green_host import (
    check_green_hosting
)

from services.carbon_calc import (
    calculate_carbon
)

from services.cost_calc import (
    calculate_monthly_cost
)

from services.score_eng import (
    calculate_score
)

from services.reccomend import (
    generate_recommendations
)


# ========================================
# Create Blueprint
# ========================================

analysis_bp = Blueprint(
    "analysis",
    __name__
)


# ========================================
# Analyze Website API
# ========================================

@analysis_bp.route(
    "/api/analyze",
    methods=["POST"]
)
def analyze():

    try:

        # --------------------------------
        # Get URL from request
        # --------------------------------

        data = request.get_json()

        if not data or "url" not in data:

            return jsonify({
                "success": False,
                "error": "Website URL is required."
            }), 400

        url = data["url"].strip()

        if not url:

            return jsonify({
                "success": False,
                "error": "Website URL cannot be empty."
            }), 400


        # --------------------------------
        # 1. PageSpeed Analysis
        # --------------------------------

        pagespeed_data = analyze_website(url)

        metrics = extract_metrics(
            pagespeed_data
        )


        # --------------------------------
        # 2. HTML Analysis
        # --------------------------------

        html_metrics = analyze_html(url)


        # --------------------------------
        # 3. Green Hosting
        # --------------------------------

        green_data = check_green_hosting(url)


        # --------------------------------
        # 4. Carbon Calculation
        # --------------------------------

        carbon_data = calculate_carbon(
            metrics["page_size_bytes"]
        )


        # --------------------------------
        # 5. Cost Calculation
        # --------------------------------

        cost_data = calculate_monthly_cost(
            metrics["page_size_bytes"]
        )


        # --------------------------------
        # 6. EcoBuilt Score
        # --------------------------------

        score_data = calculate_score(

            page_size_mb=metrics[
                "page_size_mb"
            ],

            image_wasted_bytes=metrics[
                "image_wasted_bytes"
            ],

            script_count=html_metrics[
                "script_count"
            ],

            is_green=green_data[
                "is_green"
            ]
        )


        # --------------------------------
        # 7. Recommendations
        # --------------------------------

        recommendations = generate_recommendations(

            page_size_mb=metrics[
                "page_size_mb"
            ],

            image_wasted_bytes=metrics[
                "image_wasted_bytes"
            ],

            script_count=html_metrics[
                "script_count"
            ],

            load_time_seconds=metrics[
                "load_time_seconds"
            ],

            is_green=green_data[
                "is_green"
            ]
        )


        # --------------------------------
        # Final Response
        # --------------------------------

        return jsonify({

            "success": True,

            "website": url,

            "pagespeed": {

                "performance_score":
                    metrics[
                        "performance_score"
                    ],

                "page_size_bytes":
                    metrics[
                        "page_size_bytes"
                    ],

                "page_size_mb":
                    metrics[
                        "page_size_mb"
                    ],

                "requests":
                    metrics[
                        "request_count"
                    ],

                "load_time_seconds":
                    metrics[
                        "load_time_seconds"
                    ],

                "image_wasted_bytes":
                    metrics[
                        "image_wasted_bytes"
                    ]
            },

            "html": {

                "images":
                    html_metrics[
                        "image_count"
                    ],

                "scripts":
                    html_metrics[
                        "script_count"
                    ],

                "stylesheets":
                    html_metrics[
                        "stylesheet_count"
                    ],

                "fonts":
                    html_metrics[
                        "font_count"
                    ]
            },

            "green_hosting": {

                "is_green":
                    green_data[
                        "is_green"
                    ],

                "hosted_by":
                    green_data[
                        "hosted_by"
                    ]
            },

            "carbon": carbon_data,

            "cost": cost_data,

            "score": score_data,

            "recommendations":
                recommendations

        })


    except RuntimeError as error:

        return jsonify({

            "success": False,
            "error": str(error)

        }), 500


    except Exception as error:

        return jsonify({

            "success": False,
            "error": str(error)

        }), 500