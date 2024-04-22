from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import UserProfileForm, CustomUserCreationForm
from .models import Profile, NewField, BookingInfo
from django.contrib.auth.models import User
from main import DataBaseBooking

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
        # Если пользователь аутентифицирован, показываем домашнюю страницу
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid(): # and profile_form.is_valid():
            # user = 
            user_form.save()
            user = dict(user_form.data)
            user_id = User.objects.get(username=user['username'][0])
            profile = Profile.objects.create(user=user_id, username=user['username'][0], email=user['email'][0], password=user['password1'][0])
        
            return redirect('login')  
        
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'singin.html', {'form': user_form,})#'profile_form': profile_form, 'error_message': request.method})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect to a success page.
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def choose_service(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    db_book = DataBaseBooking()

    all_tables_data = [name for name in db_book.get_all_tables()]

    return render(request, 'services.html', {'data' : all_tables_data})

# Спросить у дениса про то что когда я тыкаю на кнопку у меня по факту новая страница и типа есть пользователь 
# захочет вернуться то стрелками он врядли это сделает
def table_view(request, table_name):
    db_book = DataBaseBooking()
    col_names = db_book.get_col_names(table_name)

    newfieds = NewField.objects.filter(created_by__username=table_name)
    choises = []
    for field in newfieds:
        for f in field.choise.all():
            choises.append(f.choise) 

    
    values = []
    form_error = ''
    if request.method == "POST":
        table_data = [list(i) for i in db_book.get_table_data(table_name)]
        if 'id' in request.POST:
            id = request.POST.get('id')[0]
        if 'button-book' in request.POST:
            row = change_flag(table_data, id, 1, request.user.id)
            db_book.edit_table_row(table_name, row[0], row[1:])
        elif 'button-cancel' in request.POST:
            row = change_flag(table_data, id, 0, 0)
            db_book.edit_table_row(table_name, row[0], row[1:])
        # elif 'button-sort' in request.POST:
        #     sort_by = dict(request.POST)['option'][0]
        #     if sort_by in col_names:   
        #         table_data = db_book.sort_table(table_name, sort_by)
        #     else:
        #         form_error = 'nosuchcol'

        if 'button-book-final' in request.POST:
            # comment: тут надо будет записывать в базу юзеров их забронированные места
            # user_id | username | event(название таблицы откуда это) | book_id(юнит бронирования) |
            # что-то в этом духе
            # я гандон и не нарисовал ничего простите(  
            units_to_book = db_book.get_row_by_status(table_name, 1, request.user.id)
            return render(request, 'booking_conformation.html', {'data': units_to_book, 'table_name': table_name})
        
        
    else:
        table_data = [list(i) for i in db_book.get_table_data(table_name)]
        
    table_groups = db_book.table_groups(table_name, choises)
    return render(request, 'table_view.html', {'data': {"table_name": table_name, "col_names": col_names}, 
                                                        'help': request.POST, "current_user": request.user.id, 
                                                        'form_error': form_error, 'table_groups': table_groups})

def booking_conformation(request, table_name):
    db_book = DataBaseBooking()
    if request.method == "POST":
        table_data = [list(i) for i in db_book.get_table_data(table_name)]
        units_to_book = db_book.get_row_by_status(table_name, 1, request.user.id)

        if 'id' in request.POST:
            id = request.POST.get('id')[0]
        if 'button-book' in request.POST:
            row = change_flag(table_data, id, 1, request.user.id)
            db_book.edit_table_row(table_name, row[0], row[1:])
            units_to_book = db_book.get_row_by_status(table_name, 1, request.user.id)
        elif 'button-cancel' in request.POST:
            row = change_flag(units_to_book, id, 0, 0)
            db_book.edit_table_row(table_name, row[0], row[1:])
        if 'button-book-conformation' in request.POST:
            units_to_book = db_book.get_row_by_status(table_name, 1, request.user.id)
            for u in units_to_book:
                row = change_flag(units_to_book, u[0], 2)
                db_book.edit_table_row(table_name, row[0], row[1:])
            return render(request, 'booking_conformation.html', {'ready': True, 'data': units_to_book, 'table_name': table_name })

        return render(request, 'booking_conformation.html', {'data': units_to_book, 'table_name': table_name, 'help': request.POST})

def my_booking(request):
    db_book = DataBaseBooking()
    formated_table = []
    table = db_book.get_all_tables()
    check = [db_book.get_row_by_status(t, 2, request.user.id) for t in table]
    # Comment: Сделал вроде историю бронирования. можно отменить. По идее надо сделать так чтобы можно 
    # было обратно забронированить просто поменять sql запрос но это уже потом(когда потом бл?).
    
    if request.method == "POST":
        table = db_book.get_all_tables()
        formated_table = format_table(request, 2, table, db_book)
        if 'id' in request.POST:
            id = request.POST.get('id')[0]
            table_name = request.POST['button-cancel']
            table_format = [list(i) for i in table[table_name]['data']]
        # if 'button-book' in request.POST:
        #     row = change_flag(table_format, id, 2, request.user.id)
        #     db_book.edit_table_row(table_format, row[0], row[1:])
        if 'button-cancel' in request.POST:
            row = change_flag(table_format, id, 0, 0)
            db_book.edit_table_row(table_name, row[0], row[1:])
        formated_table = format_table(request, 2, table, db_book)
    else:
        table = db_book.get_all_tables()
        formated_table = format_table(request, 2, table, db_book)
        
    count = 0 
    check_temp = check   
    for c in check:
        if c == []:
            count += 1     
    if count == len(check):
        check = 'no'
    else:
        check = ''    



    return render(request, 'my_booking.html', {'tables': formated_table, 'help': check_temp, 'check': check})

def create_event(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    db_book = DataBaseBooking()
    newfieds = NewField.objects.filter(created_by=request.user.id)
    choises = {}
    for field in newfieds:
        choises[field.field_name] = [f.choise for f in field.choise.all()]
    

    col_names = db_book.get_col_names(request.user.username)
    all_fields = [i.field_name for i in newfieds]   
    
    help = ''
    form_error = ''
    values = []
    if request.method == 'POST':
        for field_name in request.POST:
            # comment: Потом наверное переделать список в словарь
            value = request.POST[field_name]
            values.append(value)
        values.pop(-1)
        if values != []:
            if 'button-send' in request.POST:
                db_book.insert_info(request.user.username, values[1:])
            elif 'option' in request.POST:
                if request.POST['option'][0].isdigit():
                    if 'button-edit' in request.POST:
                        db_book.edit_table_row(request.user.username, request.POST['option'][0], values[1:-1])
                    elif 'button-del' in request.POST:
                        db_book.delete_row(request.user.username, request.POST['option'][0])
                else:
                    form_error = 'isnotdigit'
        if 'edit' in request.POST:
            help = 'working'
            for id, value in list(dict(request.POST).items())[1:-1]:
                db_book.edit_table_row(request.user, id, value[1:])
            
    # db_book.drop('user')
    if not db_book.if_table(request.user.username):  
        return render(request, 'create_event.html',{'fields': all_fields, 'help': choises})
    else:
        table = db_book.get_table_data(request.user.username)
        ids = [t[0] for t in table]
        return render(request, 'create_event.html', {'table': True, 'fields': col_names,
                                                    'data': table, 'help': request.POST,
                                                    'ids': ids, 'form_error': form_error,
                                                    'choises': choises})

def create_event_conformation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    fields = [i.field_name for i in NewField.objects.filter(created_by=request.user.id)]
    if fields:
        try:
            db_book = DataBaseBooking()
            db_book.create_table(fields, request.user.username)

            return render(request, 'create_event_conformation.html',{'message': "Успех"})
        except Exception as e:
            return render(request, 'create_event_conformation.html',{'message': e})
    else: 
        return render(request, 'create_event.html',{'fields': ['У вас нет созданных полей', 'Создайте их в административной панели']})


def change_flag(table_data, id, status_to, id_to=None):
    for item in table_data:
            if item[0] == int(id):
                item[-2] = status_to
                if id_to is not None:
                    item[-1] = id_to*(id_to >= 1)
                row = item
                break
    else:
        row = f'Item ne naiden, {id} != {[item[0] for item in table_data]}, {table_data}'
    return row 

def format_table(request, status, table, db_book):
    formated_table = []
    temp_list = []
    for t in table:
        your_rows = db_book.get_row_by_status(t, status, request.user.id)
        for d in your_rows:
            cols_and_data = dict(zip(table[t]['col_names'], d))
            temp_list.append(cols_and_data)
        table_name = {t: temp_list}
        formated_table.append(table_name)
        temp_list = []
    return formated_table 
