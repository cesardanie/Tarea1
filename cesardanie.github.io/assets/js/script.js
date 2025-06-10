Ejemplo: config de Chart.js para habilidades
document.addEventListener('DOMContentLoaded', () => {
  const ctx = document.getElementById('chartSkills')?.getContext('2d');
  if (ctx) {
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Angular', 'TypeScript', 'JavaScript', 'CSS', 'SQL'],
        datasets: [{
          label: 'Nivel (%)',
          data: [80, 75, 85, 70, 65],
          backgroundColor: 'rgba(76, 175, 80, 0.5)',
          borderColor: 'rgba(76, 175, 80, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: { beginAtZero: true, max: 100 }
        }
      }
    });
  }
});