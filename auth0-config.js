// Auth0 Configuration for FIMI Taxonomy
// This file will be populated with your Auth0 credentials

const auth0Config = {
  domain: 'dev-qpwdmmy00vcxxbp0.eu.auth0.com',
  clientId: '4w10LIgGMLo4gwukZHRjiNGc0dQ76nm6',
  audience: 'https://dev-qpwdmmy00vcxxbp0.eu.auth0.com/api/v2/',
  redirectUri: window.location.origin,
  scope: 'openid profile email'
};

let auth0Client = null;

// Initialize Auth0 client
async function initAuth0() {
  auth0Client = await auth0.createAuth0Client({
    domain: auth0Config.domain,
    clientId: auth0Config.clientId,
    authorizationParams: {
      redirect_uri: auth0Config.redirectUri,
      audience: auth0Config.audience,
      scope: auth0Config.scope
    }
  });

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

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initAuth0);
} else {
  initAuth0();
}
