
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
const totalManagerRevenueElement = document.getElementById('managerRevenue');

const confirmDeleteModal = document.getElementById('confirmDeleteModal');
const confirmDeleteButton = document.getElementById('confirmDeleteButton');
const confirmValidateModal = document.getElementById('confirmValidateModal');
const confirmValidateButton = document.getElementById('confirmValidateButton');
const userChartElement = document.getElementById('userChart');
const loadingElement = document.getElementById('loading');
const logoutButton = document.getElementById('logoutButton');
const orderChartElement = document.getElementById('orderChart');
let promotionImages = [];
let itemIdToDelete; // Variable pour stocker l'ID de l'élément à supprimer
let itemIdToValidate; // Variable pour stocker l'ID de l'élément à valider
let userChart;
let userRoles;

let orderChart;
let orderDatat;
let itemIdToEdit;

// ... (Votre code existant)
const priceRulesTable = document.getElementById('priceRulesTable').getElementsByTagName('tbody')[0];




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
        row.setAttribute('data-item-id', user.id); //  Add this line


        // Vérifiez si 'image' est défini avant de l'utiliser
        photoCell.innerHTML = user.image
            ? `<img src="${user.image}" alt="Photo de profil" class="user-image">`
            : `<img src="https://via.placeholder.com/50" alt="Photo de profil" class="user-image">`;

        fullNameCell.textContent = user.full_name;
        phoneCell.textContent = user.phone;
        roleCell.textContent = user.role;
        statusCell.textContent = user.is_active ? 'Actif' : 'Inactif';
        actionsCell.innerHTML = `
          <a href="#" class="btn btn-sm btn-primary" data-bs-toggle="modal" 
            data-bs-target="#editUserModal"
          ><i class="bi bi-pencil"></i></a>

          <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" 
            data-item-id="${user.id}" 
            data-delete-url="/api/admin/users/${user.id}/delete/"  
          >
             <i class="bi bi-trash"></i>
         </a>
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
        // photoCell.innerHTML = `<img src="${ad.images[0] || 'https://via.placeholder.com/50'}" alt="Image de l'annonce" class="ad-image">`;
        // Assuming 'image' field in your Ad model now
        photoCell.innerHTML = ad.image
            ? `<img src="${ad.image}" alt="Image de l'annonce" class="ad-image">`
            : `<img src="https://via.placeholder.com/50" alt="Image de l'annonce" class="ad-image">`;
        titleCell.textContent = ad.title;
        cityCell.textContent = ad.address; // Assuming 'address' is the field for city
        priceCell.textContent = ad.price_per_kg;
        statusCell.textContent = ad.is_active ? 'Active' : 'Inactive';
        actionsCell.innerHTML = `
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
        userCell.textContent = order.user.full_name; // Assuming 'user' is an object with 'full_name'
        adCell.textContent = order.ad.title; // Assuming 'ad' is an object with 'title'
        quantityCell.textContent = order.quantity;
        statusCell.textContent = order.status;
        actionsCell.innerHTML = `
            <a href="#" class="btn btn-sm btn-success" data-bs-toggle="modal" data-bs-target="#editOrderStatusModal" data-order-id="${order.id}" data-current-status="${order.status}"><i class="bi bi-arrow-repeat"></i></a>
            <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" data-item-id="${order.id}" data-delete-url="/api/admin/orders/${order.id}/delete/"><i class="bi bi-trash"></i></a>
        `;
    });
}

// ... (Votre code existant) 

