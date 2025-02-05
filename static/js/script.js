document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.querySelector('.toggle-sidebar');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const navbar = document.querySelector('.navbar');
    const menuItems = document.querySelectorAll('.sidebar .nav-link');

    // Função para expandir o menu
    function expandSidebar() {
        sidebar.classList.remove('collapsed');
        mainContent.classList.remove('expanded');
        navbar.classList.remove('expanded');
        toggleBtn.classList.remove('collapsed');

        // Atualizar ícone do botão toggle
        const icon = toggleBtn.querySelector('i');
        icon.classList.replace('bi-chevron-right', 'bi-chevron-left');

        // Atualizar localStorage
        localStorage.setItem('sidebarCollapsed', 'false');
    }

    // Função para colapsar o menu
    function collapseSidebar() {
        sidebar.classList.add('collapsed');
        mainContent.classList.add('expanded');
        navbar.classList.add('expanded');
        toggleBtn.classList.add('collapsed');

        // Atualizar ícone do botão toggle
        const icon = toggleBtn.querySelector('i');
        icon.classList.replace('bi-chevron-left', 'bi-chevron-right');

        // Atualizar localStorage
        localStorage.setItem('sidebarCollapsed', 'true');
    }

    // Função para alternar o estado do menu
    function toggleSidebar() {
        if (sidebar.classList.contains('collapsed')) {
            expandSidebar();
        } else {
            collapseSidebar();
        }
    }

    // Adicionar evento de clique ao botão toggle
    toggleBtn.addEventListener('click', function(e) {
        e.preventDefault();
        toggleSidebar();
    });

    // Adicionar eventos aos itens do menu
    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Se o item clicado tem submenu (collapse)
            if (this.getAttribute('data-bs-toggle') === 'collapse') {
                e.preventDefault(); // Previne o comportamento padrão

                // Se o sidebar está colapsado, expande primeiro
                if (sidebar.classList.contains('collapsed')) {
                    expandSidebar();

                    // Pequeno delay para garantir que a expansão do submenu funcione corretamente
                    setTimeout(() => {
                        const collapseElement = document.querySelector(this.getAttribute('href'));
                        if (collapseElement) {
                            const bsCollapse = new bootstrap.Collapse(collapseElement);
                            bsCollapse.toggle();
                        }
                    }, 150);
                }
            } else {
                // Se o sidebar está colapsado e o item não tem submenu
                if (sidebar.classList.contains('collapsed')) {
                    expandSidebar();
                }
            }
        });
    });

    // Recuperar e aplicar estado do menu do localStorage ao carregar a página
    const isSidebarCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
    if (isSidebarCollapsed) {
        collapseSidebar();
    }

    // Adicionar responsividade para telas pequenas
    function checkScreenSize() {
        if (window.innerWidth <= 768) {
            expandSidebar();
        }
    }

    // Verificar tamanho da tela ao redimensionar
    window.addEventListener('resize', checkScreenSize);
    // Verificar tamanho inicial da tela
    checkScreenSize();
});