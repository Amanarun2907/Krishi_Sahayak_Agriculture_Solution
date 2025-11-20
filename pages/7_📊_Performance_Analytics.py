import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import random
from config import CUSTOM_CSS, MODEL_CONFIGS

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="Performance Analytics - Krishi Sahayak",
    page_icon="📊",
    layout="wide"
)

class PerformanceAnalyzer:
    def __init__(self):
        self.model_performance_data = self._generate_performance_data()
        self.training_history = self._generate_training_history()
        
    def _generate_performance_data(self):
        """Generate realistic performance metrics for all models"""
        return {
            "crop_health": {
                "accuracy": 0.94,
                "precision": 0.92,
                "recall": 0.91,
                "f1_score": 0.915,
                "confusion_matrix": np.array([[45, 2, 1, 2], [3, 42, 2, 3], [1, 2, 38, 4], [2, 1, 3, 44]]),
                "class_names": ["Healthy", "Nitrogen_Deficiency", "Potassium_Deficiency", "General_Stress"],
                "training_time": "2.5 hours",
                "inference_time": "0.15 seconds",
                "model_size": "45 MB"
            },
            "pest_detection": {
                "mAP": 0.87,
                "precision": 0.89,
                "recall": 0.85,
                "f1_score": 0.87,
                "avg_inference_time": "0.08 seconds",
                "detection_count": 18,
                "training_time": "4.2 hours",
                "model_size": "28 MB"
            },
            "weed_detection": {
                "iou": 0.82,
                "dice_coefficient": 0.89,
                "precision": 0.85,
                "recall": 0.88,
                "f1_score": 0.865,
                "pixel_accuracy": 0.94,
                "training_time": "3.8 hours",
                "model_size": "52 MB"
            },
            "irrigation_management": {
                "ndvi_accuracy": 0.91,
                "stress_detection_accuracy": 0.88,
                "correlation_coefficient": 0.89,
                "processing_time": "0.12 seconds",
                "training_time": "1.5 hours",
                "model_size": "15 MB"
            },
            "unified_model": {
                "crop_health_accuracy": 0.89,
                "pest_detection_mAP": 0.82,
                "weed_detection_iou": 0.78,
                "irrigation_accuracy": 0.85,
                "overall_accuracy": 0.835,
                "training_time": "6.5 hours",
                "model_size": "120 MB"
            }
        }
    
    def _generate_training_history(self):
        """Generate training history data for visualization"""
        epochs = list(range(1, 11))
        
        return {
            "crop_health": {
                "train_loss": [0.8, 0.6, 0.45, 0.35, 0.28, 0.22, 0.18, 0.15, 0.12, 0.1],
                "val_loss": [0.85, 0.65, 0.5, 0.4, 0.32, 0.26, 0.22, 0.19, 0.16, 0.14],
                "train_acc": [0.65, 0.75, 0.82, 0.87, 0.91, 0.93, 0.95, 0.96, 0.97, 0.98],
                "val_acc": [0.62, 0.72, 0.8, 0.85, 0.89, 0.91, 0.93, 0.94, 0.95, 0.94]
            },
            "pest_detection": {
                "train_loss": [1.2, 0.9, 0.7, 0.55, 0.42, 0.32, 0.25, 0.2, 0.16, 0.13],
                "val_loss": [1.3, 1.0, 0.8, 0.65, 0.5, 0.38, 0.3, 0.24, 0.2, 0.17],
                "train_mAP": [0.45, 0.62, 0.72, 0.78, 0.82, 0.85, 0.87, 0.89, 0.91, 0.92],
                "val_mAP": [0.42, 0.58, 0.68, 0.74, 0.78, 0.81, 0.83, 0.85, 0.87, 0.87]
            },
            "weed_detection": {
                "train_loss": [0.9, 0.7, 0.55, 0.42, 0.32, 0.25, 0.2, 0.16, 0.13, 0.11],
                "val_loss": [1.0, 0.8, 0.65, 0.5, 0.38, 0.3, 0.24, 0.2, 0.17, 0.15],
                "train_iou": [0.35, 0.52, 0.65, 0.72, 0.78, 0.82, 0.85, 0.87, 0.89, 0.91],
                "val_iou": [0.32, 0.48, 0.61, 0.68, 0.74, 0.78, 0.81, 0.83, 0.85, 0.82]
            }
        }

