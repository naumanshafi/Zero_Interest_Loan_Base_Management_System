from django.urls import path, include
from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
import django.views.static

urlpatterns = [

                  path('', views.Index, name='Committee-Home'),
                  path('signup/', views.SignUpUser.as_view(), name='Committee-SignUp'),
                  path('newsfeed/', views.newsfeed, name='Committee-newsfeed'),
                  path('newsfeed/search/', views.searchuser, name='Committee-search'),
                  path('JoinCommittee/(?P<Committee_ID>\d+)/', views.JoinCommittee, name='Committee-JoinCommittee'),
                  path('login/', views.SignInUser.as_view(), name='Committee-login'),
                  path('logout/', views.logout, name='Committee-logout'),
                  path('profile/', views.profile, name='Committee-profile'),
                  path('friendlist/', views.friendlist, name='Committee-friendlist'),
                  path('connect/(?P<operation>.+)/(?P<pk>\w+)/', views.change_friends,
                       name='Committee-changefriendlist'),

                  #
                  # path('Suggestion/(?P<operation>.+)/(?P<pk>\w+)/', views.change_friends1,
                  #      name='Committee-changefriendlist1'),
                  path('/Suggestion/<str:operation>/<str:pk>/', views.change_friends1,
                       name='Committee-changefriendlist1'),

                  path('post/', views.Post, name='post'),

                  path('messages/', views.Messages, name='messages'),

                  path('chat/<str:pk>/', views.chatHome,
                       name='Committee-chatwithfriend'),

                  path('FriendSuggestion/', views.friendsuggestion, name='Committee-friendsuggestion'),
                  path('modifyinfo/', views.UpdateProfile.as_view(), name='Committee-modifyinfo'),
                  path('createcommittee/', views.createcommittee, name='Committee-createcommittee'),
                  path('showcommittee/', views.showcommittee, name='Committee-showcommittee'),
                  path('Paid/(?P<Committee_ID>\d+)/', views.paid, name='Committee-paid'),
                  path('StartCommittee/(?P<Committee_ID>\d+)/', views.StartCommittee, name='Committee-StartCommittee'),
                  path('RequestPayment/(?P<Committee_ID>\d+)/', views.Request_Payment1,
                       name='Committee-RequestPayment'),
                  path('PaymentNotifications/', views.PaymentRequest,
                       name='Committee-PaymentRequest'),
                  path('winner/(?P<Committee_ID>\d+)/', views.winner, name='Committee-winner'),
                  path('ShowWinner/', views.ShowWinner, name='Committee-showwinner'),
                  path('CommitteeStarter/<str:Friend_ID>/<int:Committee_ID>', views.CommitteeStarter,
                       name='Committee-CommitteeStarter'),
                  path('CommitteeRequester/<str:Friend_ID>/<int:Committee_ID>', views.CommitteeRequester,
                       name='Committee-CommitteeRequester'),
                  path('CommitteeWinner/<str:Friend_ID>/<int:Committee_ID>', views.CommitteeWinner,
                       name='Committee-CommitteeWinner'),
                  url(r'^static/(?P<path>.*)$', django.views.static.serve,
                      {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG}),
                  path('checkout/(?P<Committee_ID>\d+)/', views.checkout, name='checkout'),
                  url(r'^update-transaction/(?P<token>[-\w]+)/$', views.update_transaction_records,
                      name='update_records'),
                  path('social-auth/', include('social_django.urls', namespace="social")),
                  path('facebook/', views.facebookData, name='Committee-Facebook'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
