import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random
from sklearn.metrics import precision_score, recall_score, f1_score

# Data Stream Simulation
def data_stream():
    t = 0
    while True:
        # Regular and seasonal patterns
        seasonal = 10 * np.sin(0.01 * t)
        regular = np.sin(0.1 * t)
        noise = np.random.normal(0, 0.5)
        value = seasonal + regular + noise

        # Introduce anomalies randomly
        is_anomaly = False
        if random.random() < 0.02:
            # value += np.random.choice([15, -15])
            # is_anomaly = True
            
            # Generate a random anomaly magnitude between -20 and 20, excluding 0
            anomaly_magnitude = random.uniform(-20, 20)
            # Ensure the anomaly magnitude is sufficiently large
            if abs(anomaly_magnitude) < 5:
                anomaly_magnitude = 5 * np.sign(anomaly_magnitude)
            value += anomaly_magnitude
            is_anomaly = True


        yield value, is_anomaly  # Yield both value and anomaly label
        t += 1

# Anomaly Detector Class
class AnomalyDetector:
    def __init__(self, ema_alpha=0.1, threshold=3.5):
        self.ema_alpha = ema_alpha
        self.current_ema = None
        self.mad = None
        self.threshold = threshold
        self.residuals = []

    def update(self, value):
        if self.current_ema is None:
            self.current_ema = value
            self.mad = 0
            self.residuals.append(0)
            return False

        # Update EMA
        self.current_ema = (self.ema_alpha * value) + ((1 - self.ema_alpha) * self.current_ema)
        # Calculate residual
        residual = value - self.current_ema
        self.residuals.append(residual)

        # Update MAD (Median Absolute Deviation)
        if len(self.residuals) > 30:
            median = np.median(self.residuals)
            self.mad = np.median([abs(r - median) for r in self.residuals[-30:]])
        else:
            self.mad = np.median([abs(r - np.median(self.residuals)) for r in self.residuals])

        # Avoid division by zero
        if self.mad == 0:
            modified_z_score = 0
        else:
            modified_z_score = 0.6745 * residual / self.mad

        # Determine if it's an anomaly
        is_anomaly = abs(modified_z_score) > self.threshold
        return is_anomaly

# Visualization Setup
fig, ax = plt.subplots()
data_x, data_y = [], []
anomaly_x, anomaly_y = [], []
line, = ax.plot([], [], 'b-', label='Data Stream')
anomaly_scatter = ax.scatter([], [], c='r', label='Anomalies')

def init():
    ax.set_xlim(0, 200)
    ax.set_ylim(-25, 25)
    return line, anomaly_scatter

stream = data_stream()
detector = AnomalyDetector()

# Initialize lists to store true labels and predictions
true_labels = []
predictions = []

def animate(frame):
    value, true_anomaly = next(stream)
    is_anomaly = detector.update(value)

    # Record the true label and prediction
    true_labels.append(true_anomaly)
    predictions.append(is_anomaly)

    data_x.append(frame)
    data_y.append(value)
    line.set_data(data_x, data_y)

    if is_anomaly:
        anomaly_x.append(frame)
        anomaly_y.append(value)
        anomaly_scatter.set_offsets(np.c_[anomaly_x, anomaly_y])

    # Adjust plot limits
    if frame > 200:
        ax.set_xlim(frame - 200, frame)
        data_x.pop(0)
        data_y.pop(0)
        if anomaly_x and anomaly_x[0] < frame - 200:
            anomaly_x.pop(0)
            anomaly_y.pop(0)

    return line, anomaly_scatter

# After closing the graph, compute the session metrics
def compute_metrics(event):
    # Ensure lists are of the same length
    min_len = min(len(true_labels), len(predictions))
    y_true = true_labels[:min_len]
    y_pred = predictions[:min_len]

    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f'Precision: {precision:.2f}')
    print(f'Recall: {recall:.2f}')
    print(f'F1-Score: {f1:.2f}')

# Main Execution
if __name__ == "__main__":
    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=50, blit=True)
    plt.legend()
    plt.title('Real-Time Data Stream Anomaly Detection')
    plt.xlabel('Time')
    plt.ylabel('Value')

    # Connect the compute_metrics function to the figure's close event
    fig.canvas.mpl_connect('close_event', compute_metrics)

    plt.show()