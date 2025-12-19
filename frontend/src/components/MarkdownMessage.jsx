import React, { useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

function CodeRenderer({ inline, className, children, ...props }) {
  const codeText = String(children ?? "").replace(/\n$/, "");
  const [copied, setCopied] = useState(false);

  if (inline) {
    return (
      <code
        {...props}
        style={{
          backgroundColor: "#eee",
          padding: "2px 6px",
          borderRadius: "6px",
          fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
          fontSize: "0.95em",
        }}
      >
        {children}
      </code>
    );
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(codeText);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1200);
    } catch {
      
    }
  };

  return (
    <div style={{ position: "relative", marginTop: 10 }}>
      <button
        type="button"
        onClick={handleCopy}
        style={{
          position: "absolute",
          top: 8,
          right: 8,
          padding: "6px 10px",
          borderRadius: "10px",
          border: "1px solid #333",
          backgroundColor: "black",
          color: "white",
          cursor: "pointer",
          fontSize: 12,
        }}
      >
        {copied ? "Copied" : "Copy"}
      </button>

      <pre
        style={{
          margin: 0,
          backgroundColor: "black",
          color: "white",
          borderRadius: "12px",
          padding: "14px",
          overflowX: "auto",
        }}
      >
        <code
          className={className}
          style={{
            fontFamily: "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
            fontSize: 14,
            whiteSpace: "pre",
          }}
        >
          {codeText}
        </code>
      </pre>
    </div>
  );
}

export default function MarkdownMessage({ text }) {
  const components = useMemo(
    () => ({
      code: CodeRenderer,
      p: (pProps) => <p {...pProps} style={{ margin: "8px 0" }} />,
      ul: (ulProps) => <ul {...ulProps} style={{ margin: "8px 0", paddingLeft: 20 }} />,
      ol: (olProps) => <ol {...olProps} style={{ margin: "8px 0", paddingLeft: 20 }} />,
      h2: (h2Props) => <h2 {...h2Props} style={{ margin: "12px 0 8px", fontSize: 18 }} />,
      h3: (h3Props) => <h3 {...h3Props} style={{ margin: "12px 0 8px", fontSize: 16 }} />,
    }),
    []
  );

  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]} rehypePlugins={[rehypeHighlight]} components={components}>
      {text || ""}
    </ReactMarkdown>
  );
}
