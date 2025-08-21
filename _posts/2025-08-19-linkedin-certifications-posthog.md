---
layout: post
title: "How I Added Dynamic LinkedIn Certifications to PostHog's Post-it Training"
date: 2025-08-19
categories: [technical, javascript, open-source]
tags: [linkedin, posthog, react, typescript, api-integration]
---

# How I Added Dynamic LinkedIn Certifications to PostHog's Post-it Training

*A technical deep-dive into implementing LinkedIn's Add-to-Profile API for dynamic professional certifications*

## The Challenge

PostHog has a hilarious "Post-it Training Academy" that teaches proper sticky note technique. It's a fun internal training that ends with users getting "Post-it certified" - but the LinkedIn sharing button just linked to a generic certification form.

**The goal:** Replace that static link with a dynamic "Add to Profile" button that creates actual LinkedIn certifications with current dates and unique IDs.

## The Technical Implementation

### Before: Static Generic Link
```tsx
<CallToAction
    href="https://www.linkedin.com/in/me/edit/forms/certification/new/"
    type="primary"
>
    <>Share on LinkedIn</>
</CallToAction>
```

### After: Dynamic Certification Generator
```tsx
// LinkedIn certification URL generation  
const now = new Date()
const issueYear = now.getFullYear()
const issueMonth = now.getMonth() + 1  // JS months are 0-indexed 🤮
const expirationYear = issueYear + 100
const expirationMonth = issueMonth
const liUrl =
    `https://www.linkedin.com/profile/add?` +
    new URLSearchParams({
        startTask: 'CERTIFICATION_NAME',
        name: 'Post-It Note Certified Applicator',
        organizationId: '37415928',
        organizationName: 'PostHog', 
        issueYear: String(issueYear),
        issueMonth: String(issueMonth),
        expirationYear: String(expirationYear),
        expirationMonth: String(expirationMonth),
        certUrl: 'https://www.posthog.com',
        certId: String(Date.now() + Math.random() * 1000), // Always unique
    }).toString()

<CallToAction href={liUrl} type="primary">
    <>Add to LinkedIn Profile</>
</CallToAction>
```

## Key Technical Decisions

### 1. No React State Needed
Initially considered `useState` for incrementing certification IDs, but realized a simpler approach works better:
- `Date.now() + Math.random() * 1000` generates unique IDs every time
- No state management complexity
- Each user gets a truly unique certification

### 2. JavaScript Date Quirks
JavaScript's `getMonth()` returns 0-11 instead of 1-12, so we add +1 to get human-readable months. August = 7 + 1 = 8. One of those "why JavaScript, why?" moments.

### 3. URLSearchParams for Clean Encoding
Using `URLSearchParams` handles proper URL encoding automatically instead of manual string concatenation and encoding.

### 4. 100-Year Expiration
Set certifications to expire in 2125. Because Post-it skills are timeless.

## The Result

Now when users complete the training, they can click "Add to LinkedIn Profile" and get a properly formatted certification that shows:
- **Name:** "Post-It Note Certified Applicator" 
- **Organization:** PostHog
- **Issue Date:** Current month/year
- **Unique ID:** Timestamp + random number
- **Expires:** 100 years later

## Lessons Learned

1. **Keep it simple:** Dynamic doesn't always mean complex state management
2. **JavaScript dates are cursed:** That +1 for months will forever be annoying
3. **URLSearchParams is your friend:** Let the browser handle URL encoding
4. **Unique IDs are easy:** Timestamp + random number works great for non-sequential IDs

The entire implementation was just 15 lines of clean JavaScript - no frameworks, no state, just dynamic URL generation that creates real LinkedIn certifications.

---

Want to see this in action? Check out [PostHog's Post-it Training Academy](https://posthog.com/post-it-training) and get yourself certified! 📝

**Technical specs:**
- React/TypeScript
- Gatsby framework  
- LinkedIn Add-to-Profile API
- Zero additional dependencies