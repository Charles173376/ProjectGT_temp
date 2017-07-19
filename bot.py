from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from gtts import gTTS
from os import remove

import time
import zwave
from hue_lib import set_val, get_val
import range

updater = Updater(token='407521774:AAEkpDDxsPvJCMteOiQxWE91Z6JiJfH2xXs')
dispatcher = updater.dispatcher
proper_range = range.ProperRange()


def voice_generate(bot, update, sentence):
    voice_file = gTTS(text=sentence, lang='en')
    voice_file.save(sentence + ".mp3")
    bot.sendVoice(chat_id=update.message.chat_id, voice=open(sentence + ".mp3", "rb"))
    remove("./" + sentence + ".mp3")


def startup(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Welcome to the project GT.For instructions, type  /inst")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="For instructions, type    /inst")
    voice_generate(bot, update, "Welcome to the project GT. For instructions, type slash inst")


def show(bot, update):
    cur_lum = get_lum()
    cur_bri = get_val()
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Current Luminiscence value is " + str(cur_lum))
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Current brightness value of Hue is " + str(cur_bri))
    voice_generate(bot, update, "Current Luminiscence value is " + str(cur_lum) +
                   "Current brightness value of Hue is " + str(cur_bri))


def check_lum(bot, update, check_count):
    current_lun = get_lum()
    if current_lun < 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + "Failed reading Brightness.")
        voice_generate(bot, update, "Check #" + str(check_count) + "Failed reading Brightness.")
    elif current_lun > proper_range.proper_max:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + " [ " + str(
                            current_lun) + " ] " + ": Brightness too high, turning down.")
        voice_generate(bot, update, "Check #" + str(check_count) + " [ " + str(
            current_lun) + " ] " + ": Brightness too high, turning down.")
        turn_down()
    elif current_lun < proper_range.proper_min:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + " [ " + str(
                            current_lun) + " ] " + ": Brightness too low, turning up.")
        voice_generate(bot, update, "Check #" + str(check_count) + " [ " + str(
            current_lun) + " ] " + ": Brightness too low, turning up.")
        turn_up()
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + str(check_count) + " [ " + str(
                            current_lun) + " ] " + ": Brightness in proper range.")
        voice_generate(bot, update, "Check #" + str(check_count) + " [ " + str(
            current_lun) + " ] " + ": Brightness in proper range.")


def get_lum():
    return zwave.get_lumval("192.168.0.107")


def force_high():
    set_val(254)


def force_low():
    set_val(0)


def turn_up():
    # Keep turning up until it's proper.
    bri_to_set = get_val()
    current_bri = get_lum()
    while current_bri < proper_range.proper_min & current_bri > proper_range.proper_max & bri_to_set <= 254:
        bri_to_set += 50
        set_val(bri_to_set)


def turn_down():
    # Keep turning down until it's proper.
    bri_to_set = get_val()
    current_bri = get_lum()
    while current_bri < proper_range.proper_min & current_bri > proper_range.proper_max & bri_to_set >= 0:
        bri_to_set -= 50
        set_val(bri_to_set)


def auto(bot, update):
    voice_generate(bot, update, "Now I will initiate an automatic check on Brightness: ")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Now I will initiate an automatic check on Brightness: ")
    check_count = 0
    while check_count <= 30:
        check_lum(bot, update, check_count)
        check_count = check_count + 1
        time.sleep(20)


def instructions(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/auto    :   Start a series of automatic brightness check.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/show    :   Show current Luminiscence value and current brightness value.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/demand    :   Start brightness check on demand.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/high    :   Set Philips Hue to highest brightness.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/low    :   Set Philips Hue to the lowest brightness.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/up    :   Set brightness a little higher")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/down    :   Set brightness a little lower")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/max    :   Set current brightness value to max proper value")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="/min    :   Set current brightness value to min proper value")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Moreover, you can directly enter a number (0~254) to set Philips Hue")


