// Variables globales
const loginPage = document.getElementById('loginPage');
const appContent = document.getElementById('appContent');
const loginForm = document.getElementById('loginForm');
const usersTable = document.getElementById('usersTable').getElementsByTagName('tbody')[0];
const adsTable = document.getElementById('adsTable').getElementsByTagName('tbody')[0];
const ordersTable = document.getElementById('ordersTable').getElementsByTagName('tbody')[0];
const totalUsersElement = document.getElementById('totalUsers');
const totalAdsElement = document.getElementById('totalAds');
const totalOrdersElement = document.getElementById('totalOrders');
const totalRevenueElement = document.getElementById('totalRevenue');
const confirmDeleteModal = document.getElementById('confirmDeleteModal');
const confirmDeleteButton = document.getElementById('confirmDeleteButton');
const confirmValidateModal = document.getElementById('confirmValidateModal');
const confirmValidateButton = document.getElementById('confirmValidateButton');
const loadingElement = document.getElementById('loading');
const logoutButton = document.getElementById('logoutButton');
let itemIdToDelete; // Variable pour stocker l'ID de l'élément à supprimer
let itemIdToValidate; // Variable pour stocker l'ID de l'élément à valider

// Fonction pour gérer la connexion
async function login(phone, password) {
    try {
        const response = await fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ phone, password }),
        });

        if (!response.ok) {
            const data = await response.json();
            const loginError = document.getElementById('loginError');
            loginError.textContent = data.error || 'Erreur lors de la connexion.';
            loginError.style.display = 'block';
            return;
        }

        const data = await response.json();
        localStorage.setItem('token', data.token);
        showAppContent();
    } catch (error) {
        const loginError = document.getElementById('loginError');
        loginError.textContent = error.message;
        loginError.style.display = 'block';
    }
}

// Gestionnaire d'événements pour le formulaire de connexion
loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const phone = event.target.querySelector('#phone').value;
    const password = event.target.querySelector('#password').value;
    await login(phone, password);
});

// Afficher le contenu de l'application après une authentification réussie
function showAppContent() {
    loginPage.style.display = 'none';
    appContent.style.display = 'block';
    loadData();
    showPageContent();
}

// Afficher la page de connexion en cas de déconnexion
function logout() {
    loginPage.style.display = 'flex';
    appContent.style.display = 'none';
    localStorage.removeItem('token');
}

// Afficher le contenu de la page en fonction de l'ancre de l'URL
function showPageContent(page = 'dashboard') { 
    const contentDivs = document.querySelectorAll('.content > div');
    contentDivs.forEach(div => div.style.display = 'none');

    const selectedDiv = document.getElementById(page);
    if (selectedDiv) {
        selectedDiv.style.display = 'block';
    }
}

// Ajouter des gestionnaires d'événements aux liens du menu latéral
const sidebarLinks = document.querySelectorAll('.sidebar ul.nav li a');
sidebarLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); 
        const targetPage = event.target.getAttribute('href').substring(1);
        showPageContent(targetPage);
    });
});

// Mettre à jour le tableau des utilisateurs
function updateUsersTable(users) {
    usersTable.innerHTML = '';
    users.forEach(user => {
        const row = usersTable.insertRow();
        const idCell = row.insertCell();
        const photoCell = row.insertCell();
        const fullNameCell = row.insertCell();
        const phoneCell = row.insertCell();
        const roleCell = row.insertCell();
        const statusCell = row.insertCell();
        const actionsCell = row.insertCell();

        idCell.textContent = user.id;
        photoCell.innerHTML = `<img src="${user.image || 'https://via.placeholder.com/50'}" alt="Photo de profil" class="user-image">`;
        fullNameCell.textContent = user.full_name;
        phoneCell.textContent = user.phone;
        roleCell.textContent = user.role;
        statusCell.textContent = user.is_active ? 'Actif' : 'Inactif';
        actionsCell.innerHTML = `
            <a href="#" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editUserModal" data-user-id="${user.id}"><i class="bi bi-pencil"></i></a>
            <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" data-item-id="${user.id}" data-delete-url="/api/admin/users/${user.id}/delete/"><i class="bi bi-trash"></i></a>
        `;
    });
}

// Mettre à jour le tableau des annonces
function updateAdsTable(ads) {
    adsTable.innerHTML = '';
    ads.forEach(ad => {
        const row = adsTable.insertRow();
        const idCell = row.insertCell();
        const photoCell = row.insertCell();
        const titleCell = row.insertCell();
        const cityCell = row.insertCell();
        const priceCell = row.insertCell();
        const statusCell = row.insertCell();
        const actionsCell = row.insertCell();

        idCell.textContent = ad.id;
        photoCell.innerHTML = `<img src="${ad.images[0] || 'https://via.placeholder.com/50'}" alt="Image de l'annonce" class="ad-image">`;
        titleCell.textContent = ad.title;
        cityCell.textContent = ad.city;
        priceCell.textContent = ad.price_per_kg;
        statusCell.textContent = ad.is_active ? 'Active' : 'Inactive';
        actionsCell.innerHTML = `
            <a href="#" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editAdModal" data-ad-id="${ad.id}"><i class="bi bi-pencil"></i></a>
            <a href="#" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#confirmValidateModal" data-ad-id="${ad.id}" data-validate-url="/api/admin/ads/${ad.id}/validate/"><i class="bi bi-check-circle"></i></a>
            <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" data-item-id="${ad.id}" data-delete-url="/api/admin/ads/${ad.id}/delete/"><i class="bi bi-trash"></i></a>
        `;
    });
}

// Variables globales
let orderIdToEdit; // Variable pour stocker l'ID de la commande à modifier

