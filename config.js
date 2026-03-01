/**
 * API Configuration for Stock Portfolio Risk Analyzer
 * 
 * Priority order for Backend URL:
 * 1. Environment variable VITE_BACKEND_URL (set in Vercel or .env)
 * 2. Window override (set during runtime)
 * 3. localStorage (for user customization)
 * 4. Localhost fallback (development)
 * 
 * For Vercel Deployment:
 * - Set VITE_BACKEND_URL environment variable in Vercel project settings
 * - Example value: https://your-backend-api.onrender.com
 * 
 * For Local Development:
 * - Create .env.local with: VITE_BACKEND_URL=http://127.0.0.1:5000
 * - Or backend will use default: http://127.0.0.1:5000
 */

const getBackendUrl = () => {
    // 1. Check for explicit override in window
    if (window.BACKEND_URL_OVERRIDE) {
        console.log('✓ Using Backend URL from window override:', window.BACKEND_URL_OVERRIDE);
        return window.BACKEND_URL_OVERRIDE;
    }
    
    // 2. Check for environment variable (Vercel/build time)
    const envUrl = process.env.VITE_BACKEND_URL || 
                   process.env.REACT_APP_BACKEND_URL ||
                   window.ENV?.VITE_BACKEND_URL;
    
    if (envUrl && envUrl.trim()) {
        console.log('✓ Using Backend URL from environment variable:', envUrl);
        return envUrl;
    }
    
    // 3. Check localStorage for user customization
    const storedUrl = localStorage.getItem('BACKEND_URL');
    if (storedUrl && storedUrl.trim()) {
        console.log('✓ Using Backend URL from localStorage:', storedUrl);
        return storedUrl;
    }
    
    // 4. Default localhost for development
    const isLocal = window.location.hostname === 'localhost' || 
                    window.location.hostname === '127.0.0.1';
    
    if (isLocal) {
        console.log('✓ Using localhost Backend URL (development)');
        return 'http://127.0.0.1:5000';
    }
    
    // 5. If on production but no backend URL configured
    console.warn('⚠️ Backend URL not configured!');
    console.warn('Please set VITE_BACKEND_URL environment variable in Vercel');
    console.warn('Or update config.js with your backend URL');
    console.warn('Current page hostname:', window.location.hostname);
    
    return '';
};

window.API_CONFIG = {
    BACKEND_URL: getBackendUrl(),
    
    // Helper to update backend URL at runtime
    setBackendUrl: function(url) {
        this.BACKEND_URL = url;
        localStorage.setItem('BACKEND_URL', url);
        console.log('Backend URL updated to:', url);
    },
    
    // Helper to reset backend URL
    resetBackendUrl: function() {
        localStorage.removeItem('BACKEND_URL');
        this.BACKEND_URL = getBackendUrl();
        console.log('Backend URL reset to:', this.BACKEND_URL);
    }
};

// Log configuration at startup
console.log('=== Stock Portfolio Risk Analyzer ===');
console.log('Hostname:', window.location.hostname);
console.log('Backend URL:', window.API_CONFIG.BACKEND_URL);
console.log('Environment:', window.location.hostname === 'localhost' ? 'Development' : 'Production');

