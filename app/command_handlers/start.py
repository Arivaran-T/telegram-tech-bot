import re
from aiogram import Router, types, html, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.models import User
from app.services.user.service import UserService

router = Router()


# Define states for registration
class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_email = State()


@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    tg_user_id = str(message.from_user.id)
    tg_username = message.from_user.username

    welcome_message = f"""
{html.bold("⚡ArivuTechBot Activated!")}

Hi {html.bold(name)}! 👋

{html.bold("What you're experiencing:")}
🏗️  Enterprise-Grade Architecture
🎯  Clean, Intuitive UX
⚡  Advanced Feature Integration
🔒  Professional Code Standards

💼 {html.bold("This demonstrates the exact quality I deliver to clients!")}

📈 {html.bold("Ready to build something amazing for your business?")}

Built with ❤️ by {html.bold("Arivu")} to showcase professional development standards.
"""
    await message.answer(welcome_message, parse_mode=ParseMode.HTML)

    # check if user exists, if not create
    user = await UserService.get_user_by_tg_user_id(tg_user_id=tg_user_id)

    if user:

        await message.answer(
            f"Welcome back, {user.role} {html.bold(user.name)}!",
            parse_mode=ParseMode.HTML,
        )

        if user.role == "admin":
            admin_message = f"""
⚙️ {html.bold("Admin Commands")}

👤 /account - Manage your account
👥 /manage_users - Manage users
"""
            await message.answer(admin_message, parse_mode=ParseMode.HTML)

        else:
            user_message = f"""
⚙️ {html.bold("User Commands")}

👤 /account - Manage your account
"""
            await message.answer(user_message, parse_mode=ParseMode.HTML)

    else:
        kb = InlineKeyboardBuilder()
        kb.button(text="Register", callback_data="register_start")
        await message.answer(
            f"You are new here, {html.bold(name)}! \n\nClick below to register 👇",
            parse_mode=ParseMode.HTML,
            reply_markup=kb.as_markup(),
        )


@router.callback_query(F.data == "register_start")
async def register_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("👉 Please enter your full name:")
    await state.set_state(Registration.waiting_for_name)
    await callback.answer()  # closes the loading animation


# Step 1: Get name
@router.message(Registration.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)  # store name
    await message.answer("✅ Got it! Now please enter your email address:")
    await state.set_state(Registration.waiting_for_email)


# Step 2: Get email and save user
@router.message(Registration.waiting_for_email)
async def process_email(message: types.Message, state: FSMContext):
    email = message.text
    data = await state.get_data()

    tg_user_id = str(message.from_user.id)
    tg_username = message.from_user.username

    # Basic email validation using regex
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        await message.answer(
            "⚠️ Invalid email format. Please enter a valid email address:"
        )
        return

    # Check if email already exists in the system
    existing_user = await UserService.get_user_by_email(email=email)
    if existing_user:
        await message.answer(
            f"⚠️ This email is already registered by {html.bold(existing_user.name)}.\nPlease enter a different email:"
        )
        return

    # Save to DB
    user: User = await UserService.create_user(
        tg_user_id=tg_user_id,
        tg_username=tg_username,
        name=data["name"],
        email=email,
    )

    await message.answer(
        f"🎉 Registration complete!\n\nWelcome, {html.bold(user.name)}!\nYour email: {html.bold(user.email)}",
        parse_mode=ParseMode.HTML,
    )
    await state.clear()
