from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_connection


app = FastAPI()


# =========================
# CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# MODELS
# =========================

class User(BaseModel):

    name: str
    email: str
    phone: str


class Account(BaseModel):

    user_id: int
    account_number: str
    account_type: str
    balance: float


class Deposit(BaseModel):

    amount: float


class Withdraw(BaseModel):

    amount: float


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Banking API is running"
    }


# =========================
# USERS
# =========================

@app.get("/users")
def get_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users ORDER BY id"
    )

    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "users": users
    }


@app.post("/users")
def create_user(user: User):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (name, email, phone)

        VALUES
        (%s, %s, %s)

        RETURNING id
        """,
        (
            user.name,
            user.email,
            user.phone
        )
    )

    user_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User created successfully",
        "user_id": user_id
    }


@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    user: User
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users

        SET
            name = %s,
            email = %s,
            phone = %s

        WHERE id = %s

        RETURNING id
        """,
        (
            user.name,
            user.email,
            user.phone,
            user_id
        )
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        connection.close()

        return {
            "message": "User not found"
        }

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User updated successfully",
        "user_id": result[0]
    }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM users

        WHERE id = %s

        RETURNING id
        """,
        (user_id,)
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        connection.close()

        return {
            "message": "User not found"
        }

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "User deleted successfully",
        "user_id": result[0]
    }


# =========================
# ACCOUNTS
# =========================

@app.get("/accounts")
def get_accounts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM accounts ORDER BY id"
    )

    accounts = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "accounts": accounts
    }


@app.get("/accounts/{account_id}")
def get_account(account_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM accounts
        WHERE id = %s
        """,
        (account_id,)
    )

    account = cursor.fetchone()

    cursor.close()
    connection.close()

    if account is None:

        return {
            "message": "Account not found"
        }

    return {
        "account": account
    }


@app.post("/accounts")
def create_account(account: Account):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO accounts
        (
            user_id,
            account_number,
            account_type,
            balance
        )

        VALUES
        (%s, %s, %s, %s)

        RETURNING id
        """,
        (
            account.user_id,
            account.account_number,
            account.account_type,
            account.balance
        )
    )

    account_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Account created successfully",
        "account_id": account_id
    }


@app.put("/accounts/{account_id}")
def update_account(
    account_id: int,
    account: Account
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE accounts

        SET
            user_id = %s,
            account_number = %s,
            account_type = %s,
            balance = %s

        WHERE id = %s

        RETURNING id
        """,
        (
            account.user_id,
            account.account_number,
            account.account_type,
            account.balance,
            account_id
        )
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        connection.close()

        return {
            "message": "Account not found"
        }

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Account updated successfully",
        "account_id": result[0]
    }


@app.delete("/accounts/{account_id}")
def delete_account(account_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM accounts

        WHERE id = %s

        RETURNING id
        """,
        (account_id,)
    )

    result = cursor.fetchone()

    if result is None:

        cursor.close()
        connection.close()

        return {
            "message": "Account not found"
        }

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "message": "Account deleted successfully",
        "account_id": result[0]
    }


# =========================
# DEPOSIT
# =========================

@app.post("/accounts/{account_id}/deposit")
def deposit_money(
    account_id: int,
    deposit: Deposit
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()

        if account is None:

            return {
                "message": "Account not found"
            }


        if deposit.amount <= 0:

            return {
                "message": "Amount must be greater than 0"
            }


        cursor.execute(
            """
            UPDATE accounts

            SET balance = balance + %s

            WHERE id = %s

            RETURNING balance
            """,
            (
                deposit.amount,
                account_id
            )
        )

        new_balance = cursor.fetchone()[0]


        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_id,
                transaction_type,
                amount
            )

            VALUES
            (%s, %s, %s)
            """,
            (
                account_id,
                "Deposit",
                deposit.amount
            )
        )


        connection.commit()


        return {
            "message": "Money deposited successfully",
            "account_id": account_id,
            "deposited_amount": deposit.amount,
            "new_balance": new_balance
        }


    except Exception as error:

        connection.rollback()

        return {
            "message": "Transaction failed",
            "error": str(error)
        }


    finally:

        cursor.close()
        connection.close()


# =========================
# WITHDRAW
# =========================

@app.post("/accounts/{account_id}/withdraw")
def withdraw_money(
    account_id: int,
    withdraw: Withdraw
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE id = %s
            """,
            (account_id,)
        )

        account = cursor.fetchone()


        if account is None:

            return {
                "message": "Account not found"
            }


        current_balance = account[0]


        if withdraw.amount <= 0:

            return {
                "message": "Amount must be greater than 0"
            }


        if withdraw.amount > current_balance:

            return {
                "message": "Insufficient balance",
                "current_balance": current_balance,
                "requested_amount": withdraw.amount
            }


        cursor.execute(
            """
            UPDATE accounts

            SET balance = balance - %s

            WHERE id = %s

            RETURNING balance
            """,
            (
                withdraw.amount,
                account_id
            )
        )

        new_balance = cursor.fetchone()[0]


        cursor.execute(
            """
            INSERT INTO transactions
            (
                account_id,
                transaction_type,
                amount
            )

            VALUES
            (%s, %s, %s)
            """,
            (
                account_id,
                "Withdraw",
                withdraw.amount
            )
        )


        connection.commit()


        return {
            "message": "Money withdrawn successfully",
            "account_id": account_id,
            "withdrawn_amount": withdraw.amount,
            "new_balance": new_balance
        }


    except Exception as error:

        connection.rollback()

        return {
            "message": "Transaction failed",
            "error": str(error)
        }


    finally:

        cursor.close()
        connection.close()


# =========================
# CHECK BALANCE
# =========================

@app.get("/accounts/{account_id}/balance")
def check_balance(account_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            account_number,
            balance

        FROM accounts

        WHERE id = %s
        """,
        (account_id,)
    )

    account = cursor.fetchone()

    cursor.close()
    connection.close()


    if account is None:

        return {
            "message": "Account not found"
        }


    return {
        "account_id": account_id,
        "account_number": account[0],
        "balance": account[1]
    }


# =========================
# TRANSACTIONS
# =========================

@app.get("/transactions")
def get_transactions():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            account_id,
            transaction_type,
            amount,
            transaction_date

        FROM transactions

        ORDER BY transaction_date DESC
        """
    )

    transactions = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "transactions": transactions
    }