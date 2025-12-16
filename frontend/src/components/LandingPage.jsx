import React, { useState } from "react";
import Spinner from "./Spinner";
import { loadRepo } from "../api";

export default function LandingPage({ setRepoId, setPage }) {
  const [repoUrl, setRepoUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!repoUrl) return;
    setLoading(true);

    try {
      const data = await loadRepo(repoUrl);
      setRepoId(data.repo_id);
      setPage("chat"); // switch to chat page
    } catch (err) {
      console.error(err);
      alert("Failed to load repo");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Spinner loading={true} />;

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", backgroundColor: "white" }}>
      <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: "20px" }}>
        <input 
          type="text"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="Enter GitHub repo URL"
          style={{ 
            padding: "12px 16px", 
            fontSize: "16px", 
            width: "400px", 
            borderRadius: "8px",
            border: "1px solid #ddd",
            outline: "none",
            transition: "border-color 0.2s"
          }}
          onFocus={(e) => e.target.style.borderColor = "#000"}
          onBlur={(e) => e.target.style.borderColor = "#ddd"}
        />
        <button 
          type="submit" 
          style={{ 
            padding: "12px", 
            backgroundColor: "black", 
            color: "white", 
            fontSize: "16px", 
            cursor: "pointer",
            borderRadius: "8px",
            border: "none",
            transition: "background-color 0.2s, transform 0.1s",
            fontWeight: "500"
          }}
          onMouseEnter={(e) => e.target.style.backgroundColor = "#333"}
          onMouseLeave={(e) => e.target.style.backgroundColor = "black"}
          onMouseDown={(e) => e.target.style.transform = "scale(0.98)"}
          onMouseUp={(e) => e.target.style.transform = "scale(1)"}
        >
          Load Repo
        </button>
      </form>
    </div>
  );
}