// --- Modification pour l'affichage des règles --- 
function updatePriceRulesTable(priceRules) {
    priceRulesTable.innerHTML = '';
    priceRules.forEach(rule => {
        const row = priceRulesTable.insertRow();
        row.insertCell().textContent = rule.id;
        row.insertCell().textContent = rule.role;
        row.insertCell().textContent = rule.min_price;
        row.insertCell().textContent = rule.max_price || "Illimité"; // Affichage plus clair
        row.insertCell().textContent = rule.price_increase_percentage ? rule.price_increase_percentage + "%" : "-"; //  Ajout du signe % 
        row.insertCell().textContent = rule.fixed_price || "-";
        row.insertCell().innerHTML = ` 
        <a href="#" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addPriceRuleModal"  
            data-rule-id="${rule.id}" 
            data-role="${rule.role}" 
            data-min-price="${rule.min_price}"
            data-max-price="${rule.max_price || ''}" 
            data-percentage="${rule.price_increase_percentage || ''}"
            data-fixed-price="${rule.fixed_price || ''}"
        >
            <i class="bi bi-pencil"></i>
        </a>

        <!-- Lien de suppression : -->
        <a href="#" class="btn btn-sm btn-danger" data-bs-toggle="modal" data-bs-target="#confirmDeleteModal" 
            data-item-id="${rule.id}" 
            data-delete-url="/api/admin/price_rules/${rule.id}/delete/"  
        >
            <i class="bi bi-trash"></i>
        </a>
    `;
    });
}

// --- Gestion de la modal d'ajout/modification  ---

const addPriceRuleModal = document.getElementById('addPriceRuleModal');
const priceRuleForm = document.getElementById('priceRuleForm');

addPriceRuleModal.addEventListener('show.bs.modal', (event) => {
    const button = event.relatedTarget;
    const ruleId = button ? button.getAttribute('data-rule-id') : null;

    // Réinitialisation du formulaire
    priceRuleForm.reset();
    document.getElementById('ruleId').value = '';

    // Si on modifie une règle existante
    if (ruleId) {
        document.getElementById('addPriceRuleModalLabel').textContent = "Modifier la Règle de Prix";
        document.getElementById('ruleId').value = ruleId;

        document.getElementById('role').value = button.getAttribute('data-role');
        document.getElementById('min_price').value = button.getAttribute('data-min-price');
        document.getElementById('max_price').value = button.getAttribute('data-max-price');
        document.getElementById('price_increase_percentage').value = button.getAttribute('data-percentage');
        document.getElementById('fixed_price').value = button.getAttribute('data-fixed-price');
    } else {
        document.getElementById('addPriceRuleModalLabel').textContent = "Ajouter une Règle de Prix";
    }
});

// Gestion de la soumission du formulaire
priceRuleForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const ruleId = document.getElementById('ruleId').value;
    const method = ruleId ? 'PUT' : 'POST';
    const endpoint = ruleId ? `/api/admin/price_rules/${ruleId}/` : '/api/admin/price_rules/';

    // Créer l'objet data pour la requête fetch
    const data = {
        role: document.getElementById('role').value,
        min_price: parseInt(document.getElementById('min_price').value, 10),
        max_price: document.getElementById('max_price').value ? parseInt(document.getElementById('max_price').value, 10) : null,
        price_increase_percentage: parseFloat(document.getElementById('price_increase_percentage').value) || null, // Utilise parseFloat et vérifie si NaN
        fixed_price: document.getElementById('fixed_price').value ? parseInt(document.getElementById('fixed_price').value, 10) : null
    };
    console.log("Data being sent", data)

    try {
        const response = await fetch(endpoint, {
            method: method,
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        console.log(response)

        if (response.ok) {
            // Fermer le modal
            bootstrap.Modal.getInstance(addPriceRuleModal).hide();

            // Recharger les données
            loadData();
        } else {
            // Gestion des erreurs 
            const errorData = await response.json();
            console.error('Erreur serveur :', errorData);
        }
    } catch (error) {
        // Gestion des erreurs réseau ou autres 
        console.error('Erreur :', error);
    }
});



// ... (Reste de votre code)
// Mettre à jour les statistiques du tableau de bord
function updateDashboardStats(data) {
    totalUsersElement.textContent = data.total_users;
    totalAdsElement.textContent = data.total_ads;
    totalOrdersElement.textContent = data.total_orders;
    totalRevenueElement.textContent = data.current_revenue ? data.current_revenue.toFixed(2) : '0.00'; // Affiche le revenu avec 2 décimales
    totalManagerRevenueElement.textContent = data.manager_revenue ? data.current_revenue.toFixed(2) : '0.00'; // Affiche le revenu avec 2 décimales
    userRoles = data.user_roles
    //console.log(data.orders_evolution)
    orderDatat = data.orders_evolution
}

