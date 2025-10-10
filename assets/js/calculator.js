// T1D Insulin Calculator
// Vanilla JavaScript implementation

class InsulinCalculator {
  constructor() {
    this.state = {
      currentBG: '',
      carbs: '',
      icr: 30, // Updated from 20 to 15 (more common adult baseline)
      isf: 80, // Updated from 80 to 50 mg/dL (standard adult baseline)
      targetBG: 120,
      insulinType: 'Humalog (Lispro)',
      showSources: false,
      units: 'mg/dL' // 'mg/dL' or 'mmol/L'
    };

    this.insulinTypes = [
      'Humalog (Lispro)',
      'Humalog Junior',
      'NovoLog (Aspart)',
      'Apidra (Glulisine)',
      'Fiasp (Faster Aspart)',
      'Lyumjev (Ultra-rapid Lispro)',
      'Admelog (Lispro)',
      'Other rapid-acting'
    ];

    this.init();
  }

  init() {
    this.cacheElements();
    this.loadFromLocalStorage();
    this.attachEventListeners();
    this.populateInsulinTypes();
    this.updateDisplay();
  }

  saveToLocalStorage() {
    try {
      const settings = {
        icr: this.state.icr,
        isf: this.state.isf,
        targetBG: this.state.targetBG,
        insulinType: this.state.insulinType,
        units: this.state.units
      };
      localStorage.setItem('insulinCalculatorSettings', JSON.stringify(settings));
    } catch (error) {
      console.warn('Failed to save settings to localStorage:', error);
    }
  }

