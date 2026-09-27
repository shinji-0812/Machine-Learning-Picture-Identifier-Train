
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

                <div
                    class="exit-icon"
                    onclick="closeResult()"
                >
                    X
                </div>

                <div class="result-icon">
                    ✅
                </div>

                <div class="result-label">
                    Prediction
                </div>

                <div class="prediction">
                    {prediction}
                </div>

                <div class="confidence-label">
                    Confidence
                </div>

                <div class="confidence-bar">
                    <div
                        class="confidence-fill" style="width: {confidence:.2f}%;">
                    </div>
                </div>

                <div class="confidence-value">
                    {confidence:.2f}%
                </div>

            </div>
            """

        else:

            result = f"""
            <div class="result-card">

                <div
                    class="exit-icon"
                    onclick="closeResult()"
                >
                    X
                </div>

                <div class="result-icon">
                    ⚠️
                </div>

                <div class="result-label">
                    Prediction
                </div>

                <div class="prediction">
                    Can't Determine
                </div>

                <div class="confidence-label">
                    Confidence
                </div>

                <div class="confidence-bar">
                    <div
                        class="confidence-fill"
                        style="width: 0%;">
                    </div>
                </div>

                <div class="confidence-value">
                    ERROR
                </div>

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

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

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
                linear-gradient(
                    135deg,
                    #061a17,
                    #0b2e26,
                    #063b32
                );

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

            box-shadow:
                0 0 30px
                rgba(16, 185, 129, 0.35);
            transition: 0.3s;

        }}
        .logo:hover {{
        
                    width: 70px;
        
                    height: 70px;
        
                    margin: auto;
        
                    border-radius: 50%;
        
                    background: #10b981;
        
                    display: flex;
        
                    justify-content: center;
        
                    align-items: center;
        
                    font-size: 35px;
        
                    box-shadow:
                        0 0 90px
                        rgba(16, 185, 129, 0.35);
                    transition: 0.3s;
        
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

            background:
                rgba(255, 255, 255, 0.08);

            border:
                1px solid
                rgba(255, 255, 255, 0.12);

            backdrop-filter: blur(15px);

            border-radius: 24px;

            padding: 30px;

            box-shadow:
                0 20px 50px
                rgba(0, 0, 0, 0.3);

        }}


        .upload-area {{

            border:
                2px dashed
                #2dd4bf;

            border-radius: 18px;

            padding: 45px 20px;

            text-align: center;
            cursor: pointer;

            background:
                rgba(45, 212, 191, 0.05);

            transition: 0.3s;

        }}

        .upload-area:hover {{

            background:
                rgba(45, 212, 191, 0.1);

            border-color:
                #5eead4;

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

        .upload-modal {{
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;

            background: rgba(0, 0, 0, 0.5);

            justify-content: center;
            align-items: center;
        }}

        .upload-modal-content {{
            width: 100%;
            max-width: 400px;

            background: rgba(0, 0, 0, 0.5);
            border-radius: 20px;

            padding: 65px;
            padding-left: 30px;
            padding-right: 30px;

            text-align: center;

            box-shadow: 0 15px 40px rgba(0,0,0,0.25);

            animation: popup 0.5s ease;

            backdrop-filter: blur(8px);
        }}

        .modal-title {{
            font-size: 22px;
            font-weight: bold;
            margin-bottom: 25px;
        }}

        .modal-buttons {{
            display: flex;
            gap: 10px;
        }}

        .choice-button {{
            flex: 1;

            padding: 50px;

            border: dashed 2px #10b981;
            border-radius: 14px;

            background: transparent;
            color: #10b981;

            font-size: 16px;
            font-weight: bold;

            cursor: pointer;
        }}

        .choice-button:hover {{
            opacity: 0.9;
        }}

        .cancel-button {{
            width: 100%;

            margin-top: 45px;

            padding: 13px;

            border: none;
            border-radius: 12px;

            background: red;
            color: white;

            font-size: 15px;

            cursor: pointer;
            transition: 0.3s;
        }}

        .cancel-button:hover {{
            transform: translateY(-2px);
        }}

        @keyframes popup {{
            from {{
                transform: scale(0.4);
                opacity: 0;
            }}

            to {{
                transform: scale(1);
                opacity: 1;
            }}
        }}
        


        


        .predict-button {{

            width: 100%;

            margin-top: 20px;

            padding: 15px;

            border: none;

            border-radius: 12px;

            background:
                linear-gradient(
                    135deg,
                    #10b981,
                    #14b8a6
                );

            color: white;

            font-size: 16px;

            font-weight: bold;

            cursor: pointer;

            transition: 0.3s;

        }}


        .predict-button:hover {{

            transform:
                translateY(-2px);

            box-shadow:
                0 10px 25px
                rgba(16, 185, 129, 0.3);

        }}


        .result-card {{

            padding: 30px;

            background: rgba(0, 0, 0, 0.8);
            backdrop-filter: blur(8px);

            border:
                1px solid
                rgba(45, 212, 191, 0.3);

            border-radius: 18px;

            text-align: center;

            position: fixed;

            left: 50%;

            top:59.7%;

            transform: translate(-50%, -49%);

            width: calc(100% - 40px);

            max-width: 650px;

            min-height: 0px;

            box-shadow:
                0 20px 60px
                rgba(0, 0, 0, 0.5);


            z-index: 1000;

        }}


        .exit-icon {{

            position: absolute;

            top: 15px;

            right: 20px;

            font-size: 22px;

            font-weight: bold;

            cursor: pointer;

            color: #a7c9c0;

            transition: 0.2s;

        }}


        .exit-icon:hover {{

            color: white;

            transform: scale(1.1);

        }}


        .result-icon {{

            margin-top: 60px;

            font-size: 55px;

            margin-bottom: 50px;

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

            margin: 8px 0 10px;

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

            background: white;

            border-radius: 20px;

            overflow: hidden;

        }}


        .confidence-fill {{

            height: 100%;

            background:
                linear-gradient(
                    90deg,
                    #10b981,
                    #2dd4bf
                );
            border-radius: 20px;
            animation: fillAnimation 1.3s forwards;

        }}

        @keyframes fillAnimation {{
            from {{
                width: 0%;
            }}
            to {{
                width: 100%;
            }}
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


            .result-card {{

                min-height: 0px;

            }}


            .result-icon {{

                margin-top: 60px;

                margin-bottom: 40px;

            }}

        }}


        .title::after {{
            content: "|";
            margin-left: 3px;
            animation: blink 0.7s infinite;
            
        }}

        @keyframes blink {{
            50%{{
                opacity: 0;
            }}
        }}



    </style>

</head>


<body>


    <div
        class="container"
        id="container"
    >

        <div class="header">

            <div class="logo">
                ♻
            </div>

            <h1 class="title" id="typing_title">
                
            </h1>

            <p class="subtitle">
                Upload an image and I will identify
                the type of waste.
            </p>

        </div>


        <div class="card">

            <form
                method="POST"
                enctype="multipart/form-data"
            >


                <div class="upload-area" id="upload-area">
                    <div class="upload-icon">📷</div>
                    <div class="upload-title">Upload Waste Image</div>
                    <div class="upload-text">Please select an image from your device</div>
                </div>


                <div class="upload-modal" id="uploadModal">
                    <div class="upload-modal-content">

                        <div class="modal-title">
                            Choose Image Source
                        </div>

                        <div class="modal-buttons">

                            <button type="button" class="choice-button" id="uploadButton">
                                📁 Upload
                            </button>

                            <button type="button" class="choice-button" id="cameraButton">
                                📷 Camera
                            </button>

                        </div>

                        <button type="button" class="cancel-button" id="cancelButton">
                            Cancel
                        </button>

                    </div>
                </div>

                <input
                    type="file"
                    id="imageInput"
                    name="image"
                    accept="image/*"
                    required
                    hidden
                >


                <button
                    type="submit"
                    class="predict-button"
                >
                    🔍 Analyze Image
                </button>

            </form>

        </div>


        <div class="footer">
            Waste Classification System BY DAVE
        </div>

    </div>


    {result}


    <script>
    function closeResult() {{
        const resultCard = document.querySelector(".result-card");
        const container = document.getElementById("container");

        if (resultCard) {{
            resultCard.style.display = "none";
        }}

        if (container) {{
            container.style.display = "block";
        }}
    }}


        const imageInput = document.getElementById("imageInput");
        const uploadArea = document.getElementById("upload-area");

        const uploadModal = document.getElementById("uploadModal");

        const uploadButton = document.getElementById("uploadButton");
        const cameraButton = document.getElementById("cameraButton");

        const cancelButton = document.getElementById("cancelButton");



        uploadArea.addEventListener("click", function() {{

            uploadModal.style.display = "flex";

        }});


   
        uploadButton.addEventListener("click", function() {{

            imageInput.removeAttribute("capture");

            uploadModal.style.display = "none";

            imageInput.click();

        }});


  
        cameraButton.addEventListener("click", function() {{

            imageInput.setAttribute("capture", "environment");

            uploadModal.style.display = "none";

            imageInput.click();

        }});



        cancelButton.addEventListener("click", function() {{

            uploadModal.style.display = "none";

        }});



        uploadModal.addEventListener("click", function(event) {{

            if (event.target === uploadModal) {{

                uploadModal.style.display = "none";

            }}

        }});


        
        imageInput.addEventListener("change", function() {{

            if (this.files && this.files[0]) {{

                const file = this.files[0];

                const image = document.createElement("img");

                image.src = URL.createObjectURL(file);

                image.style.width = "100%";
                image.style.height = "100%";
                image.style.objectFit = "cover";
                image.style.borderRadius = "12px";

                uploadArea.innerHTML = "";

                uploadArea.appendChild(image);

            }}

        }});
    
        function typeWriterEffect() {{

            const textContent = document.getElementById("typing_title");

            const text = "Waste Classifier";

            let index = 0;
            let deleting = false;

            function type() {{

                if (!deleting) {{

                    textContent.textContent = text.substring(0, index);

                    index++;

                    if (index > text.length) {{

                        deleting = true;

                        setTimeout(type, 1500);

                        return;
                    }}

                    setTimeout(type, 100);

                }} else {{

                    textContent.textContent = text.substring(0, index);

                    index--;

                    if (index < 0) {{

                        index = 0;

                        deleting = false;

                        setTimeout(type, 500);

                        return;
                    }}

                    setTimeout(type, 50);
                }}
            }}

            type();
        }}

        typeWriterEffect();


</script>


</body>

</html>
""")


