// 1. Konfigurasi Otomatis API_BASE_URL
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
    ? "http://localhost:8000"
    : "https://pdf-master-ai-16ke-8pvsz41o7-muhamad-ruslan.vercel.app";

console.log("PDF Master AI - Terhubung ke Backend:", API_BASE_URL);

// 2. Interceptor Global: Mengalihkan semua request localhost/127.0.0.1 ke API_BASE_URL
(function() {
    const originalFetch = window.fetch;
    window.fetch = function(resource, init) {
        if (typeof resource === 'string') {
            // Jika dipanggil via Cloudflare, alihkan semua request port 8000 ke Vercel
            if (window.location.hostname !== "localhost" && window.location.hostname !== "127.0.0.1") {
                resource = resource.replace(/http:\/\/(localhost|127\.0\.0\.1):8000/g, API_BASE_URL);
                resource = resource.replace(/\/\/(localhost|127\.0\.0\.1):8000/g, API_BASE_URL.replace('https://', ''));
            }
        }
        return originalFetch(resource, init);
    };
})();