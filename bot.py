from telegram.ext import Updater, CommandHandler
from gtts import gTTS
import os
import time
import zwave
from setVal import set_val


updater = Updater(token='407521774:AAEkpDDxsPvJCMteOiQxWE91Z6JiJfH2xXs')
dispatcher = updater.dispatcher
proper_min = 150
proper_max = 210


def startup (bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Welcome to the project GT.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Now I will initiate an automatic check on Brightness: ")
    auto(bot, update)
    voice_file = gTTS(text='Welcome to the Project GT', lang='en')
    voice_file.save('Welcome' + ".mp3")
    bot.sendVoice(chat_id=update.message.chat_id,
                 voice=open('Welcome' + ".mp3", "rb"))
    os.remove("./" + 'Welcome' + ".mp3")
    return 0


def voice_generate(bot, update, sentence):
    voice_file = gTTS(text=sentence, lang='en')
    voice_file.save(sentence + ".mp3")
    bot.sendVoice(chat_id=update.message.chat_id, voice=open(sentence + ".mp3", "rb"))
    os.remove("./" + sentence + ".mp3")


def check_lum(bot, update, check_count):
    current_lun = get_lum()
    if current_lun < 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + "Failed reading luminiscence.")
        voice_generate("Check #" + str(check_count) + "Failed reading luminiscence.")
    elif current_lun > proper_max:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence too high, turning down.")
        voice_generate("Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence too high, turning down.")
        #turn_down()
    elif current_lun < proper_min:
        bot.sendMessage(chat_id=update.message.chat_id,
                    text="Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence too low, turning up.")
        #turn_up()
        voice_generate("Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence too low, turning up.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence in proper range.")
        voice_generate("Check #" + str(check_count) + " [ " + str(current_lun) + " ] " + ": Luminiscence in proper range.")


def get_lum():
    return zwave.getlumVal('192.168.0.107')


def turn_up():
    # Keep turning up until it's proper.
    bri_to_set = 0
    while get_lum() < proper_min:
        # function for Hue comes here.
        bri_to_set += 30
        set_val(bri_to_set)
        time.sleep(5)


def turn_down():
    # Keep turning down until it's proper.
    bri_to_set = 0
    while get_lum() < proper_min:
        # function for Hue comes here.
        bri_to_set -= 30
        set_val(bri_to_set)
        time.sleep(5)


def auto (bot, update):
    check_count = 0
    while 1>0:
        check_lum(bot, update, check_count)
        check_count = check_count + 1
        time.sleep(10)


def user_initiate(bot, update):
    check_lum(bot,update,0)


def main():
    # Call function "startup" on the start up.
    start_handler = CommandHandler('start', startup)
    auto_handler = CommandHandler('auto', auto)
    user_initiate_handler = CommandHandler('check', user_initiate)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(user_initiate_handler)
    dispatcher.add_handler(auto_handler)
    updater.start_polling()

    #  Run the bot until you press Ctrl-C or the process receives SIGINT,
    #  SIGTERM or SIGABRT.
    updater.idle()


if __name__ == "__main__":
    main()