// ... Your existing JavaScript code ... 

//  ----  Handle Cloudinary Config Saving ---

// ... rest of the existing code

// ...

async function loadPromotionImages() {
    try {
        // Fetch promotion URLs from API (e.g. to display them in the UI)  
        const response = await fetch('/api/admin/promotion_images/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error: HTTP ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        if (data) {
            promotionImages = data.map(img => img.url);
            console.log('promotionImages:', promotionImages);
            //   ... if you are re-displaying the URLs 
            // updateImageUrls(); // Use this to update your HTML list of image urls (assuming this exists) 
        }

    } catch (error) {
        // ...   Log or display errors - for user experience
        console.error('Error loading promotion images', error);
        alert('Error: Unable to fetch Promotion Images.');
    }

}
// ---- Handle Cloudinary Config Saving ---- 
// Make sure this fetches the appropriate URLs
document.getElementById('saveCloudinarySettings').addEventListener('click', async (event) => {
    const cloudinary_cloud_name = document.getElementById('cloudinary_cloud_name').value;
    const cloudinary_api_key = document.getElementById('cloudinary_api_key').value;
    const cloudinary_api_secret = document.getElementById('cloudinary_api_secret').value;

    try {
        // Your post logic to the correct url (from your Django REST view): 
        const response = await fetch('/api/admin/configs/cloudinary', { // Update to match the endpoint  
            // Update method for new view (cloudinary_config)  
            method: 'PATCH',  // Use PATCH 
            headers: {
                //  ... Headers: Content-Type, authorization
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                'cloudinary_cloud_name': cloudinary_cloud_name,
                'cloudinary_api_key': cloudinary_api_key,
                'cloudinary_api_secret': cloudinary_api_secret
            })
        });

        if (response.ok) {
            console.log('Cloudinary configuration updated!');
            // If there are changes, such as to the images: 
            //  reloadPromotionImages(); // This might trigger 
            // other calls (and refreshes) of other functions! 
        }

    } catch (error) {
        //   ...  Error Handling (make sure it will be returned)
        //   You might alert the user  
        console.error('Error updating Cloudinary configs:', error);
        alert('Erreur lors de la mise à jour de la configuration Cloudinary.');
        return;
    }

});

// ---  Image Upload Function  ---  (with a Helper) 
document.getElementById('uploadPromotionImage').addEventListener('click', () => {
    const imageFile = document.getElementById('promotionImageUpload').files[0];
    const altText = document.getElementById('promotionImageAltText').value;

    // ... rest of the image upload (error handling, form, etc.).

    if (!imageFile) {
        alert("Veuillez choisir une image!");
        return;
    }

    // (Update the image using this view (use 'fetch' call)!
    uploadPromotionImage(imageFile, altText);
});

