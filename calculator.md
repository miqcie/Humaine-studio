---
layout: default
title: "T1D Insulin Calculator"
description: "Evidence-based insulin dosing calculator for Type 1 Diabetes. Calculate bolus doses using carb counting and correction factors with transparent, step-by-step calculations."
permalink: /calculator/
---

<link rel="stylesheet" href="{{ '/assets/css/calculator.css' | relative_url }}">

<div class="calculator-container">
  <div class="calculator-header">
    <div class="calculator-title-group">
      <h1 class="calculator-title">T1D Insulin Calculator</h1>
      <p class="calculator-subtitle">Evidence-based dosing for Type 1 Diabetes</p>
    </div>
    <button id="unitsToggle" class="units-toggle-btn">Switch to mmol/L</button>
  </div>

  <div class="medical-disclaimer">
    <p class="disclaimer-title">⚠️ Medical Disclaimer</p>
    <p class="disclaimer-text">
      This calculator is for educational purposes only and is NOT medical advice. Always follow your endocrinologist's prescribed insulin regimen and dosing instructions. Consult your diabetes care team before making any changes to your treatment plan. Individual insulin needs vary significantly.
    </p>
  </div>

  <div class="calculator-inputs">
    <div class="input-group-grid">
      <div class="input-group">
        <label for="insulinType" class="input-label">Insulin Type</label>
        <div class="select-wrapper">
          <select id="insulinType" class="select-field">
            <!-- Populated by JavaScript -->
          </select>
        </div>
      </div>

      <div class="input-group">
        <label for="targetBG" id="targetBGLabel" class="input-label">Target BG (mg/dL)</label>
        <input
          type="number"
          id="targetBG"
          class="input-field"
          step="1"
          value="120"
        />
      </div>
    </div>

    <div class="input-group-grid">
      <div class="input-group">
        <label for="icr" class="input-label">Carb Ratio (ICR)</label>
        <div class="slider-control">
          <input
            type="range"
            id="icr"
            class="slider"
            min="5"
            max="80"
            step="1"
            value="15"
          />
          <span id="icrValue" class="slider-value">1:15</span>
        </div>
        <p class="slider-description">1 unit per <span id="icrGrams">15</span>g carbs</p>
      </div>

      <div class="input-group">
        <label for="isf" id="isfLabel" class="input-label">Correction Factor (ISF)</label>
        <div class="slider-control">
          <input
            type="range"
            id="isf"
            class="slider"
            min="20"
            max="150"
            step="5"
            value="50"
          />
          <span id="isfValue" class="slider-value">1:50</span>
        </div>
        <p id="isfDescription" class="slider-description">1 unit drops BG by 50 mg/dL</p>
      </div>
    </div>

    <div class="input-group">
      <label for="currentBG" id="currentBGLabel" class="input-label">Current Blood Glucose (mg/dL)</label>
      <input
        type="number"
        id="currentBG"
        class="input-field"
        step="1"
        placeholder="Enter current BG in mg/dL"
      />
    </div>

    <div class="input-group">
      <label for="carbs" class="input-label">Carbs in Meal (grams)</label>
      <input
        type="number"
        id="carbs"
        class="input-field"
        placeholder="Enter carb count"
      />
    </div>
  </div>

  <!-- Results section (hidden by default) -->
  <div id="resultSection" style="display: none;">
    <div class="calculation-section">
      <h2 class="section-title">Step-by-Step Calculation</h2>

      <ul class="calculation-steps">
        <li id="step1" class="calculation-step"></li>
        <li id="step2" class="calculation-step"></li>
        <li id="step3" class="calculation-step"></li>
        <li id="step4" class="calculation-step"></li>
        <li id="step5" class="calculation-step"></li>
      </ul>

      <div class="rounding-rules">
        <strong>Rounding rules for half-unit dosing:</strong>
        <ul>
          <li>• 0.1-0.3 → Round down to whole unit</li>
          <li>• 0.4-0.6 → Round to nearest half unit (0.5)</li>
          <li>• 0.7-0.9 → Round up to whole unit</li>
        </ul>
      </div>
    </div>

    <div class="dose-recommendation">
      <h2 class="dose-title">Recommended Dose</h2>
      <div id="recommendedDose" class="dose-value">0.0 units</div>
      <p id="insulinTypeName" class="dose-insulin-type">Humalog (Lispro)</p>

      <div id="lowBGWarning" class="low-bg-warning" style="display: none;">
        <!-- Populated by JavaScript when BG is below target -->
      </div>
    </div>

    <div class="reminder-box">
      ⏰ <strong>Reminder:</strong> Check glucose monitor in 2 hours post-meal
    </div>
  </div>

  <!-- Placeholder (shown when no calculation) -->
  <div id="placeholderSection" class="calculator-placeholder">
    Enter current BG and carb count to calculate dose
  </div>

  <!-- Sources section -->
  <div class="sources-section">
    <button id="sourcesToggle" class="sources-toggle">
      ▶ Show Clinical Sources & Methodology
    </button>

    <div id="sourcesContent" class="sources-content">
      <div class="source-item">
        <strong>Carb Counting Method:</strong>
        <p>American Diabetes Association. <em>Standards of Care in Diabetes—2025</em>, Section 5 (Nutrition Therapy) & Section 9 (Type 1 Diabetes).</p>
        <a href="https://diabetesjournals.org/care/issue/48/Supplement_1" target="_blank" rel="noopener" class="source-link">
          Read ADA Standards 2025 →
        </a>
      </div>

      <div class="source-item">
        <strong>500 Rule for Insulin-to-Carb Ratio:</strong>
        <p>Walsh J, Roberts R. <em>Pumping Insulin: Everything You Need for Success on an Insulin Pump</em>. 6th ed. Torrey Pines Press; 2016. Formula: ICR = 500 ÷ Total Daily Dose.</p>
        <p>Validated in pediatrics: Hanas R, et al. "Bolus calculator settings in well-controlled prepubertal children." <em>J Diabetes Sci Technol</em>. 2017;11(3):632-639.</p>
        <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5478012/" target="_blank" rel="noopener" class="source-link">
          Read Hanas et al. study →
        </a>
      </div>

      <div class="source-item">
        <strong>1800 Rule for Insulin Sensitivity Factor:</strong>
        <p>Walsh J, Roberts R, Bailey TS. "Guidelines for optimal bolus calculator settings in adults." <em>J Diabetes Sci Technol</em>. 2011;5(1):129-135. Formula: ISF = 1800 ÷ Total Daily Dose.</p>
        <p>Based on Davidson PC, et al. "Analysis of guidelines for basal-bolus insulin dosing." <em>Endocr Pract</em>. 2008;14(7):933-946.</p>
        <a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3192590/" target="_blank" rel="noopener" class="source-link">
          Read Walsh et al. guidelines →
        </a>
      </div>

      <div class="source-item">
        <strong>Correction Dose Formula:</strong>
        <p>Correction = (Current BG - Target BG) ÷ ISF. Standard algorithm used in insulin pump bolus calculators.</p>
      </div>

      <div class="source-item">
        <strong>Pediatric Considerations:</strong>
        <p>DiMeglio LA, et al. "ISPAD Clinical Practice Consensus Guidelines 2018: Glycemic control targets." <em>Pediatr Diabetes</em>. 2018;19(Suppl 27):105-114.</p>
        <p style="color: #78350f;">Note: Young children often need more insulin per carb than the 500 Rule suggests, especially at breakfast.</p>
        <a href="https://pubmed.ncbi.nlm.nih.gov/30039513/" target="_blank" rel="noopener" class="source-link">
          Read ISPAD Guidelines →
        </a>
      </div>

      <div class="source-important">
        <p>
          ⚠️ <strong>Important:</strong> These calculations provide starting points only. Work with your endocrinologist to adjust ICR and ISF based on actual blood glucose patterns. Values change during honeymoon phase and throughout life with T1D.
        </p>
      </div>
    </div>
  </div>
</div>

<script src="{{ '/assets/js/calculator.js' | relative_url }}"></script>