  loadFromLocalStorage() {
    try {
      const savedSettings = localStorage.getItem('insulinCalculatorSettings');
      if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        Object.assign(this.state, settings);
      }
    } catch (error) {
      console.warn('Failed to load settings from localStorage:', error);
    }
  }

  cacheElements() {
    // Input elements
    this.elements = {
      currentBGInput: document.getElementById('currentBG'),
      carbsInput: document.getElementById('carbs'),
      icrSlider: document.getElementById('icr'),
      icrValue: document.getElementById('icrValue'),
      icrGrams: document.getElementById('icrGrams'),
      isfSlider: document.getElementById('isf'),
      isfValue: document.getElementById('isfValue'),
      targetBGInput: document.getElementById('targetBG'),
      insulinTypeSelect: document.getElementById('insulinType'),
      unitsToggle: document.getElementById('unitsToggle'),
      sourcesToggle: document.getElementById('sourcesToggle'),
      sourcesContent: document.getElementById('sourcesContent'),
      resultSection: document.getElementById('resultSection'),
      placeholderSection: document.getElementById('placeholderSection'),
      currentBGLabel: document.getElementById('currentBGLabel'),
      targetBGLabel: document.getElementById('targetBGLabel'),
      isfLabel: document.getElementById('isfLabel'),
      isfDescription: document.getElementById('isfDescription')
    };
  }

  attachEventListeners() {
    // Input changes
    this.elements.currentBGInput.addEventListener('input', (e) => {
      this.state.currentBG = e.target.value;
      this.calculate();
    });

    this.elements.carbsInput.addEventListener('input', (e) => {
      this.state.carbs = e.target.value;
      this.calculate();
    });

    this.elements.icrSlider.addEventListener('input', (e) => {
      this.state.icr = Number(e.target.value);
      this.elements.icrValue.textContent = `1:${this.state.icr}`;
      this.elements.icrGrams.textContent = this.state.icr;
      this.saveToLocalStorage();
      this.calculate();
    });

    this.elements.isfSlider.addEventListener('input', (e) => {
      this.state.isf = parseFloat(e.target.value);
      this.updateISFDisplay();
      this.saveToLocalStorage();
      this.calculate();
    });

    this.elements.targetBGInput.addEventListener('input', (e) => {
      this.state.targetBG = parseFloat(e.target.value);
      this.saveToLocalStorage();
      this.calculate();
    });

    this.elements.insulinTypeSelect.addEventListener('change', (e) => {
      this.state.insulinType = e.target.value;
      this.saveToLocalStorage();
      this.updateDisplay();
    });

    this.elements.unitsToggle.addEventListener('click', () => {
      this.toggleUnits();
    });

    this.elements.sourcesToggle.addEventListener('click', () => {
      this.state.showSources = !this.state.showSources;
      this.toggleSources();
    });
  }

  populateInsulinTypes() {
    this.elements.insulinTypeSelect.innerHTML = this.insulinTypes
      .map(type => `<option value="${type}">${type}</option>`)
      .join('');
  }

  updateISFDisplay() {
    const displayValue = this.displayValue(this.state.isf);
    this.elements.isfValue.textContent = `1:${displayValue}`;
    this.elements.isfDescription.textContent = `1 unit drops BG by ${displayValue} ${this.state.units}`;
  }

  // Conversion helpers
  mgdlToMmol(mgdl) {
    return (mgdl / 18).toFixed(1);
  }

  mmolToMgdl(mmol) {
    return Math.round(mmol * 18);
  }

  convertBG(value, fromUnit) {
    if (fromUnit === 'mg/dL') {
      return parseFloat(this.mgdlToMmol(value));
    } else {
      return this.mmolToMgdl(value);
    }
  }

  displayValue(value) {
    return this.state.units === 'mmol/L'
      ? parseFloat(value).toFixed(1)
      : Math.round(value);
  }

  toggleUnits() {
    const newUnits = this.state.units === 'mg/dL' ? 'mmol/L' : 'mg/dL';

    // Convert current values
    if (this.state.currentBG) {
      this.state.currentBG = this.convertBG(parseFloat(this.state.currentBG), this.state.units).toString();
      this.elements.currentBGInput.value = this.state.currentBG;
    }

    this.state.targetBG = this.convertBG(this.state.targetBG, this.state.units);
    this.state.isf = this.convertBG(this.state.isf, this.state.units);

    this.state.units = newUnits;

    // Update input attributes and labels
    if (newUnits === 'mmol/L') {
      this.elements.currentBGInput.step = '0.1';
      this.elements.targetBGInput.step = '0.1';
      this.elements.isfSlider.min = '1';
      this.elements.isfSlider.max = '8';
      this.elements.isfSlider.step = '0.1';
    } else {
      this.elements.currentBGInput.step = '1';
      this.elements.targetBGInput.step = '1';
      this.elements.isfSlider.min = '20';
      this.elements.isfSlider.max = '150';
      this.elements.isfSlider.step = '5';
    }

    this.elements.targetBGInput.value = this.displayValue(this.state.targetBG);
    this.elements.isfSlider.value = this.state.isf;

    this.updateDisplay();
    this.calculate();
    this.saveToLocalStorage();
  }

  toggleSources() {
    if (this.state.showSources) {
      this.elements.sourcesContent.style.display = 'block';
      this.elements.sourcesToggle.innerHTML = '▼ Hide Clinical Sources & Methodology';
    } else {
      this.elements.sourcesContent.style.display = 'none';
      this.elements.sourcesToggle.innerHTML = '▶ Show Clinical Sources & Methodology';
    }
  }

  calculateDose() {
    if (!this.state.currentBG || !this.state.carbs) return null;

    const bg = parseFloat(this.state.currentBG);
    const carbCount = parseFloat(this.state.carbs);

    // Convert to mg/dL for calculation if in mmol/L
    const bgInMgdl = this.state.units === 'mmol/L' ? bg * 18 : bg;
    const targetInMgdl = this.state.units === 'mmol/L' ? this.state.targetBG * 18 : this.state.targetBG;
    const isfInMgdl = this.state.units === 'mmol/L' ? this.state.isf * 18 : this.state.isf;

    const bgDifference = bgInMgdl - targetInMgdl;
    const correctionUnits = bgDifference / isfInMgdl;
    const carbUnits = carbCount / this.state.icr;
    const totalDose = correctionUnits + carbUnits;

    // Hospital rounding logic for half-unit dosing
    const decimal = totalDose - Math.floor(totalDose);
    let roundedDose;

    if (decimal >= 0 && decimal <= 0.3) {
      roundedDose = Math.floor(totalDose);
    } else if (decimal > 0.3 && decimal < 0.7) {
      roundedDose = Math.floor(totalDose) + 0.5;
    } else {
      roundedDose = Math.ceil(totalDose);
    }

    return {
      bgDifference: this.state.units === 'mmol/L' ? bgDifference / 18 : bgDifference,
      correctionUnits,
      carbUnits,
      totalDose,
      roundedDose,
      bgInMgdl,
      targetInMgdl,
      isfInMgdl
    };
  }

  calculate() {
    const result = this.calculateDose();

    if (result) {
      this.displayResult(result);
      this.elements.resultSection.style.display = 'block';
      this.elements.placeholderSection.style.display = 'none';
    } else {
      this.elements.resultSection.style.display = 'none';
      this.elements.placeholderSection.style.display = 'block';
    }
  }

  displayResult(result) {
    const currentBGDisplay = this.displayValue(this.state.currentBG);
    const targetBGDisplay = this.displayValue(this.state.targetBG);
    const isfDisplay = this.displayValue(this.state.isf);
    const bgDiffDisplay = this.displayValue(Math.abs(result.bgDifference));

    // Update calculation steps
    document.getElementById('step1').innerHTML =
      `<strong>Step 1:</strong> Current BG - Target BG<span class="calculation-value">${currentBGDisplay} - ${targetBGDisplay} = ${bgDiffDisplay}</span>`;

    document.getElementById('step2').innerHTML =
      `<strong>Step 2:</strong> Correction dose<span class="calculation-value">${bgDiffDisplay} ÷ ${isfDisplay} = ${result.correctionUnits.toFixed(2)} units</span>`;

    document.getElementById('step3').innerHTML =
      `<strong>Step 3:</strong> Carb coverage<span class="calculation-value">${this.state.carbs} ÷ ${this.state.icr} = ${result.carbUnits.toFixed(2)} units</span>`;

    document.getElementById('step4').innerHTML =
      `<strong>Step 4:</strong> Total dose<span class="calculation-value">${result.correctionUnits.toFixed(2)} + ${result.carbUnits.toFixed(2)} = ${result.totalDose.toFixed(2)} units</span>`;

    document.getElementById('step5').innerHTML =
      `<strong>Step 5:</strong> Round per hospital protocol<span class="calculation-value">${result.totalDose.toFixed(2)} → ${result.roundedDose.toFixed(1)} units</span>`;

    // Update recommended dose
    document.getElementById('recommendedDose').textContent = `${result.roundedDose.toFixed(1)} units`;
    document.getElementById('insulinTypeName').textContent = this.state.insulinType;

    // Show/hide low BG warning
    const lowBGWarning = document.getElementById('lowBGWarning');
    if (result.correctionUnits < 0) {
      const lowThreshold = this.state.units === 'mmol/L' ? '3.9' : '70';
      lowBGWarning.innerHTML = `
        ℹ️ <strong>Note:</strong> Your blood glucose is below target (${currentBGDisplay} &lt; ${targetBGDisplay} ${this.state.units}).
        The recommended dose is reduced to account for this. If BG is very low (&lt;${lowThreshold} ${this.state.units}),
        treat the low first before eating and dosing insulin.
      `;
      lowBGWarning.style.display = 'block';
    } else {
      lowBGWarning.style.display = 'none';
    }
  }

  updateDisplay() {
    // Update labels
    this.elements.currentBGLabel.textContent = `Current Blood Glucose (${this.state.units})`;
    this.elements.targetBGLabel.textContent = `Target BG (${this.state.units})`;
    this.elements.isfLabel.textContent = `Correction Factor (ISF)`;

    // Update ISF display
    this.updateISFDisplay();

    // Update units toggle button
    this.elements.unitsToggle.textContent =
      this.state.units === 'mg/dL' ? 'Switch to mmol/L' : 'Switch to mg/dL';

    // Update input placeholders
    this.elements.currentBGInput.placeholder = `Enter current BG in ${this.state.units}`;
  }
}

// Initialize calculator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  new InsulinCalculator();
});
