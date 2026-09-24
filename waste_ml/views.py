from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .predict import predict_image


@csrf_exempt
def home(request):

    if request.method == "POST":

        uploaded_image = request.FILES["image"]

        prediction, confidence = predict_image(uploaded_image)

        return HttpResponse(f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Waste Classifier</title>
            </head>

            <body>

                <h1>Waste Classifier</h1>

                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="image" required>
                    <button type="submit">Predict</button>
                </form>

                <h2>Prediction: {prediction}</h2>
                <p>Confidence: {confidence:.2f}%</p>

            </body>
            </html>
        """)

    return HttpResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Waste Classifier</title>
        </head>

        <body>

            <h1>Waste Classifier</h1>

            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="image" required>
                <button type="submit">Predict</button>
            </form>

        </body>
        </html>
    """)