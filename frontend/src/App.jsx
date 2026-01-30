import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [preview, setPreview] = useState(null)
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [history, setHistory] = useState([])

  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://localhost:8000/history')
      const data = await res.json()
      setHistory(data)
    } catch (err) {
      console.error("Failed to fetch history", err)
    }
  }

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    if (selectedFile) {
      const objectUrl = URL.createObjectURL(selectedFile)
      setPreview(objectUrl)
      setPrediction(null)
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const res = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      setPrediction(data)
      fetchHistory() // Refresh history
    } catch (error) {
      console.error('Error uploading file:', error)
      alert("Error processing image")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-container">
      <header className="header">
        <h1>🌿 Plant Disease AI</h1>
        <p>Advanced Deep Learning Diagnostics</p>
      </header>

      <main className="main-content">
        <div className="upload-section card">
          <h2>Analyze Leaf</h2>
          <div className="upload-area">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileChange}
              id="file-upload"
              className="file-input"
            />
            <label htmlFor="file-upload" className="file-label">
              {file ? file.name : "Click to Upload Image"}
            </label>
          </div>

          {preview && (
            <div className="preview-container">
              <img src={preview} alt="Preview" className="image-preview" />
            </div>
          )}

          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="analyze-btn"
          >
            {loading ? 'Processing...' : 'Diagnose Disease'}
          </button>

          {prediction && (
            <div className="result-container fade-in">
              <h3>Diagnosis Result</h3>
              <div className="result-metric">
                <span className="label">Observed Condition:</span>
                <span className="value highlight">{prediction.prediction}</span>
              </div>
              <div className="confidence-bar-container">
                <div
                  className="confidence-bar"
                  style={{ width: `${prediction.confidence * 100}%` }}
                ></div>
                <span className="confidence-text">
                  {(prediction.confidence * 100).toFixed(1)}% Confidence
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="history-section card">
          <h2>Recent Scans</h2>
          <div className="history-list">
            {history.map((item) => (
              <div key={item.id} className="history-item">
                <span className="history-pred">{item.prediction}</span>
                <span className="history-conf">{(item.confidence * 100).toFixed(0)}%</span>
                <span className="history-date">
                  {new Date(item.timestamp).toLocaleDateString()}
                </span>
              </div>
            ))}
            {history.length === 0 && <p className="no-history">No scan history yet.</p>}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
