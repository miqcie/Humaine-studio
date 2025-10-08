# T1D Insulin Calculator - Feature Roadmap

## Current Version (v1.0)
- ✅ Basic insulin dose calculation (carb coverage + correction)
- ✅ Unit conversion (mg/dL ↔ mmol/L)
- ✅ Adjustable ICR and ISF via sliders
- ✅ Multiple insulin type support
- ✅ Step-by-step calculation display
- ✅ Clinical source references
- ✅ Responsive mobile design
- ✅ Dark mode support

## Planned Features (Priority Order)

### High Priority - Safety & Usability

#### 1. Save Personal Settings (localStorage)
**Value:** Makes daily use practical, eliminates repetitive slider adjustments
- [ ] Save multiple user profiles (name, ICR, ISF, target BG, insulin type)
- [ ] Quick-load presets from dropdown
- [ ] Edit/delete saved profiles
- [ ] Export settings as JSON for backup
- [ ] Import settings from file
- [ ] Default profile selection
**Estimated effort:** 4-6 hours
**Learning value:** Browser localStorage API, JSON serialization, state persistence

#### 2. Active Insulin / Insulin On Board (IOB)
**Value:** Critical safety feature - prevents insulin stacking
- [ ] Input last dose amount and time
- [ ] Calculate remaining active insulin using 3-4 hour decay curve
- [ ] Display IOB prominently in UI
- [ ] Subtract IOB from correction dose
- [ ] Visual timeline showing insulin activity curve
- [ ] Warning when dosing too soon after previous dose
**Estimated effort:** 8-12 hours
**Learning value:** Time-based calculations, decay curves, safety-critical UX design
**Medical note:** Most important safety enhancement

#### 3. Dose History Log
**Value:** Pattern tracking, endocrinologist reporting, self-learning
- [ ] Log entries: timestamp, BG, carbs, dose given, notes
- [ ] Add 2-hour follow-up BG to entries
- [ ] View history as sortable table
- [ ] Export as CSV for medical appointments
- [ ] Simple pattern detection ("post-breakfast consistently high")
- [ ] Privacy-first: all data stored locally
**Estimated effort:** 10-15 hours
**Learning value:** Data persistence, CSV generation, basic analytics, data visualization

### Medium Priority - Enhanced Functionality

#### 4. Time-Based Ratios
**Value:** Most T1D patients need different ratios throughout the day
- [ ] Define time windows (e.g., 6-10am, 10am-4pm, 4-10pm, 10pm-6am)
- [ ] Assign different ICR/ISF to each window
- [ ] Auto-select ratio based on current time
- [ ] Manual override option
- [ ] Save time-based profiles
**Estimated effort:** 6-8 hours
**Learning value:** Time-based conditional logic, user-friendly scheduling UI

#### 5. Quick Food Database
**Value:** Reduces friction in carb counting
- [ ] Preloaded common foods with carb counts
- [ ] Search/filter food list
- [ ] Add multiple foods to running meal total
- [ ] Custom food entry (save personal items)
- [ ] Portion size adjustments
- [ ] Categories (fruits, grains, snacks, etc.)
**Estimated effort:** 8-10 hours
**Learning value:** Search/filter implementation, data structures, UX patterns

#### 6. Treatment Calculator for Hypoglycemia
**Value:** Complete toolkit - handles both highs and lows
- [ ] Rule of 15 calculator (glucose needed to raise BG)
- [ ] Account for active insulin when treating lows
- [ ] Recheck timer reminder
- [ ] Food suggestions for treatment
- [ ] Warning for severe low (<54 mg/dL / 3.0 mmol/L)
**Estimated effort:** 4-6 hours
**Learning value:** Complementary calculation logic, safety warnings

### Lower Priority - Nice to Have

#### 7. Emergency Reference Card
**Value:** Critical info when stressed or in emergency
- [ ] Glucagon administration instructions
- [ ] Sick day management rules
- [ ] DKA (diabetic ketoacidosis) warning signs
- [ ] Emergency contact quick-access
- [ ] Printable wallet card
**Estimated effort:** 3-4 hours
**Learning value:** Content design, print CSS, accessibility

#### 8. Share Calculation Feature
**Value:** Transparency with caregivers, documentation
- [ ] Generate shareable link with calculation details
- [ ] PDF export of dose calculation
- [ ] QR code for mobile sharing
- [ ] Email calculation summary
- [ ] Privacy controls (no PHI in URLs)
**Estimated effort:** 6-8 hours
**Learning value:** URL parameters, PDF generation, sharing patterns

#### 9. Unit Converter Suite
**Value:** Additional useful conversions for T1D management
- [ ] A1C % ↔ eAG (estimated average glucose)
- [ ] Total daily dose calculator
- [ ] Basal:Bolus ratio checker (recommended 40-50% basal)
- [ ] Weight-based TDD estimation
**Estimated effort:** 3-5 hours
**Learning value:** Medical formulas, conversion utilities

#### 10. Educational Tooltips & Learning Mode
**Value:** Teach while using the tool
- [ ] Inline tooltips explaining terms (ICR, ISF, IOB)
- [ ] "Why?" buttons next to each calculation step
- [ ] Link to detailed explanations
- [ ] Quiz mode: "What would you dose for this scenario?"
- [ ] Progressive disclosure of complexity
**Estimated effort:** 8-10 hours
**Learning value:** Educational UX design, progressive disclosure patterns

## Future Considerations (Research Needed)

### Advanced Features
- CGM integration (read values from Dexcom/Libre APIs)
- Trend arrows adjustment (rising/falling glucose)
- Exercise impact calculator
- Menstrual cycle tracking (hormonal impacts)
- Machine learning pattern detection
- Multi-language support
- Offline PWA (Progressive Web App) capability

### Technical Improvements
- Comprehensive unit testing
- E2E testing with Playwright/Cypress
- Accessibility audit (WCAG 2.1 AA compliance)
- Performance optimization
- Analytics (privacy-preserving usage metrics)

## Implementation Notes

**Development Principles:**
1. **Safety first** - Medical accuracy is non-negotiable
2. **Privacy by default** - All personal data stored locally
3. **Progressive enhancement** - Core functionality works without JavaScript
4. **Transparent calculations** - Show the math, cite sources
5. **Graceful degradation** - Works on older browsers
6. **Accessibility** - WCAG 2.1 AA minimum

**Before Each Feature:**
- [ ] Review clinical literature for accuracy
- [ ] Consider edge cases and error states
- [ ] Plan for mobile responsiveness
- [ ] Design for dark mode compatibility
- [ ] Write tests for critical paths
- [ ] Update medical disclaimer if needed

**User Testing Priorities:**
1. Parents of T1D children (different use case than adults)
2. T1D adults managing their own care
3. School nurses and caregivers
4. Endocrinologists (clinical validation)

## Resources & References

**Clinical Guidelines:**
- ADA Standards of Care (updated annually)
- ISPAD Clinical Practice Consensus Guidelines
- Think Like A Pancreas (Gary Scheiner)
- Pumping Insulin (Walsh & Roberts)

**Technical Resources:**
- MDN Web Docs (localStorage, time APIs)
- WebAIM (accessibility guidelines)
- HIPAA compliance for health apps
- FDA guidance on medical device software

## Version History

**v1.0.0** (Current)
- Initial release with core calculation features
- React → Vanilla JavaScript conversion
- Humaine Studio design integration
- Updated default values (ICR 1:15, ISF 1:50)
