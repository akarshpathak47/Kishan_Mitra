import React, { useState } from 'react';
import './App.css'; 

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
    } else {
      setSelectedFile(null);
      setPreviewUrl(null);
    }
  };

  const handleSubmit = () => {
    if (selectedFile) {
      console.log("Image selected:", selectedFile.name);
      alert("Image uploaded! The backend connection will be added later.");
    } else {
      alert("Please select an image first.");
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
        <button onClick={handleSubmit} disabled={!selectedFile}>
          Check Health
        </button>
      </div>

      {previewUrl && (
        <div className="image-preview">
          <h2>Image Preview:</h2>
          <img src={previewUrl} alt="Crop Preview" className="preview-image" />
        </div>
      )}

      <footer>
        <p>© 2025 Kisan Mitra. Your Digital Farming Companion.</p>
      </footer>
    </div>
  );
}

export default App;