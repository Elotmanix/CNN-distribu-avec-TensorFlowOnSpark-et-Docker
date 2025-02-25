from pyspark.sql import SparkSession
import tensorflow as tf
import horovod.tensorflow.keras as hvd
import numpy as np

def load_mnist():
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
    x_train = x_train.astype('float32') / 255.0
    x_test  = x_test.astype('float32')  / 255.0
    x_train = np.expand_dims(x_train, -1)
    x_test  = np.expand_dims(x_test, -1)
    y_train = tf.keras.utils.to_categorical(y_train, 10)
    y_test  = tf.keras.utils.to_categorical(y_test, 10)
    return (x_train, y_train), (x_test, y_test)

def build_cnn():
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
        tf.keras.layers.MaxPooling2D((2,2)),
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    return model

def main():
    spark = SparkSession.builder \
        .appName("TensorFlowOnSpark_MNIST") \
        .getOrCreate()

    hvd.init()
    rank = hvd.rank()
    size = hvd.size()

    (x_train, y_train), (x_test, y_test) = load_mnist()
    model = build_cnn()

    opt = tf.keras.optimizers.Adam(learning_rate=0.01 * size)
    opt = hvd.DistributedOptimizer(opt)

    model.compile(
        loss='categorical_crossentropy',
        optimizer=opt,
        metrics=['accuracy']
    )

    verbose = 1 if rank == 0 else 0
    callbacks = [
        hvd.callbacks.BroadcastGlobalVariablesCallback(root_rank=0),
        hvd.callbacks.MetricAverageCallback()
    ]

    history = model.fit(
        x_train, y_train,
        epochs=5,
        batch_size=64,
        validation_data=(x_test, y_test),
        callbacks=callbacks,
        verbose=verbose
    )

    if rank == 0:
        import os
        import matplotlib
        matplotlib.use('Agg')  # Required for non-GUI environments
        import matplotlib.pyplot as plt

        # Plot training metrics
        plt.figure(figsize=(12, 5))
        plt.subplot(1,2,1)
        plt.plot(history.history['accuracy'], label='Train Acc')
        plt.plot(history.history['val_accuracy'], label='Val Acc')
        plt.title('Accuracy')
        plt.legend()

        plt.subplot(1,2,2)
        plt.plot(history.history['loss'], label='Train Loss')
        plt.plot(history.history['val_loss'], label='Val Loss')
        plt.title('Loss')
        plt.legend()

        plt.tight_layout()
        plt.savefig('/tmp/training_metrics.png')
        plt.close()

        # Evaluate and save model
        loss, acc = model.evaluate(x_test, y_test, verbose=0)
        print(f"Final test loss: {loss:.4f}, test accuracy: {acc:.4f}")
        model.save('/tmp/mnist_cnn_model.h5')

    spark.stop()

if __name__ == "__main__":
    main()