from django import forms
from .models import userInfo, committeeInfo1, Friend, committeeStore, RequestDetail, WinnerDetail
from datetime import *
import datetime


class committeeStoreForm(forms.ModelForm):
    class Meta:
        model = committeeStore
        fields = {'Committee_ID', 'Email'}


class LoginForm(forms.ModelForm):
    Email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': ' Email'}))
    Password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ' Password'}))

    class Meta:
        model = userInfo
        fields = ['Email', 'Password']

    def authenticate_data(self, Email, Password):
        user = userInfo.objects.filter(Email=Email)
        if not user:
            return 1
        if len(Password) < 8:
            return 3
        user = userInfo.objects.get(Email=Email)
        if user.Password != Password:
            return 0
        return 2

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-12 col-sm-12  col-lg-12 '


class signupForm(forms.ModelForm):
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': ' Password'}))

    class Meta:
        model = userInfo
        fields = ['FullName', 'Email', 'Username', 'City', 'Password', 'ProfilePicture']

    def __init__(self, *args, **kwargs):
        super(signupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'col-md-12 col-sm-12  col-lg-12 '


def UserData(Email1):
    user = userInfo.objects.filter(Email=Email1)
    if not user:
        return False
    user = userInfo.objects.get(Email=Email1)
    return user


def CommitteeData(C_ID):
    user = committeeInfo1.objects.filter(id=C_ID)
    if not user:
        return False
    user = committeeInfo1.objects.get(id=C_ID)
    return user


class updateProfile(forms.ModelForm):
    FullName = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-xs-3', 'type': 'text', 'name': 'FullName', 'id': "ex1"}),
        label="Enter your Full Name")
    City = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-xs-3', 'type': 'text', 'name': 'City', 'id': "ex2"}),
        label="Enter your City")
    Username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control col-xs-3', 'type': 'text', 'name': 'Username', 'id': "ex3"}),
        label="Enter your User Name")
    Password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control col-xs-3 ', 'type': 'Password', 'name': 'Password', 'id': 'ex4'}),
        label="Enter Your Password")

    class Meta():
        model = userInfo
        fields = ['FullName', 'Username', 'City', 'Password', 'ProfilePicture']


class committeeInfo(forms.ModelForm):
    class Meta:
        model = committeeInfo1
        fields = ['CommitteeName', 'Price', 'StartMonth', 'EndMonth', 'PresentMember', 'TotalMember', 'Manager']


def UserCommittee(Email):
    Committees = committeeInfo1.objects.filter(Manager=Email)
    if not Committees:
        return False
    else:
        return Committees


def UserCommitteeWithoutManager(Email1):
    Committees = committeeStore.objects.filter(Email=Email1)
    return Committees


def CommitteeWithoutMe(Email1, committee):
    committees = committeeStore.objects.exclude(Email=Email1)
    if not committeeStore.objects.filter(Committee_ID=committee.id):
        return True
    for each in committees:
        if each.Committee_ID.id == committee.id:
            return True
    return False


def FriendList_Form(request, operation, pk):
    new_friend = userInfo.objects.get(Email=pk)

    if operation == 'Add Friend':
        current_user = userInfo.objects.get(Email=request.session['Email'])
        Friend.add_friend(current_user, new_friend)

    elif operation == 'Remove Friend':
        current_user = userInfo.objects.get(Email=request.session['Email'])
        Friend.remove_friend(current_user, new_friend)


def UsersExceptMe(Email):
    return userInfo.objects.exclude(Email=Email)


def MyFriends(User):
    F = Friend.objects.filter(current_user=User)
    if not F:
        return False
    else:
        return Friend.objects.get(current_user=User)


def joinCommittee1(Email1, CommitteeID1):
    obj = committeeInfo1.objects.get(id=CommitteeID1)
    Obj = committeeStore(Committee_ID=obj, Email=Email1)
    Obj.save()
    obj.PresentMember = obj.PresentMember + 1
    obj.save()


def startCommitteeForm(Committee_ID):
    Obj = committeeInfo1.objects.get(id=Committee_ID)
    if Obj.Start:
        return 0
    if datetime.date.today() < Obj.EndMonth:
        if Obj.PresentMember == Obj.TotalMember:
            Obj.Start = True
            Obj.StartMonth = datetime.date.today()
            Obj.save()
            return Obj.CommitteeName + ' with Manager ' + Obj.Manager
        else:
            return 1
    return 2


def MembersOfCommittee(Committee_ID1):
    obj = committeeStore.objects.filter(Committee_ID=Committee_ID1)
    Members = []
    for each in obj:
        Members.append(UserData(each.Email))
    return Members


def Request_Payment_Form(Email, Committee_ID1):
    Obj = committeeInfo1.objects.get(id=Committee_ID1)
    if not Obj.Start:
        return 2
    else:
        if Obj.paid_members:
            return -3
        if Obj.requested_members:
            return -2
        count = 0  # for counting paid Members
        count1 = 0  # for counting requests
        Member = MembersOfCommittee(Obj)
        Obj.requested_members = True
        Obj.save()
        if not Obj.Paid:  ##for manager
            xx = RequestDetail.objects.filter(C_ID=Obj, Sender=Email,
                                              Reciever=UserData(Obj.Manager))  ## for not requesting again
            if not xx:
                c = RequestDetail(C_ID=Obj, Sender=Email, Reciever=UserData(Obj.Manager))
                c.save()
            else:
                count1 = count1 + 1
        else:
            count = count + 1

        for each in Member:  ##for members
            x = committeeStore.objects.get(Committee_ID=Committee_ID1, Email=each.Email)
            if x.Paid:
                count = count + 1
            else:
                xx = RequestDetail.objects.filter(C_ID=Obj, Sender=Email,
                                                  Reciever=UserData(x.Email))  ## for not requesting again
                if not xx:
                    c = RequestDetail(C_ID=Obj, Sender=Email, Reciever=UserData(x.Email))
                    c.save()
                else:
                    count1 = count1 + 1

        if Obj.TotalMember == count:
            return -1

        if Obj.TotalMember == count1:
            Obj.requested_members = True
            Obj.save()
            return -2
        return 1


