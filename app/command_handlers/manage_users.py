from aiogram import Router, types, html, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.models import User
from app.services.user.service import UserService

router = Router()


@router.message(Command("manage_users"))
async def start_cmd(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    tg_user_id = str(message.from_user.id)
    tg_username = message.from_user.username

    # check if user exists, if not create
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if user:
        if user.role == "admin":
            admin_message = f"""
⚙️ <b>Admin Manage User Instructions</b>

1. Get User List: <code>get users &lt;page&gt; &lt;per_page&gt;</code>
2. Get User: <code>get user &lt;userId&gt;</code>
3. Update User Role: <code>update role &lt;userId&gt; &lt;role&gt;</code>
4. Delete User: <code>delete user &lt;userId&gt;</code>

<b>Example Commands</b>

1. Get User List: <code>get users 1 10</code>
2. Update User Role: <code>update role 1234567890 admin</code>
3. Get User: <code>get user 1234567890</code>
4. Delete User: <code>delete user 1234567890</code>
"""

            await message.answer(admin_message, parse_mode=ParseMode.HTML)

        else:
            await message.answer("You are not authorized to use this command.")
    else:
        await message.answer("You are not authorized to use this command.")


@router.message(F.text.startswith("get users"))
async def get_users(message: types.Message):
    tg_user_id = str(message.from_user.id)
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if not user or user.role != "admin":
        await message.answer("You are not authorized to use this command.")
        return

    try:
        _, _, page, per_page = message.text.split()
        page, per_page = int(page), int(per_page)
    except ValueError:
        await message.answer(
            "❌ Usage: `get users <page> <per_page>`", parse_mode=ParseMode.MARKDOWN
        )
        return

    users = await UserService.get_all_users_paginated(page, per_page)
    if not users:
        await message.answer("No users found.")
        return

    response = "\n".join(
        [
            f"👤 {u.name or '-'} | @{u.tg_username or '-'} | Role: {u.role or '-'} | ID: {u.tg_user_id}"
            for u in users
        ]
    )
    await message.answer(response)


@router.message(F.text.startswith("get user"))
async def get_user(message: types.Message):
    tg_user_id = str(message.from_user.id)
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if not user or user.role != "admin":
        await message.answer("You are not authorized to use this command.")
        return

    try:
        _, _, target_tg_id = message.text.split()
    except ValueError:
        await message.answer(
            "❌ Usage: `get user <tg_user_id>`", parse_mode=ParseMode.MARKDOWN
        )
        return

    target_user = await UserService.get_user_by_tg_user_id(tg_user_id=str(target_tg_id))
    if not target_user:
        await message.answer("User not found.")
        return

    details = f"""
<b>User Details</b>
- Name: <code>{user.name}</code>
- Email: <code>{user.email or "N/A"}</code>
- Role: <code>{user.role}</code>
- Registered: <code>{user.created_at.strftime("%Y-%m-%d %H:%M:%S")}</code>
- Last Updated: <code>{user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else "N/A"}</code>
"""
    await message.answer(details, parse_mode=ParseMode.HTML)


@router.message(F.text.startswith("update role"))
async def update_role(message: types.Message):
    tg_user_id = str(message.from_user.id)
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if not user or user.role != "admin":
        await message.answer("You are not authorized to use this command.")
        return

    try:
        _, _, target_tg_id, role = message.text.split()
    except ValueError:
        await message.answer(
            "❌ Usage: `update role <tg_user_id> <role>`", parse_mode=ParseMode.MARKDOWN
        )
        return

    try:
        updated_user = await UserService.admin_update_user_role(
            tg_user_id=str(target_tg_id), role=role
        )
        await message.answer(
            f"✅ Updated role for @{updated_user.tg_username} → {role}"
        )
    except ValueError as e:
        await message.answer(f"❌ {str(e)}")


@router.message(F.text.startswith("delete user"))
async def delete_user(message: types.Message):
    tg_user_id = str(message.from_user.id)
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if not user or user.role != "admin":
        await message.answer("You are not authorized to use this command.")
        return

    try:
        _, _, target_tg_id = message.text.split()
    except ValueError:
        await message.answer(
            "❌ Usage: `delete user <tg_user_id>`", parse_mode=ParseMode.MARKDOWN
        )
        return

    if target_tg_id == tg_user_id:
        await message.answer("⚠️ Admin can't delete his/her own account.")
        return

    try:
        success = await UserService.delete_user(target_tg_id)
        if success:
            await message.answer(f"✅ User {target_tg_id} deleted successfully.")
    except ValueError as e:
        await message.answer(f"❌ {str(e)}")
