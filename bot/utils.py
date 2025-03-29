import datetime as dt
from decimal import Decimal, InvalidOperation

from django.contrib.auth.models import User
from django.db.models import Sum

from bot.exceptions import ParameterError, DateFormatterError
from bot.models import TelegramUser, TelegramGroup
from expenses.models import Expense, Tag, ExchangeRate, Payment, CURRENCY
from gastitis.settings import DATE_INPUT_FORMATS


def user_and_group(func):
    """
    Add user and group to handler params.
    """
    async def wrapper(update, context):
        user_data = update.message.from_user
        chat_id = user_data.id
        first_name = getattr(user_data, 'first_name', chat_id)
        last_name = getattr(user_data, 'last_name') or '-'
        telegram_username = getattr(user_data, 'username', '')
        username = telegram_username or first_name
        user, _ = await User.objects.aget_or_create(telegram__chat_id=chat_id, defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        })

        await TelegramUser.objects.aupdate_or_create(
            user=user, chat_id=chat_id, defaults={
                'username': telegram_username
            })
        group_data = update.message.chat
        group_id = group_data.id
        group_name = group_data.title or username + '__private'

        group, _ = await TelegramGroup.objects.aget_or_create(chat_id=group_id, defaults={
            'name': group_name,
        })
        await group.users.aadd(user)


        await func(update, context, user, group)

    return wrapper


async def new_expense(params, user, group):
    """
    Check if params are valid and create a new expense.

    Returns a text to send to the user.
    """
    try:
        data = await decode_expense_params(params, group)
    except ParameterError as e:
        return str(e)

    response_text = ''
    amount = data['amount']
    description = data['description']
    date = data['dd']
    tags = data['tt']
    user = data['uu'] or user
    expense = Expense(user=user, group=group, description=description, amount=amount, date=date)
    if data['exchange_rate']:
        exchange_rate = data['exchange_rate']
        expense.original_currency = exchange_rate.currency
        expense.original_amount = data['original_amount']
        response_text += 'Tu gasto se convirtió de {} a $ usando un tipo de cambio = ${} \
            (cargado el {}).\n\n'.format(
                CURRENCY[exchange_rate.currency],
                exchange_rate.rate,
                exchange_rate.date
            )
    await expense.asave()
    if tags:
        for tag in tags:
            await expense.tags.aadd(tag)

    if data['uu'] is None:
        response_text += 'Se guardó tu gasto {}'.format(expense)
    else:
        response_text += 'Se guardó el gasto que hizo {} para {}'.format(expense.user, expense)
    return response_text


def parse_date(date_str, date_formats):
    for format in date_formats:
        try:
            return dt.datetime.strptime(date_str, format).date()
        except ValueError:
            continue
    raise DateFormatterError(f"Formato de fecha no válido: {date_str}")


async def decode_expense_params(params, group):
    """
    Process command params in expense's attributes, and return a dict with the following data:
    amount = expense amount.
    dd = date or None
    tt = Tag instance or None
    uu = User or None
    description = string, expense description
    """
    # define special arguments and help texts for them
    special_arguments = {
        'dd': 'Colocar la fecha en la que se generó el gasto después del argumento "dd"',
        'tt': 'Luego de "tt" colocar el nombre de la/las etiqueta/s para el gasto que estás '\
        'cargando. Podés ingresar más de una etiqueta separando los nombres por comas (sin '\
        'espacio).',
        'uu': 'A quién le estás cargando el gasto. Si no lo pasás, se te carga a vos.',
    }

    data = {}

    if not params:
        text = 'Necesito que me digas cuanto pagaste y una descripción del gasto.'
        raise ParameterError(text)

    # handle amount
    amount_received, *params = params

    amount, exchange_rate, original_amount = await get_amount_and_currency(amount_received)
    data['amount'] = amount
    data['exchange_rate'] = exchange_rate
    data['original_amount'] = original_amount

    #look for special arguments
    for argument, text in special_arguments.items():
        try:
            argument_position = params.index(argument)
            params.pop(argument_position)
            data[argument] = params.pop(argument_position)

        except ValueError:
            data[argument] = None
        except IndexError:
            raise ParameterError(text)

    # handle description
    if not params:
        raise ParameterError('Necesito que agregues en el comando una descripción del gasto')

    data['description'] = ' '.join(params)

    # handle date
    if not data['dd']:
        data['dd'] = dt.date.today()
    else:
        try:
            data['dd'] = parse_date(data['dd'], DATE_INPUT_FORMATS)
        except DateFormatterError:
            example_date = dt.date.today()
            formated_dates = [dt.datetime.strftime(example_date, format) for format in DATE_INPUT_FORMATS]
            date_bullets = '\n - '.join(formated_dates)
            text = f'El formato de fecha no es correcto. ' \
                   f'Por ejemplo a la fecha de hoy la podés escribir en cualquiera ' \
                   f'de los siguientes formatos: \n - {date_bullets}'
            raise ParameterError(text)

    # handle tags
    if data['tt']:
        tags_list = []
        for t in data['tt'].split(','):
            tag_instnce, _ = await Tag.objects.aget_or_create(name=data['tt'], group=group)
            tags_list.append(tag_instnce)
        data['tt'] = tags_list

    # handle user
    if data['uu']:
        # Remove the '@' from the username input:
        if data['uu'][0] == '@':
            data['uu'] = data['uu'][1:]
        # Only already registered users:
        try:
            data['uu'] = await group.users.aget(username=data['uu'])
        except User.DoesNotExist:
            text = 'Luego del parámetro "uu" necesito que ingreses un nombre de usuario válido.\n\n'
            text += 'El usuario debe previamente haber enviado algún comando en el grupo para que gastitis lo registre. '
            text += 'Ej: /total'
            raise ParameterError(text)

    return data

