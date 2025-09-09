# General guidelines

* Refactor code as you go to keep code clean
* Keep file sizes small and put helper functions and components in their own files.

# Commit Message Guidelines 
## The Golden Rule: One Explanation Per Change

As a seasoned developer teaching a newcomer: **Every single file modification, addition, or deletion needs its own specific reasoning.** Don't bundle explanations - be granular. Required Format:
Every commit message MUST explain WHY the change was made, not just WHAT was changed.

## ❌ Bad Example (Bundled Reasoning):
```
Add user authentication system

Reason: Users needed login functionality
- Added LoginForm.tsx component
- Updated App.tsx routing  
- Created auth service
- Added login styles
```

### ✅ Good Example (Individual Change Explanations):

- Add .env.production to gitignore to prevent accidental commits of production secrets

- Update vite config to ignore .env files during development to prevent unnecessary rebuilds

- Add setup-env script to package.json to streamline environment configuration for new developers`

- Create environment template to provide clear guidance on required variables`

- Create AuthService for API authentication calls
Reason: Needed centralized authentication logic to avoid duplicating login/logout API calls across components

- Add login form styles to match design system
Reason: Login form needed consistent styling with existing components to maintain visual coherence
```

### Commit Message Structure:
1. **Action**: What was done (Add, Update, Fix, Remove, etc.)
2. **Target**: What file/feature was modified
3. **Reason**: Why this change was necessary
4. **Context**: Additional context if helpful

### Bad Commit Messages (missing reasoning):
* `Update .gitignore`
* `Fix config`
* `Add new file`
* `Update package.json`

### Real-World Scenario:
```
❌ "Fix user profile bugs"
✅ "Add null check for user.avatar_url in ProfileImage component"
   "Reason: App crashed when users without profile photos loaded the profile page"

✅ "Update ProfileForm validation to require email format"
   "Reason: Users were submitting invalid emails causing server errors and poor UX"

✅ "Fix ProfileModal z-index to appear above navigation"
   "Reason: Modal was appearing behind the navigation bar making it unusable"
```

Each of these could be separate commits, or if done together, each needs its own explanation line.

## Enforcement
- NEVER commit without explaining the reasoning for each individual change
- If the reason for any specific change isn't clear, ask for clarification before committing
- Each commit should be atomic and focused on a single logical feature/fix
- When multiple files change for one feature, explain why each file needed modification
- Use present tense ("Add" not "Added") for consistency