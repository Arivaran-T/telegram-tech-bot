# 🤖 Telegram Tech Bot

A **Telegram bot** built with **Aiogram**, **Python**, and **PostgreSQL**.  
This bot supports user registration, account management, admin/user commands, and interactive workflows.

---

## 🚀 Features

- **Telegram Bot with Aiogram** – fast, asynchronous, and production-ready.
- **PostgreSQL** – stores all user data securely.
- **User Registration & Authentication** – register with name and email.
- **Account Management** – view and update account details.
- **Admin Commands** – manage users, update roles, delete users.
- **Inline Keyboards** – intuitive interactive buttons for actions.
- **Role-Based Access** – admin vs regular user commands.
- **FSM (Finite State Machine)** – handles multi-step workflows like registration.

---

## I - 📦 Installation

1. **Clone the repo**

2. **Create & activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Setup environment variables**  
   Create a `.env` file in the project root:

```env
BOT_TOKEN=your_telegram_token
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
```

---

## II - ▶️ Run the Bot

Start the bot:

```bash
python main.py
```

Your bot will be live on Telegram. Interact with it using the commands below.

---

## III - 📂 Bot Commands & Workflows

### 1️⃣ Start & Registration

Starts the bot, shows a welcome message, and registers new users.

- **Command:** `/start`
- **Flow:**
  1. Bot greets the user.
  2. If new, user clicks **Register** button.
  3. User enters **Full Name** → **Email**.
  4. Bot validates email format and uniqueness.
  5. Registration complete!

```
⚡️ArivuTechBot Activated!

Hi Arivu! 👋

What you're experiencing:
🏗️  Enterprise-Grade Architecture
🎯  Clean, Intuitive UX
⚡️  Advanced Feature Integration
🔒  Professional Code Standards

💼 This demonstrates the exact quality I deliver to clients!

📈 Ready to build something amazing for your business?

Built with ❤️ by Arivu to showcase professional development standards.
```

---

### 2️⃣ Account Management

View your account details and update information.

- **Command:** `/account`
- **Features:**
  - View account details (name, email, registration date).
  - Update info with inline keyboard → Instructions:

```
Account Details
Name: John Doe
Email: john@example.com
Registered On: 2025-09-28 21:00:00
Last Updated: N/A
```

```
⚡️ Update Account Info
Update Name: update name <your name>
Update Email: update email <your email>

📝 Example
update name John Doe
update email john@example.com
```

- Email validation and duplicate checking included.

### 3️⃣ Admin Commands (`/manage_users`)

- **Access:** Only for users with role `admin`.

```
⚙️ Admin Manage User Instructions

1. Get User List: get users <page> <per_page>
2. Get User: get user <userId>
3. Update User Role: update role <userId> <role>
4. Delete User: delete user <userId>

Example Commands

1. Get User List: get users 1 10
2. Update User Role: update role 1234567890 admin
3. Get User: get user 1234567890
4. Delete User: delete user 1234567890
```

**Notes:**

- Admin cannot delete their own account.
- All commands validated for correct syntax.

---

## IV - ⚡ Example Flow

1. User sends `/start` → Register if new
2. Fill in **Name** → **Email**
3. Use `/account` to view/update info
4. Admin uses `/manage_users` to manage users
5. Commands validated for email format, duplicate emails, and role restrictions

---

## 🗄️ Database

**PostgreSQL** stores all user data in a table with fields:

- `tg_user_id` – Telegram User ID
- `tg_username` – Telegram username
- `name` – User full name
- `email` – User email
- `role` – `admin` or `user`
- `created_at` – Registration timestamp
- `updated_at` – Last updated timestamp

---

## 📝 Notes

- Inline buttons improve workflow for registration and account updates.
- Proper error handling ensures only valid commands execute.
- PostgreSQL connection parameters should be correct in `.env`.

---
