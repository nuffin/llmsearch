import React, { useState, ChangeEvent, FormEvent, DragEvent } from 'react'
import './page.less'
import axios from 'axios'

interface Result {
  type: 'text' | 'image' | 'audio' | 'video'
  content?: string
  name?: string
  url?: string
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [query, setQuery] = useState<string>('')
  const [results, setResults] = useState<Result[]>([])
  const [showUploadDialog, setShowUploadDialog] = useState<boolean>(false)

  const handleFileUpload = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0])
    }
    setShowUploadDialog(false)
  }

  const handleQuerySubmit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await axios.post<{ results: Result[] }>('/api/search', {
        query,
      })
      setResults(response.data.results)
    } catch (error) {
      console.error('Error fetching results:', error)
    }
  }

  const handleFileDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
    if (event.dataTransfer.files && event.dataTransfer.files[0]) {
      setFile(event.dataTransfer.files[0])
    }
    setShowUploadDialog(false)
  }

  const handleDragOver = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault()
  }

  return (
    <div className="container">
      <h1>File Uploader and Search Query</h1>

      {/* Part 1: File Upload Button */}
      <div className="file-upload">
        <button onClick={() => setShowUploadDialog(true)}>Upload File</button>

        {showUploadDialog && (
          <div className="upload-dialog">
            <div
              className="upload-area"
              onDrop={handleFileDrop}
              onDragOver={handleDragOver}
            >
              <p>Drag and drop a file here, or</p>
              <input type="file" onChange={handleFileUpload} />
              <button
                onClick={() =>
                  document
                    .querySelector<HTMLInputElement>('input[type="file"]')
                    ?.click()
                }
              >
                Select
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Part 2: Query Text Area */}
      <div className="query-area">
        <form onSubmit={handleQuerySubmit}>
          <textarea
            rows={5}
            placeholder="Enter your query here..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          ></textarea>
          <button type="submit">Submit Query</button>
        </form>
      </div>

      {/* Part 3: Results Area */}
      <div className="results-area">
        <h2>Results:</h2>
        {results.length > 0 ? (
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                {result.type === 'text' && <p>{result.content}</p>}
                {result.type === 'image' && (
                  <div>
                    <p>{result.name}</p>
                    <a href={result.url} download>
                      <img src={result.url} alt="Downloaded" />
                    </a>
                  </div>
                )}
                {result.type === 'audio' && (
                  <div>
                    <p>{result.name}</p>
                    <a href={result.url} download>
                      <audio controls>
                        <source src={result.url} type="audio/mpeg" />
                        Your browser does not support the audio element.
                      </audio>
                    </a>
                  </div>
                )}
                {result.type === 'video' && (
                  <div>
                    <p>{result.name}</p>
                    <a href={result.url} download>
                      <video width="320" height="240" controls>
                        <source src={result.url} type="video/mp4" />
                        Your browser does not support the video tag.
                      </video>
                    </a>
                  </div>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p>No results to display.</p>
        )}
      </div>
    </div>
  )
}

export default App
