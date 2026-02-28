import { useState } from 'react'
import { exportVideo, getJobStatus } from '../api/client'

const FORMAT_LABELS = {
  landscape_1080p: 'Landscape 1080p (16:9) – YouTube, general',
  portrait_1080p: 'Portrait 1080p (9:16) – TikTok, Reels, Shorts',
  square_1080: 'Square 1080 (1:1) – Instagram feed',
}

export default function ExportPanel() {
  const [inputPath, setInputPath] = useState('')
  const [outputFilename, setOutputFilename] = useState('output.mp4')
  const [format, setFormat] = useState('landscape_1080p')
  const [jobId, setJobId] = useState(null)
  const [jobStatus, setJobStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleExport(e) {
    e.preventDefault()
    if (!inputPath.trim() || !outputFilename.trim()) return
    setLoading(true)
    setError(null)
    setJobId(null)
    setJobStatus(null)
    try {
      const result = await exportVideo({
        input_path: inputPath.trim(),
        output_filename: outputFilename.trim(),
        format,
      })
      setJobId(result.job_id)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function checkStatus() {
    if (!jobId) return
    try {
      const status = await getJobStatus(jobId)
      setJobStatus(status)
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Export for Social Media</h2>
        <p style={{ color: '#a0a0b0', marginBottom: 16, fontSize: '0.9rem' }}>
          Re-encode a composed video file to a social media–ready format.
          Select a format preset that matches your target platform.
        </p>

        <form onSubmit={handleExport}>
          <div className="form-group">
            <label>Input File Path</label>
            <input
              value={inputPath}
              onChange={(e) => setInputPath(e.target.value)}
              placeholder="/data/output/composed.mp4"
            />
          </div>

          <div className="form-group">
            <label>Output Filename</label>
            <input
              value={outputFilename}
              onChange={(e) => setOutputFilename(e.target.value)}
              placeholder="export.mp4"
            />
          </div>

          <div className="form-group">
            <label>Format Preset</label>
            <select value={format} onChange={(e) => setFormat(e.target.value)}>
              {Object.entries(FORMAT_LABELS).map(([value, label]) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !inputPath.trim()}
          >
            {loading ? 'Submitting…' : '🚀 Export'}
          </button>
        </form>

        {jobId && (
          <div style={{ marginTop: 16 }}>
            <p style={{ color: '#a0a0b0', fontSize: '0.9rem' }}>
              Job submitted: <code>{jobId}</code>
            </p>
            <button className="btn btn-sm btn-secondary" onClick={checkStatus}>
              Check Status
            </button>
            {jobStatus && (
              <div className="results-box" style={{ marginTop: 8 }}>
                {JSON.stringify(jobStatus, null, 2)}
              </div>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="card" style={{ borderColor: '#e94560' }}>
          <p style={{ color: '#e94560' }}>{error}</p>
          <button className="btn btn-sm btn-secondary" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}
    </div>
  )
}
