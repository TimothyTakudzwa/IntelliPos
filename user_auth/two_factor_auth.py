import math, random
from django.conf import settings
from django.core.cache import cache

class OTP:
    """"Represents One-Time-Password"""
    TTL = settings.OTP_TTL
    LENGTH = settings.OTP_LENGTH
    DIGITS = settings.OTP_DIGITS

    def __init__(self, to_number):
        self.to_number = to_number


    def generate(self):
        """Generates and Stores OTP in cache"""
        code = str()
        for i in range(OTP.LENGTH): 
            code += OTP.DIGITS[math.floor(random.random() * 10)] 
        cache.set(self.to_number, code, OTP.TTL)
        return code


    def verify(self, otp):
        """Verifies OTP"""
        if cache.has_key(self.to_number):
            return cache.get(self.to_number) == otp
        else:
            return False


# Usage
# Generate
otp = OTP('0773737828').generate()
print(f'---------- OTP {otp} ------------')

# Verify
valid = OTP('0773737828').verify(otp)

print(f'---------- Valid {valid} ------------')