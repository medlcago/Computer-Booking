def generate_info_about_user_message(user: dict):
    user_info = f"""<b>ID:</b> <code>{user.get('user_id')}</code>
<b>ФИО:</b> {user.get('fullname')}
<b>username:</b> {user.get('username', 'Отсутствует')}
<b>Номер телефона:</b> {user.get('phone_number')}
<b>Дата регистрации:</b> {user.get('created_at')}
<b>Дата последнего изменения:</b> {user.get('updated_at')}
<b>Админ:</b> {('Нет', 'Да')[user.get('is_admin')]}
<b>Заблокирован:</b> {('Нет', 'Да')[user.get('is_blocked')]}
<b>Активен:</b> {('Нет', 'Да')[user.get('is_active')]}
<b>Баланс:</b> {user.get('balance')} RUB
"""
    return user_info
