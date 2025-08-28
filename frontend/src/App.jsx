import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

// This is the address of your local backend.
// It must be running on port 5000 for this to work.
const API_BASE_URL = 'http://127.0.0.1:5000';

function App() {
  // State variables to hold information about the user's interaction
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // This function runs when the user selects a file.
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Create a temporary URL to display the image preview in the browser.
      setPreviewUrl(URL.createObjectURL(file));
      // Reset any previous results or errors.
      setPrediction(null);
      setError(null);
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  // This function runs when the user clicks the 'Check Health' button.
  const handleSubmit = async () => {
    // Check if an image was selected.
    if (!selectedFile) {
      setError("Please select an image first.");
      return;
    }

    // Set loading state and clear previous results.
    setLoading(true);
    setError(null);
    setPrediction(null);

    // Create a FormData object to send the image file to the backend.
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      // Make a POST request to the backend's /predict endpoint.
      const response = await axios.post(`${API_BASE_URL}/predict`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Store the prediction data from the backend in the 'prediction' state.
      setPrediction(response.data);
    } catch (err) {
      // Handle different types of errors.
      console.error("Error during prediction:", err);
      if (err.response) {
        // Server responded with an error status code.
        setError(`Prediction failed: ${err.response.data.error || err.response.statusText}`);
      } else if (err.request) {
        // The request was sent but no response was received.
        setError("No response from server. Check if the backend is running at " + API_BASE_URL + ".");
      } else {
        // An unexpected error occurred.
        setError(`Error: ${err.message}`);
      }
    } finally {
      // Always stop the loading state.
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌿 Kisan Mitra 🌾</h1>
        <p>Upload a picture of your crop to check its health.</p>
      </header>

      <div className="upload-section">
        <h2>Upload Crop Image</h2>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        <button onClick={handleSubmit} disabled={!selectedFile || loading}>
          {loading ? 'Detecting...' : 'Check Health'}
        </button>
        {error && <p className="error-message">Error: {error}</p>}
      </div>

      {previewUrl && (
        <div className="image-preview">
          <h2>Image Preview:</h2>
          <img src={previewUrl} alt="Crop Preview" className="preview-image" />
        </div>
      )}

      {prediction && (
        <div className="prediction-results">
          <h2>Detection Results:</h2>
          <p><strong>Detected Condition:</strong> {prediction.disease}</p>
          <p><strong>Confidence:</strong> {prediction.confidence}</p>

          <h3>Recommendations:</h3>
          {prediction.recommendations ? (
            <div>
              {prediction.recommendations.symptoms && (
                <p><strong>Symptoms:</strong> {prediction.recommendations.symptoms}</p>
              )}
              {prediction.recommendations.prevention && prediction.recommendations.prevention.length > 0 && (
                <div>
                  <h4>Prevention:</h4>
                  <ul>
                    {prediction.recommendations.prevention.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              {prediction.recommendations.treatment_organic && prediction.recommendations.treatment_organic.length > 0 && (
                <div>
                  <h4>Organic Treatment:</h4>
                  <ul>
                    {prediction.recommendations.treatment_organic.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              {prediction.recommendations.treatment_chemical && prediction.recommendations.treatment_chemical.length > 0 && (
                <div>
                  <h4>Chemical Treatment:</h4>
                  <ul>
                    {prediction.recommendations.treatment_chemical.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                </div>
              )}
              {(!prediction.recommendations.symptoms &&
                prediction.recommendations.prevention.length === 0 &&
                prediction.recommendations.treatment_organic.length === 0 &&
                prediction.recommendations.treatment_chemical.length === 0) && (
                  <p>No specific recommendations available for this detected status.</p>
              )}
            </div>
          ) : (
            <p>No recommendations available for this detected status.</p>
          )}
        </div>
      )}

      <footer>
        <p>© 2025 Kisan Mitra. Your Digital Farming Companion.</p>
      </footer>
    </div>
  );
}

export default App;