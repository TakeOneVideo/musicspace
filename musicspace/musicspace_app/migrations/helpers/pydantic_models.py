from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional, List
import uuid

class Genre(str, Enum):
    CLASSICAL = 'Classical'
    JAZZ = 'Jazz'
    POP = 'Pop'
    ROCK = 'Rock'
    R_AND_B = 'Rhythm and Blues'
    COUNTRY = 'Country'

class Instrument(str, Enum):
    VOICE = 'Voice'
    GUITAR = 'Guitar'
    BASS = 'Bass'
    DRUMS = 'Drums'
    CELLO = 'Cello'
    TRUMPET = 'Trumpet'
    SAXOPHONE = 'Saxophone'

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
class PyProvider(BaseModel):
    id: uuid.UUID
    username: str
    name: Name
    gender: Gender
    title: str
    location: Address
    text: str
    image_url: str
    genres: List[Genre]
    instruments: List[Instrument]
    in_person: bool
    online: bool
    created_date_time: datetime

    @property
    def truncated_text(self) -> str:
        if len(self.text) > 100:
            return self.text[:100] + '...' 
        else:
            return self.text

class ProviderFile(BaseModel):
    providers: List[PyProvider]