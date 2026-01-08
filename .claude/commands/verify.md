---
description: Review code for best practices, efficiency, and security
---

# Verify Code Quality and Security

Review all recent work for best practices, efficiency, and security.

## Instructions

Perform a comprehensive review of the codebase changes:

### 1. Security Review
- Check for hardcoded secrets, API keys, or credentials
- Look for SQL injection vulnerabilities
- Check for XSS vulnerabilities in frontend code
- Verify proper input validation and sanitization
- Check for insecure direct object references
- Review authentication and authorization patterns
- Look for sensitive data exposure in logs or error messages

### 2. Best Practices Review
- Verify proper error handling throughout
- Check for consistent code style and formatting
- Review naming conventions (variables, functions, files)
- Ensure proper separation of concerns
- Check for code duplication that should be refactored
- Verify proper use of TypeScript/JavaScript patterns
- Review component structure and organization

### 3. Efficiency Review
- Look for N+1 query problems or unnecessary API calls
- Check for inefficient loops or data processing
- Review caching strategies where applicable
- Look for memory leaks (event listeners, subscriptions)
- Check for unnecessary re-renders in Vue components
- Review bundle size implications of imports

### 4. Testing & Reliability
- Verify edge cases are handled
- Check for proper null/undefined handling
- Review error boundaries and fallback states
- Ensure loading states are implemented
- Check for race conditions in async code

### 5. Documentation
- Verify important functions have clear purpose
- Check that complex logic is explained
- Review API endpoint documentation

## Output Format

Provide a structured report with:
1. **Issues Found** - List any problems discovered, categorized by severity (Critical, High, Medium, Low)
2. **Recommendations** - Suggestions for improvement
3. **What's Working Well** - Positive patterns observed
4. **Action Items** - Specific fixes to implement (if any)

If issues are found, ask the user if they want you to fix them.
