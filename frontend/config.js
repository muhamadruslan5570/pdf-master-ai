// Konfigurasi API yang Aman untuk Lokal dan Cloudflare
const IS_LOCAL = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1";

const API_BASE_URL = IS_LOCAL
    ? "http://localhost:8000"                                                    // Mode Lokal (Laptop Anda)
    : "https://pdf-master-ai-16ke-8pvsz41o7-muhamad-ruslan.vercel.app";        // Mode Production (Cloudflare/Vercel)

console.log("PDF Master AI - Terhubung ke Backend:", API_BASE_URL);

// Hanya lakukan replacement URL jika sedang berjalan di Cloudflare/Production
if (!IS_LOCAL) {
    const originalFetch = window.fetch;
    window.fetch = function(resource, init) {
        if (typeof resource === 'string') {
            resource = resource.replace(/http:\/\/(localhost|127\.0\.0\.1):8000/g, API_BASE_URL);
        }
        return originalFetch(resource, init);
    };
}