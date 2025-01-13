from bot_data.models import Text, Translate, Language
import json
from randomizer.models import Price

def get_text_list():
    all_keys = Text.objects.prefetch_related('all_translates').all()
    result = []
    for key in all_keys:
        translates = []
        for translate in key.all_translates.all():
            translates.append({
                "language": translate.language.name,
                "translate": translate.translate
            })
        data = {
            "key": key.key,
            "key_type": key.key_type,
            "translates": translates
        }
        result.append(data)
    to_json = {"data": result}
    with open("translates.json", 'w', encoding='utf-8') as json_file:
        json.dump(to_json, json_file, ensure_ascii=False, indent=4)


def fill_db():
    languages = ["Русский язык", "Английский язык"]
    for language in languages:
        lang = Language.objects.create(name=language)
    languages_dict = {"Русский язык": Language.objects.filter(name="Русский язык").first(),
                 "Английский язык": Language.objects.filter(name="Английский язык").first()}
    keys_list = [
        {
            "key": "rk_support",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Поддержать бота ⭐"
                },
                {
                    "language": "Английский язык",
                    "translate": "Donate ⭐"
                }
            ]
        },
        {
            "key": "help_text",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "..."
                },
                {
                    "language": "Английский язык",
                    "translate": "..."
                }
            ]
        },
        {
            "key": "support",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "..."
                },
                {
                    "language": "Английский язык",
                    "translate": "..."
                }
            ]
        },
        {
            "key": "not_admin",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "❌ Вы не являетесь администратором этого канала"
                },
                {
                    "language": "Английский язык",
                    "translate": "❌ You are not channels admin"
                }
            ]
        },
        {
            "key": "ik_del_ch_name",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Удалить из бота"
                },
                {
                    "language": "Английский язык",
                    "translate": "Delete from bot"
                }
            ]
        },
        {
            "key": "ik_upd_ch_name",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Обновить имя"
                },
                {
                    "language": "Русский язык",
                    "translate": "Update name"
                }
            ]
        },
        {
            "key": "ik_add_channel",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "➕ Добавить новый канал"
                },
                {
                    "language": "Английский язык",
                    "translate": "➕ Add new channel"
                }
            ]
        },
        {
            "key": "winners_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "🧮 Сколько победителей выбрать боту?"
                },
                {
                    "language": "Английский язык",
                    "translate": "🧮 Сколько победителей выбрать боту? англ"
                }
            ]
        },
        {
            "key": "need_number",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "❌ Введите число."
                },
                {
                    "language": "Английский язык",
                    "translate": "❌ Введите число. англ"
                }
            ]
        },
        {
            "key": "ik_end_by_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "По времени"
                },
                {
                    "language": "Английский язык",
                    "translate": "By time"
                }
            ]
        },
        {
            "key": "ik_giv_end_by_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "По времени"
                },
                {
                    "language": "Английский язык",
                    "translate": "By time"
                }
            ]
        },
        {
            "key": "ik_save_giv",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Сохранить розыгрыш"
                },
                {
                    "language": "Английский язык",
                    "translate": "Save giveaway"
                }
            ]
        },
        {
            "key": "ik_cancel_giv",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отмена"
                },
                {
                    "language": "Английский язык",
                    "translate": "Cancel"
                }
            ]
        },
        {
            "key": "ik_yes",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Да"
                },
                {
                    "language": "Английский язык",
                    "translate": "Yes"
                }
            ]
        },
        {
            "key": "ik_del_lot",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Удалить розыгрыш"
                },
                {
                    "language": "Английский язык",
                    "translate": "Delete lot"
                }
            ]
        },
        {
            "key": "ik_end_giv",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Завершить"
                },
                {
                    "language": "Английский язык",
                    "translate": "Finish"
                }
            ]
        },
        {
            "key": "check_lot",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Проверить результаты."
                },
                {
                    "language": "Английский язык",
                    "translate": "Check the results."
                }
            ]
        },
        {
            "key": "giv_results_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш #{giv_num}.\r\nКол-во участников: {parts_count}.\r\nКол-во победителей: {winers_count}.\r\nРозыгрыш завершен по количеству участников.\r\n\r\nРезультаты розыгрыша:\r\n\r\nПобедители:"
                },
                {
                    "language": "Английский язык",
                    "translate": "Draw #{giv_num}.\r\nNumber of participants: {parts_count}.\r\nNumber of winners: {winers_count}.\r\nDraw completed by number of participants.\r\n\r\nDraw results:\r\n\r\nWinners:"
                }
            ]
        },
        {
            "key": "giv_results_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш #{giv_num}.\r\nКол-во участников: {parts_count}.\r\nКол-во победителей: {winers_count}.\r\nРозыгрыш завершен по времени, {dt}.\r\n\r\nРезультаты розыгрыша:\r\n\r\nПобедители:"
                },
                {
                    "language": "Английский язык",
                    "translate": "Giveaway #{giv_num}.\r\nNumber of participants: {parts_count}.\r\nNumber of winners: {winers_count}.\r\nGiveaway ended in time, {dt}.\r\n\r\nGiveaway results:\r\n\r\nWinners:"
                }
            ]
        },
        {
            "key": "giv_winners_list",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Результаты розыгрыша:\r\n\r\nПобедитель:\r\n{winners}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Raffle Results:\r\n\r\nWinner:\r\n{winners}"
                }
            ]
        },
        {
            "key": "giv_nobody_in",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Победители не определены. Никто не участвовал в розыгрыше."
                },
                {
                    "language": "Английский язык",
                    "translate": "No winners have been chosen. No one has participated in the giveaway."
                }
            ]
        },
        {
            "key": "waiting_lot_deleted",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш был помечен как удаленный."
                },
                {
                    "language": "Английский язык",
                    "translate": "The drawing has been marked as deleted."
                }
            ]
        },
        {
            "key": "lot_already_deleted",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш уже удален."
                },
                {
                    "language": "Английский язык",
                    "translate": "The giveaway has already been deleted."
                }
            ]
        },
        {
            "key": "lot_deleted",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш был помечен как удаленный, рекомендуем удалить <a href=\"{link}\">пост с розыгрышем</a> из канала."
                },
                {
                    "language": "Английский язык",
                    "translate": "The giveaway has been marked as deleted, we recommend deleting <a href=\"{link}\">the giveaway post</a> from the channel."
                }
            ]
        },
        {
            "key": "delete_lot",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Подтверждение.\r\n\r\nДля удаления розыгрыша введите команду:\r\n`/delete_lot {pk}`"
                },
                {
                    "language": "Английский язык",
                    "translate": "Confirmation.\r\n\r\nTo delete a lottery, enter the command:\r\n`/delete_lot {pk}`"
                }
            ]
        },
        {
            "key": "when_end_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Укажите количество участников для проведения розыгрыша:\r\n\r\nДля отмены изменений нажмите /cancel."
                },
                {
                    "language": "Английский язык",
                    "translate": "Specify the number of participants for the draw:\r\n\r\nTo cancel changes, click /cancel."
                }
            ]
        },
        {
            "key": "when_end_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Когда нужно определить победителя? Укажите точную дату в формате ДД.ММ.ГГ ЧЧ:ММ.\r\n\r\nУстановленный часовой пояс - (GMT+3) Москва, Россия\r\n\r\nДля отмены изменений нажмите /cancel."
                },
                {
                    "language": "Английский язык",
                    "translate": "When should the winner be determined? Specify the exact date in the format DD.MM.YY HH:MM.\r\n\r\nThe set time zone is (GMT+3) Moscow, Russia.\r\n\r\nTo cancel changes press /cancel."
                }
            ]
        },
        {
            "key": "ik_cpn_2",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отмена"
                },
                {
                    "language": "Английский язык",
                    "translate": "Cancel"
                }
            ]
        },
        {
            "key": "ik_bcu",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "По кол-ву участников"
                },
                {
                    "language": "Английский язык",
                    "translate": "By number of participants"
                }
            ]
        },
        {
            "key": "ik_ebt",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "По времени"
                },
                {
                    "language": "Английский язык",
                    "translate": "By the time"
                }
            ]
        },
        {
            "key": "ik_add_winners",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Выбрать дополнительных победителей"
                },
                {
                    "language": "Английский язык",
                    "translate": "Select additional winners"
                }
            ]
        },
        {
            "key": "ik_get_excel",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Выгрузить таблицу участников"
                },
                {
                    "language": "Английский язык",
                    "translate": "Upload table of participants"
                }
            ]
        },
        {
            "key": "ik_get_link",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Получить ссылку на результаты"
                },
                {
                    "language": "Английский язык",
                    "translate": "Get a link to the results"
                }
            ]
        },
        {
            "key": "ik_end_now",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Подвести итоги прямо сейчас"
                },
                {
                    "language": "Английский язык",
                    "translate": "Sum up right now"
                }
            ]
        },
        {
            "key": "not_your_giv",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Вы не являетесь автором этого розыгрыша."
                },
                {
                    "language": "Английский язык",
                    "translate": "You are not the author of this giveaway."
                }
            ]
        },
        {
            "key": "ik_cpn",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отмена"
                },
                {
                    "language": "Английский язык",
                    "translate": "Cancel"
                }
            ]
        },
        {
            "key": "will_we_pub_giv_to",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Публикуем в канал - {place_name}?"
                },
                {
                    "language": "Английский язык",
                    "translate": "Publish to the channel - {place_name}?"
                }
            ]
        },
        {
            "key": "giv_ended_or_not_posted_postlot",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "The giveaway has not yet been published or has already ended."
                },
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш еще не был опубликован или уже завершен."
                }
            ]
        },
        {
            "key": "add_channels_to_pub",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "В каком канале опубликовать розыгрыш?"
                },
                {
                    "language": "Английский язык",
                    "translate": "In which channel the giveaway must published?"
                }
            ]
        },
        {
            "key": "giv_parts_less_than_winners",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Победителей не может быть больше, чем участников розыгрыша."
                },
                {
                    "language": "Английский язык",
                    "translate": "There cannot be more winners than participants in the drawing."
                }
            ]
        },
        {
            "key": "my_givs",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Ваши розыгрыши.\r\n\r\n{givs_data}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Your giveaways.\r\n\r\n{givs_data}"
                }
            ]
        },
        {
            "key": "ik_change_cond",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Изменить условия подведения итогов"
                },
                {
                    "language": "Английский язык",
                    "translate": "Change the conditions for summing up"
                }
            ]
        },
        {
            "key": "lot_not_found",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш не найден."
                },
                {
                    "language": "Английский язык",
                    "translate": "Draw not found."
                }
            ]
        },
        {
            "key": "giv_too_much_winners",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Слишком большое число призовых мест. Максимальное количество: 1000 победителей."
                },
                {
                    "language": "Английский язык",
                    "translate": "The number of winners is too high. Maximum number: 1000."
                }
            ]
        },
        {
            "key": "lot_data_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш №{pk}\r\n<a href=\"{link}\">Сообщение с розыгрышем</a>\r\nСтатус: {status}\r\nКоличество участников: {parts_count}\r\nКоличество победителей: {winners_count}\r\nВремя завершения: {end_dt}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Draw #{pk}\r\n<a href=\"{link}\">Draw message</a>\r\nStatus: {status}\r\nNumber of participants: {parts_count}\r\nNumber of winners: {winners_count}\r\nEnd time: {end_dt}"
                }
            ]
        },
        {
            "key": "lot_data_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш №{pk}\r\n<a href=\"{link}\">Сообщение с розыгрышем</a>\r\nСтатус: {status}\r\nКоличество участников: {parts_count}\r\nКоличество победителей: {winners_count}\r\nЗавершение при количестве участников: {end_count}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Draw #{pk}\r\n<a href=\"{link}\">Draw message</a>\r\nStatus: {status}\r\nNumber of participants: {parts_count}\r\nNumber of winners: {winners_count}\r\nEnds at number of participants: {end_count}"
                }
            ]
        },
        {
            "key": "rk_switch_language",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Сменить язык"
                },
                {
                    "language": "Английский язык",
                    "translate": "Change language"
                }
            ]
        },
        {
            "key": "check_giv_before_post_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Внимательно перепроверьте настройки розыгрыша.\r\n\r\nРозыгрыш завершится, когда количество участников станет равно {dt_or_count}\r\nКоличество победителей: {count}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Carefully double-check the giveaway settings.\r\n\r\nThe giveaway will end when the number of participants equals {dt_or_count}\r\nNumber of winners: {count}"
                }
            ]
        },
        {
            "key": "giv_created",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш успешно создан. В ближайшие 5 минут он автоматические будет опубликован в вашем канале."
                },
                {
                    "language": "Английский язык",
                    "translate": "The giveaway has been successfully created. In the next 5 minutes it will be automatically published in your channel."
                }
            ]
        },
        {
            "key": "giv_creation_canceled",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Создание розыгрыша отменено.\r\n\r\nДля вызова меню напишите /start."
                },
                {
                    "language": "Английский язык",
                    "translate": "The creation of the giveaway has been canceled.\r\n\r\nTo call the menu, type /start."
                }
            ]
        },
        {
            "key": "sure_cancel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Вы действительно хотите отменить создание розыгрыша?"
                },
                {
                    "language": "Английский язык",
                    "translate": "Are you sure you want to cancel the creation of the giveaway?"
                }
            ]
        },
        {
            "key": "giv_dt_select_winner",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Дата и время подведения результатов сохранено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Date and time of summarizing the results saved."
                }
            ]
        },
        {
            "key": "giv_end_users_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "You have specified the number of participants to stop the giveaway and summarize the results: {count}"
                },
                {
                    "language": "Русский язык",
                    "translate": "Вы указали количество участников для остановки розыгрыша и подведения итогов: {count}"
                }
            ]
        },
        {
            "key": "giv_when_select_winer",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Когда нужно определить победителя? Укажите точную дату в формате ДД.ММ.ГГ ЧЧ:ММ.\r\n\r\nУстановленный часовой пояс - (GMT+3) Москва, Россия."
                },
                {
                    "language": "Английский язык",
                    "translate": "When should the winner be determined? Specify the exact date in the format DD.MM.YY HH:MM.\r\n\r\nThe set time zone is (GMT+3) Moscow, Russia."
                }
            ]
        },
        {
            "key": "giv_end_by_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Укажите количество участников для проведения розыгрыша:\r\n\r\nУчастник - пользователь, нажавший кнопку \"Участвовать\" под постом с розыгрышем."
                },
                {
                    "language": "Английский язык",
                    "translate": "Specify the number of participants for the drawing:\r\n\r\nParticipant - a user who clicked the \"Participate\" button under the drawing post."
                }
            ]
        },
        {
            "key": "giv_td_examples",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Примеры:\r\n\r\n{ten_min} \\- через 10 минут\r\n{one_hour} \\- через час\r\n{one_day} \\- через день\r\n{one_week} \\- через неделю"
                },
                {
                    "language": "Английский язык",
                    "translate": "Examples:\r\n\r\n{ten_min} \\- in 10 minutes\r\n{one_hour} \\- in an hour\r\n{one_day} \\- in a day\r\n{one_week} \\- in a week"
                }
            ]
        },
        {
            "key": "giv_when_plan_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Когда нужно опубликовать пост с розыгрышем? Укажите точную дату в формате ДД.ММ.ГГ ЧЧ:ММ.\r\n\r\nУстановленный часовой пояс - (GMT+3) Москва, Россия."
                },
                {
                    "language": "Английский язык",
                    "translate": "When should I publish the post with the giveaway? Specify the exact date in the format DD.MM.YY HH:MM.\r\n\r\nThe established time zone is (GMT+3) Moscow, Russia."
                }
            ]
        },
        {
            "key": "ik_end_by_count",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "По количеству участников."
                },
                {
                    "language": "Английский язык",
                    "translate": "By number of participants."
                }
            ]
        },
        {
            "key": "giv_how_to_end",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Каким образом завершить розыгрыш?"
                },
                {
                    "language": "Английский язык",
                    "translate": "How to complete the draw?"
                }
            ]
        },
        {
            "key": "giv_dt_selected",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Время публикации поста с розыгрышем определено."
                },
                {
                    "language": "Английский язык",
                    "translate": "The time to publish the post with the giveaway has been set."
                }
            ]
        },
        {
            "key": "ik_plan_giv",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Запланировать публикацию"
                },
                {
                    "language": "Английский язык",
                    "translate": "Schedule a publication"
                }
            ]
        },
        {
            "key": "ik_now",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Прямо сейчас"
                },
                {
                    "language": "Английский язык",
                    "translate": "Right now"
                }
            ]
        },
        {
            "key": "giv_wrong_dt_format",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Неверно указана дата публикации.\r\n\r\nВерный формат: ДД.ММ.ГГ ЧЧ:ММ.\r\n\r\nНапример: 01.02.2024 12:00."
                },
                {
                    "language": "Английский язык",
                    "translate": "Incorrect date of publication.\r\n\r\nCorrect format: DD.MM.YY HH:MM.\r\n\r\nFor example: 01.02.2024 12:00"
                }
            ]
        },
        {
            "key": "giv_channel_selected",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Channel selected."
                },
                {
                    "language": "Русский язык",
                    "translate": "Канал выбран."
                }
            ]
        },
        {
            "key": "giv_select_dt",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Когда вы хотите опубликовать розыгрыш?"
                },
                {
                    "language": "Английский язык",
                    "translate": "When do you want to post the giveaway?"
                }
            ]
        },
        {
            "key": "giv_select_channel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "В каком канале опубликовать пост с розыгрышем?"
                },
                {
                    "language": "Английский язык",
                    "translate": "In which channel the giveaway post must be published?"
                }
            ]
        },
        {
            "key": "ik_giv_enough_ch",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Все необходимые каналы указаны"
                },
                {
                    "language": "Английский язык",
                    "translate": "Necessary channels are indicated"
                }
            ]
        },
        {
            "key": "giv_channel_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Канал добавлен.\r\n\r\nЧтобы добавить другие каналы, просто пришлите их мне.\r\n\r\nБот должен иметь права администратора канала. Если вы заберете их - он не сможет проверять подписку на необходимые каналы среди участников конкурса."
                },
                {
                    "language": "Английский язык",
                    "translate": "The channel has been added.\r\n\r\nTo add other channels, just send them to me.\r\n\r\nThe bot must have channel administrator rights. If you take them away, it will not be able to check the subscription to the necessary channels among the contest participants."
                }
            ]
        },
        {
            "key": "winners_count_saved",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Количество победителей сохранено: {count}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Number of winners saved: {count}"
                }
            ]
        },
        {
            "key": "channels_saved",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Сохранено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Saved."
                }
            ]
        },
        {
            "key": "ik_no_sub_channels",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш без обязательных подписок."
                },
                {
                    "language": "Английский язык",
                    "translate": "Giveaway with no required subscriptions."
                }
            ]
        },
        {
            "key": "giv_add_chanels_to_sub",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Add channels that participants will need to subscribe to in order to participate in the giveaway.\r\n\r\nTo add a channel, you need to:\r\n\r\n1. Add the bot (@GiveRandomizerBot) to your channel as an administrator. Without this, the bot will not be able to check whether the participant is subscribed to the channel.\r\n\r\n2. Send the channel to the bot in the @channelname format or forward any message from the channel.\r\n\r\nIf you want to create a giveaway without necessarily subscribing to the channel, click the button below:"
                },
                {
                    "language": "Русский язык",
                    "translate": "Добавьте каналы, на которые участникам необходимо будет подписаться для участия в розыгрыше.\r\n\r\nДля того чтобы добавить канал, необходимо:\r\n\r\n1. Добавить бота (@GiveRandomizerBot) в ваш канал в роли администратора. Без этого бот не сможет проверять подписан ли участник на канал.\r\n\r\n2. Отправить боту канал в формате @channelname или переслать любое сообщение из канала.\r\n\r\nЕсли вы хотите создать розыгрыш без обязательной подписки на канал, нажмите кнопку ниже:"
                }
            ]
        },
        {
            "key": "wrong_format",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Неверный формат, попробуйте еще раз."
                },
                {
                    "language": "Английский язык",
                    "translate": "Invalid format, please try again."
                }
            ]
        },
        {
            "key": "ik_cancel_action",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отменить действие."
                },
                {
                    "language": "Английский язык",
                    "translate": "Cancel action."
                }
            ]
        },
        {
            "key": "ik_giv_im_in_3",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Принять участие"
                },
                {
                    "language": "Английский язык",
                    "translate": "Take part"
                }
            ]
        },
        {
            "key": "ik_giv_im_in_2",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Участвовать"
                },
                {
                    "language": "Английский язык",
                    "translate": "Participate"
                }
            ]
        },
        {
            "key": "ik_giv_im_in_1",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Участвую!"
                },
                {
                    "language": "Английский язык",
                    "translate": "I'm in!"
                }
            ]
        },
        {
            "key": "giv_get_button_type",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отправьте текст, который будет отображаться на кнопке, или выберите один из установленных вариантов:"
                },
                {
                    "language": "Английский язык",
                    "translate": "Send the text to be displayed on the button or select one of the set options:"
                }
            ]
        },
        {
            "key": "giv_text_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Text successfully added"
                },
                {
                    "language": "Русский язык",
                    "translate": "Текст успешно добавлен"
                }
            ]
        },
        {
            "key": "giv_video_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Видео успешно добавлено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Video successfully added."
                }
            ]
        },
        {
            "key": "giv_photo_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Photo successfully added."
                },
                {
                    "language": "Русский язык",
                    "translate": "Фото успешно добавлено."
                }
            ]
        },
        {
            "key": "no_channels_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Вы не добавили ни один канал, чтобы добавить канал в бота, нажмите кнопку \"Мои каналы\"."
                },
                {
                    "language": "Английский язык",
                    "translate": "You haven't added any channels, to add a channel to the bot, click “My Channels”."
                }
            ]
        },
        {
            "key": "giv_creation",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Создание розыгрыша.\r\n\r\nОтправьте текст для вашего поста с розыгрышем.\r\n\r\nВместе с текстом вы можете отправить 1 медиафайл: картинку, видео или GIF-изображение.\r\n\r\nВы также можете использовать эмодзи и любые другие встроенные в Telegram функции.\r\n\r\nНаписанный вами пост будет опубликован в вашем канале вместе с кнопкой для участия."
                },
                {
                    "language": "Английский язык",
                    "translate": "Creating a giveaway.\r\n\r\nSend the text for your giveaway post.\r\n\r\nAlong with the text, you can send 1 media file: a picture, video or GIF image.\r\n\r\nYou can also use emoji and any other built-in Telegram features.\r\n\r\nThe post you write will be published in your channel along with a button to participate."
                }
            ]
        },
        {
            "key": "error_not_admin",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Ошибка.\r\n\r\nВы не являетесь администратором в канале, который пытаетесь добавить."
                },
                {
                    "language": "Английский язык",
                    "translate": "Error.\r\n\r\nYou are not an admin in the channel you are trying to add."
                }
            ]
        },
        {
            "key": "hello_message",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Hello.\r\n\r\nI am a randomizer bot, I can help you create and conduct a giveaway in the Telegram channel.\r\n\r\nCreate a new giveaway?"
                },
                {
                    "language": "Русский язык",
                    "translate": "Привет.\r\n\r\nЯ - бот рандомайзер, могу помочь вам создать и провести розыгрыш в Telegram канале.\r\n\r\nСоздать новый розыгрыш?"
                }
            ]
        },
        {
            "key": "bot_not_admin",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Ошибка.\r\n\r\nБот не является администратором вашего канала.\r\n\r\nБот без прав администратора не может проверять подписку на канала среди участников розыгрыша. \r\n\r\nДобавьте бота в администраторы канала, затем пришлите название вашего канала или перешлите любой пост."
                },
                {
                    "language": "Английский язык",
                    "translate": "Error.\r\n\r\nThe bot is not an administrator of your channel.\r\n\r\nA bot without administrator rights cannot check the channel subscription among the participants of the giveaway.\r\n\r\nAdd the bot to the channel administrators, then send the name of your channel or forward any post."
                }
            ]
        },
        {
            "key": "no_channel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Ошибка.\r\n\r\nКанал не найден."
                },
                {
                    "language": "Английский язык",
                    "translate": "Error.\r\n\r\nThe channel not found."
                }
            ]
        },
        {
            "key": "channel_added",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Channel {name} has been successfully added. You can move on to creating a draw.\r\n\r\nTo create a new giveaway, enter the command /new_lot."
                },
                {
                    "language": "Русский язык",
                    "translate": "Канал {name} успешно добавлен. Вы можете перейти к созданию розыгрыша.\r\n\r\nЧтобы создать новый розыгрыш, введите команду /new_lot."
                }
            ]
        },
        {
            "key": "auto_cancel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Действие отменено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Action canceled."
                }
            ]
        },
        {
            "key": "channel_deleted",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Канал был успешно удален."
                },
                {
                    "language": "Английский язык",
                    "translate": "The channel was successfully deleted."
                }
            ]
        },
        {
            "key": "delete_channel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Для того, чтобы удалить канал, введите команду:\r\n{command}"
                },
                {
                    "language": "Английский язык",
                    "translate": "To delete a channel, enter the command:\r\n{command}"
                }
            ]
        },
        {
            "key": "have_changes",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Имя канала обновлено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Channels name updated."
                }
            ]
        },
        {
            "key": "no_changes",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Имя канала не изменилось."
                },
                {
                    "language": "Английский язык",
                    "translate": "Channel name wasn't changed."
                }
            ]
        },
        {
            "key": "channel_menu",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Меню канала:"
                },
                {
                    "language": "Английский язык",
                    "translate": "Channel's menu:"
                }
            ]
        },
        {
            "key": "cancel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Действие отменено."
                },
                {
                    "language": "Английский язык",
                    "translate": "Action canceled."
                }
            ]
        },
        {
            "key": "ik_cancel",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Отмена"
                },
                {
                    "language": "Английский язык",
                    "translate": "Cancel"
                }
            ]
        },
        {
            "key": "add_channel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Инструкция.\r\n\r\n1. Добавьте бота @GiveRandomizerBot в ваш канал или чат как администратора - с правом публиковать посты в канале или писать сообщения.\r\n\r\n2. Пришлите мне название вашего канала в формате @channelname или перешлите любой пост, опубликованный в нём."
                },
                {
                    "language": "Английский язык",
                    "translate": "Instructions.\r\n\r\n1. Add the @GiveRandomizerBot to your channel or chat as an admin - with the right to publish posts in the channel or write messages.\r\n\r\n2. Send me the name of your channel in @channelname format or forward me any post published in it."
                }
            ]
        },
        {
            "key": "my_channels",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Добавленные вами каналы:"
                },
                {
                    "language": "Английский язык",
                    "translate": "The channels you have added:"
                }
            ]
        },
        {
            "key": "rk_help",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Поддержка"
                },
                {
                    "language": "Английский язык",
                    "translate": "Help"
                }
            ]
        },
        {
            "key": "rk_my_channels",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "My channels"
                },
                {
                    "language": "Русский язык",
                    "translate": "Мои каналы"
                }
            ]
        },
        {
            "key": "rk_my_givs",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Мои розыгрыши"
                },
                {
                    "language": "Английский язык",
                    "translate": "My giveaways"
                }
            ]
        },
        {
            "key": "rk_create_giv",
            "key_type": "RK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Создать розыгрыш"
                },
                {
                    "language": "Английский язык",
                    "translate": "Create giveaway"
                }
            ]
        },
        {
            "key": "ik_back",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Назад"
                },
                {
                    "language": "Английский язык",
                    "translate": "Back"
                }
            ]
        },
        {
            "key": "giv_repost_command",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "If you want to post a giveaway in another channel or chat, enter the command:\r\n\r\n`/postlot{giv_uuid}`\r\n\r\nThe user entering the command must add their channel or chat to the \"My Channels\" section\\."
                },
                {
                    "language": "Русский язык",
                    "translate": "Если вы хотите опубликовать розыгрыш в другом канале или чате, то введите команду:\r\n\r\n`/postlot{giv_uuid}`\r\n\r\nПользователь, вводящий команду, должен добавить свой канал или чат в раздел \"Мои каналы\"\\."
                }
            ]
        },
        {
            "key": "payment_body",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Строки в количестве: {count}."
                },
                {
                    "language": "Английский язык",
                    "translate": "Number of lines: {count}."
                }
            ]
        },
        {
            "key": "payment_head",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Выгрузка участников розыгрыша #{pk}."
                },
                {
                    "language": "Английский язык",
                    "translate": "Unloading the participants of the draw #{pk}."
                }
            ]
        },
        {
            "key": "get_table_start",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "В розыгрыше #{pk} набралось {parts_count} участников.\r\nДля полной выгрузки всех участников розыгрыша в таблицу необходимо оплатить {price} Telegram Stars.\r\n\r\nВы можете осуществить платеж, нажав по кнопке ниже."
                },
                {
                    "language": "Английский язык",
                    "translate": "There are {parts_count} participants in the #{pk} draw.\r\nTo fully upload all participants of the draw to the table, you need to pay {price} Telegram Stars.\r\n\r\nYou can make the payment by clicking the button below."
                }
            ]
        },
        {
            "key": "csv_data",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Выгрузка по розыгрышу #{giv_pk}, строк: {lines_count}."
                },
                {
                    "language": "Английский язык",
                    "translate": "Unload by draw #{giv_pk}, lines: {lines_count}."
                }
            ]
        },
        {
            "key": "giv_already_ended",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш уже завершен."
                },
                {
                    "language": "Английский язык",
                    "translate": "The draw has already ended."
                }
            ]
        },
        {
            "key": "not_subbed",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Вы не выполнили все условия розыгрыша, подпишитесь на необходимые каналы и попробуйте снова."
                },
                {
                    "language": "Английский язык",
                    "translate": "You haven't fulfilled all the conditions of the giveaway, subscribe to the necessary channels and try again."
                }
            ]
        },
        {
            "key": "now_in",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Теперь вы участвуете в этом розыгрыше."
                },
                {
                    "language": "Английский язык",
                    "translate": "You are now entered into this giveaway."
                }
            ]
        },
        {
            "key": "already_in",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Вы уже участвуете в этом розыгрыше."
                },
                {
                    "language": "Английский язык",
                    "translate": "You are already participating in this giveaway."
                }
            ]
        },
        {
            "key": "re_select_ended",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Перевыбор завершен."
                },
                {
                    "language": "Английский язык",
                    "translate": "The re-election is complete."
                }
            ]
        },
        {
            "key": "new_winners_list",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Список дополнительных победителей:\r\n{winners}"
                },
                {
                    "language": "Английский язык",
                    "translate": "List of additional winners:\r\n{winners}"
                }
            ]
        },
        {
            "key": "new_winners_not_found",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Не нашлось участников, выполнивших условия розыгрыша, дополнительных победителей нет."
                },
                {
                    "language": "Английский язык",
                    "translate": "There were no participants who fulfilled the terms of the drawing, there are no additional winners."
                }
            ]
        },
        {
            "key": "check_link",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Эту ссылку вы можете опубликовать в канале для подтверждение честности проведенного розыгрыша:\r\n\r\n`{link}`"
                },
                {
                    "language": "Английский язык",
                    "translate": "You can publish this link in the channel to confirm the honesty of the draw:\r\n\r\n`{link}`"
                }
            ]
        },
        {
            "key": "cant_end_giv",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Невозможно закончить этот розыгрыш."
                },
                {
                    "language": "Английский язык",
                    "translate": "There is no way to finish this giveaway."
                }
            ]
        },
        {
            "key": "giv_ended",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш завершен."
                },
                {
                    "language": "Английский язык",
                    "translate": "The giveaway is over."
                }
            ]
        },
        {
            "key": "select_new_winners",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Английский язык",
                    "translate": "Selecting additional winners.\r\n\r\nUse this function to select additional winners (for example, if one of the winners does not contact).\r\n\r\nSelecting additional winners is possible only after the main draw has ended.\r\n\r\nThe bot will select additional winners randomly.\r\n\r\nHow many additional winners should the bot select?\r\n\r\nTo cancel the action, type /cancel."
                },
                {
                    "language": "Русский язык",
                    "translate": "Выбор дополнительных победителей.\r\n\r\nИспользуйте эту функцию, чтобы выбрать дополнительных победителей (например, если один из победителей не выходит на связь).\r\n\r\nВыбор дополнительных победителей возможен только после завершения основного розыгрыша.\r\n\r\nБот будет выбирать дополнительных победителей случайным образом.\r\n\r\nСколько дополнительных победителей выбрать боту?\r\n\r\nДля отмены действия нажмите /cancel"
                }
            ]
        },
        {
            "key": "apply_end",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Подтвердите завершение розыгрыша."
                },
                {
                    "language": "Английский язык",
                    "translate": "Confirm the completion of the draw."
                }
            ]
        },
        {
            "key": "help_giv_results",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Если победитель не выходит на связь, или не выполнил все условия розыгрыша, то вы можете перевыбрать победителя среди участников розыгрыша. Перевыборы осуществляются случайным образом.\nДля вызова меню напишите /start."
                },
                {
                    "language": "Английский язык",
                    "translate": "If the winner does not contact or does not fulfill all the conditions of the drawing, then you can re-select the winner from among the participants of the drawing. Re-elections are carried out randomly.\nTo call the menu, type /start."
                }
            ]
        },
        {
            "key": "ik_end_giv_cancel",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Не завершать"
                },
                {
                    "language": "Русский язык",
                    "translate": "Don't complete"
                }
            ]
        },
        {
            "key": "giv_results_autor",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Розыгрыш #{giv_num}.\r\nКол-во участников: {parts_count}.\r\nКол-во победителей: {winers_count}.\r\nРозыгрыш завершен по запросу автора.\r\n\r\nРезультаты розыгрыша:\r\n\r\nПобедители:"
                },
                {
                    "language": "Английский язык",
                    "translate": "Giveaway #{giv_num}.\r\nNumber of participants: {parts_count}.\r\nNumber of winners: {winers_count}.\r\nGiveaway ended at the request of the author.\r\n\r\nGiveaway results:\r\n\r\nWinners:"
                }
            ]
        },
        {
            "key": "ik_pnt",
            "key_type": "IK",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Опубликовать"
                },
                {
                    "language": "Английский язык",
                    "translate": "Publish"
                }
            ]
        },
        {
            "key": "check_giv_before_post",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Внимательно перепроверьте настройки розыгрыша.\r\n\r\nРозыгрыш завершится {dt_or_count}\r\nКоличество победителей: {count}"
                },
                {
                    "language": "Английский язык",
                    "translate": "Carefully double-check the giveaway settings.\r\n\r\nThe giveaway will end {dt_or_count}\r\nNumber of winners: {count}"
                }
            ]
        },
        {
            "key": "button_text_save",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Текст кнопки сохранен."
                },
                {
                    "language": "Английский язык",
                    "translate": "Button text saved."
                }
            ]
        },
        {
            "key": "already_added_channel",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Ошибка.\r\n\r\nВы уже добавили этот канал."
                },
                {
                    "language": "Английский язык",
                    "translate": "Error.\r\n\r\nChannel already added."
                }
            ]
        },
        {
            "key": "default_message",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Стандартный ответ"
                },
                {
                    "language": "Английский язык",
                    "translate": "Стандартный ответ ENG"
                }
            ]
        },
        {
            "key": "giv_dt_not_future",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Запрещается использовать даты и время, которые уже прошли."
                },
                {
                    "language": "Английский язык",
                    "translate": "Запрещается использовать даты и время, которые уже прошли.  ENG"
                }
            ]
        },
        {
            "key": "giv_post_before_results",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Дата и время подведения результатов должны быть позже даты и времени публикации розыгрыша."
                },
                {
                    "language": "Английский язык",
                    "translate": "Дата и время подведения результатов должны быть позже даты и времени публикации розыгрыша. ENG"
                }
            ]
        },
        {
            "key": "recreate_giv",
            "key_type": "TXT",
            "translates": [
                {
                    "language": "Русский язык",
                    "translate": "Время подведения итогов не может быть раньше времени публикации розыгрыша, пересоздайте розыгрыш"
                },
                {
                    "language": "Английский язык",
                    "translate": "Время подведения итогов не может быть раньше времени публикации розыгрыша, пересоздайте розыгрыш ENG"
                }
            ]
        }
    ]
    for key in keys_list:
        rk = Text.objects.create(
            key=key["key"],
            key_type=key["key_type"],
        )
        for tranlate in key["translates"]:
            Translate.objects.create(
                text_key=rk,
                language=languages_dict[tranlate["language"]],
                translate=tranlate["translate"]
            )
    prices_info = [
        {
            "lt_count": 10,
            "price": 10,
        },
        {
            "lt_count": 50,
            "price": 50,
        },
        {
            "lt_count": 100,
            "price": 100,
        },
        {
            "lt_count": 250,
            "price": 250,
        },
        {
            "lt_count": 500,
            "price": 500,
        },
        {
            "lt_count": 1000,
            "price": 1000,
        },
        {
            "lt_count": 2500,
            "price": 2000,
        },
        {
            "lt_count": 5000,
            "price": 4000,
        },
        {
            "lt_count": 10000,
            "price": 8000,
        },
        {
            "lt_count": 10000000,
            "price": 10000,
        },
    ]
    for price in prices_info:
        Price.objects.create(**price)
