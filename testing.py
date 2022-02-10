import json

holivar = []
holivar.append({
    'id': 1,
    'mess': "друзья, нужен совет бывалых",
    'answer_to':0,
    'user_id':1,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})
holivar.append({
    'id':2,
    'mess':"???",
    'answer_to':1,
    'user_id':2,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'

})
holivar.append({
    'id':3,
    'mess':"может лучше сразу вопрос написать?",
    'answer_to':1,
    'user_id':3,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id':4,
    'mess':"Кто-то пользовался ботом для создания ПЦР-тестов онлайн? Собираюсь лететь в Египет, турагент говорит что все работает, туристы летают с этими тестами на ура. Но что-то я очкую)) вот ссылка @grant_test_bot",
    'answer_to':0,
    'user_id':1,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})
holivar.append({
    'id':5,
    'mess': "по-идее, чтобы не заморачиваться с фотошопом, то норм вариант. Мне справки делал дизайнер в фотошопе.",
    'answer_to': 4,
    'user_id': 3,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 6,
    'mess': "а что на счет проверки QR-кодов? Смотрят их?",
    'answer_to': 0,
    'user_id': 1,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})
holivar.append({
    'id':7,
    'mess': "несколько раз летал с тестами из аналогичного бота, только название было другое. Там коды рабочие, считываются камерой без проблем. Но их даже не пытались проверить в аеропорту. Вот так работает наша безопасность",
    'answer_to': 6,
    'user_id':2,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 8,
    'mess': "офигеть, любит правительство усложнять жизнь! Хоть бы уже проверяли серьезно!",
    'answer_to': 0,
    'user_id': 1,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 9,
    'mess': "кстати да, у меня тоже никогда не проверяли",
    'answer_to': 8,
    'user_id': 3,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 10,
    'mess': "сестра в туризме работает. Почти всех кто не вакцинирован, отправляют делать тесты в боте каком-то. Люди довольны что дешево и не надо никуда ходить сдавать. Жалоб или курьезных ситуаций за 2 года не слышал.",
    'answer_to': 0,
    'user_id': 4,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
    })
holivar.append({
    'id': 11,
    'mess': "что это за бот? Как открыть его?",
    'answer_to': 10,
    'user_id': 5,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 12,
    'mess': "для тех кто в танке)) вот моя рефссылка на бот: @grant_test_bot.  Вам пофиг, а мне приятно тесты на халяву.",
    'answer_to': 0,
    'user_id': 1,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})

holivar.append({
    'id': 13,
    'mess': "спасибо, увидел. Поеду завтра на поезде с этим тестом, отпишусь потом как прошло.",
    'answer_to': 12,
    'user_id': 5,
    'json_data': "-",
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})
data ={
  "action": "send_image",
  "data": "static/holivar_1.jpg",
}
holivar.append({
    'id': 14,
    'mess': "-",
    'answer_to': 0,
    'user_id': 5,
    'json_data': json.dumps(data),
    'delay_before': 0,
    'delay_after': 120,
    'funnel_name':'dimon3'
})
