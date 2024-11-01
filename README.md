# **Efficient Data Stream Anomaly Detection**

*This document was prepared as part of a research project for Cobblestone Energy.*

---

## **1. Algorithm Selection**

For real-time anomaly detection in data streams with concept drift and seasonal variations, an appropriate algorithm is the **Exponential Moving Average (EMA)** combined with the **Modified Z-Score** method. This approach is efficient, adapts to changes over time, and is computationally light, making it suitable for real-time applications.

### **Why EMA with Modified Z-Score?**

- **Adaptability**: EMA gives more weight to recent data, allowing the model to adapt to concept drift.
- **Efficiency**: Computationally simple, suitable for real-time processing.
- **Robustness**: Modified Z-Score is less sensitive to outliers compared to the standard Z-Score.

---

## **2. Data Stream Simulation**

We'll create a generator function that simulates a data stream with:

- **Regular Patterns**: A sine wave to represent periodic behaviour.
- **Seasonal Elements**: A slower sine wave to simulate seasonal changes.
- **Random Noise**: Gaussian noise added to each data point.
- **Anomalies**: Randomly injected spikes or drops to simulate anomalies.

---

## **3. Anomaly Detection Mechanism**

Implement a real-time anomaly detection mechanism that:

- **Calculates EMA**: Updates the moving average with each new data point.
- **Computes Modified Z-Score**: Determines how many standard deviations a point is from the EMA.
- **Flags Anomalies**: If the Modified Z-Score exceeds a threshold (e.g., 3.5), the point is flagged.

---

## **4. Optimization**

To ensure speed and efficiency:

- **Use Efficient Data Structures**: Utilize variables and simple data types over heavy structures.
- **Minimize Library Use**: Rely on core Python and essential libraries only.
- **Optimize Calculations**: Update calculations incrementally where possible.

---

## **5. Visualization**

Create a real-time visualization using **matplotlib** to display:

- **Data Stream**: Plot the incoming data points.
- **Anomalies**: Highlight detected anomalies on the plot.

---

## **6. Parameter Tuning and Performance Considerations**

When manipulating the parameters of the anomaly detection algorithm, it's important to consider how they affect the model's performance, especially in relation to the size of the anomalies.

### **Key Parameters**

- **Threshold**: Determines the sensitivity of the detector.
  - **Lower Threshold**: Increases sensitivity, allowing detection of smaller anomalies but may lead to more false positives.
  - **Higher Threshold**: Decreases sensitivity, reducing false positives but may miss smaller anomalies.
- **EMA Alpha (α)**: Controls the rate at which EMA responds to new data.
  - **Higher Alpha**: EMA adapts more quickly to recent changes, which is useful for detecting sudden anomalies.
  - **Lower Alpha**: EMA responds more slowly, smoothing out noise but potentially lagging behind rapid changes.
- **MAD Window Size**: The number of recent residuals used to calculate the Median Absolute Deviation.
  - **Larger Window**: Provides a stable estimate of variability but may not adapt quickly to changes.
  - **Smaller Window**: Adapts quickly to recent changes but may be influenced by outliers.

### **Considerations Based on Anomaly Size**

- **Detecting Smaller Anomalies**
  - **Adjust Threshold**: Lower the threshold to make the detector more sensitive.
  - **Increase EMA Alpha**: Allows EMA to respond faster to changes, helping to detect subtle anomalies.
  - **Balance Sensitivity**: Be cautious of increasing false positives; adjust parameters gradually.
- **Detecting Larger Anomalies**
  - **Maintain or Increase Threshold**: Larger anomalies naturally exceed higher thresholds.
  - **Adjust EMA Alpha**: A lower alpha can help filter out noise, focusing on significant deviations.
  - **Optimize MAD Window Size**: A larger window can provide a more robust estimation of normal variability.

### **Balancing Sensitivity and Specificity**

