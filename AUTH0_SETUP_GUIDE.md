---
title: "Auth0 Setup Guide"
description: "Step-by-step instructions for configuring Auth0 authentication"
date: "2026-02-14"
---

# Auth0 Authentication Setup for FIMI Taxonomy

This guide will walk you through setting up Auth0 authentication for your Quarto website.

## Step 1: Create Auth0 Account

1. Go to [https://auth0.com](https://auth0.com)
2. Click "Sign Up" (it's free for up to 7,000 users)
3. Choose "Personal" account type
4. Verify your email

## Step 2: Create Application

1. In Auth0 Dashboard, go to **Applications** → **Applications**
2. Click **"+ Create Application"**
3. Settings:
   - **Name:** FIMI Taxonomy
   - **Application Type:** Single Page Application
4. Click **Create**

## Step 3: Configure Application Settings

In your new application's settings:

### Allowed Callback URLs
```
http://localhost:3000,
https://fimi.infoepi.org,
https://your-preview-url.netlify.app
```

### Allowed Logout URLs
```
http://localhost:3000,
https://fimi.infoepi.org,
https://your-preview-url.netlify.app
```

### Allowed Web Origins
```
http://localhost:3000,
https://fimi.infoepi.org,
https://your-preview-url.netlify.app
```

### Allowed Origins (CORS)
```
http://localhost:3000,
https://fimi.infoepi.org,
https://your-preview-url.netlify.app
```

Click **Save Changes** at the bottom.

## Step 4: Get Your Credentials

From the same settings page, copy:

1. **Domain** (e.g., `dev-abc123.us.auth0.com`)
2. **Client ID** (e.g., `aBcD1234567890XyZ`)

## Step 5: Update Configuration File

Open `auth0-config.js` and replace the placeholders:

```javascript
const auth0Config = {
  domain: 'dev-abc123.us.auth0.com',  // Your Auth0 domain
  clientId: 'aBcD1234567890XyZ',       // Your Client ID
  audience: 'https://dev-abc123.us.auth0.com/api/v2/',
  redirectUri: window.location.origin,
  scope: 'openid profile email'
};
```

## Step 6: Enable Social Logins (Optional)

To add Google, GitHub, etc.:

1. Go to **Authentication** → **Social** in Auth0 Dashboard
2. Click **"+ Create Connection"**
3. Choose provider (Google, GitHub, Microsoft, etc.)
4. Follow provider-specific setup
5. Enable for your FIMI Taxonomy application

### Google Setup Example:
1. Select "Google"
2. Enter your Google OAuth credentials (or use Auth0's dev keys for testing)
3. Enable for "FIMI Taxonomy" application
4. Save

## Step 7: Test Locally

1. Build your site:
   ```bash
   quarto preview
   ```

2. Click the "Login" button in navbar
3. You should be redirected to Auth0 login page
4. After login, you'll return to your site as authenticated

## Step 8: Protect Content (Optional)

To make certain content visible only to logged-in users:

### In any .qmd file:

```markdown
## Public Content

This is visible to everyone.

::: {.protected-content}
## Members Only Section

This content is only visible after login.

- Access to advanced research
- Downloadable resources
- Premium features
:::
```

The `.protected-content` div will be hidden until user logs in.

## Step 9: Customize Login Experience

### Change Login Page Branding:

1. Go to **Branding** → **Universal Login**
2. Customize logo, colors to match FIMI Taxonomy
3. Upload your favicon.png as logo
4. Set primary color to `#551638` (mulberry)

### Customize Email Templates:

1. Go to **Branding** → **Email Templates**
2. Edit verification email, password reset, etc.
3. Match FIMI Taxonomy style

## Step 10: Deploy

When deploying to production:

1. Update `auth0-config.js` allowed URLs to include production domain
2. Rebuild site: `quarto render`
3. Deploy to your hosting (Netlify, GitHub Pages, etc.)

## Troubleshooting

### "Origin not allowed" error
- Check Allowed Web Origins in Auth0 dashboard
- Make sure your domain is listed exactly (with/without trailing slash)

### Login button not appearing
- Check browser console for JavaScript errors
- Verify auth0-config.js is loaded
- Ensure Auth0 SDK script loaded before auth0-config.js

### User info not displaying
- Check `user-profile` div exists in navbar
- Verify user has completed profile in Auth0

## Advanced: Role-Based Access

To restrict certain pages to specific user roles:

1. Go to **User Management** → **Roles** in Auth0
2. Create roles: `admin`, `researcher`, `member`
3. Assign roles to users
4. Update `auth0-config.js` to check roles:

```javascript
async function updateUI() {
  const isAuthenticated = await auth0Client.isAuthenticated();
  
  if (isAuthenticated) {
    const user = await auth0Client.getUser();
    const roles = user['https://fimi.infoepi.org/roles'] || [];
    
    // Show admin content only to admins
    if (roles.includes('admin')) {
      document.querySelectorAll('.admin-only').forEach(el => {
        el.style.display = 'block';
      });
    }
  }
}
```

## Cost Estimate

Auth0 Free Tier:
- ✅ Up to 7,000 users
- ✅ Unlimited logins
- ✅ Social logins (Google, GitHub, etc.)
- ✅ Email/password authentication
- ✅ Multi-factor authentication
- ✅ Customizable login page

Perfect for academic/research projects!

## Support

- Auth0 Documentation: [https://auth0.com/docs](https://auth0.com/docs)
- FIMI Taxonomy Issues: Create issue in GitHub repo
- Auth0 Community: [https://community.auth0.com](https://community.auth0.com)

---

**You're all set!** Your FIMI Taxonomy site now has professional authentication with social logins.
