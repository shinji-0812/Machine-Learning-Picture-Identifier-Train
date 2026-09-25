
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .predict import predict_image


@csrf_exempt
def home(request):

    prediction = None
    confidence = None

    if request.method == "POST":

        uploaded_image = request.FILES["image"]

        prediction, confidence = predict_image(uploaded_image)

    result = ""

    if prediction is not None:
        if confidence > 50:
            result = f"""
            <div class="result-card">
                <div class="result-icon">✅</div>
                <div class="result-label">Prediction</div>
                <div class="prediction">{prediction}</div>
                <div class="confidence-label">Confidence</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence:.2f}%;"></div>
                </div>
                <div class="confidence-value">{confidence:.2f}%</div>
            </div>
            """
        else:
            result = f"""
            <div class="result-card">
                <div class="result-icon">⚠️</div>
                <div class="result-label">Prediction</div>
                <div class="prediction">Cant Determine</div>
                <div class="confidence-label">Confidence</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 0;"></div>
                </div>
                <div class="confidence-value">ERROR</div>
                <p style="color: #f87171; margin-top: 10px;">
                    Please try uploading a clearer image.
                </p>
            </div>
            """

    return HttpResponse(f"""
<!DOCTYPE html>
<html>
<head>

    <title>Waste Classifier</title>

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <style>

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: Arial, sans-serif;
            min-height: 100vh;
            background:
                linear-gradient(135deg, #061a17, #0b2e26, #063b32);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
        }}

        .container {{
            width: 100%;
            max-width: 650px;
        }}

        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}

        .logo {{
            width: 70px;
            height: 70px;
            margin: auto;
            border-radius: 50%;
            background: #10b981;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 35px;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.35);
        }}

        h1 {{
            margin-top: 18px;
            font-size: 36px;
            font-weight: 700;
        }}

        .subtitle {{
            color: #a7c9c0;
            margin-top: 8px;
            font-size: 15px;
        }}

        .card {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(15px);
            border-radius: 24px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
        }}

        .upload-area {{
            border: 2px dashed #2dd4bf;
            border-radius: 18px;
            padding: 45px 20px;
            text-align: center;
            background: rgba(45, 212, 191, 0.05);
            transition: 0.3s;
        }}

        .upload-area:hover {{
            background: rgba(45, 212, 191, 0.1);
            border-color: #5eead4;
        }}

        .upload-icon {{
            font-size: 45px;
            margin-bottom: 15px;
        }}

        .upload-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 8px;
        }}

        .upload-text {{
            color: #9fbdb7;
            font-size: 13px;
            margin-bottom: 20px;
        }}

        input[type="file"] {{
            width: 100%;
            max-width: 350px;
            padding: 12px;
            border-radius: 10px;
            background: #102f29;
            color: white;
            border: 1px solid #28594f;
        }}

        input[type="file"]::file-selector-button {{
            background: #10b981;
            color: white;
            border: none;
            padding: 9px 14px;
            border-radius: 7px;
            cursor: pointer;
            margin-right: 10px;
        }}

        .predict-button {{
            width: 100%;
            margin-top: 20px;
            padding: 15px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(135deg, #10b981, #14b8a6);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }}

        .predict-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
        }}

        .result-card {{
            margin-top: 25px;
            padding: 25px;
            background: rgba(16, 185, 129, 0.08);
            border: 1px solid rgba(45, 212, 191, 0.3);
            border-radius: 18px;
            text-align: center;
        }}

        .result-icon {{
            font-size: 35px;
            margin-bottom: 10px;
        }}

        .result-label {{
            color: #7dd3c7;
            font-size: 12px;
            letter-spacing: 2px;
            font-weight: bold;
        }}

        .prediction {{
            font-size: 32px;
            font-weight: bold;
            color: #5eead4;
            margin: 8px 0 20px;
            text-transform: capitalize;
        }}

        .confidence-label {{
            color: #a7c9c0;
            font-size: 14px;
            margin-bottom: 8px;
        }}

        .confidence-bar {{
            width: 100%;
            height: 10px;
            background: #173d35;
            border-radius: 20px;
            overflow: hidden;
        }}

        .confidence-fill {{
            height: 100%;
            background: linear-gradient(90deg, #10b981, #2dd4bf);
            border-radius: 20px;
        }}

        .confidence-value {{
            margin-top: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #6ee7b7;
        }}

        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #71948c;
            font-size: 12px;
        }}

        @media (max-width: 600px) {{

            body {{
                padding: 20px;
            }}

            h1 {{
                font-size: 28px;
            }}

            .card {{
                padding: 20px;
            }}

            .upload-area {{
                padding: 35px 15px;
            }}

            .prediction {{
                font-size: 26px;
            }}

        }}

    </style>

</head>

<body>

    <div class="container">

        <div class="header">

            <div class="logo">
                ♻
            </div>

            <h1>Waste Classifier</h1>

            <p class="subtitle">
                Upload an image and let the AI identify the type of waste.
            </p>

        </div>


        <div class="card">

            <form method="POST" enctype="multipart/form-data">

                <div class="upload-area">

                    <div class="upload-icon">
                        📷
                    </div>

                    <div class="upload-title">
                        Upload Waste Image
                    </div>

                    <div class="upload-text">
                        Select an image from your computer
                    </div>

                    <input
                        type="file"
                        name="image"
                        accept="image/*"
                        required
                    >

                </div>

                <button type="submit" class="predict-button">
                    🔍 Analyze Image
                </button>

            </form>

            {result}

        </div>

        <div class="footer">
            AI-Powered Waste Classification System BY DAVE
        </div>

    </div>

</body>
</html>
""")

