import { useState } from 'react';

export default function Home() {
  const [text, setText] = useState('');
  const [data, setData] = useState(null);

  const generate = async () => {
    const res = await fetch('https://YOUR-RAILWAY-URL/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const result = await res.json();
    setData(result);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Patent AI Clean</h1>
      <textarea onChange={(e) => setText(e.target.value)} />
      <br /><br />
      <button onClick={generate}>Generate</button>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}
