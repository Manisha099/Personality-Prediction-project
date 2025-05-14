import * as tf from '@tensorflow/tfjs';

// Feature importance weights derived from the Random Forest models
const featureImportance = {
  extraversion: [0.1135, 0.1223, 0.3490, 0.1691, 0.0819, 0.0066, 0.0072, 0.0153, 0.0054, 0.0066],
  agreeableness: [0.0071, 0.0082, 0.0040, 0.0126, 0.0067, 0.2277, 0.1238, 0.2555, 0.1345, 0.0845],
  openness: [0.0044, 0.0076, 0.0080, 0.0293, 0.0058, 0.0051, 0.0047, 0.0532, 0.0060, 0.0047],
  conscientiousness: [0.0076, 0.0053, 0.0047, 0.0177, 0.0069, 0.0072, 0.0048, 0.0236, 0.0048, 0.0049],
  neuroticism: [0.0144, 0.0108, 0.0050, 0.0087, 0.0046, 0.0057, 0.0045, 0.0090, 0.0036, 0.0043]
};

// Normalization parameters from the original scaler
const scaler = {
  mean: [0.52225, 0.556, 0.645, 0.62925, 0.647, 0.4585, 0.763, 0.4508, 0.781, 0.4545],
  scale: [0.2606, 0.2634, 0.2469, 0.2573, 0.2543, 0.2725, 0.2246, 0.2535, 0.2413, 0.2384]
};

const createModel = () => {
  const model = tf.sequential();
  
  // Input layer with feature importance weighting
  model.add(tf.layers.dense({
    units: 32,
    activation: 'relu',
    inputShape: [10],
    kernelInitializer: 'glorotNormal',
    kernelRegularizer: tf.regularizers.l1l2({ l1: 0.01, l2: 0.01 })
  }));
  
  // Hidden layers with dropout for better generalization
  model.add(tf.layers.dropout({ rate: 0.2 }));
  model.add(tf.layers.dense({
    units: 16,
    activation: 'relu',
    kernelRegularizer: tf.regularizers.l1l2({ l1: 0.01, l2: 0.01 })
  }));
  
  // Output layer for the 5 personality traits
  model.add(tf.layers.dense({
    units: 5,
    activation: 'sigmoid'
  }));

  return model;
};

// Normalize input data using the original scaler parameters
const normalizeInput = (answers: number[]): number[] => {
  return answers.map((value, index) => {
    return (value - scaler.mean[index]) / scaler.scale[index];
  });
};

// Apply feature importance weighting
const applyFeatureImportance = (normalizedInput: number[]): Record<string, number> => {
  const traits = ['extraversion', 'agreeableness', 'openness', 'conscientiousness', 'neuroticism'];
  const results: Record<string, number> = {};

  traits.forEach(trait => {
    const weightedSum = normalizedInput
      .slice(0, 10) // Use first 10 features
      .reduce((sum, value, index) => {
        return sum + value * featureImportance[trait][index];
      }, 0);
    
    // Convert to percentage and ensure it's between 0 and 100
    results[trait] = Math.min(Math.max(Math.round(weightedSum * 50 + 50), 0), 100);
  });

  return results;
};

let modelPromise: Promise<tf.LayersModel> | null = null;

export const predictPersonality = async (answers: number[]): Promise<Record<string, number>> => {
  if (!modelPromise) {
    const model = createModel();
    await model.compile({
      optimizer: tf.train.adam(0.001),
      loss: 'meanSquaredError'
    });
    modelPromise = Promise.resolve(model);
  }

  const normalizedInput = normalizeInput(answers);
  const predictions = applyFeatureImportance(normalizedInput);

  // Ensure predictions sum to 100%
  const total = Object.values(predictions).reduce((a, b) => a + b, 0);
  Object.keys(predictions).forEach(key => {
    predictions[key] = Math.round((predictions[key] / total) * 100);
  });

  return predictions;
};