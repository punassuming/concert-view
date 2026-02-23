const BASE_URL = import.meta.env.VITE_API_URL || ''

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}/api${path}`, {
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
  return request(`/feeds/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
}

export async function deleteFeed(id) {
  const res = await fetch(`${BASE_URL}/api/feeds/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`API error ${res.status}`)
}

export function uploadFeedVideo(id, file) {
  const formData = new FormData()
  formData.append('file', file)
  return fetch(`${BASE_URL}/api/feeds/${id}/upload`, {
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
  return request(`/layouts/${id}`, { method: 'PATCH', body: JSON.stringify(data) })
}

export async function deleteLayout(id) {
  const res = await fetch(`${BASE_URL}/api/layouts/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error(`API error ${res.status}`)
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