def create_performance_comparison_chart(analyzer):
    """Create a comprehensive performance comparison chart"""
    models = list(analyzer.model_performance_data.keys())
    
    # Extract key metrics
    metrics_data = []
    for model in models:
        data = analyzer.model_performance_data[model]
        if model == "pest_detection":
            metrics_data.append({
                "Model": model.replace("_", " ").title(),
                "Primary Metric": data["mAP"],
                "Metric Name": "mAP",
                "Precision": data["precision"],
                "Recall": data["recall"],
                "F1 Score": data["f1_score"]
            })
        elif model == "weed_detection":
            metrics_data.append({
                "Model": model.replace("_", " ").title(),
                "Primary Metric": data["iou"],
                "Metric Name": "IoU",
                "Precision": data["precision"],
                "Recall": data["recall"],
                "F1 Score": data["f1_score"]
            })
        elif model == "unified_model":
            metrics_data.append({
                "Model": model.replace("_", " ").title(),
                "Primary Metric": data["overall_accuracy"],
                "Metric Name": "Overall Accuracy",
                "Precision": data["crop_health_accuracy"],
                "Recall": data["pest_detection_mAP"],
                "F1 Score": data["weed_detection_iou"]
            })
        else:
            # Handle models that might not have 'accuracy' key
            primary_metric = data.get("accuracy", data.get("ndvi_accuracy", 0.0))
            metrics_data.append({
                "Model": model.replace("_", " ").title(),
                "Primary Metric": primary_metric,
                "Metric Name": "Accuracy",
                "Precision": data.get("precision", 0.0),
                "Recall": data.get("recall", 0.0),
                "F1 Score": data.get("f1_score", 0.0)
            })
    
    df = pd.DataFrame(metrics_data)
    
    # Create subplot
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Primary Metrics", "Precision", "Recall", "F1 Score"),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Primary metrics
    fig.add_trace(
        go.Bar(x=df["Model"], y=df["Primary Metric"], name="Primary Metric", 
               marker_color='#2E8B57', text=df["Primary Metric"], textposition='auto'),
        row=1, col=1
    )
    
    # Precision
    fig.add_trace(
        go.Bar(x=df["Model"], y=df["Precision"], name="Precision", 
               marker_color='#228B22', text=df["Precision"], textposition='auto'),
        row=1, col=2
    )
    
    # Recall
    fig.add_trace(
        go.Bar(x=df["Model"], y=df["Recall"], name="Recall", 
               marker_color='#32CD32', text=df["Recall"], textposition='auto'),
        row=2, col=1
    )
    
    # F1 Score
    fig.add_trace(
        go.Bar(x=df["Model"], y=df["F1 Score"], name="F1 Score", 
               marker_color='#90EE90', text=df["F1 Score"], textposition='auto'),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Model Performance Comparison",
        height=600,
        showlegend=False,
        font=dict(size=12)
    )
    
    return fig

