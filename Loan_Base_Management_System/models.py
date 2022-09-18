from django.db import models
from django.contrib.auth.models import User


class userInfo(models.Model):
    FullName = models.CharField(max_length=250)
    Email = models.EmailField(max_length=250, primary_key=True)
    Username = models.CharField(max_length=250, unique=True)
    City = models.CharField(max_length=250)
    Password = models.CharField(max_length=250)
    ProfilePicture = models.ImageField(default='default.jpg', upload_to='images')

    def __str__(self):
        return f'{self.FullName, self.Email, self.Username, self.City, self.Password, self.ProfilePicture}'


class committeeInfo1(models.Model):
    id = models.AutoField(primary_key=True)
    CommitteeName = models.CharField(max_length=250)
    Price = models.IntegerField(default=0)
    StartMonth = models.DateField()
    EndMonth = models.DateField()
    PresentMember = models.IntegerField(default=1)
    TotalMember = models.IntegerField(default=1)
    Manager = models.EmailField(max_length=250)
    Start = models.BooleanField(default=False)  # Committee Started or not
    Paid = models.BooleanField(default=False)  # paid this time or not
    payment_count = models.IntegerField(default=0)  # total count of individual payments
    payment_Done = models.BooleanField(default=False)  # for Managers total payment -one time
    requested_members = models.BooleanField(default=False)  # Check for all has been requested or not
    paid_members = models.BooleanField(default=False)  # check for all paid or not
    count_per_request = models.IntegerField(default=0)  # counter per partition of committee

    def __str__(self):
        return f'{self.id, self.CommitteeName, self.Price, self.StartMonth, self.EndMonth, self.PresentMember, self.TotalMember, self.Manager}'


class committeeStore(models.Model):
    Committee_ID = models.ForeignKey(committeeInfo1, on_delete=models.CASCADE)
    Email = models.EmailField(max_length=250)
    Paid = models.BooleanField(default=False)  # paid this time or not
    payment_count = models.IntegerField(default=0)  # total count of payments
    payment_Done = models.BooleanField(default=False)  # for members total payment -one time
    Start_Committee = models.BooleanField(default=False)  # Duty
    Request_Payment = models.BooleanField(default=False)
    Winner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.Committee_ID, self.Email, self.Start_Committee, self.Request_Payment, self.Winner}'


class RequestDetail(models.Model):
    C_ID = models.ForeignKey(committeeInfo1, on_delete=models.CASCADE)
    Sender = models.CharField(max_length=250)
    Reciever = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    Paid = models.BooleanField(default=False)  # paid this time or not


class Friend(models.Model):
    users = models.ManyToManyField(userInfo)
    current_user = models.ForeignKey(userInfo, related_name='Owner', on_delete=models.CASCADE, null=True)

    @classmethod
    def add_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)
        friend.save()

    @classmethod
    def remove_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)
        friend.save()


class WinnerDetail(models.Model):
    id = models.AutoField(primary_key=True)
    C_ID = models.ForeignKey(committeeInfo1, on_delete=models.CASCADE)
    user_ID = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    Date = models.DateTimeField(('created'), auto_now_add=True)


class Transaction(models.Model):
    profile = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=120)
    committee_id = models.ForeignKey(committeeInfo1, on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    success = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.committee_id

    class Meta:
        ordering = ['-timestamp']


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    message = models.TextField()
    friend = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message
