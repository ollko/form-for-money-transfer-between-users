# form-for-money-transfer-between-users

Приложение для Django 2.2 (Python 3.7), состоящее из формы для перевода денег между пользователей (без REST API).

У пользователей есть помимо основных полей 2 дополнительных: ИНН (может повторяться у разных пользователей, пользователей в системе может быть очень много) и счет (в рублях, с точностью до копеек). Также есть форма состоящая из полей:

- Выпадающий список со всеми пользователями в системе, со счета которого нужно перевести деньги
- Поле для ввода ИНН пользователей, на счета которых будут переведены деньги
- Поле для указания какую сумму нужно перевести с одного счета на другие

Необходимо проверять есть ли достаточная сумма у пользователя, со счета которого списываются средства, и есть ли пользователи с указанным ИНН в БД. При валидности введенных данных необходимо указанную сумму списать со счета указанного пользователя и перевести на счета пользователей с указанным ИНН в равных частях

- если переводится 60 рублей 10ти пользователям, то каждому попадет 6 рублей на счет.
- если переводится 63 рублей 10ти пользователям, то каждому попадет 6 рублей на счет (3 руб останутся у пользователя).
- если пользователь-отправитель имеет ИНН тот же, что и пользователи-получатели, на счет от получателя ничего не переводится (только списывается)

