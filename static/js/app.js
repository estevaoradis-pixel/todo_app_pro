// ToDo Pro Senior - JS Avançado
document.addEventListener('DOMContentLoaded', function() {
    AOS.init({
        duration: 800,
        once: true,
        offset: 100
    });

    // Dark Mode Toggle
    const darkToggle = document.getElementById('darkToggle');
    const body = document.body;
    const isDark = localStorage.getItem('darkMode') === 'true';
    
    if (isDark) {
        body.classList.add('dark-mode');
        darkToggle.querySelector('i').className = 'fas fa-sun';
    }

    darkToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        const isDarkMode = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkMode);
        this.querySelector('i').className = isDarkMode ? 'fas fa-sun' : 'fas fa-moon';
    });

    // Live Search & Filter
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    const sortSelect = document.getElementById('sortSelect');
    const clearFiltersBtn = document.getElementById('clearFilters');
    const tasksContainer = document.getElementById('tasksContainer');

    function filterTasks() {
        const query = searchInput.value.toLowerCase();
        const filter = filterSelect.value;
        const sort = sortSelect.value;

        const taskCards = tasksContainer.querySelectorAll('.task-card-wrapper');
        
        taskCards.forEach(card => {
            const title = card.querySelector('.task-title').textContent.toLowerCase();
            const completed = card.querySelector('.task-check') ? card.querySelector('.task-check').checked : false;
            const priority = parseInt(card.dataset.priority || 2);
            
            // Search
            const matchesSearch = title.includes(query);
            
            // Filter
            let matchesFilter = true;
            if (filter === 'pending' && completed) matchesFilter = false;
            if (filter === 'completed' && !completed) matchesFilter = false;
            if (filter === 'high' && priority !== 1) matchesFilter = false;
            
            card.style.display = (matchesSearch && matchesFilter) ? '' : 'none';
        });

        // Simple sort (client-side)
        const visibleCards = Array.from(taskCards).filter(c => c.style.display !== 'none');
        visibleCards.sort((a, b) => {
            if (sort === 'priority') {
                return parseInt(a.dataset.priority) - parseInt(b.dataset.priority);
            }
            // Add more sorts
            return 0;
        });
        
        visibleCards.forEach(card => tasksContainer.appendChild(card));
    }

    if (searchInput) {
        searchInput.addEventListener('input', filterTasks);
    }
    if (filterSelect) {
        filterSelect.addEventListener('change', filterTasks);
    }
    if (sortSelect) {
        sortSelect.addEventListener('change', filterTasks);
    }
    if (clearFiltersBtn) {
        clearFiltersBtn.addEventListener('click', function() {
            searchInput.value = '';
            filterSelect.value = 'all';
            sortSelect.value = 'created';
            filterTasks();
        });
    }

    // Form focus
    const contentInput = document.querySelector('input[name="content"]');
    if (contentInput) contentInput.focus();

    // Toggle animations
    document.addEventListener('click', function(e) {
        if (e.target.closest('.toggle-btn')) {
            const card = e.target.closest('.task-card');
            card.classList.add('loading');
            setTimeout(() => {
                card.classList.add('check-bounce');
                setTimeout(() => card.classList.remove('loading', 'check-bounce'), 600);
            }, 300);
        }
    });

    // Realtime updates via API (bonus)
    setInterval(function() {
        fetch('/api/tasks')
            .then(res => res.json())
            .then(tasks => {
                // Update stats if available
                if (window.location.pathname === '/') {
                    // Simple refresh trigger if changed
                }
            })
            .catch(() => {}); // Silent fail
    }, 30000); // 30s

    // Enter to add task
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        taskForm.addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA') {
                e.preventDefault();
                taskForm.submit();
            }
        });
    }

    // Smooth scroll reveal
    window.addEventListener('scroll', function() {
        const cards = document.querySelectorAll('.task-card-wrapper');
        cards.forEach((card, index) => {
            const rect = card.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom > 0) {
                card.style.animationDelay = `${index * 0.1}s`;
                card.style.animationPlayState = 'running';
            }
        });
    });
});