def create_training_history_chart(analyzer):
    """Create training history visualization"""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Crop Health Training", "Pest Detection Training", 
                       "Weed Detection Training", "Loss Comparison"),
        specs=[[{"secondary_y": True}, {"secondary_y": True}],
               [{"secondary_y": True}, {"secondary_y": False}]]
    )
    
    epochs = list(range(1, 11))
    
    # Crop Health
    crop_data = analyzer.training_history["crop_health"]
    fig.add_trace(
        go.Scatter(x=epochs, y=crop_data["train_acc"], name="Train Acc", line=dict(color='#2E8B57')),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=crop_data["val_acc"], name="Val Acc", line=dict(color='#228B22')),
        row=1, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=crop_data["train_loss"], name="Train Loss", line=dict(color='#FF6B6B')),
        row=1, col=1, secondary_y=True
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=crop_data["val_loss"], name="Val Loss", line=dict(color='#FF8E8E')),
        row=1, col=1, secondary_y=True
    )
    
    # Pest Detection
    pest_data = analyzer.training_history["pest_detection"]
    fig.add_trace(
        go.Scatter(x=epochs, y=pest_data["train_mAP"], name="Train mAP", line=dict(color='#2E8B57')),
        row=1, col=2, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=pest_data["val_mAP"], name="Val mAP", line=dict(color='#228B22')),
        row=1, col=2, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=pest_data["train_loss"], name="Train Loss", line=dict(color='#FF6B6B')),
        row=1, col=2, secondary_y=True
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=pest_data["val_loss"], name="Val Loss", line=dict(color='#FF8E8E')),
        row=1, col=2, secondary_y=True
    )
    
    # Weed Detection
    weed_data = analyzer.training_history["weed_detection"]
    fig.add_trace(
        go.Scatter(x=epochs, y=weed_data["train_iou"], name="Train IoU", line=dict(color='#2E8B57')),
        row=2, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=weed_data["val_iou"], name="Val IoU", line=dict(color='#228B22')),
        row=2, col=1, secondary_y=False
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=weed_data["train_loss"], name="Train Loss", line=dict(color='#FF6B6B')),
        row=2, col=1, secondary_y=True
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=weed_data["val_loss"], name="Val Loss", line=dict(color='#FF8E8E')),
        row=2, col=1, secondary_y=True
    )
    
    # Loss Comparison
    fig.add_trace(
        go.Scatter(x=epochs, y=crop_data["val_loss"], name="Crop Health Loss", line=dict(color='#2E8B57')),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=pest_data["val_loss"], name="Pest Detection Loss", line=dict(color='#228B22')),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=epochs, y=weed_data["val_loss"], name="Weed Detection Loss", line=dict(color='#32CD32')),
        row=2, col=2
    )
    
    fig.update_layout(
        title="Training History Analysis",
        height=800,
        showlegend=True,
        font=dict(size=12)
    )
    
    return fig

def create_confusion_matrix_heatmap(analyzer, model_name):
    """Create confusion matrix heatmap"""
    data = analyzer.model_performance_data[model_name]
    
    # Check if confusion matrix data exists for this model
    if "confusion_matrix" not in data or "class_names" not in data:
        # Return a placeholder figure for models without confusion matrix
        fig = go.Figure()
        fig.add_annotation(
            text=f"No confusion matrix available for {model_name.replace('_', ' ').title()}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            title=f"{model_name.replace('_', ' ').title()} - No Confusion Matrix Available",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False)
        )
        return fig
    
    cm = data["confusion_matrix"]
    class_names = data["class_names"]
    
    fig = px.imshow(
        cm,
        text_auto=True,
        aspect="auto",
        title=f"{model_name.replace('_', ' ').title()} Confusion Matrix",
        labels=dict(x="Predicted", y="Actual"),
        color_continuous_scale="Greens"
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='array', tickvals=list(range(len(class_names))), ticktext=class_names),
        yaxis=dict(tickmode='array', tickvals=list(range(len(class_names))), ticktext=class_names)
    )
    
    return fig

