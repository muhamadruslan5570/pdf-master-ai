// Konfigurasi API Dasar (Lokal vs Cloudflare/Vercel)
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://localhost:8000"
    : "https://pdf-master-ai-16ke-8pvsz41o7-muhamad-ruslan.vercel.app";

console.log("PDF Master AI - API Target:", API_BASE_URL);