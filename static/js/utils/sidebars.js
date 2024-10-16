// Funciones para abrir y cerrar sidebars
function openSidebar(id) {
    document.getElementById(id).classList.remove('-translate-x-full', 'translate-x-full');
}

function closeSidebarLeft(id) {
    console.log(`Cerrando sidebar: ${id}`);
    document.getElementById(id).classList.add('-translate-x-full');
}

function closeSidebarRight(id) {
    console.log(`Cerrando sidebar: ${id}`);
    document.getElementById(id).classList.add('translate-x-full');
}


// se tendrian que mover a la izquierda para ocultarse
document.getElementById('menuButton').addEventListener('click', () => openSidebar('menuSidebar'));
document.getElementById('closeMenuButton').addEventListener('click', () => closeSidebarLeft('menuSidebar'));

document.getElementById('openCategoriaSidebar').addEventListener('click', () => openSidebar('CategoriaSidebar'));
document.getElementById('closeCategoriaSidebar').addEventListener('click', () => closeSidebarLeft('CategoriaSidebar'));

for (let i = 1; i <= 15; i++) {
    document.getElementById(`openCat${i}Sidebar`).addEventListener('click', () => openSidebar(`Cat${i}Sidebar`));
    document.getElementById(`closeCat${i}Sidebar`).addEventListener('click', () => closeSidebarLeft(`Cat${i}Sidebar`));
}

// se tendrian que mover a la izquierda para desaparecer de pantalla
document.getElementById('searchButton').addEventListener('click', () => openSidebar('searchSidebar'));
document.getElementById('closeSearchButton').addEventListener('click', () => closeSidebarRight('searchSidebar'));

document.getElementById('cartButton').addEventListener('click', () => openSidebar('cartSidebar'));
document.getElementById('closeCartButton').addEventListener('click', () => closeSidebarRight('cartSidebar'));

document.getElementById('userButton').addEventListener('click', () => openSidebar('userSidebar'));
document.getElementById('closeUserButton').addEventListener('click', () => closeSidebarRight('userSidebar'));