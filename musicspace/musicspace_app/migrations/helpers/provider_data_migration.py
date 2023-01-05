import random
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password
import lorem
from typing import List, Tuple, Optional
from pydantic import BaseModel
from enum import Enum


class PyAddress(BaseModel):
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

class PyName(BaseModel):
    given_name: str
    family_name: str

    @property
    def full_name(self) -> str:
        return f'{self.given_name} {self.family_name}'

class PyGender(str, Enum):
    MALE = 'male'
    FEMALE = 'female'
    NONBINARY = 'nonbinary'
    OTHER = 'other'

NUMBER_OF_PROVIDERS_TO_ADD = 15

GENRES = [
    ('classical', 'Classical'),
    ('pop', 'Pop'),
    ('jazz', 'Jazz'),
    ('rock', 'Rock'),
    ('r_and_b', 'Rhythm and Blues'),
    ('country', 'Country'),
]

INSTRUMENTS = [
    ('voice', 'Voice'),
    ('guitar', 'Guitar'),
    ('bass', 'Bass'),
    ('drums', 'Drums'),
    ('cello', 'Cello'),
    ('trumpet', 'Trumpet'),
    ('saxophone', 'Saxophone'),
    ('piano', 'Piano')
]

male_given_names = [
    'James',
    'Robert',
    'John',
    'Michael',
    'David',
    'William',
    'Richard',
    'Joseph',
    'Thomas',
    'Charles'
]
female_given_names = [
    'Mary',
    'Patricia',
    'Jennifer',
    'Linda',
    'Elizabeth',
    'Barbara',
    'Susan',
    'Jessica',
    'Sara',
    'Karen'
]
family_names = [
    'Smith',
    'Johnson',
    'Williams',
    'Brown',
    'Jones',
    'Garcia',
    'Miller',
    'Davis',
    'Rodriguez',
    'Martinez'
]

titles = [
    'NAFME Certified Music Teacher'
]

male_image_urls = [
    'http://rockandrollgarage.com/wp-content/uploads/2021/01/Dave-Grohl-2.jpg'
]

female_image_urls = [
    'https://media.pitchfork.com/photos/5cd4956093a5367fe31ed7d7/16:9/w_1280,c_limit/St%2520Vincent%25202009.png'
]

starting_timestamp = 1640922589
ending_timestamp = 1672458589

GENRE_DISTRIBUTION = [
    1, 1,
    2, 2, 2, 2,
    3, 3,
    4 
]

INSTRUMENT_DISTRIBUTION = [
    1, 1, 1, 1,
    2, 2, 
    3
]

PROVIDER_USER_PREFIX = 'teacher_'
DEFAULT_USER_PASSWORD = make_password('passwordabc123')

locations = [
    PyAddress(
        street_1='1 1st Ave',
        street_2='Suite 100',
        city='New York',
        state='NY',
        zip='10011'
    ),
    PyAddress(
        street_1='54 5th Ave',
        city='New York',
        state='NY',
        zip='10057'
    )
]

def generate_random_name(
    gender: PyGender
) -> PyName:
    if gender == PyGender.MALE:
        given_name_list = male_given_names
    elif gender == PyGender.FEMALE:
        given_name_list = female_given_names
    else:
        given_name_list = male_given_names + female_given_names

    return PyName(
        given_name=random.choice(given_name_list),
        family_name=random.choice(family_names)
    )

## 47.5% male, 47.5% female, 2.5% nonbinary, 2.5% other
def generate_random_gender() -> PyGender:
    value = random.random()
    if value < 0.475:
        return PyGender.MALE
    elif value < 0.95:
        return PyGender.FEMALE
    elif value < 0.975:
        return PyGender.NONBINARY
    else:
        return PyGender.OTHER

def generate_random_title() -> str:
    return random.choice(titles)

def generate_random_location() -> PyAddress:
    return random.choice(locations)

def generate_random_image_url(gender: PyGender) -> str:
    if gender == PyGender.MALE:
        image_urls = male_image_urls
    elif gender == PyGender.FEMALE:
        image_urls = female_image_urls
    else:
        image_urls = male_image_urls + female_image_urls

    return random.choice(image_urls)

def generate_random_created_date_time() -> datetime:
    timestamp = random.uniform(starting_timestamp, ending_timestamp)
    return timezone.make_aware(datetime.utcfromtimestamp(timestamp))

def generate_random_text() -> str:
    return lorem.get_paragraph()

def generate_genres() -> List[str]:
    count = random.choice(GENRE_DISTRIBUTION)
    return random.sample([pair[0] for pair in GENRES], k=count)

def generate_instruments() -> List[str]:
    count = random.choice(INSTRUMENT_DISTRIBUTION)
    return random.sample([pair[0] for pair in INSTRUMENTS], k=count)

def generate_username(index: int) -> str:
    return f'{PROVIDER_USER_PREFIX}{index}'

def generate_in_person_online() -> Tuple[bool, bool]:
    in_person_value = random.random()
    if in_person_value > 0.8:
        return (False, True)
    else:
        online_value = random.random()
        return (True, online_value <= 0.75)

def insert_genres(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Genre = apps.get_model('musicspace_app', 'Genre')
    for (id, display_text) in GENRES:
        Genre.objects.create(
            id=id,
            display_text=display_text
        )

def delete_genres(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Genre = apps.get_model('musicspace_app', 'Genre')
    Genre.objects.all().delete()

def insert_instruments(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Instrument = apps.get_model('musicspace_app', 'Instrument')
    for (id, display_text) in INSTRUMENTS:
        Instrument.objects.create(
            id=id,
            display_text=display_text
        )

def delete_instruments(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Instrument = apps.get_model('musicspace_app', 'Instrument')
    Instrument.objects.all().delete()

def insert_providers(apps, schema_editor):

    if schema_editor.connection.alias != 'default':
        return

    MusicspaceUser = apps.get_model('musicspace_app', 'MusicspaceUser')
    Address = apps.get_model('musicspace_app', 'Address')
    Provider = apps.get_model('musicspace_app', 'Provider')

    for i in range(NUMBER_OF_PROVIDERS_TO_ADD):
        username = generate_username(index=i)
        gender = generate_random_gender()
        name = generate_random_name(gender=gender)
        title = generate_random_title()
        location = generate_random_location()
        image_url = generate_random_image_url(gender=gender)
        created_date_time = generate_random_created_date_time()
        genres = generate_genres()
        instruments = generate_instruments()
        (in_person, online) = generate_in_person_online()

        text = generate_random_text()

        try:
            user = MusicspaceUser.objects.create(
                username=username,
                password=DEFAULT_USER_PASSWORD,
                first_name=name.given_name,
                last_name=name.family_name,
                date_joined=created_date_time
            )

            address = Address.objects.create(
                street_1=location.street_1,
                street_2=location.street_2 or '',
                city=location.city,
                state=location.state,
                zip=location.zip
            )

            provider = Provider.objects.create(
                user=user,
                title=title,
                text=text,
                gender=gender.value.lower(),
                location=address,
                image_url=image_url,
                in_person=in_person,
                online=online
            )

            provider.genres.add(*genres)
            provider.instruments.add(*instruments)

        except BaseException as e:
            print(f'got an exception {e}')
            raise e

def delete_providers(apps, schema_editor):
    if schema_editor.connection.alias != 'default':
        return

    Provider = apps.get_model('musicspace_app', 'Provider')

    for provider in Provider.objects.all():
        location = provider.location
        user = provider.user
        provider.delete()
        location.delete()
        user.delete()