def up(bot, update):
    current_bri = get_val()
    set_val(current_bri + 20)
    if current_bri > proper_range.proper_max:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="This room seems to be too bright, take care.")
        voice_generate(bot, update, "This room seems to be too bright, take care.")


def down(bot, update):
    current_bri = get_val()
    set_val(current_bri + 20)
    if current_bri < proper_range.proper_min:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="This room seems to be too dark, take care.")
        voice_generate(bot, update, "This room seems to be too bright, take care.")


def set_by_value(bot, update):
    req = int(update.message.text)
    if req > 254 | req < 0:
        set_val(update.message.text)
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Requested value set.")
        voice_generate(bot, update, "Requested value set.")
        check_on_demand(bot, update)
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="You can enter a specific number to set the Hue.")
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="But it should be with [0,254]")
        voice_generate(bot, update, "You can enter a specific number to set the Hue." +
                       "But it should be with zero to 254")


def check_on_demand(bot, update):
    current_lun = get_lum()
    if current_lun < 0:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + "Failed reading Brightness.")
        voice_generate(bot, update, "Check #" + "Failed reading Brightness.")
    elif current_lun > proper_range.proper_max:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + " [ " + str(current_lun)
                             + " ] " + ": Brightness too high, turning down.")
        voice_generate(bot, update, "Check #" + " [ " + str(current_lun)
                       + " ] " + ": Brightness too high, turning down.")
    elif current_lun < proper_range.proper_min:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + " [ " + str(current_lun)
                             + " ] " + ": Brightness too low, turning up.")
        voice_generate(bot, update, "Check #" + " [ " + str(current_lun)
                       + " ] " + ": Brightness too low, turning up.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="Check #" + " [ " + str(current_lun)
                             + " ] " + ": Brightness in proper range.")
        voice_generate(bot, update, "Check #" + " [ " + str(current_lun)
                       + " ] " + ": Brightness in proper range.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="You can now adjust brightness by typing /up or /down")
    voice_generate(bot, update, "You can now adjust brightness by typing /up or /down")


def adjust_max(bot, update):
    voice_generate(bot, update, "Here you can adjust the maximum value for proper brightness")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Here you can adjust the maximum value for proper brightness")
    proper_range.set_max(get_lum())


def adjust_min(bot, update):
    voice_generate(bot, update, "Here you can adjust the minimum value for proper brightness")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Here you can adjust the minimum value for proper brightness")
    proper_range.set_min(get_lum())


def stop(bot, update):
    voice_generate(bot, update, "Bot is stopping.")
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Bot is stopping.")
    updater.stop()


def main():
    start_handler = CommandHandler('start', startup)
    show_handler = CommandHandler('show', show)
    auto_handler = CommandHandler('auto', auto)
    force_high_handler = CommandHandler('high', force_high)
    force_low_handler = CommandHandler('low', force_low)
    instructions_handler = CommandHandler('inst', instructions)
    check_on_demand_handler = CommandHandler('demand', check_on_demand)
    up_handler = CommandHandler('up', up)
    down_handler = CommandHandler('down', down)
    adjust_max_handler = CommandHandler('max', adjust_max)
    adjust_min_handler = CommandHandler('min', adjust_min)
    stop_handler = CommandHandler('stop', stop)
    message_handler = MessageHandler(filters.Filters.text, set_by_value)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(show_handler)
    dispatcher.add_handler(auto_handler)
    dispatcher.add_handler(force_high_handler)
    dispatcher.add_handler(force_low_handler)
    dispatcher.add_handler(instructions_handler)
    dispatcher.add_handler(check_on_demand_handler)
    dispatcher.add_handler(up_handler)
    dispatcher.add_handler(down_handler)
    dispatcher.add_handler(message_handler)
    dispatcher.add_handler(adjust_max_handler)
    dispatcher.add_handler(adjust_min_handler)
    dispatcher.add_handler(stop_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