async function uploadPromotionImage(imageFile, altText) {
    try {
        // 1. Create FormData
        const formData = new FormData();
        formData.append('image', imageFile); // Appending image to form data
        formData.append('altText', altText);  // Appending Alt text, if applicable

        // 2. Send the fetch Request
        const response = await fetch('/api/admin/upload_promotion_image/', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            //  --- Handle errors, including an error response. 
            console.error("Error uploading image: ", response);
            const data = await response.json(); // This will likely get an "error" message from your Django View. 
            alert(`Error uploading image: ${data.message || data.error || 'General error'}.`);
            return; // stop executing if there is an error  
        }

        // 3. Get the Image URL (if success) 
        const data = await response.json();
        console.log(data)

        // 4. Success! 
        // (Note, "data.url" or any other way you will need to check how 
        // you want to structure your response - such as sending the 
        // ID if you also need this to be added into your 
        //   "promotionImages" array:
        if (data.success) {
            const cloudinaryImageURL = data.url;  // Update image URL

            if (cloudinaryImageURL) {
                // (Reload promotion images array/display it using  
                // your promotionImages array that you are using - or using a function that makes a new GET call and refreshes it!  
                // Such as your `loadPromotionImages() ` that was used for initial loading, to update on the screen -  (if you are updating in a "view")   

                console.log(cloudinaryImageURL)

                //   If there is a user (and if your Django logic 
                //   allows this to save it to your database for a user!)  
                //  // Add this image to your "promotionImages" array:
                // promotionImages.push(cloudinaryImageURL) // or handle your UI for promotionImages (if a <ul>, etc).

                // Make the call to your backend! Make a new 
                // `loadPromotionImages` (if you already have it defined)!

                loadPromotionImages();  // reload your promotion images, this
                // assumes that it's going to get new values (by going
                // through your Django endpoint to reload).  
                // if your images are displayed via `<li>`s, ensure this call
                // refreshes them - for a better UI, instead of reloading, just
                // do it with JS after it's fetched.  (the list might need to be 
                // added, or you need to modify your data to make a more
                //  dynamic, cleaner setup.

            } else {
                // Handle error (alert message).
                console.error("Error getting promotion image URL: ", response);
                // Handle error appropriately in front-end (alert to user). 
            }

        } else {
            // ...  Handle the failure response ... (e.g., alert the user, and give any "error messages") 
            alert('Image upload failed.')  // Handle errors in front-end and backend
            return;
            // Don't proceed (it'll continue) if there is a failure during this
            //   image uploading
        }

    } catch (error) {
        // ... handle errors - could be network, timeout, etc ...  (use `console.error`, use `alert`,  use the Javascript Error method (such as throwing errors!) for more robust control
    }

}

// ---  Add a new URL ---- (For Image URLs):
// document.getElementById('uploadPromotionImage').addEventListener('click', async (event) => {
//     // const newImageUrl = promotionImageUrlInput.value.trim();

//     // if (!newImageUrl || (!newImageUrl.startsWith('http') && !newImageUrl.startsWith('https'))) {
//     //     alert('Veuillez saisir une URL d’image valide.');
//     //     return;
//     // }

//     try {
//         // ... ( your post fetch)

//         const response = await fetch('/api/admin/promotion_images/add/', {
//             method: 'POST',
//             headers: {
//                 'Authorization': `Bearer ${localStorage.getItem('token')}`,
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ url: newImageUrl }),
//         });

//         if (!response.ok) {
//             // Handle errors!  ... (If 5 max URLs, return to front end and 
//             // prevent it from showing. This can all be done with the same
//             // backend logic.
//         }

//         const result = await response.json();

//         // promotionImages.push(newImageUrl); // Note this: "push" onto array.
//         //   You are using this array if the user is typing in the images: 
//         //  --- (Your HTML is where this array will need to be iterated)

//         // promotionImageUrlInput.value = "";  // Resetting 

//         // ... Update UI after success to add a new Image or update  
//         //        your view of the promotion Images list on the  page!

//     } catch (error) {
//         console.error('Error saving promotion image url:', error);
//         // ... (User Alerts /  Displaying)
//     }
// });

//  --- (Existing  Code for "fetch", loading)  ----


//  --- ... Your existing JavaScript for your application ... ---


// Fonction pour mettre à jour le graphique en camembert
function updateUserChart(userRoles) {
    if (userChart) {
        userChart.destroy();
    }
    userChart = new Chart(userChartElement, {
        type: 'pie',
        data: {
            labels: Object.keys(userRoles),
            datasets: [{
                data: Object.values(userRoles),
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                hoverBackgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                }
            }
        }
    });
}

