from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, Assign_role, create_group, view_group_list_with_permission, Sign_In, User_Profile, Change_Password, PasswordReset, Confirm_Reset_Password, Update_Profile
from django.contrib.auth.views import LogoutView, PasswordChangeDoneView

urlpatterns = [

    path("sign_up/", sign_up, name="sign_up"),
    # path("sign_in/", sign_in, name="sign_in"),
    path("sign_in/", Sign_In.as_view(), name="sign_in"),
    # path("sign_out/", sign_out, name="sign_out"),
    path("sign_out/", LogoutView.as_view(), name="sign_out"),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin/dashboard/", admin_dashboard, name="admin_dashboard"),
    path("admin/<int:user_id>/assign_role/", Assign_role, name="assign_role"),
    path("admin/create_group/", create_group, name="create_group"),
    path("admin/view_group_list_with_permission/", view_group_list_with_permission, name="view_group"),
    path("profile/", User_Profile.as_view(), name="user_profile"),
    path("change_password/", Change_Password.as_view(), name="change_password"),
    path("password_changed/done/", PasswordChangeDoneView.as_view(template_name="accounts/password_changed_done.html"), name="password_change_done"),
    path("password_reset/", PasswordReset.as_view(), name="reset_password"),
    path("password_reset/confirm/<uidb64>/<token>/", Confirm_Reset_Password.as_view(), name="password_reset_confirm"),
    path("edit_profile/", Update_Profile.as_view(), name="edit_profile")

]
