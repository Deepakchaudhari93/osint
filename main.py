
import os
import requests
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN", "8391838423:AAHQ8PNOBRb51M15v6Br9QpD79422pg3hIs")
IFSC_API_BASE_URL = "https://ifsc.razorpay.com"
NUMBER_API_BASE_URL = "https://api.x10.network/numapi.php"
REQUEST_TIMEOUT = 10

def get_main_keyboard():
    keyboard = [
        ['🏦 IFSC', '📱 Number']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_user_full_name(user):
    full_name = user.first_name or ""
    if user.last_name:
        full_name += " " + user.last_name
    return full_name.strip()

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    full_name = get_user_full_name(user)

    welcome_msg = f"""👋🏻 Hey {full_name} Welcome To OSINT Bot 🔎

🎯 Explore OSINT Tools & Legal Services"""

    await update.message.reply_text(
        welcome_msg,
        reply_markup=get_main_keyboard()
    )

async def get_ifsc_info(ifsc_code):
    ifsc_clean = ifsc_code.upper().strip()
    
    if len(ifsc_clean) != 11:
        return "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗜𝗙𝗦𝗖 𝗖𝗼𝗱𝗲!\nPlease enter a valid 11-character IFSC code"
    
    try:
        url = f"{IFSC_API_BASE_URL}/{ifsc_clean}"
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            info = f"""🏦 IFSC INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━
🔢 IFSC: `{data.get('IFSC', 'N/A')}`
🏛️ BANK: {data.get('BANK', 'N/A')}
🏢 BRANCH: {data.get('BRANCH', 'N/A')}
📍 ADDRESS: {data.get('ADDRESS', 'N/A')}
📞 CONTACT: {data.get('CONTACT', 'N/A')}
🏙️ CITY: {data.get('CITY', 'N/A')}
📮 DISTRICT: {data.get('DISTRICT', 'N/A')}
🏛️ STATE: {data.get('STATE', 'N/A')}`"""
            return info
            
        elif response.status_code == 404:
            return "❌ 𝗜𝗙𝗦𝗖 𝗖𝗼𝗱𝗲 𝗡𝗼𝘁 𝗙𝗼𝘂𝗻𝗱!\nThe provided IFSC code doesn't exist in our database."
        else:
            return "❌ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿!\nUnable to fetch IFSC details. Please try again later."
    
    except requests.exceptions.Timeout:
        return "❌ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗧𝗶𝗺𝗲𝗱 𝗢𝘂𝘁!\nPlease try again later."
    
    except requests.exceptions.ConnectionError:
        return "❌ 𝗡𝗲𝘁𝘄𝗼𝗿𝗸 𝗘𝗿𝗿𝗼𝗿!\nPlease check your internet connection and try again."
    
    except requests.exceptions.RequestException as e:
        return f"❌ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿!\nError fetching IFSC details: {str(e)}"
    
    except Exception as e:
        return "❌ 𝗨𝗻𝗲𝘅𝗽𝗲𝗰𝘁𝗲𝗱 𝗘𝗿𝗿𝗼𝗿!\nPlease try again later."

async def get_number_info(phone_number):
    phone_clean = phone_number.strip()
    
    if not phone_clean.isdigit() or len(phone_clean) < 10:
        return "❌ 𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿!\nPlease enter a valid 10-digit phone number"
    
    try:
        params = {
            'action': 'api',
            'key': 'ASHUSHARMA_JI',
            'term': phone_clean
        }
        
        response = requests.get(NUMBER_API_BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            result = data.get('data', {})
            
            info = f"""📱 PHONE NUMBER INFORMATION
━━━━━━━━━━━━━━━━━━━━━━━
📞 Number: {phone_clean}
🏛️ Operator: {result.get('operator', 'N/A')}
🌍 Circle: {result.get('circle', 'N/A')}
🏢 Country: {result.get('country', 'N/A')}
🔢 Series: {result.get('series', 'N/A')}
📟 Number Type: {result.get('number_type', 'N/A')}

📊 Additional Info:
• Status: {data.get('status', 'N/A')}
• DND: {result.get('dnd', 'N/A')}
• Ported: {result.get('ported', 'N/A')}"""
            
            return info
            
        else:
            return "❌ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿!\nUnable to fetch number details. Please try again later."
    
    except requests.exceptions.Timeout:
        return "❌ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁 𝗧𝗶𝗺𝗲𝗱 𝗢𝘂𝘁!\nPlease try again later."
    
    except requests.exceptions.ConnectionError:
        return "❌ 𝗡𝗲𝘁𝘄𝗼𝗿𝗸 𝗘𝗿𝗿𝗼𝗿!\nPlease check your internet connection and try again."
    
    except requests.exceptions.RequestException as e:
        return f"❌ 𝗔𝗣𝗜 𝗘𝗿𝗿𝗼𝗿!\nError fetching number details: {str(e)}"
    
    except Exception as e:
        return f"❌ 𝗨𝗻𝗲𝘅𝗽𝗲𝗰𝘁𝗲𝗱 𝗘𝗿𝗿𝗼𝗿!\n{str(e)}"

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    
    if user_message == '🏦 IFSC':
        await update.message.reply_text("""🏦 𝗜𝗙𝗦𝗖 𝗜𝗻𝗳𝗼

Enter a valid 11-character IFSC code (SBIN0000001)""", reply_markup=get_main_keyboard())
        context.user_data['awaiting'] = 'ifsc'
    
    elif user_message == '📱 Number':
        await update.message.reply_text("""📱 𝗣𝗵𝗼𝗻𝗲 𝗡𝘂𝗺𝗯𝗲𝗿 𝗜𝗻𝗳𝗼

Enter a valid 10-digit phone number (without country code)""", reply_markup=get_main_keyboard())
        context.user_data['awaiting'] = 'number'
    
    else:
        awaiting = context.user_data.get('awaiting')
        
        if awaiting == 'ifsc':
            result = await get_ifsc_info(user_message)
            await update.message.reply_text(result, reply_markup=get_main_keyboard(), parse_mode='Markdown')
            context.user_data['awaiting'] = None
        
        elif awaiting == 'number':
            result = await get_number_info(user_message)
            await update.message.reply_text(result, reply_markup=get_main_keyboard())
            context.user_data['awaiting'] = None
        
        else:
            await update.message.reply_text("Please use the keyboard menu below 👇", reply_markup=get_main_keyboard())

async def error_handler(update: Update, context: CallbackContext):
    print(f"Error: {context.error}")

def main():
    if not BOT_TOKEN:
        print("❌ Error: BOT_TOKEN not found!")
        return
    
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        
        print("🤖 Bot is running...")
        print(f"🔧 Configuration:")
        print(f"   - Bot Token: {BOT_TOKEN[:10]}...")
        print(f"   - IFSC API: {IFSC_API_BASE_URL}")
        print(f"   - Number API: {NUMBER_API_BASE_URL}")
        print(f"   - Timeout: {REQUEST_TIMEOUT}s")
        
        application.run_polling()
    
    except Exception as e:
        print(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    main()
