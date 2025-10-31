// For web/mobile apps
const API_URL = "https://models-2-ctfm.onrender.com";

async function predictSymptoms(poseFeatures) {
    try {
        const response = await fetch(`${API_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                pose_features: poseFeatures
            })
        });
        
        const results = await response.json();
        return results.predictions;
    } catch (error) {
        console.error('Prediction failed:', error);
    }
}

// Usage
const poseData = [/* your 225 features */];
const clinicalResults = await predictSymptoms(poseData);