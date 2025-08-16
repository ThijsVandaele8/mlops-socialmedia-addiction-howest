from enum import Enum

class AcademicLevelEnum(str, Enum):
    undergraduate = "Undergraduate"
    graduate = "Graduate"
    high_school = "High School"
    
class GenderEnum(str, Enum):
    female = "Female"
    male = "Male"
    
class MostUsedPlatformEnum(str, Enum):
    instagram = "Instagram"
    tiktok = "TikTok"
    facebook = "Facebook"
    whatsapp = "WhatsApp"
    twitter = "Twitter"
    other = "Other"
    
class RelantionshipStatusEnum(str, Enum):
    single = "Single",
    in_relationship = "In Relationship",
    complicated = "Complicated"
    