async def decode_payments_params(params,user,group):
    """
    Process command params in payment's attributes, and return a dict with the following data:
    amount = expense amount
    date = date
    to_user = User
    """
    result = {}
    if len(params) == 3:
        try:
            date = parse_date(params.pop(-1), DATE_INPUT_FORMATS)
        except DateFormatterError:
            example_date = dt.date.today()
            formated_dates = [dt.datetime.strftime(example_date, format) for format in DATE_INPUT_FORMATS]
            date_bullets = '\n - '.join(formated_dates)
            text = f'El formato de fecha no es correcto. ' \
                   f'Por ejemplo a la fecha de hoy la podés escribir en cualquiera ' \
                   f'de los siguientes formatos: \n - {date_bullets}'
            raise ParameterError(text)
    else:
        date = dt.date.today().strftime("%Y-%m-%d")
    result["date"] = date
    try:
        amount, to_user = params
        amount = float(amount)
        if to_user.startswith("@"):
            to_user = to_user[1:]
        to_user = await User.objects.exclude(pk=user.pk).aget(username=to_user, telegram_groups=group)
        result["amount"] =amount
        result["to_user"] = to_user
    except ValueError:
        text =  "El primer argumento debe ser el monto a pagar, y el segundo argumento el "\
                "username del usuario al que le estás pagando. \n\n"\
                "Opcionalmente puede contener un tercer argumento con la fecha en la que se "\
                "desea  computar el gasto, con el formato dd/mm/yy."
        raise ParameterError(text)
    except User.DoesNotExist:
        text = "El usuario espcificado ({}) no existe dentro de este grupo. \n".format(to_user)
        text += "Los posibles usuarios a los que les podes cargar un pago son: \n"
        async for member in group.users.exclude(pk=user.pk):
            text += "- {}\n".format(member.username)
        raise ParameterError(text)
    return result

async def get_amount_and_currency(raw_amount):
    """
    Given a string it returns an amount (in the default currency), the original amount  and a
    ExchangeRate instance.  If the string doesn't have a currency specified, it assumes the
    default currency and returns None as ExchangeRate.

    Params:
        - raw_amount = string of an amount (it may have a currency)
    Returns:
        - amount = Decimal number that represent the amount in the default currency.
        - exchange_rate = an exchange rate instance or None if the amount is in the default
        currency.
        - original_amount = the raw amount received, converted in Decimal.
    """
    for key, value in CURRENCY.items():
        if raw_amount.startswith((key, value)) or raw_amount.endswith((key, value)):
            # TODO: get current exchanger rate from api.
            exchange_rate = await ExchangeRate.objects.filter(currency=key).alast()
            break
    else:
        key, value = ['', '']
        exchange_rate = None
    amount_without_currency = raw_amount.replace(value, '').replace(key, '')

    try:
        original_amount = amount_without_currency.replace(',', '.')
        original_amount = Decimal(original_amount)
    except InvalidOperation:
        text = 'El primer valor que me pasas después del comando tiene que ser el valor de lo '\
               'que pagaste. \n\n También podés especificar un tipo de cambio con el codigo y '\
                ' monto, por ejemplo 40u para 40 dolares (o usd40). \n Los códigos posibles son:'
        for k, v in CURRENCY.items():
            text += '\n - {} ({})'.format(k, v)
            text += '\n - {}'.format(v)

        text += '\n\n El valor "{}" no es un número válido.'.format(amount_without_currency)
        raise ParameterError(text)
    if exchange_rate:
        amount = original_amount * exchange_rate.rate
    else:
        amount = original_amount

    return amount, exchange_rate, original_amount


