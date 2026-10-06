const API_URL = "http://127.0.0.1:8000";


// =========================
// LOAD USERS
// =========================

async function loadUsers() {

    const tableBody =
        document.getElementById("usersTableBody");

    if (!tableBody) {
        return;
    }

    try {

        const response =
            await fetch(`${API_URL}/users`);

        if (!response.ok) {
            throw new Error("Failed to load users");
        }

        const data =
            await response.json();

        tableBody.innerHTML = "";

        data.users.forEach(user => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${user[0]}</td>
                <td>${user[1]}</td>
                <td>${user[2]}</td>
                <td>${user[3]}</td>

                <td>

                    <button
                        class="edit-button"
                        onclick='editUser(
                            ${user[0]},
                            ${JSON.stringify(user[1])},
                            ${JSON.stringify(user[2])},
                            ${JSON.stringify(user[3])}
                        )'>

                        Edit

                    </button>

                    <button
                        class="delete-button"
                        onclick="deleteUser(${user[0]})">

                        Delete

                    </button>

                </td>
            `;

            tableBody.appendChild(row);

        });

    }

    catch (error) {

        console.error(error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="5">
                    Unable to load users.
                    Check FastAPI and CORS.
                </td>
            </tr>
        `;

    }
}


// =========================
// LOAD ACCOUNTS
// =========================

async function loadAccounts() {

    const tableBody =
        document.getElementById("accountsTableBody");

    if (!tableBody) {
        return;
    }

    try {

        const response =
            await fetch(`${API_URL}/accounts`);

        if (!response.ok) {
            throw new Error("Failed to load accounts");
        }

        const data =
            await response.json();

        tableBody.innerHTML = "";

        data.accounts.forEach(account => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${account[0]}</td>
                <td>${account[1]}</td>
                <td>${account[2]}</td>
                <td>${account[3]}</td>
                <td>₹${account[4]}</td>

                <td>

                    <button
                        class="edit-button"
                        onclick="editAccount(${account[0]})">

                        Edit

                    </button>

                    <button
                        class="delete-button"
                        onclick="deleteAccount(${account[0]})">

                        Delete

                    </button>

                </td>
            `;

            tableBody.appendChild(row);

        });

    }

    catch (error) {

        console.error(error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="6">
                    Unable to load accounts.
                </td>
            </tr>
        `;

    }
}


// =========================
// LOAD TRANSACTIONS
// =========================

async function loadTransactions() {

    const tableBody =
        document.getElementById("transactionsTableBody");

    if (!tableBody) {
        return;
    }

    try {

        const response =
            await fetch(`${API_URL}/transactions`);

        if (!response.ok) {
            throw new Error("Failed to load transactions");
        }

        const data =
            await response.json();

        tableBody.innerHTML = "";

        data.transactions.forEach(transaction => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${transaction[0]}</td>
                <td>${transaction[1]}</td>
                <td>${transaction[2]}</td>
                <td>₹${transaction[3]}</td>
                <td>${transaction[4]}</td>
            `;

            tableBody.appendChild(row);

        });

    }

    catch (error) {

        console.error(error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="5">
                    Unable to load transactions.
                </td>
            </tr>
        `;

    }
}


// =========================
// SHOW USER FORM
// =========================

function showUserForm() {

    document.getElementById(
        "userFormTitle"
    ).textContent = "Add New User";

    document.getElementById(
        "editUserId"
    ).value = "";

    document.getElementById(
        "userName"
    ).value = "";

    document.getElementById(
        "userEmail"
    ).value = "";

    document.getElementById(
        "userPhone"
    ).value = "";

    document.getElementById(
        "userForm"
    ).style.display = "block";
}


// =========================
// HIDE USER FORM
// =========================

function hideUserForm() {

    document.getElementById(
        "userForm"
    ).style.display = "none";
}


// =========================
// EDIT USER
// =========================

function editUser(
    id,
    name,
    email,
    phone
) {

    document.getElementById(
        "userFormTitle"
    ).textContent = "Edit User";

    document.getElementById(
        "editUserId"
    ).value = id;

    document.getElementById(
        "userName"
    ).value = name;

    document.getElementById(
        "userEmail"
    ).value = email;

    document.getElementById(
        "userPhone"
    ).value = phone;

    document.getElementById(
        "userForm"
    ).style.display = "block";
}


// =========================
// SAVE USER
// =========================

async function saveUser(event) {

    event.preventDefault();

    const id =
        document.getElementById(
            "editUserId"
        ).value;

    const name =
        document.getElementById(
            "userName"
        ).value;

    const email =
        document.getElementById(
            "userEmail"
        ).value;

    const phone =
        document.getElementById(
            "userPhone"
        ).value;


    let url =
        `${API_URL}/users`;

    let method = "POST";


    if (id) {

        url =
            `${API_URL}/users/${id}`;

        method = "PUT";

    }


    try {

        const response =
            await fetch(
                url,
                {
                    method: method,

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            name: name,
                            email: email,
                            phone: phone
                        })
                }
            );


        const data =
            await response.json();

        alert(data.message);


        if (response.ok) {

            hideUserForm();

            loadUsers();

        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// DELETE USER
// =========================

async function deleteUser(id) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this user?"
        );


    if (!confirmation) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/users/${id}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();

        alert(data.message);


        if (response.ok) {

            loadUsers();

        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// DEPOSIT
// =========================

async function depositMoney() {

    const accountId =
        document.getElementById(
            "operationAccountId"
        ).value;

    const amount =
        document.getElementById(
            "operationAmount"
        ).value;


    if (!accountId || !amount) {

        alert(
            "Please enter account ID and amount."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/accounts/${accountId}/deposit`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            amount: Number(amount)
                        })
                }
            );


        const data =
            await response.json();

        alert(data.message);


        if (response.ok) {

            document.getElementById(
                "operationAmount"
            ).value = "";

            loadAccounts();

        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// WITHDRAW
// =========================

async function withdrawMoney() {

    const accountId =
        document.getElementById(
            "operationAccountId"
        ).value;

    const amount =
        document.getElementById(
            "operationAmount"
        ).value;


    if (!accountId || !amount) {

        alert(
            "Please enter account ID and amount."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/accounts/${accountId}/withdraw`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            amount: Number(amount)
                        })
                }
            );


        const data =
            await response.json();

        alert(data.message);


        if (response.ok) {

            document.getElementById(
                "operationAmount"
            ).value = "";

            loadAccounts();

        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// CHECK BALANCE
// =========================

async function checkBalance() {

    const accountId =
        document.getElementById(
            "operationAccountId"
        ).value;


    if (!accountId) {

        alert(
            "Please enter account ID."
        );

        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/accounts/${accountId}/balance`
            );


        const data =
            await response.json();


        if (data.message) {

            alert(data.message);

            return;

        }


        alert(
            "Account Number: " +
            data.account_number +
            "\nBalance: ₹" +
            data.balance
        );

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// EDIT ACCOUNT
// =========================

function editAccount(id) {

    alert(
        "Account Edit functionality will be added next.\nAccount ID: " +
        id
    );

}


// =========================
// DELETE ACCOUNT
// =========================

async function deleteAccount(id) {

    const confirmation =
        confirm(
            "Are you sure you want to delete this account?"
        );


    if (!confirmation) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_URL}/accounts/${id}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();

        alert(data.message);


        if (response.ok) {

            loadAccounts();

        }

    }

    catch (error) {

        console.error(error);

        alert(
            "Unable to connect to FastAPI."
        );

    }
}


// =========================
// START
// =========================

loadUsers();

loadAccounts();

loadTransactions();