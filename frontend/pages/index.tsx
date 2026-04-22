import { useState } from "react";

export default function Home() {
  const [text, setText] = useState("");
  const [data, setData] = useState<any>(null);

  const generate = async () => {
    const res = await fetch("https://qantent-ia-qqa1-production.up.railway.app/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text })
    });

    const result = await res.json();
    setData(result);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>Patent AI</h1>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />

      <button onClick={generate}>Generate</button>

      {data && (
        <div>
          <h2>Keywords</h2>
          <pre>{JSON.stringify(data.keywords, null, 2)}</pre>

          <h2>WordCloud</h2>
          <img
  src={`${process.env.NEXT_PUBLIC_API_URL}/wordcloud?t=${Date.now()}`}
  width="400"
/>
          
        <h2>TF-IDF Chart</h2>
        <img
  src={`${process.env.NEXT_PUBLIC_API_URL}/tfidf?t=${Date.now()}`}
  width="400"
/>
        </div>
      )}
    </div>
  );
}
