async function searchFood() {
  const query = document.getElementById('searchInput').value;

  const response = await fetch('https://fatsecret.onrender.com/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  });

  const data = await response.json();
  const foods = data.foods?.food || [];
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  if (foods.length === 0) {
    resultsDiv.textContent = 'No results found.';
    return;
  }

  foods.forEach(food => {
    const p = document.createElement('p');
    p.textContent = `${food.food_name} (${food.brand_name || 'Generic'})`;
    p.style.cursor = 'pointer';
    p.onclick = () => getNutrition(food.food_id);  // 👈 attaches click
    resultsDiv.appendChild(p);
  });

  console.log("🍕 API raw response:", data);
}

async function getNutrition(food_id) {
  const response = await fetch('https://fatsecret.onrender.com/food_details', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ food_id })
  });

  const data = await response.json();
  const serving = data.food?.servings?.serving;

  if (!serving) {
    alert("Nutrition data not available.");
    return;
  }

  alert(`🍕 Nutrition per serving:
- Calories: ${serving.calories}
- Protein: ${serving.protein}g
- Fat: ${serving.fat}g
- Carbs: ${serving.carbohydrate}g`);
}
