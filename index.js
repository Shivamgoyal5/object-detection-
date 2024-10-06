import { useState } from 'react';
import axios from 'axios';

export default function Home() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/detect/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResults(response.data);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Object Detection</h1>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleFileChange} required />
        <button type="submit">Detect Objects</button>
      </form>
      <div>
        <h2>Results:</h2>
        <ul>
          {results.map((result, index) => (
            <li key={index}>
              {result.label} with confidence {result.confidence} at location {result.box.toString()}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