// Gérer la modification du statut d'une commande
const editOrderStatusModal = document.getElementById('editOrderStatusModal');
const editOrderStatusForm = document.getElementById('editOrderStatusForm');

editOrderStatusModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    orderIdToEdit = button.getAttribute('data-order-id');
    const currentStatus = button.getAttribute('data-current-status');
    const statusSelect = document.getElementById('orderStatus');
    statusSelect.value = currentStatus;
});

editOrderStatusForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const newStatus = document.getElementById('orderStatus').value;
    try {
        const response = await fetch(`/api/admin/orders/${orderIdToEdit}/update-status/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status: newStatus }),
        });

        if (!response.ok) {
            throw new Error('Erreur lors de la mise à jour du statut.');
        }

        // Mise à jour réussie, mettre à jour le tableau des commandes
        loadData();

        // Masquer la modal
        const modalInstance = bootstrap.Modal.getInstance(editOrderStatusModal);
        modalInstance.hide();
    } catch (error) {
        console.error('Erreur:', error);
    }
});

// Mettre à jour le tableau des commandes
function updateOrdersTable(orders) {
    ordersTable.innerHTML = '';
    orders.forEach(order => {
        const row = ordersTable.insertRow();
        const idCell = row.insertCell();
        const userCell = row.insertCell();
        const adCell = row.insertCell();
        const quantityCell = row.insertCell();
        const statusCell = row.insertCell();
        const actionsCell = row.insertCell();

        idCell.textContent = order.id;
        userCell.textContent = order.user.full_name;
        adCell.textContent = order.ad.title;
        quantityCell.textContent = order.quantity;
        statusCell.textContent = order.status;
        actionsCell.innerHTML = `
            <a href="#" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editOrderModal" data-order-id="${order.id}"><i class="bi bi-pencil"></i></a>
            <a href="#" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#editOrderStatusModal" data-order-id="${order.id}" data-current-status="${order.status}"><i class="bi bi-arrow-repeat"></i></a>
            <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" data-item-id="${order.id}" data-delete-url="/api/admin/orders/${order.id}/delete/"><i class="bi bi-trash"></i></a>
        `;
    });
}



// Mettre à jour les statistiques du tableau de bord
function updateDashboardStats(data) {
    totalUsersElement.textContent = data.total_users;
    totalAdsElement.textContent = data.total_ads;
    totalOrdersElement.textContent = data.total_orders;
    totalRevenueElement.textContent = data.revenue.toFixed(2); // Affiche le revenu avec 2 décimales
}

// Gérer la suppression d'un élément
confirmDeleteModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    itemIdToDelete = button.getAttribute('data-item-id');
    const deleteUrl = button.getAttribute('data-delete-url');
    confirmDeleteButton.setAttribute('data-delete-url', deleteUrl);
});

confirmDeleteButton.addEventListener('click', () => {
    const deleteUrl = confirmDeleteButton.getAttribute('data-delete-url');
    deleteItem(deleteUrl)
        .then(() => {
            // Supprimer la ligne du tableau après la suppression réussie
            const rowToDelete = document.querySelector(`[data-item-id="${itemIdToDelete}"]`).closest('tr');
            rowToDelete.remove();
            // Masquer la modal de confirmation
            const modalInstance = bootstrap.Modal.getInstance(confirmDeleteModal);
            modalInstance.hide();
        })
        .catch(error => console.error(error));
});

async function deleteItem(deleteUrl) {
    try {
        const response = await fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error('Erreur lors de la suppression.');
        }
        // Suppression réussie
        return;
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
}

// Gérer la validation d'une annonce
confirmValidateModal.addEventListener('show.bs.modal', event => {
    const button = event.relatedTarget;
    itemIdToValidate = button.getAttribute('data-ad-id');
    const validateUrl = button.getAttribute('data-validate-url');
    confirmValidateButton.setAttribute('data-validate-url', validateUrl);
});

confirmValidateButton.addEventListener('click', () => {
    const validateUrl = confirmValidateButton.getAttribute('data-validate-url');
    validateAd(validateUrl)
        .then(() => {
            // Mettre à jour le statut de l'annonce après la validation réussie
            const rowToUpdate = document.querySelector(`[data-ad-id="${itemIdToValidate}"]`).closest('tr');
            const statusCell = rowToUpdate.querySelector('td:nth-child(6)');
            statusCell.textContent = 'Active';
            // Masquer la modal de confirmation
            const modalInstance = bootstrap.Modal.getInstance(confirmValidateModal);
            modalInstance.hide();
        })
        .catch(error => console.error(error));
});

async function validateAd(validateUrl) {
    try {
        const response = await fetch(validateUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });
        if (!response.ok) {
            throw new Error('Erreur lors de la validation.');
        }
        // Validation réussie
        return;
    } catch (error) {
        console.error('Erreur:', error);
        throw error;
    }
}

// Charger les données depuis l'API
async function loadData() {
    try {
        loadingElement.style.display = 'block';
        const response = await fetch('/api/dashboard/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error('Erreur lors du chargement des données.');
        }

        const data = await response.json();
        updateUsersTable(data.users);
        updateAdsTable(data.ads);
        updateOrdersTable(data.orders);
        updateDashboardStats(data.stats);
    } catch (error) {
        console.error('Erreur:', error);
    } finally {
        loadingElement.style.display = 'none';
    }
}

// Vérifier si un jeton est présent dans localStorage
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        showAppContent();
    } else {
        loginPage.style.display = 'flex';
    }
});

// Gérer la déconnexion
logoutButton.addEventListener('click', () => {
    logout();
});
