from django.test import TestCase
from django.test.utils import override_settings
from django.utils.encoding import force_str

from password_policies.forms import (
    PasswordPoliciesChangeForm,
    PasswordPoliciesForm,
    PasswordResetForm,
)
from password_policies.forms.fields import PasswordPoliciesField
from password_policies.tests.lib import create_password_history, create_user, passwords


class PasswordPoliciesFieldTest(TestCase):
    def test_password_field_1(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {"EUAdEHI3ES": [u"The new password must contain 1 or more symbol."]},
        )

    def test_password_field_2(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {u"4+53795": [u"The new password must contain 3 or more letters."]},
        )

    @override_settings(PASSWORD_MIN_LOWERCASE_LETTERS=1)
    def test_password_field_lowercase(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {u"CHAD+PHER9K": [u"The new password must contain 1 or more lowercase letter."]},
        )

    @override_settings(PASSWORD_MIN_UPPERCASE_LETTERS=1)
    def test_password_field_uppercase(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {u"chad+pher9k": [u"The new password must contain 1 or more uppercase letter."]},
        )

    def test_password_field_3(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {u"Chad+pherg": [u"The new password must contain 1 or more number."]},
        )

    def test_password_field_4(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {
                u"aaaa5+56dddddd": [
                    u"The new password contains consecutive characters. Only 3 consecutive characters are allowed.",
                    u"The new password is not varied enough.",
                ]
            },
        )

    def test_password_field_5(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {"Chad+pher9k": "Chad+pher9k"},
            {
                u"someone2@example.com": [
                    u"The new password is not varied enough.",
                    u"The new password is similar to an email address.",
                ]
            },
        )

    def test_password_field_6(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {u"Ch\xc4d+pher9k": u"Ch\xc4d+pher9k"},
            {
                u"\xc1\xc2\xc3\xc4\u0662\xc5\xc6": [
                    u"The new password must contain 1 or more symbol."
                ]
            },
        )

    def test_password_field_7(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {u"Ch\xc4d+pher9k": u"Ch\xc4d+pher9k"},
            {
                u"\xc1\xc2\xc3\xc4\u0662\xc5\u20ac": [
                    u"Ensure this value has at least 8 characters (it has 7)."
                ]
            },
            field_kwargs={"min_length": 8},
        )

    def test_password_field_8(self):
        self.assertFieldOutput(
            PasswordPoliciesField,
            {u"Ch\xc4d+pher9k": u"Ch\xc4d+pher9k"},
            {
                u"a": [
                    u"The new password is based on a common sequence of characters.",
                    u"The new password must contain 3 or more letters.",
                    u"The new password must contain 1 or more number.",
                    u"The new password must contain 1 or more symbol.",
                    u"The new password is not varied enough.",
                ]
            },
        )


class PasswordPoliciesFormTest(TestCase):
    def setUp(self):
        self.user = create_user()
        create_password_history(self.user)
        return super(PasswordPoliciesFormTest, self).setUp()

    def test_reused_password(self):
        data = {"new_password1": "ooDei1Hoo+Ru", "new_password2": "ooDei1Hoo+Ru"}
        form = PasswordPoliciesForm(self.user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form["new_password1"].errors,
            [force_str(form.error_messages["password_used"])],
        )

    def test_password_mismatch(self):
        data = {"new_password1": "Chah+pher9k", "new_password2": "Chah+pher8k"}
        form = PasswordPoliciesForm(self.user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form["new_password2"].errors,
            [force_str(form.error_messages["password_mismatch"])],
        )

    def test_password_verification_unicode(self):
        password = u"\xc1\u20ac\xc3\xc4\u0662\xc5\xc6\xc7"
        self.assertEqual(len(password), 8)
        data = {"new_password1": password, "new_password2": password}
        form = PasswordPoliciesForm(self.user, data)
        self.assertTrue(form.is_valid())

    def test_success(self):
        data = {"new_password1": "Chah+pher9k", "new_password2": "Chah+pher9k"}
        form = PasswordPoliciesForm(self.user, data)
        self.assertTrue(form.is_valid())


class PasswordPoliciesChangeFormTest(TestCase):
    def setUp(self):
        self.user = create_user()
        return super(PasswordPoliciesChangeFormTest, self).setUp()

    def test_password_invalid(self):
        data = {
            "old_password": "Oor0ohf4bi",
            "new_password1": "Chah+pher9k",
            "new_password2": "Chah+pher9k",
        }
        form = PasswordPoliciesChangeForm(self.user, data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form["old_password"].errors,
            [force_str(form.error_messages["password_incorrect"])],
        )
        self.assertFalse(form.is_valid())

    def test_success(self):
        data = {
            "old_password": passwords[-1],
            "new_password1": "Chah+pher9k",
            "new_password2": "Chah+pher9k",
        }
        form = PasswordPoliciesChangeForm(self.user, data)
        self.assertTrue(form.is_valid())


class PasswordResetFormTest(TestCase):
    def setUp(self):
        self.user = create_user()
        return super(PasswordResetFormTest, self).setUp()

    def test_unusable_password(self):
        self.user.set_unusable_password()
        self.user.save()
        data = {"email": self.user.email}
        form = PasswordResetForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form["email"].errors, [force_str(form.error_messages["unusable"])]
        )
        self.assertFalse(form.is_valid())

    def test_success(self):
        data = {"email": self.user.email}
        form = PasswordResetForm(data)
        self.assertTrue(form.is_valid())
