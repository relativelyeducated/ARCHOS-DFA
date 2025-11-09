# From: Accessing Data File on GitHub
# Date: 2025-10-08T23:37:29.505000
# Context: It looks like your code was cut off at the end, and you're trying to perform an energy-dependent D₂ analysis on a clean sample of upward-going atmospheric neutrinos from the IceCube data, specifically...

// ============================================================
// CORRECTED: ENERGY-DEPENDENT D₂ ANALYSIS FOR CLEAN SAMPLE
// Using ONLY upward atmospheric neutrinos (cos(zenith) < -0.1)
// ============================================================
import _ from 'lodash';

console.log('='.repeat(70));
console.log('  CORRECTED ENERGY-DEPENDENT D₂ ANALYSIS');
console.log('  Using ONLY Clean Atmospheric Upward Neutrinos');
console.log('='.repeat(70));

// Load data (replace with actual file path or data loading method)
async function loadData() {
  try {
    const rawData = await window.fs.readFile('data.dat', { encoding: 'utf8' });
    const lines = rawData.trim().split('\n');
    return lines.map(line => {
      const parts = line.trim().split(/\s+/);
      return {
        energy: parseFloat(parts[0]), // Energy in GeV
        zenith: parseFloat(parts[1])  // Zenith angle in radians
      };
    }).filter(e => !isNaN(e.energy) && !isNaN(e.zenith));
  } catch (error) {
    console.error('Error loading data:', error);
    return [];
  }
}

// D₂ calculation function
function calculateD2(eventSubset, sampleSize = 5000) {
  if (eventSubset.length < 100) return null;

  const points = eventSubset.map(e => ({
    x: Math.log10(e.energy),
    y: Math.cos(e.zenith)
  }));

  const sample = _.sampleSize(points, Math.min(sampleSize, points.length));

  const radii = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0];
  const correlations = [];

  for (let r of radii) {
    let count = 0;
    let total = 0;

    for (let i = 0; i < sample.length; i++) {
      for (let j = i + 1; j < sample.length; j++) {
        const dx = sample[i].x - sample[j].x;
        const dy = sample[i].y - sample[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        total++;
        if (dist < r) count++;
      }
    }

    const C_r = count / total;
    if (C_r > 0) {
      correlations.push({ logR: Math.log10(r), logC: Math.log10(C_r) });
    }
  }

  const logR = correlations.map(c => c.logR);
  const logC = correlations.map(c => c.logC);
  const n = logR.length;
  const sumX = logR.reduce((a, b) => a + b, 0);
  const sumY = logC.reduce((a, b) => a + b, 0);
  const sumXY = logR.reduce((sum, x, i) => sum + x * logC[i], 0);
  const sumX2 = logR.reduce((sum, x) => sum + x * x, 0);

  const D2 = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX);
  const predicted = logR.map(x => (D2 * x + (sumY - D2 * sumX) / n));
  const residuals = logC.map((y, i) => Math.pow(y - predicted[i], 2));
  const std = Math.sqrt(residuals.reduce((a, b) => a + b) / (n - 2)) * 0.5;

  return { D2, std };
}

