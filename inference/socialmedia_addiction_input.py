from typing import Annotated
from pydantic import BaseModel, Field, PrivateAttr, field_validator

from enums import GenderEnum, AcademicLevelEnum, MostUsedPlatformEnum, RelantionshipStatusEnum
# from socialmedia_modeling.utils.earth_utils import country_by_ISO
import pycountry

class SocialmediaAddictionInput(BaseModel):
    age: Annotated[int, Field(ge=18, le=25)]
    gender: GenderEnum
    academic_level: AcademicLevelEnum
    country_iso: str
    avg_daily_usage_hours: Annotated[float, Field(ge=0, le=16)]
    most_used_platform: MostUsedPlatformEnum
    affects_academic_performance: bool
    sleep_hours_per_night: Annotated[float, Field(ge=3, le=10)]
    mental_health_score: Annotated[float, Field(ge=1, le=10)]
    relationship_status: RelantionshipStatusEnum
    conflicts_over_social_media: Annotated[int, Field(ge=0, le=5)]

    @property
    def affects_academic_performance_str(self):
        return "Yes" if self.affects_academic_performance else "No"
    
    _country: str = PrivateAttr(default=None)
    @property
    def country(self):
        if self._country is None:
           self._country = country_by_ISO(self.country_iso)
        return self._country

    @field_validator("country_iso")
    def validate_iso(cls, country_iso):
        country_by_ISO(country_iso)
        return country_iso
    
    def to_dict(self) -> dict:
        return {
            'Unnamed: 0': [0],
            'Student_ID': [0],
            'Age': [self.age],
            'Gender': [self.gender.value],
            'Academic_Level': [self.academic_level.value],
            'Country': [self.country],
            'Avg_Daily_Usage_Hours': [self.avg_daily_usage_hours],
            'Most_Used_Platform': [self.most_used_platform.value],
            'Affects_Academic_Performance': [self.affects_academic_performance_str],
            'Sleep_Hours_Per_Night': [self.sleep_hours_per_night],
            'Mental_Health_Score': [self.mental_health_score],
            'Relationship_Status': [self.relationship_status.value],
            'Conflicts_Over_Social_Media': [self.conflicts_over_social_media]
        }
        
def country_by_ISO(iso: str):
    try:
        country_obj = pycountry.countries.get(alpha_2=iso)
        if not country_obj:
            country_obj = pycountry.countries.get(alpha_3=iso)
        if not country_obj:
            country_obj = pycountry.countries.get(numeric=iso)
        if not country_obj:
            raise ValueError(f"Invalid ISO country code: {iso}")
        return country_obj.name
    except LookupError:
        raise ValueError(f"Invalid ISO country code: {iso}")
