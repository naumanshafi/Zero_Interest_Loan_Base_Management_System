from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from Committee import serializers
from .forms import *
from .models import *
from django.contrib import messages
from django.conf import settings
import datetime
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def Index(request):
    return render(request, 'Committee/index.html')


def PaymentRequest(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email1 = request.session.get('Email', "Unknown")
    me = UserData(Email1)
    Myrequests = PaymentRequestFrom(Email1)
    Senders = []
    Committees = []
    Price = []
    if Myrequests == 0:
        messages.error(request, 'No Payment Request Found from any Committee Manager')
        x = []
    elif Myrequests == 1:
        messages.error(request, 'You have No More Pending payment Requests')
        x = []
    else:
        for each in Myrequests:
            if each.Paid == False:
                Senders.append(UserData(each.Sender))
                n = CommitteeData(each.C_ID.id)
                Committees.append(n)
                Price.append(n.Price / n.TotalMember)
        x = zip(Committees, Senders, Price)
        if not Senders:
            x = []
    return render(request, 'Committee/PaymentRequests.html', {'Requests': x, 'MyData': me})


def paid(request, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get('Email', "Unknown")
    PaymentDoneForm(Committee_ID, Email)
    messages.error(request, 'Payment Done Successfully')
    return redirect('Committee-PaymentRequest')


def JoinCommittee(request, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email1 = request.session.get('Email', "Unknown")
    joinCommittee1(Email1, Committee_ID)
    return redirect('Committee-newsfeed')


def StartCommittee(request, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    x = startCommitteeForm(Committee_ID)
    if x == 1:
        messages.error(request, 'Committee cannot start because Members are not Complete')
    elif x == 2:
        messages.error(request, 'Current Data has been passed from End Date of Committee')
    elif x == 0:
        messages.error(request, 'Committee has already started')
    else:
        messages.error(request, 'Committee Name " ' + x + ' " has started Succesfully')
    return redirect('Committee-showcommittee')


def Request_Payment1(request, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    x = Request_Payment_Form(Email, Committee_ID)
    if x == 0:
        messages.error(request, 'Request not Send because everyone has paid Money')
    elif x == 1:
        messages.error(request, 'Request has been sent to members of committee')
    elif x == 2:
        messages.error(request, 'Kindly start this committee to request members of committee for payment')
    elif x == -1:
        messages.error(request, 'All members has been requested for Money. Wait for Payments')
    elif x == -2:
        messages.error(request, 'All members has already been Requested. Wait for payments')
    elif x == -3:
        messages.error(request, 'Committee has completed. No more Operations can be done now')
    return redirect('Committee-showcommittee')


def winner(request, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    x = winnerForm(Committee_ID)
    obj = committeeInfo1.objects.filter(id=Committee_ID)
    if x == 0:
        messages.error(request, 'All members has not paid money yet.')
    elif x == -3:
        messages.error(request, 'Committee has completed. No more Operations can be done now')
    elif x == 3:
        messages.error(request, 'Kindly request the members to pay for money')
    else:
        messages.error(request,
                       'Successfully declared the winner of Committee. Money has been transferred to his account.')
    return redirect('Committee-showcommittee')


def newsfeed(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    Friend = MyFriends(User)
    Person = []
    Show = []
    if not Friend:
        messages.error(request, 'No Friends Found')
    else:
        Friends = Friend.users.all()
        if not Friends:
            messages.error(request, 'No Friends Found')
        else:
            flag = False
            Person = []
            Show = []
            for each in Friends:
                Committees = UserCommittee(each.Email)
                if Committees:
                    for each1 in Committees:
                        if CommitteeWithoutMe(Email, each1) == True:
                            if each1.PresentMember < each1.TotalMember:
                                Show.append(each1)
                                Person.append(each)
                                flag = True
            if not flag:
                messages.error(request, 'Your Friends has No more Committees yet')
        Show.reverse()
        Person.reverse()
    zipped_list = zip(Show, Person)
    return render(request, 'Committee/newsfeed.html', {"Committees": zipped_list, "MyData": User})


def change_friends(request, operation, pk):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    FriendList_Form(request, operation, pk)
    return redirect('Committee-friendlist')


def change_friends1(request, operation, pk):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    FriendList_Form(request, operation, pk)
    return redirect('Committee-friendsuggestion')


def friendlist(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    Users = UsersExceptMe(Email)
    Friend = MyFriends(User)
    Friends = False
    if not Friend or not Users:
        return render(request, 'Committee/Friendlist.html', {'users': Users, "friends": Friends, "MyData": User})
    else:
        Friends = Friend.users.all()
        return render(request, 'Committee/Friendlist.html', {'users': Users, "friends": Friends, "MyData": User})


def profile(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    if not User:
        form = signupForm()
        login_form = LoginForm()
        return render(request, 'Committee/login.html', {'form': form, 'loginForm': login_form, "User": User})
    return render(request, 'Committee/Profile.html', {"User": User})


def friendsuggestion(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    Users = UsersExceptMe(Email)
    Friend = MyFriends(User)
    Friends = False
    Related = []
    if not Friend:
        Friend = []
    else:
        Friends = Friend.users.all()
    if not Users:
        Users = []
        messages.error(request, 'No More Users Found')
    else:
        for each in Users:
            if User.City.lower() == each.City.lower():
                Related.append(each)
    Flag = False
    for e in Related:
        if Friends:
            if e not in Friends:
                Flag = True
                break
    if not Friends:
        Flag = True
    return render(request, 'Committee/FriendSuggession.html',
                  {'users': Related, "friends": Friends, "Flag": Flag, "MyData": User})


def showcommittee(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    Committees1 = UserCommittee(Email)
    withoutManager = UserCommitteeWithoutManager(Email)
    Ruser = []
    Committees_Members = []
    Other_Committee_Members = []
    Duties = []
    if not Committees1:
        Committees1 = []
        messages.error(request, 'You have not any Committee')
    else:
        for committee in Committees1:
            Committees_Members.append(MembersOfCommittee(committee))
    zipped_list_My_Committees = zip(Committees1, Committees_Members)

    if not withoutManager:
        withoutManager = []
        messages.error(request, 'You are not registered in Friends Committees')
    else:
        for RealUser in withoutManager:
            Ruser.append(UserData(RealUser.Committee_ID.Manager))
        for R in withoutManager:
            Duties.append(R)
        for committee in withoutManager:
            x = MembersOfCommittee(committee.Committee_ID.id)
            if x:
                Other_Committee_Members.append(x)
    zipped_list = zip(withoutManager, Duties, Other_Committee_Members, Ruser)
    return render(request, 'Committee/ShowCommittee.html',
                  {"zipped_list_My_Committees": zipped_list_My_Committees, "User": User, "withoutManager": zipped_list})


class SignInUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Committee/login.html'

    def post(self, request):
        if not 'Email' in request.session:
            login_form = LoginForm(request.POST or None)
            x = login_form.authenticate_data(request.POST.get('Email'), request.POST.get('Password'))
            if x == 0:
                messages.error(request, 'Password Does not match')
            elif x == 1:
                messages.error(request, 'Email Not Found')
            elif x == 3:
                messages.error(request, 'Password length must be greater than or equal to 8 characters')
            else:
                Email = request.POST.get('Email')
                User = UserData(Email)
                serializer = serializers.LoginSerializer(User, data=request.data)
                if serializer.is_valid():
                    request.session["Email"] = Email
                    return redirect("Committee-newsfeed")
                else:
                    messages.error(request, "Authentication failed. Please try again.")
            return render(request, 'Committee/login.html', {'loginForm': login_form})
        else:
            return redirect("Committee-newsfeed")

    def get(self, request):
        if not 'Email' in request.session:
            login_form = LoginForm(request.POST or None)
            return render(request, 'Committee/login.html', {'loginForm': login_form})
        else:
            return redirect("Committee-newsfeed")


class SignUpUser(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Committee/signup.html'

    def post(self, request):
        if 'Email' in request.session:
            request.session.flush()
        form = signupForm(request.POST or None)
        if form.is_valid():
            try:
                if len(request.POST.get('Password')) < 8:
                    messages.error(request, 'Password length must be greater than or equal to 8 characters')
                    return render(request, "Committee/signup.html", {'form': form})
                else:
                    form.save()
                    user = UserData(request.POST.get('Email'))
                    serializer = serializers.SignUpSerializer(user, data=request.data)
                    if serializer.is_valid():
                        request.session["Email"] = request.POST.get("Email")
                        username = form.cleaned_data.get('Email')
                        messages.success(request, f'Account created for {username}!')
                        return redirect('Committee-newsfeed')
                    else:
                        messages.error(request, "Sorry. The information entered was invalid. Please try again.")
                        user.delete()
                        return render(request, "Committee/signup.html", {'form': form})
            except:
                messages.error(request, "An error occured. Please try again")
                return render(request, "Committee/signup.html", {'form': form})

        else:
            messages.error(request, "The information entered was invalid. Please try again")
            return render(request, "Committee/signup.html", {'form': form})

    def get(self, request):
        if 'Email' in request.session:
            request.session.flush()
        form = signupForm(request.POST or None)
        return render(request, "Committee/signup.html", {'form': form})


def createcommittee(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')

    Email = request.session.get("Email", "Unknown")
    if request.method == 'POST':
        form = committeeInfo(
            {'CommitteeName': request.POST['CommitteeName'], 'Price': request.POST['Price'],
             'StartMonth': datetime.date.today(), 'EndMonth': request.POST['EndMonth'],
             'PresentMember': 1, 'TotalMember': request.POST['TotalMember'], 'Manager': Email})
        if str(datetime.date.today()) > request.POST['EndMonth']:
            messages.success(request, f'Start Date Must be greater than End Date... Take date from now onward')
        elif (request.POST.get('Price')) < '1000':
            messages.success(request, f'Price must be greater than or equal to 1000 rupees')
        elif (request.POST.get('TotalMember')) < '2':
            messages.success(request, f'You must have atleast 2 Members for a Committee')
        else:
            if form.is_valid():
                form.save()
                messages.success(request, f'Committee has been Created Successfully')
                return redirect('Committee-createcommittee')
            else:
                messages.success(request, f'Data is not valid Kindly submit committee again')
    date = str(datetime.date.today())
    User = UserData(Email)
    return render(request, 'Committee/CreateCommittee.html', {"date": date, "MyData": User})


def logout(request):
    if 'Email' in request.session:
        request.session.flush()
    return redirect('Committee-login')


def modifyinfo(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = userInfo.objects.get(Email=Email)
    if request.method == 'POST':
        form = updateProfile(request.POST, request.FILES, instance=User)
        if form.is_valid():
            if len(request.POST.get('Password')) < 8:
                messages.error(request, 'Password length must be greater than or equal to 8 characters')
            else:
                form.save()
                messages.success(request, f'Your account has been updated')
                return redirect('Committee-modifyinfo')
        else:
            messages.success(request, f'Kindly Enter Valid Data')
    form = updateProfile(instance=User)
    context = {"signupform": form, "MyData": User}
    return render(request, 'Committee/ModifyInfo.html', context)


class UpdateProfile(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'Committee/ModifyInfo.html'

    def post(self, request):
        Email = request.session.get("Email", "Unknown")
        User = userInfo.objects.get(Email=Email)
        form = updateProfile(request.POST, request.FILES, instance=User)
        if form.is_valid():
            if len(request.POST.get('Password')) < 8:
                messages.error(request, 'Password length must be greater than or equal to 8 characters')
            else:
                serializer = serializers.UpdateUserSerialzer(User, data=request.data)
                if serializer.is_valid():
                    form.save()
                    messages.success(request, f'Your account has been updated')
                    return redirect('Committee-modifyinfo')
                else:
                    messages.error(request, "Authentication failed. Please try again")
        else:
            messages.success(request, f'Kindly Enter Valid Data')
        form = updateProfile(instance=User)
        context = {"signupform": form, "MyData": User}
        return render(request, 'Committee/ModifyInfo.html', context)

    def get(self, request):
        if not 'Email' in request.session:
            login_form = LoginForm(request.POST or None)
            return render(request, 'Committee/login.html', {'loginForm': login_form})
        else:
            Email = request.session.get("Email", "Unknown")
            User = userInfo.objects.get(Email=Email)
            form = updateProfile(instance=User)
            context = {"signupform": form, "MyData": User}
            return render(request, 'Committee/ModifyInfo.html', context)


def ShowWinner(request):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    x = ShowWinnerForm(Email)
    Whole = []
    if not x:
        messages.error(request, 'No Winner Record Found')
    else:
        Data = []
        CNames = []
        for i in range(0, len(x)):
            Name = []
            Price = []
            Date = []
            Number = []
            counter = 0
            for each in x[i]:
                counter = counter + 1
                C = each.C_ID.CommitteeName
                Name.append(each.user_ID.FullName)
                Price.append(each.C_ID.Price)
                Date.append(each.Date)
                Number.append(counter)
            CNames.append(C)
            Zipped = zip(Name, Price, Date, Number)
            Data.append(Zipped)
        if CNames and Data:
            Whole = zip(CNames, Data)
    return render(request, 'Committee/Winner.html', {'Winner': Whole, "MyData": User})


def CommitteeStarter(request, Friend_ID, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    x = CommitteeStarterForm(Friend_ID, Committee_ID)
    if x == 0:
        messages.error(request,
                       'This Member( ' + Friend_ID + ' ) of Committee is already a Sub-Manager for this Post (as Committee-Starter)')
    elif x == 1:
        messages.error(request,
                       'This Member( ' + Friend_ID + ' ) of Committee has Successfully been assigned as Sub-Manager for this Post (as Committee-Starter)')
    return redirect('Committee-showcommittee')


def CommitteeRequester(request, Friend_ID, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    x = CommitteeRequesterForm(Friend_ID, Committee_ID)
    if x == 0:
        messages.error(request,
                       'This Member( ' + Friend_ID + ' ) of Committee is already a Sub-Manager for this Post (as Committee-Requester)')
    elif x == 1:
        messages.error(request,
                       'This Member( ' + Friend_ID + ' ) of Committee has Successfully been assigned as Sub-Manager for this Post (as Committee-Requester)')
    return redirect('Committee-showcommittee')


def CommitteeWinner(request, Friend_ID, Committee_ID):
    if not 'Email' in request.session:
        return redirect('Committee-login')
    obj = UserData(Friend_ID)
    C = CommitteeData(Committee_ID)
    x = CommitteeWinnerForm(Friend_ID, Committee_ID)
    if x == 0:
        messages.error(request,
                       'This Member( ' + obj.FullName + ' ) of Committee( ' + C.CommitteeName + ' ) is already a Sub-Manager for this Post (as Committee-Winner-Computation)')
    elif x == 1:
        messages.error(request,
                       'This Member( ' + obj.FullName + ' ) of Committee( ' + C.CommitteeName + ' ) has Successfully been assigned as Sub-Manager for this Post (as Committee-Winner-Computation)')
    return redirect('Committee-showcommittee')


def facebookData(request):
    if not 'Email' in request.session:
        arr = User.objects.all()
        if arr:
            temp = []
            for x in arr:
                temp = x
            obj = userInfo(FullName=temp.first_name, Email=temp.email, Password='12345678',
                           Username=temp.first_name + temp.last_name, City='Lahore')
            obj.save()
        request.session["Email"] = temp.email
    return redirect('Committee-newsfeed')


# payment


def update_transaction_records(request, token):
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    transaction = Transaction(profile=User,
                              token=token,
                              committee_id=CommitteeData(1),
                              amount=100,
                              success=True)
    # save the transcation (otherwise doesn't exist)
    transaction.save()
    messages.info(request, "Thank you! Your purchase was successful!")
    return redirect('checkout')


def checkout(request, Committee_ID):
    instance1 = committeeInfo1.objects.get(id=str(Committee_ID))
    stripe.api_key = 'sk_test_BuWVlqbCCzax1wBbWsFfKim200N4V2C7Ar'
    if request.method == 'POST':
        token = request.POST.get('stripeToken', False)
        if token:
            try:
                charge = stripe.Charge.create(
                    amount=2000,
                    currency='usd',
                    description='Example charge',
                    source=token,
                    capture=False,
                )
                instance1 = committeeInfo1.objects.get(id=str(Committee_ID))
                messages.success(request, f'Payment Done Successfully::!')
                return redirect('Committee-PaymentRequest')
            except:
                messages.info(request, "Your card has been declined.")
    context = {
        # 'order': existing_order,
        'instance1': instance1,
        'STRIPE_PUBLISHABLE_KEY': stripe.api_key,

    }

    return render(request, 'Committee/checkout.html', context)


@csrf_exempt
def searchuser(request):
    if request.method == 'POST':
        search_text = request.POST['search_text']
    else:
        search_text = ''
        articles = userInfo.objects.none()
        articles.count = 0
        return render_to_response('Committee/ajax_search.html', {'articles': articles})
    if search_text > '':
        articles = userInfo.objects.filter(
            Q(Username__contains=search_text) | Q(City__contains=search_text) | Q(FullName__contains=search_text))
    else:
        articles = userInfo.objects.none()
    args = {}
    args.update(csrf(request))
    args = {
        'articles': articles,
    }
    return render_to_response('Committee/ajax_search.html', args)


def chatwithfriend(request, operation, pk):
    if not 'Email' in request.session:
        return render(request, 'Committee/index.html')
    FriendList_Form(request, operation, pk)
    return redirect('Committee-friendlist')


def chatHome(request, pk):
    friend = userInfo.objects.get(Email=pk)
    name = friend.Username
    request.session['fav_color'] = name
    c = Chat.objects.all()
    d = c
    d = c  # create a copy of this queryset
    object = []
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    for obj in d:
        if obj.user == User and friend.Username == obj.friend:
            object.append(obj)
        elif obj.friend == User.Username and friend == obj.user:
            object.append(obj)
    return render(request, "Committee/chathome.html", {'home': 'active', 'chat': object})


@csrf_exempt
def Post(request):
    if 'fav_color' in request.session:
        names = request.session.get('fav_color')
        Email = request.session.get("Email", "Unknown")
        User = UserData(Email)
    if request.method == "POST":
        msg = request.POST.get('msgbox')
        c = Chat(user=User, message=msg, friend=names)
        if len(msg) > 0:
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.Username})
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    friend = []
    if 'fav_color' in request.session:
        friend = request.session['fav_color']
    c = Chat.objects.all()
    Email = request.session.get("Email", "Unknown")
    User = UserData(Email)
    object = []
    for obj in c:
        if obj.user == User and friend == obj.friend:
            object.append(obj)
        elif obj.friend == User.Username and friend == obj.user.Username:
            object.append(obj)

    return render(request, 'Committee/messages.html', {'chat': object})