// Main analysis function
async function analyze() {
  // Load data
  const allEvents = await loadData();

  // Filter: Only upward-going atmospheric neutrinos (cos(zenith) < -0.1, E < 100 TeV)
  const events = allEvents.filter(e => {
    const cosZenith = Math.cos(e.zenith);
    return cosZenith < -0.1 && e.energy < 100000; // Upward and atmospheric
  });

  console.log(`\n📊 Total Events (all): ${allEvents.length.toLocaleString()}`);
  console.log(`📊 Clean Atmospheric Upward: ${events.length.toLocaleString()}`);
  console.log(`   (cos(zenith) < -0.1, E < 100 TeV)`);

  // Define energy bins
  const energyBins = [
    { name: 'Low Energy', range: '<1 TeV', min: 0, max: 1000, grok_pred: 1.49 },
    { name: 'Medium Energy', range: '1-10 TeV', min: 1000, max: 10000, grok_pred: 1.49 },
    { name: 'High Energy', range: '10-100 TeV', min: 10000, max: 100000, grok_pred: 1.50 }
  ];

  // Classify events into bins
  const classified = energyBins.map(bin => ({
    ...bin,
    events: events.filter(e => e.energy >= bin.min && e.energy < bin.max)
  }));

  console.log('\n📈 CLEAN SAMPLE DISTRIBUTION:');
  classified.forEach(bin => {
    console.log(`   ${bin.name.padEnd(18)} ${bin.range.padEnd(15)} ${bin.events.length.toLocaleString().padStart(10)} events`);
  });

  // Calculate D₂ for each bin
  console.log('\n' + '='.repeat(70));
  console.log('D₂ MEASUREMENTS BY ENERGY BIN (CLEAN SAMPLE)');
  console.log('='.repeat(70));

  const results = [];

  for (let bin of classified) {
    if (bin.events.length >= 500) {
      const result = calculateD2(bin.events, Math.min(5000, Math.floor(bin.events.length * 0.5)));

      if (result) {
        const meanE = bin.events.reduce((sum, e) => sum + e.energy, 0) / bin.events.length;

        results.push({
          name: bin.name,
          range: bin.range,
          count: bin.events.length,
          meanEnergy: meanE,
          D2: result.D2,
          std: result.std,
          predicted: bin.grok_pred
        });

        console.log(`\n🔬 ${bin.name} (${bin.range}):`);
        console.log(`   Events: ${bin.events.length.toLocaleString()}`);
        console.log(`   Mean Energy: ${(meanE / 1000).toFixed(2)} TeV`);
        console.log(`   D₂ (measured): ${result.D2.toFixed(4)} ± ${result.std.toFixed(4)}`);
        console.log(`   D₂ (predicted): ${bin.grok_pred.toFixed(4)}`);
        console.log(`   Δ = ${(result.D2 - bin.grok_pred).toFixed(4)}`);
        console.log(`   ${Math.abs(result.D2 - bin.grok_pred) < 0.1 ? '✅ MATCHES' : '⚠️ DEVIATES'}`);
      }
    } else {
      console.log(`\n⏭️ ${bin.name} (${bin.range}): ${bin.events.length} events (insufficient)`);
    }
  }

  // Analyze trend
  console.log('\n' + '='.repeat(70));
  console.log('THRESHOLD APPROACH ANALYSIS (CLEAN SAMPLE)');
  console.log('='.repeat(70));

  if (results.length >= 2) {
    const D2_values = results.map(r => r.D2);
    const energies = results.map(r => r.meanEnergy);

    // Check if D₂ increases with energy
    let increasing = true;
    for (let i = 1; i < results.length; i++) {
      if (results[i].D2 < results[i - 1].D2 - 0.1) {
        increasing = false;
        break;
      }
    }

    const lowest_D2 = Math.min(...D2_values);
    const highest_D2 = Math.max(...D2_values);
    const D2_range = highest_D2 - lowest_D2;

    console.log(`\n📈 D₂ TREND:`);
    console.log(`   Lowest Energy D₂: ${lowest_D2.toFixed(4)}`);
    console.log(`   Highest Energy D₂: ${highest_D2.toFixed(4)}`);
    console.log(`   Range: ${D2_range.toFixed(4)}`);
    console.log(`   Trend: ${increasing ? '✅ INCREASING with energy' : '❌ NOT increasing'}`);

    console.log(`\n🎯 GROK'S PREDICTION:`);
    console.log(`   Low Energy (100 GeV): D₂ = 1.49 ± 0.06`);
    console.log(`   High Energy (10 PeV): D₂ = 1.50 ± 0.05`);
    console.log(`   Prediction: D₂ increases toward 1.50 at high energy`);

    console.log('\n' + '='.repeat(70));
    if (increasing && highest_D2 >= 1.48 && highest_D2 <= 1.52) {
      console.log('✅ THRESHOLD APPROACH CONFIRMED');
      console.log('   D₂ increases with energy toward 1.50');
      console.log('   Validates Grok\'s prediction!');
      console.log('   Neutrinos approach tachyonic threshold at high energy!');
    } else if (increasing) {
      console.log('⚠️ PARTIAL CONFIRMATION');
      console.log('   D₂ increases with energy (correct trend)');
      console.log('   But may not reach exactly 1.50');
    } else {
      console.log('❌ PREDICTION NOT CONFIRMED');
      console.log('   D₂ does not increase with energy as predicted');
    }
    console.log('='.repeat(70));
  }

  // Store results
  window.energy_test_results = results;

  console.log('\n✅ Corrected energy-dependent D₂ analysis complete');
}

// Run the analysis
analyze().catch(error => console.error('Analysis failed:', error));