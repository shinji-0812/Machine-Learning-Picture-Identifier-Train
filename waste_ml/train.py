import tensorflow
from tensorflow.keras import layers, models
import numpy
import os
from sklearn.metrics import classification_report, confusion_matrix

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
DATASET_PATH = 'waste_classifier/dataset'
MODEL_DIR = 'waste_ml/DATA'
EPOCHS_FROZEN = 15
EPOCHS_FINE_TUNE = 15
SEED = 123

os.makedirs(MODEL_DIR, exist_ok=True)

train_val_data = tensorflow.keras.preprocessing.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.15,
    subset="training",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

test_data = tensorflow.keras.preprocessing.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.15,
    subset="validation",
    seed=SEED,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_val_data.class_names
print("Class names:", class_names)

val_batches = int(0.176 * tensorflow.data.experimental.cardinality(train_val_data).numpy())
val_data = train_val_data.take(val_batches)
train_data = train_val_data.skip(val_batches)

print(f"Train batches: {tensorflow.data.experimental.cardinality(train_data).numpy()}")
print(f"Val batches:   {tensorflow.data.experimental.cardinality(val_data).numpy()}")
print(f"Test batches:  {tensorflow.data.experimental.cardinality(test_data).numpy()}")

class_counts = {}
for cls in class_names:
    cls_path = os.path.join(DATASET_PATH, cls)
    class_counts[cls] = len(os.listdir(cls_path))
print("Image counts per class:", class_counts)

total = sum(class_counts.values())
n_classes = len(class_names)
class_weight = {
    i: total / (n_classes * class_counts[cls])
    for i, cls in enumerate(class_names)
}
print("Class weights:", class_weight)

AUTOTUNE = tensorflow.data.AUTOTUNE
train_data = train_data.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_data = val_data.cache().prefetch(buffer_size=AUTOTUNE)
test_data = test_data.cache().prefetch(buffer_size=AUTOTUNE)

data_augmentation = models.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
    layers.RandomContrast(0.15),
    layers.RandomTranslation(0.1, 0.1),
], name="data_augmentation")

base_model = tensorflow.keras.applications.MobileNetV2(
    input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False

inputs = layers.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
x = data_augmentation(inputs)
x = layers.Rescaling(1.0 / 127.5, offset=-1)(x)
x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(128, activation='relu')(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(len(class_names), activation='softmax')(x)

model = models.Model(inputs, outputs)

model.compile(
    optimizer=tensorflow.keras.optimizers.Adam(learning_rate=1e-3),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

checkpoint_path = os.path.join(MODEL_DIR, 'waste_model.keras')

callbacks = [
    tensorflow.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=5, restore_best_weights=True
    ),
    tensorflow.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss', factor=0.5, patience=3, min_lr=1e-6
    ),
    tensorflow.keras.callbacks.ModelCheckpoint(
        checkpoint_path, monitor='val_accuracy', save_best_only=True
    ),
]

print("\n=== Phase 1: training with frozen base model ===")
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_FROZEN,
    class_weight=class_weight,
    callbacks=callbacks
)

print("\n=== Phase 2: fine-tuning top layers of base model ===")
base_model.trainable = True

fine_tune_at = len(base_model.layers) - 30
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=tensorflow.keras.optimizers.Adam(learning_rate=1e-5),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

history_fine = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS_FROZEN + EPOCHS_FINE_TUNE,
    initial_epoch=history.epoch[-1] + 1,
    class_weight=class_weight,
    callbacks=callbacks
)

print("\n=== Final evaluation on test set ===")
test_loss, test_acc = model.evaluate(test_data)
print(f"Test accuracy: {test_acc:.4f}")
print(f"Test loss:     {test_loss:.4f}")

y_true = []
y_pred = []
for images, labels in test_data:
    preds = model.predict(images, verbose=0)
    y_true.extend(labels.numpy())
    y_pred.extend(numpy.argmax(preds, axis=1))

print("\n=== Classification report ===")
print(classification_report(y_true, y_pred, target_names=class_names))
print("=== Confusion matrix ===")
print(confusion_matrix(y_true, y_pred))

model.save(checkpoint_path)

class_names_path = os.path.join(MODEL_DIR, 'class_names.txt')
with open(class_names_path, 'w') as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")

print("\nModel and class names saved successfully.")
print(f"Model:       {checkpoint_path}")
print(f"Class names: {class_names_path}")
print("Training completed.")