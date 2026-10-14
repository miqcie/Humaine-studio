// Run: node --test scripts/tests/
const test = require('node:test');
const assert = require('node:assert');

function makeEl(extra = {}) {
  return Object.assign({ value: '', textContent: '', innerHTML: '', style: {}, step: '', min: '', max: '',
    listeners: {}, addEventListener(t, f) { this.listeners[t] = f; } }, extra);
}

function setup(saved) {
  const ids = ['currentBG','carbs','icr','icrValue','icrGrams','isf','isfValue','targetBG','insulinType',
    'unitsToggle','sourcesToggle','sourcesContent','resultSection','placeholderSection','currentBGLabel',
    'targetBGLabel','isfLabel','isfDescription','step1','step2','step3','step4','step5','recommendedDose',
    'insulinTypeName','lowBGWarning'];
  const els = {};
  ids.forEach(i => { els[i] = makeEl(); });
  // Mirror the static HTML in calculator.md (stale values the page ships with)
  els.icr.value = '15'; els.icrValue.textContent = '1:15'; els.icrGrams.textContent = '15';
  els.isf.value = '50'; els.isfValue.textContent = '1:50';
  els.isfDescription.textContent = '1 unit drops BG by 50 mg/dL';
  els.targetBG.value = '120';
  global.document = { getElementById: id => els[id], addEventListener() {} };
  const store = saved ? { insulinCalculatorSettings: JSON.stringify(saved) } : {};
  global.localStorage = { getItem: k => store[k] ?? null, setItem: (k, v) => { store[k] = v; } };
  global.window = {};
  delete require.cache[require.resolve('../../assets/js/calculator.js')];
  const { InsulinCalculator, CALCULATOR_DEFAULTS } = require('../../assets/js/calculator.js');
  const calc = new InsulinCalculator();
  return { els, calc, store, CALCULATOR_DEFAULTS };
}

test('fresh load: controls and labels show the values the math uses', () => {
  const { els, calc } = setup();
  assert.strictEqual(Number(els.icr.value), calc.state.icr);
  assert.strictEqual(els.icrValue.textContent, `1:${calc.state.icr}`);
  assert.strictEqual(String(els.icrGrams.textContent), String(calc.state.icr));
  assert.strictEqual(Number(els.isf.value), calc.state.isf);
  assert.strictEqual(els.isfValue.textContent, `1:${calc.state.isf}`);
  assert.match(els.isfDescription.textContent, new RegExp(`by ${calc.state.isf} mg/dL`));
});

test('fresh load: state equals the single defaults constant', () => {
  const { calc, CALCULATOR_DEFAULTS } = setup();
  assert.strictEqual(calc.state.icr, CALCULATOR_DEFAULTS.icr);
  assert.strictEqual(calc.state.isf, CALCULATOR_DEFAULTS.isf);
});

test('saved settings are respected and shown, not overwritten', () => {
  const saved = { icr: 12, isf: 45, targetBG: 110, insulinType: 'NovoLog (Aspart)', units: 'mg/dL' };
  const { els, calc, store } = setup(saved);
  assert.strictEqual(calc.state.icr, 12);
  assert.strictEqual(calc.state.isf, 45);
  assert.strictEqual(Number(els.icr.value), 12);
  assert.strictEqual(els.icrValue.textContent, '1:12');
  assert.strictEqual(Number(els.isf.value), 45);
  assert.strictEqual(els.isfValue.textContent, '1:45');
  assert.strictEqual(els.insulinType.value, 'NovoLog (Aspart)');
  assert.deepStrictEqual(JSON.parse(store.insulinCalculatorSettings), saved); // load must not rewrite storage
});

test('saved mmol/L settings: slider range matches units and shows saved value', () => {
  const { els, calc } = setup({ icr: 10, isf: 2.5, targetBG: 6.7, units: 'mmol/L', insulinType: 'Humalog (Lispro)' });
  assert.strictEqual(els.isf.max, '8');
  assert.strictEqual(Number(els.isf.value), 2.5);
  assert.strictEqual(els.isfValue.textContent, '1:2.5');
  assert.strictEqual(calc.state.isf, 2.5);
});

test('dose formula unchanged for given inputs', () => {
  const { calc } = setup({ icr: 10, isf: 50, targetBG: 100, units: 'mg/dL', insulinType: 'Humalog (Lispro)' });
  calc.state.currentBG = '200'; calc.state.carbs = '30';
  const r = calc.calculateDose();
  assert.strictEqual(r.correctionUnits, 2);
  assert.strictEqual(r.carbUnits, 3);
  assert.strictEqual(r.totalDose, 5);
  assert.strictEqual(r.roundedDose, 5);
});

test('slider input still syncs state, label and storage', () => {
  const { els, calc, store } = setup();
  els.icr.listeners.input({ target: { value: '20' } });
  assert.strictEqual(calc.state.icr, 20);
  assert.strictEqual(els.icrValue.textContent, '1:20');
  assert.strictEqual(JSON.parse(store.insulinCalculatorSettings).icr, 20);
});
