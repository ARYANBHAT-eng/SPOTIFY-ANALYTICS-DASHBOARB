import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker

# Initialize Faker for generating realistic text
fake = Faker()

def generate_indian_music_dataset(num_songs=20000):
    # Popular Indian artists across different genres (expanded list)
    artists = [
        # Bollywood (expanded)
        'Arijit Singh', 'Neha Kakkar', 'Shreya Ghoshal', 'Jubin Nautiyal', 
        'Darshan Raval', 'Armaan Malik', 'Sunidhi Chauhan', 'A.R. Rahman',
        'Pritam', 'Vishal-Shekhar', 'Atif Aslam', 'KK', 'Mohit Chauhan',
        'Shaan', 'Sonu Nigam', 'Udit Narayan', 'Alka Yagnik', 'Kumar Sanu',
        'Shankar Mahadevan', 'Hariharan', 'S.P. Balasubrahmanyam', 'Sid Sriram',
        'Jonita Gandhi', 'Asees Kaur', 'Tulsi Kumar', 'Palak Muchhal',
        
        # Punjabi (expanded)
        'Diljit Dosanjh', 'AP Dhillon', 'Guru Randhawa', 'Ammy Virk',
        'Sidhu Moosewala', 'Karan Aujla', 'Babbu Maan', 'Gurdas Maan',
        'Harbhajan Mann', 'Jazzy B', 'Surjit Bindrakhia', 'Mankirt Aulakh',
        'Ninja', 'Bohemia', 'R Nait', 'Kaka',
        
        # Indie/Independent (expanded)
        'Prateek Kuhad', 'Ritviz', 'When Chai Met Toast', 'The Local Train',
        'Anuv Jain', 'Seedhe Maut', 'Kanishk Seth', 'Taba Chake',
        'Parvaaz', 'The Yellow Diary', 'Blackstratblues', 'Ankur Tewari',
        'Raghav Kaushik', 'Arjun Kanungo', 'Nucleya', 'Midival Punditz',
        
        # Regional (expanded)
        'S.P. Balasubrahmanyam', 'K.J. Yesudas', 'S. Janaki', 'Chitra',
        'K.S. Chithra', 'Sid Sriram', 'Anirudh Ravichander', 'Yuvan Shankar Raja',
        'Harris Jayaraj', 'G.V. Prakash', 'Shreya Ghoshal', 'Kailash Kher',
        'Rahat Fateh Ali Khan', 'Sukhwinder Singh', 'Richa Sharma', 'Harshdeep Kaur'
    ]
    
    # Indian music genres and subgenres (expanded)
    genres = [
        'Bollywood', 'Punjabi Pop', 'Indie Pop', 'Romantic', 'Devotional',
        'Bhajan', 'Ghazal', 'Qawwali', 'Filmi', 'Item Song', 'Patriotic',
        'Folk', 'Sufi', 'Lofi', 'Bhangra', 'Electronic', 'Hip-Hop', 'Rap',
        'Classical', 'Semi-Classical', 'Fusion', 'Rock', 'Pop Rock', 'R&B',
        'Dance', 'EDM', 'Dubstep', 'Trap', 'Indie Folk', 'Indie Rock'
    ]
    
    # Common words in Indian song titles (Hindi/English/Punjabi/Tamil/Telugu expanded)
    hindi_words = [
        'Tum', 'Mere', 'Dil', 'Pyar', 'Ishq', 'Mohabbat', 'Jaan', 'Dard',
        'Aashiqui', 'Raatan', 'Lambiyan', 'Maan', 'Pasoori', 'Chaleya', 'Kesariya',
        'Phir', 'Kabhi', 'Aaj', 'Kal', 'Hawa', 'Badal', 'Sawan', 'Barish',
        'Duniya', 'Jahan', 'Dilbar', 'Soniye', 'Rabba', 'Tere', 'Bina', 'Zindagi',
        'Yaara', 'Dosti', 'Yaad', 'Wafa', 'Intezaar', 'Aarzoo', 'Khwab', 'Sapne'
    ]
    
    english_words = [
        'Love', 'Heart', 'Dream', 'Fly', 'Sky', 'Moon', 'Star', 'Night',
        'Day', 'Time', 'Life', 'Story', 'Magic', 'Touch', 'Feel', 'Crazy',
        'Wild', 'Free', 'Fire', 'Ice', 'Rain', 'Sun', 'Light', 'Dark',
        'Angel', 'Demon', 'Heaven', 'Paradise', 'Desire', 'Passion'
    ]
    
    punjabi_words = [
        'Brown', 'Munde', 'Chak', 'De', 'Pind', 'Gaon', 'Shehar', 'Jatt',
        'Singh', 'Kaur', 'Putt', 'Jaan', 'Dil', 'Ishq', 'Mohabbat', 'Sohniye',
        'Laung', 'Gawacha', 'Koka', 'Jugni', 'Mirza', 'Heer', 'Ranja', 'Sohna'
    ]
    
    # Actual popular Indian song names to mix in (expanded list)
    popular_songs = [
        'Maan Meri Jaan', 'Pasoori Nu', 'Kesariya', 'Raatan Lambiyan', 
        'Brown Munde', 'Tum Hi Ho', 'Channa Mereya', 'Lut Gaye', 'Naatu Naatu',
        'Phir Bhi Tumko Chaahunga', 'Tere Vaaste', 'Besharam Rang', 'Aashiqui Aa Gayi',
        'Tum Se Hi', 'Ae Dil Hai Mushkil', 'Gerua', 'Janam Janam', 'Tum Prem Ho',
        'Dil Diyan Gallan', 'Tera Ban Jaunga', 'Pehla Pyaar', 'Kabira', 'Samjhawan',
        'Bulleya', 'Agar Tum Saath Ho', 'Tumhari Sulu', 'Zingaat', 'Malang', 'Garmi',
        'Dilbar', 'O Saki Saki', 'Kamariya', 'Slow Motion', 'Bekhayali', 'Ve Maahi',
        'Tujhe Kitna Chahne Lage', 'Shayad', 'Ghungroo', 'Dus Bahane', 'Muqabla',
        'Tip Tip Barsa Paani', 'Chaiyya Chaiyya', 'Dil Se Re', 'Roja Janeman', 'Tu Hi Re',
        'Tere Bina', 'Mitwa', 'Saudebaazi', 'Ilahi', 'Tere Sang Yaara'
    ]
    
    # Generate release dates (last 10 years)
    start_date = datetime.now() - timedelta(days=10*365)
    date_list = [start_date + timedelta(days=x) for x in range(0, 10*365)]
    
    # Create dataset
    data = {
        'track_id': [],
        'name': [],
        'artist': [],
        'album': [],
        'popularity': [],
        'duration_ms': [],
        'duration_min': [],
        'danceability': [],
        'energy': [],
        'key': [],
        'loudness': [],
        'mode': [],
        'speechiness': [],
        'acousticness': [],
        'instrumentalness': [],
        'liveness': [],
        'valence': [],
        'tempo': [],
        'time_signature': [],
        'explicit': [],
        'artist_genres': [],
        'release_date': [],
        'preview_url': [],
        'image_url': [],
        'language': [],
        'mood': []
    }
    
    for i in range(num_songs):
        # Track ID
        data['track_id'].append(f"spotify:track:{''.join(random.choices('0123456789abcdef', k=22))}")
        
        # Mix actual popular songs with generated ones
        if i < len(popular_songs) and random.random() < 0.2:
            name = popular_songs[i]
        else:
            # Choose language base
            lang = random.choices(['hindi', 'english', 'punjabi'], weights=[0.7, 0.2, 0.1])[0]
            if lang == 'hindi':
                name = ' '.join(random.sample(hindi_words, random.randint(1, 3)))
            elif lang == 'english':
                name = ' '.join(random.sample(english_words, random.randint(1, 3)))
            else:
                name = ' '.join(random.sample(punjabi_words, random.randint(1, 3)))
        
        data['name'].append(name)
        
        # Artist selection with some artists being more common
        artist = random.choices(artists, weights=[5 if 'Arijit' in a or 'Neha' in a else 3 if 'Diljit' in a or 'AP' in a else 1 for a in artists])[0]
        data['artist'].append(artist)
        
        # Album name (realistic sounding)
        album_words = ['Love', 'Heart', 'Dreams', 'Memories', 'Wishes', 'Desires', 
                      'Vol. 1', 'Vol. 2', 'Collection', 'Hits', 'Greatest']
        data['album'].append(f"{artist}'s {random.choice(album_words)}")
        
        # Popularity based on artist and randomness
        base_pop = 70
        if artist in ['Arijit Singh', 'Neha Kakkar', 'AP Dhillon']:
            base_pop += 15
        elif artist in ['Diljit Dosanjh', 'Shreya Ghoshal', 'A.R. Rahman']:
            base_pop += 10
        
        popularity = np.clip(np.random.normal(base_pop, 10), 30, 100)
        data['popularity'].append(int(popularity))
        
        # Duration (2.0-6.0 minutes)
        duration_min = np.round(np.random.uniform(2.0, 6.0), 2)
        duration_ms = int(duration_min * 60000)
        data['duration_ms'].append(duration_ms)
        data['duration_min'].append(duration_min)
        
        # Genre selection based on artist
        if 'Arijit' in artist or 'Neha' in artist:
            genre = random.choice(['Bollywood', 'Romantic', 'Filmi'])
            language = 'Hindi'
        elif 'Diljit' in artist or 'AP' in artist:
            genre = random.choice(['Punjabi Pop', 'Bhangra', 'Hip-Hop'])
            language = 'Punjabi'
        elif 'Shreya' in artist or 'Sonu' in artist:
            genre = random.choice(['Bollywood', 'Classical', 'Semi-Classical'])
            language = 'Hindi'
        else:
            genre = random.choice(genres)
            language = random.choice(['Hindi', 'English', 'Punjabi', 'Tamil', 'Telugu'])
        
        data['language'].append(language)
        data['artist_genres'].append(f"{genre}, {random.choice(genres)}")
        
        # Audio features with realistic distributions
        # Danceability (0-1)
        if genre in ['Bhangra', 'Dance', 'EDM']:
            danceability = np.clip(np.random.normal(0.8, 0.1), 0.1, 0.99)
        elif genre in ['Bhajan', 'Ghazal']:
            danceability = np.clip(np.random.normal(0.4, 0.15), 0.1, 0.99)
        else:
            danceability = np.clip(np.random.normal(0.7, 0.15), 0.1, 0.99)
        data['danceability'].append(round(danceability, 3))
        
        # Energy (0-1)
        if genre in ['Bhangra', 'Rock', 'EDM']:
            energy = np.clip(np.random.normal(0.85, 0.1), 0.1, 0.99)
        elif genre in ['Ghazal', 'Bhajan']:
            energy = np.clip(np.random.normal(0.4, 0.15), 0.1, 0.99)
        else:
            energy = np.clip(np.random.normal(0.7, 0.15), 0.1, 0.99)
        data['energy'].append(round(energy, 3))
        
        # Key (0-11)
        data['key'].append(random.randint(0, 11))
        
        # Loudness (-60 to 0 dB)
        data['loudness'].append(round(np.random.uniform(-20, -5), 1))
        
        # Mode (0=Minor, 1=Major)
        data['mode'].append(random.randint(0, 1))
        
        # Speechiness (0-1)
        if genre in ['Rap', 'Hip-Hop']:
            speechiness = np.clip(np.random.normal(0.2, 0.05), 0.02, 0.3)
        else:
            speechiness = np.clip(np.random.normal(0.06, 0.03), 0.02, 0.3)
        data['speechiness'].append(round(speechiness, 3))
        
        # Acousticness (0-1)
        if genre in ['Ghazal', 'Bhajan', 'Classical']:
            acousticness = np.clip(np.random.normal(0.85, 0.1), 0.1, 0.99)
        elif genre in ['EDM', 'Dance']:
            acousticness = np.clip(np.random.normal(0.15, 0.1), 0.01, 0.99)
        else:
            acousticness = np.clip(np.random.normal(0.4, 0.2), 0.01, 0.99)
        data['acousticness'].append(round(acousticness, 3))
        
        # Instrumentalness (0-1)
        if genre in ['Classical', 'Instrumental']:
            instrumentalness = np.clip(np.random.normal(0.8, 0.15), 0.1, 0.99)
        else:
            instrumentalness = np.clip(np.random.normal(0.05, 0.03), 0, 0.99)
        data['instrumentalness'].append(round(instrumentalness, 3))
        
        # Liveness (0-1)
        data['liveness'].append(round(np.clip(np.random.normal(0.2, 0.1), 0.01, 0.99), 3))
        
        # Valence (0-1)
        if genre in ['Romantic', 'Bhangra']:
            valence = np.clip(np.random.normal(0.8, 0.1), 0.1, 0.99)
        elif genre in ['Ghazal', 'Sad']:
            valence = np.clip(np.random.normal(0.3, 0.1), 0.1, 0.99)
        else:
            valence = np.clip(np.random.normal(0.6, 0.15), 0.1, 0.99)
        data['valence'].append(round(valence, 3))
        
        # Tempo (60-200 BPM)
        if genre in ['Bhangra', 'Dance']:
            tempo = np.clip(np.random.normal(130, 15), 100, 200)
        elif genre in ['Ghazal', 'Classical']:
            tempo = np.clip(np.random.normal(80, 10), 60, 100)
        else:
            tempo = np.clip(np.random.normal(120, 20), 60, 200)
        data['tempo'].append(round(tempo, 1))
        
        # Time signature (3, 4, or 6)
        data['time_signature'].append(random.choice([3, 4, 6]))
        
        # Explicit content (15% chance)
        data['explicit'].append(random.random() < 0.15)
        
        # Release date
        release_date = random.choice(date_list).strftime('%Y-%m-%d')
        data['release_date'].append(release_date)
        
        # Preview URL (20% chance of having one)
        data['preview_url'].append(f"https://example.com/preview/{i}" if random.random() < 0.2 else None)
        
        # Image URL (album art)
        data['image_url'].append(f"https://picsum.photos/300/300?random={i}")
        
        # Mood based on valence
        if valence > 0.7:
            mood = 'Happy/Energetic'
        elif valence < 0.3:
            mood = 'Sad/Calm'
        else:
            mood = 'Neutral'
        data['mood'].append(mood)
    
    return pd.DataFrame(data)

# Generate and save dataset
print("Generating 20,000 Indian songs dataset...")
indian_music_df = generate_indian_music_dataset(20000)

# Save to CSV with proper encoding
indian_music_df.to_csv('indian_music_20k.csv', index=False, encoding='utf-8')
print("Dataset saved as 'indian_music_20k.csv'")
print(f"Total songs generated: {len(indian_music_df)}")
print("Columns included:", indian_music_df.columns.tolist())