import tensorflow
from tensorflow.keras import layers, models

IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
DATASET_PATH = 'waste_classifier/dataset'

train_data = tensorflow.keras.preprocessing.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_data = tensorflow.keras.preprocessing.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_data.class_names

print("Class names:", class_names)

model = models.Sequential([
    layers.Rescaling(1.0/255, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((3, 3)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam',
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy'])

model.fit(train_data, validation_data=val_data, epochs=10)

model.save('waste_ml/DATA/waste_model.keras')

with open('waste_ml/DATA/class_names.txt', 'w') as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")
print("Model and class names saved successfully.")
print("Training completed.")