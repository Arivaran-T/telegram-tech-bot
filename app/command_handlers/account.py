import re
from aiogram import Router, types, html, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from app.models import User
from app.services.user.service import UserService

router = Router()


@router.message(Command("account"))
async def start_cmd(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    tg_user_id = str(message.from_user.id)
    tg_username = message.from_user.username

    # check if user exists, if not create
    user: User = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if user:

        account_details = f"""
{html.underline(html.bold("Account Details"))}

Name: {html.code(user.name)}
Email: {html.code(user.email) if user.email else "N/A"}
Registered On: {html.code(user.created_at.strftime("%Y-%m-%d %H:%M:%S"))}
Last Updated: {html.code(user.updated_at.strftime("%Y-%m-%d %H:%M:%S")) if user.updated_at else "N/A"}
"""
        kb = InlineKeyboardBuilder()
        kb.button(text="Update Info", callback_data="account_update_info")
        await message.answer(
            text=account_details, parse_mode=ParseMode.HTML, reply_markup=kb.as_markup()
        )

    else:
        await message.answer(
            f"Hi {html.bold(name)}! 👋\n\nYou don't have an account yet. Please use /start to register.",
            parse_mode=ParseMode.HTML,
        )


@router.callback_query(F.data == "account_update_info")
async def account_update_info(callback: types.CallbackQuery, state: FSMContext):

    update_instructions = f"""
<b>⚡ Update Account Info</b>
Update Name: <code>update name &lt;your name&gt;</code>
Update Email: <code>update email &lt;your email&gt;</code>

<b>📝 Example</b>
<code>update name John Doe</code>
<code>update email john@example.com</code>
"""

    await callback.message.answer(text=update_instructions, parse_mode=ParseMode.HTML)


# --- Handle "update name ..."
@router.message(F.text.lower().startswith("update name "))
async def update_name(message: types.Message):
    tg_user_id = str(message.from_user.id)
    new_name = message.text[len("update name ") :].strip()

    if not new_name:
        await message.answer("⚠️ Please provide a valid name after `update name`.")
        return

    try:
        updated_user = await UserService.update_user_details(
            tg_user_id=tg_user_id, name=new_name
        )
        await message.answer(
            f"✅ Your name has been updated to: {html.bold(updated_user.name)}",
            parse_mode=ParseMode.HTML,
        )
    except ValueError as e:
        await message.answer(f"❌ {str(e)}")


# --- Handle "update email ..."
@router.message(F.text.lower().startswith("update email "))
async def update_email(message: types.Message):
    tg_user_id = str(message.from_user.id)
    new_email = message.text[len("update email ") :].strip()

    if not new_email or "@" not in new_email:
        await message.answer(
            "⚠️ Please provide a valid email after `update email`.",
            parse_mode=ParseMode.HTML,
        )
        return

    # Basic email validation using regex
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, new_email):
        await message.answer(
            "⚠️ Invalid email format. Please enter a valid email address:",
            parse_mode=ParseMode.HTML,
        )
        return

    # Check if email already exists in the system
    existing_user = await UserService.get_user_by_email(email=new_email)
    if existing_user:
        if existing_user.tg_user_id == tg_user_id:
            await message.answer(
                f"⚠️ You are already registered with this email: {html.bold(existing_user.email)}",
                parse_mode=ParseMode.HTML,
            )
            return
        else:
            await message.answer(
                f"⚠️ This email is already registered by {html.bold(existing_user.name)}.\nPlease enter a different email:",
                parse_mode=ParseMode.HTML,
            )
            return

    try:
        updated_user = await UserService.update_user_details(
            tg_user_id=tg_user_id, email=new_email
        )
        await message.answer(
            f"✅ Your email has been updated to: {html.bold(updated_user.email)}",
            parse_mode=ParseMode.HTML,
        )
    except ValueError as e:
        await message.answer(f"❌ {str(e)}")
