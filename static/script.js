async function searchFood() {
  const query = document.getElementById('searchInput').value;

const response = await fetch('https://your-fatsecret-api.onrender.com/search', {
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
  foods.forEach(food => {
    const p = document.createElement('p');
    p.textContent = `${food.food_name} (${food.brand_name || 'Generic'})`;
    resultsDiv.appendChild(p);
  });
}
