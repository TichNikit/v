@app.get("/rating_entry")
async def rating_entry(request: Request):
    return templates.TemplateResponse("rating_entry.html", {"request": request})


@app.post("/check_rating_entry")
async def check_rating_entry(request: Request, db: Annotated[Session, Depends(get_db)], username: str = Form(...),
                     password: str = Form(...), user_id: int = Form(...)) -> HTMLResponse:

    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        error = 'Пользователь не найден -_-\nПопробуйте снова'
        return templates.TemplateResponse('rating_entry.html', {"request": request, 'error': error})

    if username == user.username and password == user.password and user_id == user.id:
        global global_user
        global_user = user
        print(global_user.id)
        return templates.TemplateResponse('rating.html', {"request": request})
    else:
        error = 'Что-то пошло не так ((\nПопробуйте снова'
        return templates.TemplateResponse('rating_entry.html', {"request": request, 'error': error})


@app.get("/rating")
async def rating(request: Request):
    return templates.TemplateResponse("rating.html", {"request": request})


@app.post("/rating_finish")
async def rating_finish(request: Request, db: Annotated[Session, Depends(get_db)], rating_int: int = Form(...),
                   game_id: int = Form(...)) -> HTMLResponse:
    if global_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authenticated")
    user_id = global_user.id

    game = db.scalar(select(Game).where(Game.id == game_id))
    if game is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="GAME NOT FOUND")



def regist_user(request):

    users = User.objects.all()
    users_list = [user.username for user in users]


    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')

        context = {
            'username': username,
        }

        if username not in users_list:
            User.objects.create(username=username, firstname=firstname,lastname=lastname,password=password)
            return render(request, 'welcome_user.html', context=context)
        else:
            return HttpResponse(f'Логин уже занят((( Попробуйте другой')
    return render(request, 'regist_user.html')