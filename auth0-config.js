// Auth0 Configuration for FIMI Taxonomy
// This file will be populated with your Auth0 credentials

// Auth0 Configuration for FIMI Taxonomy
// Note: Client ID is safe to expose publicly - security comes from
// the Allowed Callback URLs configured in your Auth0 dashboard
const auth0Config = {
  domain: 'dev-qpwdmmy00vcxxbp0.eu.auth0.com',
  clientId: 'GDuKIxdR8792TiX9D8t6ObrauXoDJCI0',
  // Removed audience - not needed for basic authentication
  // audience: 'https://dev-qpwdmmy00vcxxbp0.eu.auth0.com/api/v2/',
  redirectUri: window.location.origin,
  scope: 'openid profile email'
};

let auth0Client = null;

// Initialize Auth0 client
async function initAuth0() {
  const clientConfig = {
    domain: auth0Config.domain,
    clientId: auth0Config.clientId,
    authorizationParams: {
      redirect_uri: auth0Config.redirectUri,
      scope: auth0Config.scope
    }
  };

  // Only add audience if it exists
  if (auth0Config.audience) {
    clientConfig.authorizationParams.audience = auth0Config.audience;
  }

  auth0Client = await auth0.createAuth0Client(clientConfig);

  // Check if returning from Auth0 callback
  const query = window.location.search;
  if (query.includes('code=') && query.includes('state=')) {
    await auth0Client.handleRedirectCallback();
    window.history.replaceState({}, document.title, '/');
  }

  // Update UI based on authentication status
  await updateUI();
}

// Update UI elements based on login status
async function updateUI() {
  const isAuthenticated = await auth0Client.isAuthenticated();

  // Show/hide login/logout buttons
  document.getElementById('login-btn')?.classList.toggle('hidden', isAuthenticated);
  document.getElementById('logout-btn')?.classList.toggle('hidden', !isAuthenticated);
  document.getElementById('user-profile')?.classList.toggle('hidden', !isAuthenticated);

  if (isAuthenticated) {
    const user = await auth0Client.getUser();

    // Display user info
    const profileElement = document.getElementById('user-profile');
    if (profileElement && user) {
      profileElement.innerHTML = `
        <img src="${user.picture}" alt="${user.name}" class="user-avatar">
        <span class="user-name">${user.name}</span>
      `;
    }

    // Optional: Show protected content
    document.querySelectorAll('.protected-content').forEach(el => {
      el.style.display = 'block';
    });
  } else {
    // Hide protected content
    document.querySelectorAll('.protected-content').forEach(el => {
      el.style.display = 'none';
    });
  }
}

// Login function
async function login() {
  await auth0Client.loginWithRedirect();
}

// Logout function
async function logout() {
  await auth0Client.logout({
    logoutParams: {
      returnTo: window.location.origin
    }
  });
}

// Protect entire site - redirect to login if not authenticated
async function protectSite() {
  // Skip protection on login page itself
  if (window.location.pathname.includes('login.html') || 
      window.location.pathname.includes('auth-debug.html')) {
    return;
  }
  
  // Allow front page (index) to be public
  if (window.location.pathname === '/' || 
      window.location.pathname === '/index.html') {
    return;
  }
  
  // Check authentication
  if (auth0Client) {
    const isAuthenticated = await auth0Client.isAuthenticated();
    
    if (!isAuthenticated) {
      // Save the page they were trying to visit
      sessionStorage.setItem('redirectAfterLogin', window.location.href);
      // Redirect to login
      window.location.href = '/login.html';
    }
  }
}

// Initialize when DOM is ready and protect site
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', async () => {
    await initAuth0();
    await protectSite();
  });
} else {
  initAuth0().then(protectSite);
}
