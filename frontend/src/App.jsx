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
      setResult(null);
    }
  };

  const handleDetect = () => {
    if (!image) return alert("Please upload an image first!");
    setLoading(true);

    // Simulate API call
    setTimeout(() => {
      setResult({
        disease: "Leaf Spot",
        confidence: "92%",
        treatment: "Apply fungicide and maintain proper soil drainage.",
      });
      setLoading(false);
    }, 2000);
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>🌱 Plant Disease Detection</h1>
        <p>Upload a leaf image to detect possible diseases and treatments.</p>
      </header>

      <div className="upload-section">
        <div className="upload-box">
          {preview ? (
            <img src={preview} alt="Preview" className="preview-image" />
          ) : (
            <p className="upload-placeholder">Drag & Drop or Click to Upload Image</p>
          )}
          <input type="file" accept="image/*" onChange={handleImageUpload} />
        </div>
        <button className="detect-btn" onClick={handleDetect}>
          {loading ? "Detecting..." : "Detect Disease"}
        </button>
      </div>

      {loading && <div className="loading-spinner"></div>}

      {result && (
        <div className="result-card">
          <h2>🔍 Detection Result</h2>
          <p><strong>Disease:</strong> {result.disease}</p>
          <p><strong>Confidence:</strong> {result.confidence}</p>
          <p><strong>Treatment:</strong> {result.treatment}</p>
        </div>
      )}

      <footer className="footer">
        <p>Made with ❤️ for farmers | © 2025 Plant AI</p>
      </footer>
    </div>
  );
}

export default App;
