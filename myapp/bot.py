import telebot
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView

from myapp.models import PUser
from pub_g.settings import BOT_TOKEN

bot = telebot.TeleBot(token=BOT_TOKEN)


class UpdateBot(APIView):
    def post(self, request):
        json_string = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return Response({'code': 200})


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.from_user.id, 'Для авторизации в боте пришлите код из личного кабинета')


@bot.message_handler(content_types=['location', 'contact', 'text',
                                    'document', 'audio', 'photo', 'sticker', 'video', 'voice'])
def all_message(message):
    if User.objects.filter(id=message.text).exists():
        user = User.objects.get(id=message.text)
        p_user = PUser.objects.get(user=user)
        p_user.telegram_id = message.from_user.id
        p_user.save()
        bot.send_message(message.from_user.id,
                         f'Поздравляем, теперь вы будете получать уведомления для пользователя {user.username} в Telegram ')
    else:
        bot.send_message(message.from_user.id,
                         'Мы не нашли пользователя с таким кодом телеграм')
