import { useState } from 'react'
import FeedManager from './components/FeedManager'
import LayoutEditor from './components/LayoutEditor'
import AudioControls from './components/AudioControls'

const TABS = ['Feeds', 'Layout', 'Audio']

export default function App() {
  const [activeTab, setActiveTab] = useState('Feeds')

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
        {activeTab === 'Feeds' && <FeedManager />}
        {activeTab === 'Layout' && <LayoutEditor />}
        {activeTab === 'Audio' && <AudioControls />}
      </main>
    </div>
  )
}