- **Sensitivity (Recall)**: Ability of the model to correctly identify true anomalies.
- **Specificity (Precision)**: Ability of the model to avoid false positives.

Adjusting parameters requires a trade-off between sensitivity and specificity. The optimal settings depend on the specific application and the acceptable rate of false positives versus missed detections.

---

## **7. Testing and Performance Metrics**

To evaluate the performance of the anomaly detection system, I implemented a testing mechanism that calculates key metrics:

- **Precision**: The proportion of detected anomalies that are actual anomalies.
- **Recall**: The proportion of actual anomalies that were correctly detected.
- **F1-Score**: The harmonic mean of precision and recall, providing a single metric that balances both.

### **Testing Procedure**

- **Labeling Anomalies**: Modify the data stream to yield both the value and a label indicating whether it's an anomaly.
- **Recording Predictions**: During the detection process, record the true labels and the model's predictions.
- **Calculating Metrics**: After running the simulation, use **scikit-learn** to compute precision, recall, and F1-score.

### **Interpreting the Metrics**

- **High Precision**: Indicates a low rate of false positives; the anomalies detected are mostly true anomalies.
- **High Recall**: Indicates a low rate of false negatives; most actual anomalies are detected.
- **F1-Score**: Provides a balanced measure, especially useful when the class distribution is uneven.

### **Example Results**

After running the simulation and closing the visualization:

```
Precision: 0.83 
Recall: 0.92 
F1-Score: 0.87
```

These metrics suggest that the model has a good balance between detecting anomalies and minimizing false positives.

### **Adjusting Parameters Based on Metrics**

- **Low Precision**: Consider increasing the threshold to reduce false positives.
- **Low Recall**: Consider decreasing the threshold or increasing the EMA alpha to detect more anomalies.
- **Optimal F1-Score**: Aim for parameter settings that maximize the F1-score for balanced performance.

---

## **Explanation of the Algorithm**

### **Exponential Moving Average (EMA)**

- **Purpose**: Smooths out the data to identify trends by giving more weight to recent observations.
- **Adaptation**: Helps the model adjust to recent changes in the data, accommodating concept drift.

### **Modified Z-Score**

- **Calculation**:

  \[
  \text{Modified Z-Score} = 0.6745 \times \frac{\text{Value} - \text{EMA}}{\text{MAD}}
  \]

- **MAD (Median Absolute Deviation)**: A robust measure of variability less affected by outliers.
- **Threshold**: A common threshold is 3.5; values beyond this are considered anomalies.

### **Anomaly Detection Process**

1. **Update EMA** with the new data point.
2. **Calculate Residual**: Difference between the data point and EMA.
3. **Update MAD** using recent residuals.
4. **Compute Modified Z-Score**.
5. **Flag Anomaly** if Modified Z-Score exceeds the threshold.

---

## **Key Features of the Code**

### **Data Simulation**

- Uses a combination of sine waves and noise to simulate realistic data with patterns and anomalies.
- Anomalies are randomly injected to test the detection mechanism.

### **Anomaly Detection Class**

- Maintains state with EMA and MAD for real-time updates.
- Efficiently updates statistics without storing all historical data.

### **Visualization**

- Real-time plotting with `matplotlib.animation.FuncAnimation`.
- Anomalies are highlighted in red for easy identification.

---

## **Error Handling and Data Validation**

- **Division by Zero**: Checks if MAD is zero before division to prevent errors.
- **Data Consistency**: Ensures that the residuals list maintains enough data for accurate MAD calculation.

---

## **Requirements**

### **External Libraries Used**

- **numpy**
- **matplotlib**
- **scikit-learn**

### **`requirements.txt` File**

```
numpy
matplotlib
scikit-learn
```

---

## **Conclusion**

The script developed implements an efficient and adaptive anomaly detection system suitable for real-time data streams. By combining EMA with the Modified Z-Score method, it effectively adapts to concept drift and seasonal variations while maintaining computational efficiency.

---
