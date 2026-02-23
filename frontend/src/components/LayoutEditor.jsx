import { useState, useEffect } from 'react'
import { getLayouts, createLayout, updateLayout, deleteLayout, suggestLayout } from '../api/client'

const PRESETS = {
  Grid: [
    { feed_id: 'feed-1', x: 0, y: 0, width: 0.5, height: 0.5 },
    { feed_id: 'feed-2', x: 0.5, y: 0, width: 0.5, height: 0.5 },
    { feed_id: 'feed-3', x: 0, y: 0.5, width: 0.5, height: 0.5 },
    { feed_id: 'feed-4', x: 0.5, y: 0.5, width: 0.5, height: 0.5 },
  ],
  'Picture-in-Picture': [
    { feed_id: 'feed-1', x: 0, y: 0, width: 1, height: 1 },
    { feed_id: 'feed-2', x: 0.7, y: 0.7, width: 0.28, height: 0.28 },
  ],
}

export default function LayoutEditor() {
  const [layouts, setLayouts] = useState([])
  const [layoutName, setLayoutName] = useState('')
  const [slots, setSlots] = useState([])
  const [error, setError] = useState(null)
  const [suggestResult, setSuggestResult] = useState(null)

  useEffect(() => {
    loadLayouts()
  }, [])

  async function loadLayouts() {
    try {
      const data = await getLayouts()
      setLayouts(Array.isArray(data) ? data : [])
    } catch (err) {
      setError(err.message)
    }
  }

  function addSlot() {
    setSlots([...slots, { feed_id: `feed-${slots.length + 1}`, x: 0, y: 0, width: 0.5, height: 0.5 }])
  }

  function updateSlot(index, field, value) {
    const updated = slots.map((s, i) =>
      i === index ? { ...s, [field]: Number(value) / 100 } : s
    )
    setSlots(updated)
  }

  function removeSlot(index) {
    setSlots(slots.filter((_, i) => i !== index))
  }

  function applyPreset(name) {
    setSlots([...PRESETS[name]])
    setLayoutName(name)
  }

  async function handleCreate(e) {
    e.preventDefault()
    if (!layoutName.trim() || slots.length === 0) return
    try {
      await createLayout({ name: layoutName.trim(), slots })
      setLayoutName('')
      setSlots([])
      loadLayouts()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleDelete(id) {
    try {
      await deleteLayout(id)
      loadLayouts()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleSuggest() {
    try {
      const result = await suggestLayout({ feed_count: 4, style: 'grid' })
      setSuggestResult(result)
      if (result.layout && result.layout.slots) {
        setSlots(result.layout.slots)
        setLayoutName(result.layout.name || 'AI Suggested')
      }
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Layout Preview</h2>
        <div className="layout-preview">
          {slots.map((slot, i) => (
            <div
              key={i}
              className="layout-slot"
              style={{
                left: `${slot.x * 100}%`,
                top: `${slot.y * 100}%`,
                width: `${slot.width * 100}%`,
                height: `${slot.height * 100}%`,
              }}
            >
              Slot {i + 1}
            </div>
          ))}
          {slots.length === 0 && (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#a0a0b0' }}>
              Add slots or select a preset
            </div>
          )}
        </div>
      </div>

      <div className="card">
        <h2>Create Layout</h2>
        <div className="preset-buttons">
          {Object.keys(PRESETS).map((name) => (
            <button key={name} className="btn btn-secondary" onClick={() => applyPreset(name)}>
              {name}
            </button>
          ))}
          <button className="btn btn-primary" onClick={handleSuggest}>
            🤖 AI Suggest
          </button>
        </div>

        <form onSubmit={handleCreate}>
          <div className="form-group">
            <label>Layout Name</label>
            <input value={layoutName} onChange={(e) => setLayoutName(e.target.value)} placeholder="My Layout" />
          </div>

          {slots.map((slot, i) => (
            <div key={i} style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
                <span style={{ fontSize: '0.85rem', color: '#a0a0b0' }}>Slot {i + 1}</span>
                <button type="button" className="btn btn-sm btn-danger" onClick={() => removeSlot(i)}>Remove</button>
              </div>
              <div className="slot-controls">
                <div className="form-group">
                  <label>X (%)</label>
                  <input type="number" min="0" max="100" value={Math.round(slot.x * 100)} onChange={(e) => updateSlot(i, 'x', e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Y (%)</label>
                  <input type="number" min="0" max="100" value={Math.round(slot.y * 100)} onChange={(e) => updateSlot(i, 'y', e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Width (%)</label>
                  <input type="number" min="1" max="100" value={Math.round(slot.width * 100)} onChange={(e) => updateSlot(i, 'width', e.target.value)} />
                </div>
                <div className="form-group">
                  <label>Height (%)</label>
                  <input type="number" min="1" max="100" value={Math.round(slot.height * 100)} onChange={(e) => updateSlot(i, 'height', e.target.value)} />
                </div>
              </div>
            </div>
          ))}

          <div className="actions">
            <button type="button" className="btn btn-secondary" onClick={addSlot}>+ Add Slot</button>
            <button type="submit" className="btn btn-primary">Save Layout</button>
          </div>
        </form>

        {suggestResult && (
          <div className="results-box">
            {JSON.stringify(suggestResult, null, 2)}
          </div>
        )}
      </div>

      {error && (
        <div className="card" style={{ borderColor: '#e94560' }}>
          <p style={{ color: '#e94560' }}>{error}</p>
          <button className="btn btn-sm btn-secondary" onClick={() => setError(null)}>Dismiss</button>
        </div>
      )}

      <div className="card">
        <h2>Saved Layouts</h2>
        {layouts.length === 0 ? (
          <p style={{ color: '#a0a0b0' }}>No layouts saved yet.</p>
        ) : (
          <div className="grid">
            {layouts.map((layout) => (
              <div key={layout.id} className="card feed-item">
                <div className="feed-header">
                  <h3>{layout.name}</h3>
                  <span style={{ fontSize: '0.85rem', color: '#a0a0b0' }}>
                    {layout.slots?.length || 0} slots
                  </span>
                </div>
                <div className="layout-preview" style={{ height: 120 }}>
                  {(layout.slots || []).map((slot, i) => (
                    <div
                      key={i}
                      className="layout-slot"
                      style={{
                        left: `${(slot.x || 0) * 100}%`,
                        top: `${(slot.y || 0) * 100}%`,
                        width: `${(slot.width || 0.25) * 100}%`,
                        height: `${(slot.height || 0.25) * 100}%`,
                      }}
                    >
                      {i + 1}
                    </div>
                  ))}
                </div>
                <div className="actions">
                  <button className="btn btn-sm btn-danger" onClick={() => handleDelete(layout.id)}>Delete</button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
