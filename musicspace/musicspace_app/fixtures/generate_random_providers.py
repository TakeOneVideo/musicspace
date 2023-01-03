import os
import sys
import uuid
import random
from datetime import datetime
import lorem
from typing import List, Tuple
## This is needed in order to reference the imports from the level above
sys.path.append(os.path.realpath('../..'))

output_file = '/src/musicspace_app/fixtures/providers.json'

from musicspace_app.models import (
    Provider, ProviderFile, 
    Name, Address, Gender, Genre, Instrument
)

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
    'NAFME Certified Music Provider'
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

locations = [
    Address(
        street_1='1 1st Ave',
        street_2='Suite 100',
        city='New York',
        state='NY',
        zip='10011'
    ),
    Address(
        street_1='54 5th Ave',
        city='New York',
        state='NY',
        zip='10057'
    )
]

def generate_random_name(
    gender: Gender
) -> Name:
    if gender == Gender.MALE:
        given_name_list = male_given_names
    elif gender == Gender.FEMALE:
        given_name_list = female_given_names
    else:
        given_name_list = male_given_names + female_given_names

    return Name(
        given_name=random.choice(given_name_list),
        family_name=random.choice(family_names)
    )
    
## 47.5% male, 47.5% female, 2.5% nonbinary, 2.5% other
def generate_random_gender() -> Gender:
    value = random.random()
    if value < 0.475:
        return Gender.MALE
    elif value < 0.95:
        return Gender.FEMALE
    elif value < 0.975:
        return Gender.NONBINARY
    else:
        return Gender.OTHER

def generate_random_title() -> str:
    return random.choice(titles)

def generate_random_location() -> Address:
    return random.choice(locations)

def generate_random_image_url(gender) -> str:
    if gender == Gender.MALE:
        image_urls = male_image_urls
    elif gender == Gender.FEMALE:
        image_urls = female_image_urls
    else:
        image_urls = male_image_urls + female_image_urls

    return random.choice(image_urls)

def generate_random_created_date_time() -> datetime:
    timestamp = random.uniform(starting_timestamp, ending_timestamp)
    return datetime.utcfromtimestamp(timestamp)

def generate_random_text() -> str:
    return lorem.get_paragraph()

def generate_genres() -> List[Genre]:
    count = random.choice(GENRE_DISTRIBUTION)
    return random.sample(list(Genre.__members__.values()), k=count)

def generate_instruments() -> List[Instrument]:
    count = random.choice(INSTRUMENT_DISTRIBUTION)
    return random.sample(list(Instrument.__members__.values()), k=count)

def generate_in_person_online() -> Tuple[bool, bool]:
    in_person_value = random.random()
    if in_person_value > 0.8:
        return (False, True)
    else:
        online_value = random.random()
        return (True, online_value <= 0.75)

def generate_random_provider() -> Provider:
    tid = uuid.uuid4()
    gender = generate_random_gender()
    # print(gender)
    name = generate_random_name(gender=gender)
    # print(name)
    title = generate_random_title()
    # print(title)
    location = generate_random_location()
    # print(location)
    image_url = generate_random_image_url(gender=gender)
    # print(image_url)
    created_date_time = generate_random_created_date_time()

    genres = generate_genres()

    instruments = generate_instruments()

    (in_person, online) = generate_in_person_online()

    text = generate_random_text()

    return Provider(
        id=tid,
        name=name,
        gender=gender,
        title=title,
        location=location,
        text=text,
        image_url=image_url,
        genres=genres,
        instruments=instruments,
        in_person=in_person,
        online=online,
        created_date_time=created_date_time
    )

providers = [generate_random_provider() for i in range(20)]
providers = sorted(providers, key=lambda provider: provider.created_date_time)

provider_file = ProviderFile(
    providers=providers
)

with open(output_file, 'w') as output_file:
    output_file.write(provider_file.json(exclude_none=True, indent=4))