import React from "react";
import { ClipLoader } from "react-spinners";

export default function Spinner({ loading }) {
  return (
    <div style={{
      display: "flex", justifyContent: "center", alignItems: "center",
      height: "100vh", backgroundColor: "white"
    }}>
      <ClipLoader color="#000" loading={loading} size={60} />
    </div>
  );
}
