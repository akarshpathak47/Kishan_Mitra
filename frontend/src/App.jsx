import React, { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      setPreview(URL.createObjectURL(file));
      setResult(null); // Reset result when new image is uploaded
    }
  };

  const handleDetect = async () => {
    if (!image) return alert("Please upload an image first!");
    
    setLoading(true);
    setResult(null);

    // Prepare the form data to send the file
    const formData = new FormData();
    formData.append("file", image);

    try {
      // Connect to your Flask backend
      const response = await fetch("https://kishan-mitra-drh5.onrender.com//predict", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setResult({
          disease: data.disease,
          confidence: data.confidence,
          // Your backend returns an array of recommendations
          recommendations: data.recommendations || [] 
        });
      } else {
        alert("Server Error: " + (data.error || "Unknown error occurred"));
      }
    } catch (error) {
      console.error("Connection failed:", error);
      alert("Could not connect to the backend. Is app.py running on port 5000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🌱 Kishan Mitra</h1>
        <p>Upload a leaf image to detect possible diseases and treatments.</p>
      </header>

      <div className="upload-section">
        <div className="upload-box">
          {preview ? (
            <img src={preview} alt="Preview" className="preview-image" />
          ) : (
            <p className="upload-placeholder">Click to Upload Crop Image</p>
          )}
          <input type="file" accept="image/*" onChange={handleImageUpload} />
        </div>
        <button className="detect-btn" onClick={handleDetect} disabled={loading}>
          {loading ? "Analyzing..." : "Detect Disease"}
        </button>
      </div>

      {loading && (
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Processing image with AI...</p>
        </div>
      )}

      {result && (
        <div className="result-card">
          <h2>🔍 Detection Result</h2>
          <div className="result-info">
            <p><strong>Disease:</strong> {result.disease.replace(/___/g, " ").replace(/_/g, " ")}</p>
            <p><strong>Confidence:</strong> {result.confidence}</p>
          </div>
          
          <div className="treatment-section">
            <h3>📋 Recommended Actions:</h3>
            {result.recommendations.length > 0 ? (
              <ul>
                {result.recommendations.map((step, index) => (
                  <li key={index}>{step}</li>
                ))}
              </ul>
            ) : (
              <p>No specific recommendations found for this condition.</p>
            )}
          </div>
        </div>
      )}

      <footer className="footer">
        <p>Made with ❤️ for farmers | © 2025 Kishan Mitra</p>
      </footer>
    </div>
  );
}

export default App;
