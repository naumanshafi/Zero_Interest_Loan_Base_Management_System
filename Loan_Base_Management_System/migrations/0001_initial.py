# Generated by Django 2.1.7 on 2019-05-23 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('friend', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='committeeInfo1',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('CommitteeName', models.CharField(max_length=250)),
                ('Price', models.IntegerField(default=0)),
                ('StartMonth', models.DateField()),
                ('EndMonth', models.DateField()),
                ('PresentMember', models.IntegerField(default=1)),
                ('TotalMember', models.IntegerField(default=1)),
                ('Manager', models.EmailField(max_length=250)),
                ('Start', models.BooleanField(default=False)),
                ('Paid', models.BooleanField(default=False)),
                ('payment_count', models.IntegerField(default=0)),
                ('payment_Done', models.BooleanField(default=False)),
                ('requested_members', models.BooleanField(default=False)),
                ('paid_members', models.BooleanField(default=False)),
                ('count_per_request', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='committeeStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Email', models.EmailField(max_length=250)),
                ('Paid', models.BooleanField(default=False)),
                ('payment_count', models.IntegerField(default=0)),
                ('payment_Done', models.BooleanField(default=False)),
                ('Start_Committee', models.BooleanField(default=False)),
                ('Request_Payment', models.BooleanField(default=False)),
                ('Winner', models.BooleanField(default=False)),
                ('Committee_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.committeeInfo1')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='RequestDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Sender', models.CharField(max_length=250)),
                ('Paid', models.BooleanField(default=False)),
                ('C_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.committeeInfo1')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=120)),
                ('amount', models.FloatField(default=0)),
                ('success', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('committee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.committeeInfo1')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='userInfo',
            fields=[
                ('FullName', models.CharField(max_length=250)),
                ('Email', models.EmailField(max_length=250, primary_key=True, serialize=False)),
                ('Username', models.CharField(max_length=250, unique=True)),
                ('City', models.CharField(max_length=250)),
                ('Password', models.CharField(max_length=250)),
                ('ProfilePicture', models.ImageField(default='default.jpg', upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='WinnerDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('C_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.committeeInfo1')),
                ('user_ID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.userInfo')),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.userInfo'),
        ),
        migrations.AddField(
            model_name='requestdetail',
            name='Reciever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.userInfo'),
        ),
        migrations.AddField(
            model_name='friend',
            name='current_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Owner', to='Committee.userInfo'),
        ),
        migrations.AddField(
            model_name='friend',
            name='users',
            field=models.ManyToManyField(to='Committee.userInfo'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Committee.userInfo'),
        ),
    ]
