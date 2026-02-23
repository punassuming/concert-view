const BASE_URL = import.meta.env.VITE_API_URL || '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })
  if (!res.ok) {
    const body = await res.text()
    throw new Error(`API error ${res.status}: ${body}`)
  }
  return res.json()
}

// Feeds
export function getFeeds() {
  return request('/feeds')
}

export function createFeed(data) {
  return request('/feeds', { method: 'POST', body: JSON.stringify(data) })
}

export function updateFeed(id, data) {
  return request(`/feeds/${id}`, { method: 'PUT', body: JSON.stringify(data) })
}

export function deleteFeed(id) {
  return request(`/feeds/${id}`, { method: 'DELETE' })
}

export function uploadFeedVideo(id, file) {
  const formData = new FormData()
  formData.append('file', file)
  return fetch(`${BASE_URL}/feeds/${id}/upload`, {
    method: 'POST',
    body: formData,
  }).then((res) => {
    if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
    return res.json()
  })
}

// Layouts
export function getLayouts() {
  return request('/layouts')
}

export function createLayout(data) {
  return request('/layouts', { method: 'POST', body: JSON.stringify(data) })
}

export function updateLayout(id, data) {
  return request(`/layouts/${id}`, { method: 'PUT', body: JSON.stringify(data) })
}

export function deleteLayout(id) {
  return request(`/layouts/${id}`, { method: 'DELETE' })
}

export function suggestLayout(data) {
  return request('/layouts/suggest', { method: 'POST', body: JSON.stringify(data) })
}

// Audio
export function syncAudio(data) {
  return request('/audio/sync', { method: 'POST', body: JSON.stringify(data) })
}

export function optimizeAudio(data) {
  return request('/audio/optimize', { method: 'POST', body: JSON.stringify(data) })
}
