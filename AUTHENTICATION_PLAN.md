# Complete Authentication System Plan

## Current Problems
1. Authentication checking happens but doesn't persist properly
2. MFA enrollment breaks the login flow
3. No account management interface
4. Redirect loops and repeated login prompts
5. No user dashboard or profile
6. Half-baked integration between Auth0 and the site

## Architecture Requirements

### Core Features
1. **Complete Login Flow**
   - Email/password registration and login
   - GitHub OAuth (already configured)
   - Google OAuth (should add)
   - MFA support (SMS + Authenticator app)
   - Password reset flow
   - Email verification

2. **Session Management**
   - Persistent sessions across browser sessions
   - Automatic token refresh
   - Single sign-on behavior
   - Proper logout that clears everything

3. **User Account System**
   - Account dashboard page (`/account`)
   - View profile (name, email, avatar)
   - Edit profile information
   - Manage connected accounts (GitHub, Google)
   - MFA settings (enable/disable, backup codes)
   - Session management (view active sessions, logout all)

4. **Site Protection**
   - Front page public
   - Everything else requires login
   - No redirect loops
   - Graceful handling of auth errors
   - Remember where user was trying to go

5. **User Experience**
   - Clear authentication state in navbar
   - Smooth transitions, no jarring redirects
   - Helpful error messages
   - Loading states during auth checks

## Technical Implementation

### Auth0 Configuration Needed
```yaml
Application Settings:
  - Type: Single Page Application
  - Allowed Callback URLs: https://fimi.infoepi.org, https://fimi.infoepi.org/callback
  - Allowed Logout URLs: https://fimi.infoepi.org
  - Allowed Web Origins: https://fimi.infoepi.org
  - Grant Types: Authorization Code, Refresh Token
  
Authentication:
  - Email/Password: Enabled
  - GitHub OAuth: Enabled (done)
  - Google OAuth: Enable
  - MFA: Optional (not required but available)
  
User Profile:
  - Collect: email, name, picture
  - Email verification: Required
```

### File Structure
```
/
├── index.html              # Public front page
├── login.html              # Login/signup page
├── callback.html           # Auth0 callback handler (NEW)
├── account.html            # User account dashboard (NEW)
├── auth0-config.js         # Core auth logic (REWRITE)
├── auth-styles.css         # Auth UI styles (UPDATE)
└── [all other pages]       # Protected content
```

### Implementation Steps

#### 1. Rewrite auth0-config.js
- Use `cacheLocation: 'localstorage'` for persistence
- Proper callback handling with dedicated page
- Token refresh logic
- Session state management
- Error boundary for all auth operations

#### 2. Create callback.html
- Dedicated page for handling Auth0 redirects
- Processes authorization code
- Handles MFA enrollment
- Redirects to original destination
- Shows loading state during processing

#### 3. Create account.html
- User profile display
- Edit profile form
- Connected accounts management
- MFA enrollment interface
- Active sessions list
- Logout all devices button

#### 4. Update login.html
- Better UX with loading states
- Social login buttons (GitHub, Google)
- Email/password form
- "Forgot password" link
- "Sign up" vs "Sign in" toggle

#### 5. Fix Site Protection
- Check auth on every protected page
- Use Auth0's `checkSession()` for silent auth
- Proper loading states
- No redirect loops
- Save return URL in sessionStorage

#### 6. Navbar Integration
- Show user avatar + name when logged in
- Dropdown menu:
  - My Account
  - Settings
  - Sign Out
- Loading state while checking auth
- Smooth transitions

## Auth Flow Diagram

### First-Time User
```
1. Visit protected page → Redirect to /login.html
2. Click "Sign up with Email" or "Continue with GitHub"
3. Auth0 Universal Login → Enter credentials
4. [If MFA enabled] → Enroll in MFA
5. Redirect to /callback.html
6. Process tokens → Store in localStorage
7. Redirect to original protected page
8. User sees content + their name in navbar
```

### Returning User
```
1. Visit any page → auth0-config.js checks localStorage
2. Token valid? → Allow access immediately
3. Token expired? → Silent refresh via checkSession()
4. Refresh works? → Continue seamlessly
5. Refresh fails? → Redirect to /login.html
```

### Account Management
```
1. Click name in navbar → Dropdown appears
2. Click "My Account" → /account.html
3. View profile, edit info, manage MFA
4. Click "Sign Out" → Clear tokens + redirect to /
```

## Success Criteria

- [ ] User can sign up with email or GitHub
- [ ] User can log in and stay logged in across browser restarts
- [ ] User can enable MFA without breaking the flow
- [ ] User can access account dashboard
- [ ] User can edit profile information
- [ ] User can sign out properly
- [ ] Protected pages are actually protected
- [ ] No redirect loops or repeated login prompts
- [ ] Navbar shows correct auth state
- [ ] Works on both localhost and production
- [ ] Error messages are helpful and clear
- [ ] Loading states during auth operations

## Timeline
1. Rewrite core auth logic (auth0-config.js) - 30 min
2. Create callback.html - 15 min
3. Create account.html - 45 min
4. Update login.html - 20 min
5. Fix site protection logic - 20 min
6. Test complete flow - 30 min
7. Deploy and verify - 15 min

**Total: ~3 hours of focused work**

## Next: Start Implementation
Begin with rewriting auth0-config.js with proper architecture.
