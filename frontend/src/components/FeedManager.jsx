import { useState, useEffect } from 'react'
import { getFeeds, createFeed, updateFeed, deleteFeed, uploadFeedVideo } from '../api/client'

export default function FeedManager() {
  const [feeds, setFeeds] = useState([])
  const [name, setName] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [editOffset, setEditOffset] = useState(0)
  const [editVolume, setEditVolume] = useState(1.0)
  const [editTrimStart, setEditTrimStart] = useState('')
  const [editTrimEnd, setEditTrimEnd] = useState('')
  const [error, setError] = useState(null)

  useEffect(() => {
    loadFeeds()
  }, [])

  async function loadFeeds() {
    try {
      const data = await getFeeds()
      setFeeds(Array.isArray(data) ? data : [])
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleCreate(e) {
    e.preventDefault()
    if (!name.trim()) return
    try {
      await createFeed({ name: name.trim() })
      setName('')
      loadFeeds()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    try {
      await deleteFeed(id)
      loadFeeds()
    } catch (err) {
      setError(err.message)
    }
  }

  function startEdit(feed) {
    setEditingId(feed.id)
    setEditOffset(feed.offset_seconds || 0)
    setEditVolume(feed.volume || 1.0)
    setEditTrimStart(feed.trim_start != null ? feed.trim_start : '')
    setEditTrimEnd(feed.trim_end != null ? feed.trim_end : '')
  }

  async function handleUpdate(id) {
    try {
      const patch = {
        offset_seconds: Number(editOffset),
        volume: Number(editVolume),
        trim_start: editTrimStart !== '' ? Number(editTrimStart) : null,
        trim_end: editTrimEnd !== '' ? Number(editTrimEnd) : null,
      }
      await updateFeed(id, patch)
      setEditingId(null)
      loadFeeds()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleUpload(id, file) {
    try {
      await uploadFeedVideo(id, file)
      loadFeeds()
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Add Video Clip</h2>
        <form onSubmit={handleCreate} className="inline-form">
          <div className="form-group">
            <label>Name</label>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Camera 1" />
          </div>
          <button type="submit" className="btn btn-primary">Add Clip</button>
        </form>
      </div>

      {error && (
        <div className="card" style={{ borderColor: '#e94560' }}>
          <p style={{ color: '#e94560' }}>{error}</p>
          <button className="btn btn-sm btn-secondary" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      <div className="card">
        <h2>Video Clips</h2>
        {feeds.length === 0 ? (
          <p style={{ color: '#a0a0b0' }}>No clips yet. Add one above, then upload a video file.</p>
        ) : (
          <div className="grid">
            {feeds.map((feed) => (
              <div key={feed.id} className="card feed-item">
                <div className="feed-header">
                  <h3>{feed.name}</h3>
                  <span className={`status-badge ${feed.file_path ? 'status-active' : 'status-inactive'}`}>
                    {feed.file_path ? 'file loaded' : 'no file'}
                  </span>
                </div>
                {feed.file_path && (
                  <div className="detail-row">
                    <span>File</span>
                    <span style={{ fontSize: '0.8rem', wordBreak: 'break-all' }}>{feed.file_path.split('/').pop()}</span>
                  </div>
                )}
                {feed.duration_seconds != null && (
                  <div className="detail-row">
                    <span>Duration</span>
                    <span>{feed.duration_seconds.toFixed(1)}s</span>
                  </div>
                )}
                <div className="detail-row">
                  <span>Trim</span>
                  <span>
                    {feed.trim_start != null ? `${feed.trim_start}s` : 'start'}
                    {' → '}
                    {feed.trim_end != null ? `${feed.trim_end}s` : 'end'}
                  </span>
                </div>
                <div className="detail-row">
                  <span>Offset</span>
                  <span>{feed.offset_seconds || 0}s</span>
                </div>
                <div className="detail-row">
                  <span>Volume</span>
                  <span>{feed.volume ?? 1.0}</span>
                </div>

                {editingId === feed.id && (
                  <div className="edit-form">
                    <div className="form-group">
                      <label>Trim Start (seconds)</label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        placeholder="beginning"
                        value={editTrimStart}
                        onChange={(e) => setEditTrimStart(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label>Trim End (seconds)</label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        placeholder="end of clip"
                        value={editTrimEnd}
                        onChange={(e) => setEditTrimEnd(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label>Offset (seconds)</label>
                      <input
                        type="number"
                        step="0.1"
                        value={editOffset}
                        onChange={(e) => setEditOffset(e.target.value)}
                      />
                    </div>
                    <div className="form-group">
                      <label>Volume (0–1)</label>
                      <input
                        type="number"
                        step="0.1"
                        min="0"
                        max="1"
                        value={editVolume}
                        onChange={(e) => setEditVolume(e.target.value)}
                      />
                    </div>
                    <div className="actions">
                      <button className="btn btn-sm btn-primary" onClick={() => handleUpdate(feed.id)}>Save</button>
                      <button className="btn btn-sm btn-secondary" onClick={() => setEditingId(null)}>Cancel</button>
                    </div>
                  </div>
                )}

                <div className="actions">
                  <button className="btn btn-sm btn-secondary" onClick={() => startEdit(feed)}>Edit</button>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(feed.id)}>Delete</button>
                  <label className="btn btn-sm btn-secondary" style={{ cursor: 'pointer' }}>
                    Upload File
                    <input
                      type="file"
                      accept="video/*,audio/*"
                      style={{ display: 'none' }}
                      onChange={(e) => {
                        if (e.target.files[0]) handleUpload(feed.id, e.target.files[0])
                      }}
                    />
                  </label>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
