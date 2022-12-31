from django.db import models
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum

class Address(BaseModel):
    street_1: str
    street_2: Optional[str]
    city: str
    state: str
    zip: str

    @property
    def short(self) -> str:
        return f'{self.city}, {self.state}'

    @property
    def full(self) -> str:
        lines = []
        lines.append(self.street_1)
        if self.street_2:
            lines.append(self.street_2)
        lines.append(f'{self.city}, {self.state} {self.zip}')

        return '\n'.join(lines)

class Name(BaseModel):
    given_name: str
    family_name: str

    @property
    def full_name(self) -> str:
        return f'{self.given_name} {self.family_name}'

class Gender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'
    OTHER = 'other'

# Create your models here.
class Provider(BaseModel):
    id: UUID
    name: Name
    gender: Gender
    title: str
    location: Address
    text: str
    image_url: str
    created_date_time: datetime

    @property
    def truncated_text(self) -> str:
        if len(self.text) > 100:
            return self.text[:100] + '...' 
        else:
            return self.text

class ProviderFile(BaseModel):
    providers: List[Provider]
    
