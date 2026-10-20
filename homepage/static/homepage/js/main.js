document.addEventListener('DOMContentLoaded', () => {
  const cards = document.querySelectorAll('.incident-card');
  cards.forEach(card => card.setAttribute('title', 'Откройте карточку для подробностей'));
  console.info('Интерфейс учета инцидентов загружен');
});
