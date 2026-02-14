// FIMI Taxonomy - Complete Authentication System
// Auth0 SPA Integration with full session management

const AUTH0_CONFIG = {
  domain: 'dev-qpwdmmy00vcxxbp0.eu.auth0.com',
  clientId: 'GDuKIxdR8792TiX9D8t6ObrauXoDJCI0',
  redirectUri: window.location.origin + '/callback.html',
  scope: 'openid profile email',
  cacheLocation: 'localstorage',
  useRefreshTokens: true
};

let auth0Client = null;
let currentUser = null;

// Initialize Auth0 client
async function initAuth0() {
  try {
    // Wait for createAuth0Client to be available (from CDN script)
    let attempts = 0;
    while (typeof createAuth0Client === 'undefined' && attempts < 50) {
      await new Promise(resolve => setTimeout(resolve, 100));
      attempts++;
    }
    
    if (typeof createAuth0Client === 'undefined') {
      throw new Error('Auth0 SDK failed to load. Please check your internet connection.');
    }
    
    // Note: The Auth0 SPA SDK exposes createAuth0Client as a global function
    auth0Client = await createAuth0Client({
      domain: AUTH0_CONFIG.domain,
      clientId: AUTH0_CONFIG.clientId,
      authorizationParams: {
        redirect_uri: AUTH0_CONFIG.redirectUri,
        scope: AUTH0_CONFIG.scope
      },
      cacheLocation: AUTH0_CONFIG.cacheLocation,
      useRefreshTokens: AUTH0_CONFIG.useRefreshTokens
    });

    return auth0Client;
  } catch (error) {
    console.error('Failed to initialize Auth0:', error);
    throw error;
  }
}

// Check if user is authenticated
async function isAuthenticated() {
  if (!auth0Client) {
    await initAuth0();
  }
  
  try {
    return await auth0Client.isAuthenticated();
  } catch (error) {
    console.error('Authentication check failed:', error);
    return false;
  }
}

// Get current user profile
async function getUser() {
  if (currentUser) {
    return currentUser;
  }
  
  if (!auth0Client) {
    await initAuth0();
  }
  
  try {
    const authenticated = await auth0Client.isAuthenticated();
    if (authenticated) {
      currentUser = await auth0Client.getUser();
      return currentUser;
    }
  } catch (error) {
    console.error('Failed to get user:', error);
  }
  
  return null;
}

// Login with redirect to Auth0
async function login() {
  if (!auth0Client) {
    await initAuth0();
  }
  
  try {
    // Save current page for redirect after login
    sessionStorage.setItem('auth_return_url', window.location.href);
    
    await auth0Client.loginWithRedirect({
      authorizationParams: {
        redirect_uri: AUTH0_CONFIG.redirectUri
      }
    });
  } catch (error) {
    console.error('Login failed:', error);
    alert('Login failed. Please try again.');
  }
}

// Logout and clear session
async function logout() {
  if (!auth0Client) {
    return;
  }
  
  try {
    currentUser = null;
    await auth0Client.logout({
      logoutParams: {
        returnTo: window.location.origin
      }
    });
  } catch (error) {
    console.error('Logout failed:', error);
    // Force logout anyway
    window.location.href = '/';
  }
}

// Handle Auth0 callback (call this on callback.html)
async function handleCallback() {
  if (!auth0Client) {
    await initAuth0();
  }
  
  try {
    await auth0Client.handleRedirectCallback();
    
    // Get user info
    currentUser = await auth0Client.getUser();
    
    // Get return URL or default to home
    const returnUrl = sessionStorage.getItem('auth_return_url') || '/';
    sessionStorage.removeItem('auth_return_url');
    
    return {
      success: true,
      user: currentUser,
      returnUrl: returnUrl
    };
  } catch (error) {
    console.error('Callback handling failed:', error);
    return {
      success: false,
      error: error.message,
      errorDescription: error.error_description
    };
  }
}

// Get access token (for API calls if needed)
async function getAccessToken() {
  if (!auth0Client) {
    await initAuth0();
  }
  
  try {
    return await auth0Client.getTokenSilently();
  } catch (error) {
    console.error('Failed to get access token:', error);
    return null;
  }
}

// Public pages that don't require authentication
const PUBLIC_PAGES = [
  '/',
  '/index.html',
  '/login.html',
  '/callback.html',
  '/auth-debug.html'
];

// Check if current page is public
function isPublicPage() {
  const path = window.location.pathname;
  return PUBLIC_PAGES.some(page => path === page || path.endsWith(page));
}

// Protect page - redirect to login if not authenticated
async function protectPage() {
  // Skip if on public page
  if (isPublicPage()) {
    return;
  }
  
  // Skip if on callback page (it has its own handler)
  if (window.location.pathname.includes('/callback')) {
    return;
  }
  
  try {
    const authenticated = await isAuthenticated();
    
    if (!authenticated) {
      // Save current page
      sessionStorage.setItem('auth_return_url', window.location.href);
      // Redirect to login
      window.location.href = '/login.html';
    }
  } catch (error) {
    console.error('Page protection failed:', error);
    // On error, redirect to login to be safe
    window.location.href = '/login.html';
  }
}

// Update UI based on authentication state
async function updateAuthUI() {
  try {
    const authenticated = await isAuthenticated();
    const user = authenticated ? await getUser() : null;
    
    // Update login/logout buttons
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const userProfile = document.getElementById('user-profile');
    
    if (loginBtn) {
      loginBtn.classList.toggle('hidden', authenticated);
    }
    
    if (logoutBtn) {
      logoutBtn.classList.toggle('hidden', !authenticated);
    }
    
    if (userProfile && user) {
      userProfile.classList.toggle('hidden', !authenticated);
      userProfile.innerHTML = `
        <img src="${user.picture}" alt="${user.name}" class="user-avatar">
        <span class="user-name">${user.name}</span>
      `;
    }
    
    // Show/hide protected content
    const protectedElements = document.querySelectorAll('.protected-content');
    protectedElements.forEach(el => {
      el.style.display = authenticated ? 'block' : 'none';
    });
    
    return { authenticated, user };
  } catch (error) {
    console.error('UI update failed:', error);
    return { authenticated: false, user: null };
  }
}

// Initialize on page load - only for pages that need auto-protection
// Login page and callback page handle initialization themselves
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    // Only auto-protect if not on login or callback page
    if (!isPublicPage() && !window.location.pathname.includes('/callback.html')) {
      await protectPage();
      await updateAuthUI();
    }
  });
} else {
  // Only auto-protect if not on login or callback page
  if (!isPublicPage() && !window.location.pathname.includes('/callback.html')) {
    (async () => {
      await protectPage();
      await updateAuthUI();
    })();
  }
}

// Export functions for use in other pages
window.auth0 = {
  isAuthenticated,
  getUser,
  login,
  logout,
  handleCallback,
  getAccessToken,
  updateAuthUI
};
