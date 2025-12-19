import React, { useState } from "react";
import { askQuestion } from "../api";
import MarkdownMessage from "./MarkdownMessage";

export default function ChatPage({ repoId }) {
  const [messages, setMessages] = useState([{ sender: "bot", text: "Hi! How can I help you with this repo?", sources: [] }]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (!input) return;
    const userMsg = { sender: "user", text: input };
    setMessages([...messages, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const data = await askQuestion(repoId, input);
      setLoading(false);
      let botText = "";
      const botMsg = { sender: "bot", text: "", sources: data.sources || [] };
      setMessages((prev) => [...prev, botMsg]);

      for (let i = 0; i < data.answer.length; i += 1) {
        botText += data.answer[i];
        setMessages((prev) => [...prev.slice(0, -1), { sender: "bot", text: botText, sources: data.sources || [] }]);
        await new Promise((r) => setTimeout(r, 20)); // 20ms per char
      }
    } catch (err) {
      console.error(err);
      setLoading(false);
      setMessages((prev) => [...prev, { sender: "bot", text: "Error fetching answer", sources: [] }]);
    }
  };

  return (
    <div style={{ backgroundColor: "white", height: "100vh", display: "flex", flexDirection: "column", maxWidth: "900px", margin: "0 auto", width: "100%" }}>
      <style>{`
        @keyframes bounce {
          0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
          }
          40% {
            transform: scale(1);
            opacity: 1;
          }
        }
      `}</style>
      <div style={{ flex: 1, overflowY: "auto", padding: "20px", paddingBottom: "10px" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ margin: "12px 0", textAlign: m.sender === "user" ? "right" : "left" }}>
            <div style={{ 
              display: "inline-block", 
              padding: "12px 16px", 
              borderRadius: "12px", 
              backgroundColor: m.sender === "user" ? "black" : "#f5f5f5", 
              color: m.sender === "user" ? "white" : "black", 
              border: m.sender === "bot" ? "1px solid #e5e5e5" : "none", 
              maxWidth: "80%",
              textAlign: "left",
              lineHeight: "1.6",
              boxShadow: "0 1px 2px rgba(0,0,0,0.05)"
            }}>
              {m.sender === "bot" ? <MarkdownMessage text={m.text} /> : m.text}
              {m.sender === "bot" && m.sources && m.sources.length > 0 && (
                <div style={{ marginTop: "10px", paddingTop: "10px", borderTop: "1px solid #ddd", fontSize: "12px", color: "#666" }}>
                  <strong>Sources:</strong>
                  <ul style={{ margin: "5px 0", paddingLeft: "20px" }}>
                    {m.sources.map((src, idx) => (
                      <li key={idx}>{src}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ margin: "12px 0", textAlign: "left" }}>
            <div style={{ 
              display: "inline-block", 
              padding: "12px 16px", 
              borderRadius: "12px", 
              backgroundColor: "#f5f5f5", 
              border: "1px solid #e5e5e5",
              boxShadow: "0 1px 2px rgba(0,0,0,0.05)"
            }}>
              <div style={{ display: "flex", gap: "4px", alignItems: "center" }}>
                <span style={{ 
                  width: "8px", 
                  height: "8px", 
                  borderRadius: "50%", 
                  backgroundColor: "#666",
                  animation: "bounce 1.4s infinite ease-in-out both",
                  animationDelay: "0s"
                }}></span>
                <span style={{ 
                  width: "8px", 
                  height: "8px", 
                  borderRadius: "50%", 
                  backgroundColor: "#666",
                  animation: "bounce 1.4s infinite ease-in-out both",
                  animationDelay: "0.16s"
                }}></span>
                <span style={{ 
                  width: "8px", 
                  height: "8px", 
                  borderRadius: "50%", 
                  backgroundColor: "#666",
                  animation: "bounce 1.4s infinite ease-in-out both",
                  animationDelay: "0.32s"
                }}></span>
              </div>
            </div>
          </div>
        )}
      </div>
      <div style={{ 
        padding: "16px 20px", 
        borderTop: "1px solid #e5e5e5",
        backgroundColor: "white",
        display: "flex", 
        gap: "10px",
        alignItems: "center"
      }}>
        <input 
          type="text" 
          value={input} 
          onChange={(e) => setInput(e.target.value)} 
          style={{ 
            flex: 1, 
            padding: "12px 16px", 
            fontSize: "16px",
            borderRadius: "24px",
            border: "1px solid #ddd",
            outline: "none",
            transition: "border-color 0.2s"
          }}
          onFocus={(e) => e.target.style.borderColor = "#000"}
          onBlur={(e) => e.target.style.borderColor = "#ddd"}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Message..."
          disabled={loading}
        />
        <button 
          onClick={handleSend} 
          disabled={loading || !input}
          style={{ 
            padding: "12px 24px", 
            backgroundColor: loading || !input ? "#ccc" : "black", 
            color: "white", 
            fontSize: "16px", 
            cursor: loading || !input ? "not-allowed" : "pointer",
            borderRadius: "24px",
            border: "none",
            transition: "background-color 0.2s, transform 0.1s",
            fontWeight: "500",
            minWidth: "80px"
          }}
          onMouseEnter={(e) => !loading && input && (e.target.style.backgroundColor = "#333")}
          onMouseLeave={(e) => !loading && input && (e.target.style.backgroundColor = "black")}
          onMouseDown={(e) => !loading && input && (e.target.style.transform = "scale(0.98)")}
          onMouseUp={(e) => !loading && input && (e.target.style.transform = "scale(1)")}
        >
          {loading ? "..." : "Send"}
        </button>
      </div>
    </div>
  );
}
