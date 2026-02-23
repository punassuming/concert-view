import { useState, useEffect } from 'react'
import { getFeeds, syncAudio, optimizeAudio } from '../api/client'

export default function AudioControls() {
  const [feeds, setFeeds] = useState([])
  const [masterFeedId, setMasterFeedId] = useState('')
  const [normalize, setNormalize] = useState(true)
  const [noiseReduction, setNoiseReduction] = useState(false)
  const [syncResult, setSyncResult] = useState(null)
  const [optimizeResult, setOptimizeResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadFeeds()
  }, [])

  async function loadFeeds() {
    try {
      const data = await getFeeds()
      const list = Array.isArray(data) ? data : []
      setFeeds(list)
      if (list.length > 0 && !masterFeedId) {
        setMasterFeedId(list[0].id)
      }
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSync() {
    setLoading(true)
    setSyncResult(null)
    try {
      const feedIds = feeds.map((f) => f.id)
      const result = await syncAudio({ feed_ids: feedIds })
      setSyncResult(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleOptimize() {
    setLoading(true)
    setOptimizeResult(null)
    try {
      const result = await optimizeAudio({
        master_feed_id: masterFeedId,
        normalize,
        noise_reduction: noiseReduction,
      })
      setOptimizeResult(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Audio Sync Analysis</h2>
        <p style={{ color: '#a0a0b0', marginBottom: 12, fontSize: '0.9rem' }}>
          Analyze audio across all feeds to detect timing offsets and synchronization issues.
        </p>
        <button className="btn btn-primary" onClick={handleSync} disabled={loading || feeds.length === 0}>
          {loading ? 'Analyzing...' : 'Run Sync Analysis'}
        </button>
        {syncResult && (
          <div className="results-box">
            {JSON.stringify(syncResult, null, 2)}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Audio Optimization</h2>

        <div className="form-group">
          <label>Master Feed</label>
          <select value={masterFeedId} onChange={(e) => setMasterFeedId(e.target.value)}>
            {feeds.map((feed) => (
              <option key={feed.id} value={feed.id}>
                {feed.name}
              </option>
            ))}
          </select>
        </div>

        <div className="toggle-row">
          <span>Normalize Audio Levels</span>
          <button
            type="button"
            className={`toggle-switch ${normalize ? 'on' : ''}`}
            onClick={() => setNormalize(!normalize)}
          />
        </div>

        <div className="toggle-row">
          <span>Noise Reduction</span>
          <button
            type="button"
            className={`toggle-switch ${noiseReduction ? 'on' : ''}`}
            onClick={() => setNoiseReduction(!noiseReduction)}
          />
        </div>

        <button
          className="btn btn-primary"
          onClick={handleOptimize}
          disabled={loading || !masterFeedId}
          style={{ marginTop: 12 }}
        >
          {loading ? 'Optimizing...' : 'Run Optimization'}
        </button>

        {optimizeResult && (
          <div className="results-box">
            {JSON.stringify(optimizeResult, null, 2)}
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
