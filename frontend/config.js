// Konfigurasi Otomatis API (Lokal vs Cloudflare/Vercel)
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "${API_BASE_URL}"                                                    // Backend Lokal (Komputer/Laptop)
    : "https://pdf-master-ai-16ke-8pvsz41o7-muhamad-ruslan.vercel.app";        // Backend Vercel (Production)

console.log("PDF Master AI - Terhubung ke Backend:", API_BASE_URL);