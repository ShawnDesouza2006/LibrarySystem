// Get template and container elements from HTML
const userCardTemplate = document.querySelector('[data-user-template]');
const userCardContainer = document.querySelector('[data-user-cards-container] table');
const searchInput = document.querySelector('[data-search]');
const categorySelect = document.querySelector('[data-category-select]');
let users = [];

// Fetch all media items from API
fetch('/api/tasks')
  .then(response => response.json())
  .then(data => {
    // Create table rows for each media item
    users = data.map(task => {
      const card = userCardTemplate.content.cloneNode(true).children[0];
      card.querySelector('[data-name]').textContent = task.name;
      card.querySelector('[data-date]').textContent = task.publication_date; 
      card.querySelector('[data-author]').textContent = task.author;
      card.querySelector('[data-category]').textContent = task.category;
      // Link delete button to delete route
      card.querySelector('[data-delete]').href = `/delete/${task.id}`;

      userCardContainer.appendChild(card);

      // Store searchable data for filtering
      return { nameLower: task.name.toLowerCase(), categoryLower: task.category.toLowerCase(), element: card };
    });
  })
  .catch(error => console.error('Error:', error));

// Filter by search input
searchInput.addEventListener('input', e => {
  const value = e.target.value.toLowerCase();
  users.forEach(u => {
    const isVisible = u.nameLower.includes(value);
    u.element.classList.toggle('hide', !isVisible);
  });
});

// Filter by category selection
categorySelect.addEventListener('input', e => {
  const value = e.target.value.toLowerCase();
  users.forEach(u => {
    const isVisible = u.categoryLower.includes(value) || value === "none";
    u.element.classList.toggle('hide', !isVisible);
  });
});