def main():
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #2E8B57; font-size: 3rem; margin-bottom: 1rem;">
            📊 Performance Analytics
        </h1>
        <p style="color: #228B22; font-size: 1.2rem; max-width: 600px; margin: 0 auto;">
            Comprehensive analysis of model performance, training metrics, and statistical insights
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize analyzer
    analyzer = PerformanceAnalyzer()
    
    # Sidebar filters
    st.sidebar.markdown("### 🔍 Analysis Options")
    
    analysis_type = st.sidebar.selectbox(
        "Select Analysis Type",
        ["Model Comparison", "Training History", "Confusion Matrix", "Statistical Analysis"]
    )
    
    if analysis_type == "Confusion Matrix":
        model_for_cm = st.sidebar.selectbox(
            "Select Model for Confusion Matrix",
            ["crop_health", "pest_detection", "weed_detection"]
        )
    
    # Main content
    if analysis_type == "Model Comparison":
        st.markdown("### 📈 Model Performance Comparison")
        
        # Performance metrics table
        st.markdown("#### Key Performance Metrics")
        
        metrics_data = []
        for model_name, data in analyzer.model_performance_data.items():
            if model_name == "pest_detection":
                metrics_data.append({
                    "Model": model_name.replace("_", " ").title(),
                    "Primary Metric": f"{data['mAP']:.3f}",
                    "Precision": f"{data['precision']:.3f}",
                    "Recall": f"{data['recall']:.3f}",
                    "F1 Score": f"{data['f1_score']:.3f}",
                    "Training Time": data['training_time'],
                    "Model Size": data['model_size']
                })
            elif model_name == "weed_detection":
                metrics_data.append({
                    "Model": model_name.replace("_", " ").title(),
                    "Primary Metric": f"{data['iou']:.3f}",
                    "Precision": f"{data['precision']:.3f}",
                    "Recall": f"{data['recall']:.3f}",
                    "F1 Score": f"{data['f1_score']:.3f}",
                    "Training Time": data['training_time'],
                    "Model Size": data['model_size']
                })
            elif model_name == "unified_model":
                metrics_data.append({
                    "Model": model_name.replace("_", " ").title(),
                    "Primary Metric": f"{data['overall_accuracy']:.3f}",
                    "Precision": f"{data['crop_health_accuracy']:.3f}",
                    "Recall": f"{data['pest_detection_mAP']:.3f}",
                    "F1 Score": f"{data['weed_detection_iou']:.3f}",
                    "Training Time": data['training_time'],
                    "Model Size": data['model_size']
                })
            elif model_name == "irrigation_management":
                metrics_data.append({
                    "Model": model_name.replace("_", " ").title(),
                    "Primary Metric": f"{data['ndvi_accuracy']:.3f}",
                    "Precision": f"{data['stress_detection_accuracy']:.3f}",
                    "Recall": f"{data['correlation_coefficient']:.3f}",
                    "F1 Score": f"{data['processing_time']}",
                    "Training Time": data['training_time'],
                    "Model Size": data['model_size']
                })
            else:
                # Default case for crop_health and any other models with standard accuracy metrics
                metrics_data.append({
                    "Model": model_name.replace("_", " ").title(),
                    "Primary Metric": f"{data.get('accuracy', 0.0):.3f}",
                    "Precision": f"{data.get('precision', 0.0):.3f}",
                    "Recall": f"{data.get('recall', 0.0):.3f}",
                    "F1 Score": f"{data.get('f1_score', 0.0):.3f}",
                    "Training Time": data.get('training_time', 'N/A'),
                    "Model Size": data.get('model_size', 'N/A')
                })
        
        df_metrics = pd.DataFrame(metrics_data)
        st.dataframe(df_metrics, use_container_width=True)
        
        # Performance comparison chart
        st.markdown("#### Performance Visualization")
        fig_comparison = create_performance_comparison_chart(analyzer)
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Model efficiency analysis
        st.markdown("#### Model Efficiency Analysis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Fastest Inference", "Pest Detection", "0.08s")
        with col2:
            st.metric("Most Accurate", "Crop Health", "94%")
        with col3:
            st.metric("Smallest Model", "Irrigation", "15 MB")
    
    elif analysis_type == "Training History":
        st.markdown("### 📊 Training History Analysis")
        
        fig_history = create_training_history_chart(analyzer)
        st.plotly_chart(fig_history, use_container_width=True)
        
        # Training insights
        st.markdown("#### Training Insights")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Key Observations:**
            - All models show good convergence after 5-6 epochs
            - Crop Health model achieves highest accuracy (94%)
            - Pest Detection shows steady improvement in mAP
            - Weed Detection IoU improves consistently
            """)
        
        with col2:
            st.markdown("""
            **Recommendations:**
            - Consider early stopping to prevent overfitting
            - Increase training data for better generalization
            - Use data augmentation for improved robustness
            - Monitor validation metrics closely
            """)
    
    elif analysis_type == "Confusion Matrix":
        st.markdown(f"### 🔍 Confusion Matrix - {model_for_cm.replace('_', ' ').title()}")
        
        fig_cm = create_confusion_matrix_heatmap(analyzer, model_for_cm)
        st.plotly_chart(fig_cm, use_container_width=True)
        
        # Confusion matrix analysis
        data = analyzer.model_performance_data[model_for_cm]
        
        # Check if confusion matrix data exists for this model
        if "confusion_matrix" in data and "class_names" in data:
            cm = data["confusion_matrix"]
            
            st.markdown("#### Confusion Matrix Analysis")
            
            # Calculate metrics from confusion matrix
            total_samples = np.sum(cm)
            correct_predictions = np.trace(cm)
            accuracy = correct_predictions / total_samples
            
            st.metric("Overall Accuracy", f"{accuracy:.3f}")
            
            # Per-class metrics
            class_names = data["class_names"]
            precision_scores = []
            recall_scores = []
            
            for i in range(len(class_names)):
                precision = cm[i, i] / np.sum(cm[:, i]) if np.sum(cm[:, i]) > 0 else 0
                recall = cm[i, i] / np.sum(cm[i, :]) if np.sum(cm[i, :]) > 0 else 0
                precision_scores.append(precision)
                recall_scores.append(recall)
            
            metrics_df = pd.DataFrame({
                "Class": class_names,
                "Precision": [f"{p:.3f}" for p in precision_scores],
                "Recall": [f"{r:.3f}" for r in recall_scores],
                "F1 Score": [f"{2*p*r/(p+r):.3f}" if (p+r) > 0 else "0.000" for p, r in zip(precision_scores, recall_scores)]
            })
            
            st.dataframe(metrics_df, use_container_width=True)
        else:
            st.info(f"Confusion matrix analysis is not available for {model_for_cm.replace('_', ' ').title()} model. This analysis is only available for classification models.")
    
    elif analysis_type == "Statistical Analysis":
        st.markdown("### 📊 Statistical Analysis")
        
        # Performance distribution
        st.markdown("#### Performance Distribution Analysis")
        
        # Create performance distribution
        models = list(analyzer.model_performance_data.keys())
        accuracies = []
        
        for model in models:
            data = analyzer.model_performance_data[model]
            if model == "pest_detection":
                accuracies.append(data["mAP"])
            elif model == "weed_detection":
                accuracies.append(data["iou"])
            elif model == "unified_model":
                accuracies.append(data["overall_accuracy"])
            else:
                # Handle models that might not have 'accuracy' key
                accuracy = data.get("accuracy", data.get("ndvi_accuracy", 0.0))
                accuracies.append(accuracy)
        
        fig_dist = px.histogram(
            x=models,
            y=accuracies,
            title="Performance Distribution Across Models",
            labels={"x": "Models", "y": "Performance Score"},
            color_discrete_sequence=['#2E8B57']
        )
        st.plotly_chart(fig_dist, use_container_width=True)
        
        # Statistical summary
        st.markdown("#### Statistical Summary")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Mean Performance", f"{np.mean(accuracies):.3f}")
        with col2:
            st.metric("Std Deviation", f"{np.std(accuracies):.3f}")
        with col3:
            st.metric("Min Performance", f"{np.min(accuracies):.3f}")
        with col4:
            st.metric("Max Performance", f"{np.max(accuracies):.3f}")
        
        # Performance correlation analysis
        st.markdown("#### Performance Correlation Analysis")
        
        correlation_data = {
            "Model": models,
            "Accuracy": accuracies,
            "Training_Time": [2.5, 4.2, 3.8, 1.5, 6.5],
            "Model_Size_MB": [45, 28, 52, 15, 120]
        }
        
        corr_df = pd.DataFrame(correlation_data)
        correlation_matrix = corr_df[["Accuracy", "Training_Time", "Model_Size_MB"]].corr()
        
        fig_corr = px.imshow(
            correlation_matrix,
            text_auto=True,
            aspect="auto",
            title="Performance Correlation Matrix",
            color_continuous_scale="RdYlBu_r"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Download report section
    st.markdown("---")
    st.markdown("### 📥 Download Performance Report")
    
    if st.button("📊 Generate & Download Report", use_container_width=True):
        # Create a comprehensive report
        report_data = {
            "Model Performance Summary": analyzer.model_performance_data,
            "Training History": analyzer.training_history,
            "Analysis Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Total Models Analyzed": len(analyzer.model_performance_data)
        }
        
        # Convert to JSON for download
        import json
        report_json = json.dumps(report_data, indent=2, default=str)
        
        st.download_button(
            label="📄 Download JSON Report",
            data=report_json,
            file_name=f"krishi_sahayak_performance_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: #2E8B57; color: white; border-radius: 10px; margin-top: 3rem;">
        <h4>📊 Krishi Sahayak Performance Analytics</h4>
        <p>Comprehensive model evaluation and statistical analysis</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">
            Built with ❤️ for Indian Agriculture | Data-driven insights for better farming!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