// Edit user role: 
usersTable.addEventListener('click', (event) => {
    if (event.target.classList.contains('btn-primary')) {
        // Edit button is pressed: 
        const userId = event.target.closest('tr').getAttribute('data-item-id');
        itemIdToEdit = userId;

        //  Show Edit User Role modal
        const editUserForm = document.getElementById('editUserForm');
        const roleDropdown = editUserForm.querySelector('#userRole');
        editUserForm.querySelector('#userId').value = userId; // Update User ID in Form

        fetch(`/api/users/${userId}/`, { // API call to fetch user data 
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Error: HTTP ${response.status} ${response.statusText}`);
                }
                return response.json();
            })
            .then(userData => {
                if (!userData.role) {
                    console.error("Error fetching user role data!");
                } else {
                    roleDropdown.value = userData.role;
                }
            })
            .catch(error => {
                console.error('Error updating user role data:', error);
                // Handle the error gracefully 
            })


    }
});

document.getElementById('editUserForm').addEventListener('submit', (event) => {
    event.preventDefault(); // Prevents default form submit
    const form = event.target;

    const userId = itemIdToEdit;
    const newRole = form.querySelector('#userRole').value;

    if (!userId) {
        console.error("Error: Missing userId for the edit form.");
        return; // Return and do nothing more. 
    }

    fetch(`/api/admin/users/${userId}/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
        body: JSON.stringify({ role: newRole })
    })
        .then(response => {
            if (response.ok) {
                // Reload users table for data to refresh 
                loadData();

                // Close Modal after submitting.  
                const editUserModal = bootstrap.Modal.getInstance(document.getElementById('editUserModal'));
                editUserModal.hide();
            } else {
                // ... handle error, likely get error response data here. 
            }
        })
        .catch(error => {
            // handle the error more gracefully
            console.error('Error saving user role data', error)
        });


});

function updateOrderChart(orderDatat) {
    if (orderChart) {
        orderChart.destroy();
    }

    const dates = orderDatat.map(item => {
        let formattedDate = new Date(item.created_at__date); // Use the JS `Date` constructor
        //  You can still use moment to format this date object further if you wish!
        //  Example (you will probably not need this as it was the default output of `DateTimeField`) 
        //  const datePart = moment(formattedDate).format('DD/MM'); // Use this only if needed to format 
        return formattedDate;
    });

    console.log(dates);
    const orderCounts = orderDatat.map(item => item.count);

    orderChart = new Chart(orderChartElement, {
        type: 'line',
        data: {
            labels: dates,
            datasets: [{
                label: 'Nombre de Commandes',
                data: orderCounts,
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1,
                tension: 0.2
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: {
                            day: 'dd/MM' // Use Moment for display formatting if desired
                        }
                    },
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}


async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard/', { // Use the correct API endpoint for dashboard stats
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error(`Erreur HTTP : ${response.status} ${response.statusText}`);
        }

        const data = await response.json();

        // Update Dashboard Stats 
        updateDashboardStats(data);

        // Update User Roles Chart


    } catch (error) {
        console.error('Erreur lors du chargement des données du tableau de bord :', error);
        // Handle errors by showing error messages to the user 
    } finally {
        hideLoading();
    }
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
            method: 'PUT', // Use PUT for updating
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

        // Charger les statistiques du tableau de bord
        const statsResponse = await fetch('/api/admin/stats/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!statsResponse.ok) {
            throw new Error('Erreur lors du chargement des statistiques.');
        }

        const statsData = await statsResponse.json();
        updateDashboardStats(statsData);

        // Charger les utilisateurs
        const usersResponse = await fetch('/api/admin/users/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!usersResponse.ok) {
            throw new Error('Erreur lors du chargement des utilisateurs.');
        }

        const usersData = await usersResponse.json();
        updateUsersTable(usersData);

        // Charger les annonces
        const adsResponse = await fetch('/api/admin/ads/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!adsResponse.ok) {
            throw new Error('Erreur lors du chargement des annonces.');
        }

        const adsData = await adsResponse.json();
        updateAdsTable(adsData);

        // Charger les commandes
        const ordersResponse = await fetch('/api/admin/orders/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json',
            },
        });

        if (!ordersResponse.ok) {
            throw new Error('Erreur lors du chargement des commandes.');
        }

        const ordersData = await ordersResponse.json();
        updateOrdersTable(ordersData);

        const priceRulesResponse = await fetch('/api/admin/price_rules/', {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
        });

        if (!priceRulesResponse.ok) {
            throw new Error('Erreur lors du chargement des règles de prix.');
        }

        const priceRulesData = await priceRulesResponse.json();
        updatePriceRulesTable(priceRulesData); // Met à jour le tableau HTML

        updateUserChart(userRoles);
        updateOrderChart(orderDatat);

        await loadPromotionImages()



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