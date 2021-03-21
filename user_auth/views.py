

class RegisterView(RegisterView):
    def get_response_data(self, user):
        if allauth_settings.EMAIL_VERIFICATION == \
                allauth_settings.EmailVerificationMethod.MANDATORY:
            return {"detail": _("Verification e-mail sent."), "token": self.token}

        if getattr(settings, 'REST_USE_JWT', False):
            data = {
                'user': user,
                'token': self.token
            }
            logger.info('Successfully Registered User')
            return JWTSerializer(data).data
        else:
            logger.info('Successfully Registered User')
            return TokenSerializer(user.auth_token).data