def winnerForm(C_ID1):
    obj = CommitteeData(C_ID1)
    if obj.paid_members:
        return -3
    if obj.requested_members == False:
        return 3
    if obj.count_per_request == obj.TotalMember:
        Members = committeeStore.objects.filter(Committee_ID=obj)
        Manager = committeeInfo1.objects.filter(id=C_ID1)
        if Manager:
            Manager = committeeInfo1.objects.get(id=C_ID1)
            if Manager.payment_Done == False:
                obj.payment_Done = True
                w = WinnerDetail(C_ID=obj, user_ID=UserData(Manager.Manager))
                w.save()
            else:
                counter = 1
                for each in Members:
                    if each.payment_Done == False:
                        each.payment_Done = True
                        w = WinnerDetail(C_ID=obj, user_ID=UserData(each.Email))
                        w.save()
                        break
                    else:
                        counter = counter + 1
                if counter == obj.TotalMember:  # for all payments done for this committee, now close comittee
                    obj.paid_members = True
                    obj.save()

            obj.Paid = False  # for manager
            obj.requested_members = False
            obj.save()
        for each in Members:
            each.Paid = False;
            each.save()
        req = RequestDetail.objects.filter(C_ID=obj)
        for each in req:
            each.delete()
        counterr = 0
        if Manager.payment_Done == True:
            counterr = counterr + 1
        for last in Members:
            if last.payment_Done == True:
                counterr = counterr + 1
        if counterr == obj.TotalMember:
            obj.paid_members = True
        obj.count_per_request = 0
        obj.save()
        Winners = WinnerDetail.objects.filter(C_ID=obj)
        return Winners
    else:
        return 0


def PaymentRequestFrom(Email1):
    Member = RequestDetail.objects.filter(Reciever=Email1)
    List = []
    if not Member:
        return 0
    else:
        for each in Member:
            if not each.Paid:
                List.append(each)
        if not List:
            return 1

        return List


def PaymentDoneForm(Committee_ID, Email1):
    obj = CommitteeData(Committee_ID)
    x = committeeInfo1.objects.filter(id=Committee_ID, Manager=Email1)
    y = committeeStore.objects.filter(Committee_ID=CommitteeData(Committee_ID), Email=Email1)
    z = RequestDetail.objects.filter(C_ID=CommitteeData(Committee_ID), Reciever=UserData(Email1))
    if x:
        obj.payment_count = obj.payment_count + 1
        obj.Paid = True
        obj.count_per_request = obj.count_per_request + 1
        obj.save()
    elif y:
        y = committeeStore.objects.get(Committee_ID=CommitteeData(Committee_ID), Email=Email1)
        y.payment_count = y.payment_count + 1
        y.Paid = True
        y.save()
        obj.count_per_request = obj.count_per_request + 1
        obj.save()
    if z:
        z = RequestDetail.objects.get(C_ID=CommitteeData(Committee_ID), Reciever=UserData(Email1))
        z.Paid = True
        z.save()


def ShowWinnerForm(Email1):
    My = UserCommittee(Email1)
    Other = UserCommitteeWithoutManager(Email1)
    List = []
    if not My and not Other:
        return 0
    if My:
        for each in My:
            x = WinnerDetail.objects.filter(C_ID=each)
            if x:
                List.append(x)
    if Other:
        for each in Other:
            x = WinnerDetail.objects.filter(C_ID=CommitteeData(each.Committee_ID.id))
            if x:
                List.append(x)
    return List


def CommitteeStarterForm(Friend_ID, Committee_ID):
    Committee = CommitteeData(Committee_ID)
    Obj = committeeStore.objects.filter(Email=Friend_ID, Committee_ID=Committee)
    if Obj[0].Start_Committee == True:
        return 0
    else:
        Obj = committeeStore.objects.get(Email=Friend_ID, Committee_ID=Committee)
        Obj.Start_Committee = True
        Obj.save()
        return 1


def CommitteeRequesterForm(Friend_ID, Committee_ID):
    Committee = CommitteeData(Committee_ID)
    Obj = committeeStore.objects.filter(Email=Friend_ID, Committee_ID=Committee)
    if Obj[0].Request_Payment == True:
        return 0
    else:
        Obj = committeeStore.objects.get(Email=Friend_ID, Committee_ID=Committee)
        Obj.Request_Payment = True
        Obj.save()
        return 1


def CommitteeWinnerForm(Friend_ID, Committee_ID):
    Committee = CommitteeData(Committee_ID)
    Obj = committeeStore.objects.filter(Email=Friend_ID, Committee_ID=Committee)
    if Obj[0].Winner == True:
        return 0
    else:
        Obj = committeeStore.objects.get(Email=Friend_ID, Committee_ID=Committee)
        Obj.Winner = True
        Obj.save()
        return 1
