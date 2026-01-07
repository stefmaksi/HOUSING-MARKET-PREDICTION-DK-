# 🏠 Danish Residential Housing Analysis

This project provides a comprehensive analysis of the Danish residential housing market. By leveraging a dataset of housing transactions, I explore price trends across regions, property types, and sales conditions. Finally, I build a Random Forest model to predict property values.

## 📊 Visual Exploration (EDA)

The following visualizations capture the core findings of the market analysis, from price distributions to regional correlations.

### Market Overview & Pricing
<table>
  <tr>
    <td width="50%"><img src="utils/output1.png" alt="House Type Distribution"><br><b>1. House Type Distribution</b></td>
    <td width="50%"><img src="utils/output2.png" alt="Regional Benchmarks"><br><b>2. Regional Price Benchmarks</b></td>
  </tr>
  <tr>
    <td width="50%"><img src="utils/output3.png" alt="SQM Price"><br><b>3. Price per m² by Type</b></td>
    <td width="50%"><img src="utils/output4.png" alt="Correlation Heatmap"><br><b>4. Feature Correlation Matrix</b></td>
  </tr>
</table>

### Detailed Trends
<table>
  <tr>
    <td width="50%"><img src="utils/output5.png" alt="Sales Type Analysis"><br><b>5. Average Price by Sales Type</b></td>
    <td width="50%"><img src="utils/output6.png" alt="Scatter Plot Trend"><br><b>6. Size (sqm) vs. Price Relationship</b></td>
  </tr>
  <tr>
    <td width="50%"><img src="utils/output7.png" alt="Price Boxplots"><br><b>7. Regional Price Volatility (Boxplot)</b></td>
    <td width="50%"><img src="utils/output8.png" alt="Price over Time"><br><b>8. Yearly Construction Trends</b></td>
  </tr>
</table>

---

## 🤖 Machine Learning Performance

The final phase of the project focuses on predicting property values using an optimized **Random Forest Regressor**.

### Model Evaluation
<p align="center">
  <img src="utils/output9.png" width="600" alt="Actual vs Predicted Results"><br>
  <b>9. Model Accuracy: Actual vs. Predicted Values</b>
</p>

* **R² Score:** 0.9999 (Potential data leakage under investigation).
* **Optimization:** Hyperparameters tuned via `RandomizedSearchCV`.
* **Features:** Square meters, Year built, Region, and Number of rooms.

---

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Data Handling:** `pandas`, `numpy`, `pyarrow`
* **Visualization:** `matplotlib`, `seaborn`
* **Machine Learning:** `scikit-learn`