async def new_payment(params, update, user, group):
    """
    Save a new Payment instance.
    params can have two values (amount and user to pay) or three values (amount, user to pay and
    date to save the payment.
    """
    if await group.users.acount() == 1:
        text = "Solo se pueden cargar pagos entre usuarios dentro de un grupo. Este chat tiene "\
               "un único miembro, por lo que no se pueden realizar pagos."
        return text

    try:
        data = await decode_payments_params(params,user, group)
    except ParameterError as e:
        return str(e)

    payment_details = {
        'from_user': user,
        'to_user': data['to_user'],
        'group': group,
        'amount': data['amount'],
        'date': data['date'],
    }
    payment = await Payment.objects.acreate(**payment_details)

    return "Se ha registrado su pago a {} por ${} en la fecha {}".format(data['to_user'], data['amount'], data['date'])


async def show_expenses(group, **expense_filters):
    """
    Return a text with expenses processed and filtered according to the expense filters recived.
    """
    group_expenses_qs = Expense.objects.filter(group=group, **expense_filters)
    if not await group_expenses_qs.aexists():
        return "Todavía no hay gastos cargados en este grupo"
    total_expenses = await group_expenses_qs.aaggregate(Sum('amount'))
    total_expenses = total_expenses['amount__sum']
    total_expenses = round(total_expenses, 2)
    user_expenses = {}
    quantity_expenses = await group_expenses_qs.acount()
    text = "*Total: ${} ({} gastos)*\n".format(total_expenses, quantity_expenses)
    if await group.users.acount() > 1:
        async for user in group.users.all():
            expense_qs = group_expenses_qs.filter(user=user)
            expenses = await expense_qs.aaggregate(Sum('amount'))
            expenses = expenses['amount__sum'] or 0

            payments_done = user.payments_done.filter(group=group, **expense_filters)
            payments_done = await payments_done.aaggregate(Sum('amount'))
            payments_done = payments_done['amount__sum'] or 0

            payments_recived = user.payments_recived.filter(group=group, **expense_filters)
            payments_recived = await payments_recived.aaggregate(Sum('amount'))
            payments_recived = payments_recived['amount__sum'] or 0

            amount = expenses + payments_done - payments_recived
            amount = round(amount, 2)
            user_expenses[user.username] = amount

        for user, total in user_expenses.items():
            text += "- {}: ${} ({}%)\n".format(user, total, round(total/total_expenses*100))

        expenses_equal_parts = round(total_expenses / len(user_expenses), 2)
        text += f"\n\nPara estar a mano cada uno debería haber gastado ${expenses_equal_parts}:\n"
        for user, total in user_expenses.items():
            if total < expenses_equal_parts:
                debt = round(expenses_equal_parts - total, 2)
                text += f"- {user} debe pagar ${debt}.\n"

            elif total > expenses_equal_parts:
                credit = round(total - expenses_equal_parts, 2)
                text += f"- {user} debe recibir ${credit}.\n"

            else:
                text += f" - {user} no debe ni le deben nada.\n"

    return text


def get_month_filters(year, month):
    first_day_of_month = dt.date(year, month, 1)
    if month == 12:
        next_month = 1
        year += 1
    else:
        next_month = month + 1
    first_day_of_next_month = dt.date(year, next_month, 1)

    expense_filters = {
        'date__gte': first_day_of_month,
        'date__lt': first_day_of_next_month,
    }
    return expense_filters


async def get_month_expenses(group, year, month):
    expense_filters = get_month_filters(year, month)
    text = "Gastos del mes {} del año {}\n\n".format(month, year)
    text += await show_expenses(group, **expense_filters)
    return text


def get_month_and_year(params):
    today = dt.date.today()
    month = today.month
    year = today.year
    if not params:
        return month, year
    elif len(params) == 1:
        param_month = params[0]
        param_year = year
    else:
        param_month, param_year = params

    try:
        param_month = int(param_month)
        param_year = int(param_year)
        if param_month <= 12:
            month = param_month
        year = param_year
        if year < 100:
            year += 2000

    except:
        pass

    return month, year


def is_group(update):
    # if the sender id is the same as the chat id, the message is recived from a private chat
    return update.message.from_user.id != update.message.chat_id
