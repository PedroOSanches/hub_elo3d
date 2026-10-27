function initProjectsPage() {
  const search = document.getElementById('project-search');
  const rows = [...document.querySelectorAll('#projects-list project-row')];

  if (!search) return;

  search.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    rows.forEach(row => {
      row.hidden = query !== '' && !row.dataset.project.includes(query);
    });
  });
}

window.initProjectsPage = initProjectsPage;
