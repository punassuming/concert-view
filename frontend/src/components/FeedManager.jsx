import { useState, useEffect } from 'react'
import { getFeeds, createFeed, updateFeed, deleteFeed, uploadFeedVideo } from '../api/client'

export default function FeedManager() {
  const [feeds, setFeeds] = useState([])
  const [name, setName] = useState('')
  const [sourceUrl, setSourceUrl] = useState('')
  const [editingId, setEditingId] = useState(null)
  const [editOffset, setEditOffset] = useState(0)
  const [editVolume, setEditVolume] = useState(1.0)
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
      await createFeed({ name: name.trim(), source_url: sourceUrl.trim() })
      setName('')
      setSourceUrl('')
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
  }

  async function handleUpdate(id) {
    try {
      await updateFeed(id, { offset_seconds: Number(editOffset), volume: Number(editVolume) })
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
        <h2>Add Feed</h2>
        <form onSubmit={handleCreate} className="inline-form">
          <div className="form-group">
            <label>Name</label>
            <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Camera 1" />
          </div>
          <div className="form-group">
            <label>Source URL</label>
            <input value={sourceUrl} onChange={(e) => setSourceUrl(e.target.value)} placeholder="rtmp://..." />
          </div>
          <button type="submit" className="btn btn-primary">Add Feed</button>
        </form>
      </div>

      {error && (
        <div className="card" style={{ borderColor: '#e94560' }}>
          <p style={{ color: '#e94560' }}>{error}</p>
          <button className="btn btn-sm btn-secondary" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      <div className="card">
        <h2>Feeds</h2>
        {feeds.length === 0 ? (
          <p style={{ color: '#a0a0b0' }}>No feeds yet. Add one above.</p>
        ) : (
          <div className="grid">
            {feeds.map((feed) => (
              <div key={feed.id} className="card feed-item">
                <div className="feed-header">
                  <h3>{feed.name}</h3>
                  <span className={`status-badge ${feed.status === 'active' ? 'status-active' : 'status-inactive'}`}>
                    {feed.status || 'inactive'}
                  </span>
                </div>
                <div className="detail-row">
                  <span>Source</span>
                  <span>{feed.source_url || '—'}</span>
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
                    Upload
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
