import { useState } from 'react'
import FeedManager from './components/FeedManager'
import LayoutEditor from './components/LayoutEditor'
import AudioControls from './components/AudioControls'
import ExportPanel from './components/ExportPanel'

const TABS = ['Clips', 'Layout', 'Audio', 'Export']

export default function App() {
  const [activeTab, setActiveTab] = useState('Clips')

  return (
    <div className="app">
      <header className="app-header">
        <h1>🎬 Concert View</h1>
        <nav className="tab-nav">
          {TABS.map((tab) => (
            <button
              key={tab}
              className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
              onClick={() => setActiveTab(tab)}
            >
              {tab}
            </button>
          ))}
        </nav>
      </header>
      <main>
        {activeTab === 'Clips' && <FeedManager />}
        {activeTab === 'Layout' && <LayoutEditor />}
        {activeTab === 'Audio' && <AudioControls />}
        {activeTab === 'Export' && <ExportPanel />}
      </main>
    </div>
  )
}
