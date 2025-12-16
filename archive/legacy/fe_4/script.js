// Function to run prediction using backend API
async function runPrediction() {
  const button = document.getElementById('predict-btn');
  try {
    if (button) {
      button.classList.add('is-loading');
      button.disabled = true;
      button.textContent = 'Predicting...';
    }

    // Call backend API
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        risk_level: 'medium',  // Default value since no control in UI
        horizon: 'Mid'  // Default value since no control in UI
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // Handle error response (if error field exists but we still got 200)
    if (data.error && !data.direction) {
      throw new Error(data.error);
    }

    // Update Market Direction
    const marketDirCard = document.querySelector('.result-card.market-dir p');
    if (marketDirCard) {
      const direction = data.direction === 'UP' ? '▲' : '▼';
      const trendText = data.direction === 'UP' ? 'Bullish Trend Expected' : 'Bearish Trend Expected';
      marketDirCard.innerHTML = `<span class="${data.direction.toLowerCase()}">${direction}</span> ${trendText}`;
    }

    // Update Top Sectors
    const sectorsCard = document.querySelector('.result-card.sectors ul');
    if (sectorsCard && Array.isArray(data.sectors)) {
      sectorsCard.innerHTML = data.sectors.map(sector => `<li>${sector}</li>`).join('');
    }

    // Update Company Recommendations
    const companiesCard = document.querySelector('.result-card.companies ul');
    if (companiesCard && Array.isArray(data.companies)) {
      companiesCard.innerHTML = data.companies.slice(0, 10).map(company => `<li>${company}</li>`).join('');
    }

    // Update Why Tier 3 chose this prediction
    const rationaleCard = document.querySelector('.result-card.rationale p');
    if (rationaleCard) {
      rationaleCard.textContent = data.reasoning || '';
    }

    // Update Market Decision Rationale Section
    const rationaleSection = document.querySelector('.rationale-dark .rationale-text');
    if (rationaleSection) {
      rationaleSection.textContent = data.reasoning || '';
    }

  } catch (error) {
    console.error('Error:', error);
    alert('Error running prediction: ' + error.message + '. Make sure the backend server is running on http://localhost:5000');
  } finally {
    if (button) {
      button.classList.remove('is-loading');
      button.disabled = false;
      button.textContent = 'Predict';
    }
  }
}

// Attach event listener to Predict button
const predictBtn = document.getElementById('predict-btn');
if (predictBtn) {
  predictBtn.addEventListener('click', async () => {
    await runPrediction();
  });
}