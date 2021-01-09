"""Вариант 9, Задача 1:Взять любую предметную область, выделить 3 сущности и описать 3 пользовательских класса. Определить для них
конструктор с параметрами; метод, возвращающий строковое представление объекта; 2–3 операции (сложение, вычитание,
умножение, деление, сравнение и т.п.).
Создать несколько экземпляров разных классов, осуществить различные операции с
ними, отобразить результаты на экране. Учесть возможные исключительные ситуации (тщательно протестировать программу).

Краткая информация о созданных классах:

    Сущность исполнитель:
        содержит поля:
            Имя исполнителя
            Жанр
            Список альбомов

    Сущность плэйлист:
        содержит поля:
            Название
            Трэки

    Сущность альбом (расширяет плэйлист):
        содержит поля:
            Дата записи
            Исполнитель

    Сущность трэк
        содержит поля:
            Название
            Продолжительность
            Альбом
            Исполнитель
"""
from enum import Enum
import datetime


class Genre(Enum):
    Rock = "Рок"
    Pop = "Поп"
    Classic = "Классика"


class Artist:
    def __init__(self, name: str, genre: Genre):
        if not isinstance(genre, Genre):
            raise Exception('Необходимо указывать жанр класса Genre')
        self.__name = name
        self.__genre = genre
        self.__albums = []

    def __str__(self):
        s = f"Исполнитель: {self.getName()} в жанре: {self.getGenre()}"
        if len(self.getAlbums()) > 0:
            s = s + ", имеет следующие альбомы:"
            for i in range(len(self.getAlbums())):
                s = s + f"\n {i + 1}. {self.getAlbums()[i].getTitle()}, {self.getAlbums()[i].getReleaseDate()}"

        return s

    def getName(self):
        return self.__name

    def getGenre(self):
        return self.__genre.value

    def getAlbums(self):
        return self.__albums

    def addAlbum(self, album):
        if isinstance(album, Album):
            if album not in self.getAlbums():
                self.__albums.append(album)
                album.setArtist(self)
        else:
            raise Exception(f'Нельзя добавить к объекту класса Album объект класса {album.__class__.__name__}')

    def removeAlbum(self, album):
        if isinstance(album, Album) and album in self.getAlbums():
            self.__albums = list(filter(lambda a: a != album, self.getAlbums()))
            if album not in self.getAlbums():
                self.__albums.append(album)
                album.setArtist(self)

    def removeAlbumByIndex(self, index):
        if isinstance(index, int):
            del self.getAlbums()[index - 1]


class Playlist:
    def __init__(self, title=f"New playlist, created at {datetime.date.today()}", tracks=None):
        if tracks is None or not isinstance(tracks, list):
            if isinstance(tracks, Track):
                tracks = [tracks]
            else:
                tracks = []
        self.__title = title
        self.__tracks = tracks

    def getTitle(self):
        return self.__title

    def getTracks(self):
        return self.__tracks

    def addTrack(self, added_track):
        if isinstance(added_track, Track):
            self.__tracks.append(added_track)
        elif isinstance(added_track, Playlist):
            self.__tracks = self.getTracks() + added_track.getTracks()

    def removeTrack(self, track):
        self.__tracks = list(filter(lambda a: a != track, self.getTracks()))

    def __add__(self, other):
        self.addTrack(other)

    def __sub__(self, other):
        self.removeTrack(other)

    def removeTrackByIndex(self, index):
        if isinstance(index, int):
            del self.getTracks()[index - 1]

    def __str__(self):
        s = f"Плэйлист \"{self.getTitle()}\""
        if len(self.getTracks()) > 0:
            s = self.__addTracksToStr__(s)
        else:
            s = s + " не содержит трэков."
        return s

    def __addTracksToStr__(self, text):
        text = text + ", содержит следующие трэки:"
        for i in range(len(self.getTracks())):
            currentTrack = self.getTracks()[i]
            author = currentTrack.getArtist().getName() if isinstance(currentTrack.getArtist(),
                                                                      Artist) else currentTrack.getArtist()
            title = currentTrack.getTitle()
            duration = currentTrack.getDuration()
            text = text + f"\n {i + 1}. {author} - {title} - {duration} сек"

        return text


class Album(Playlist):
    def __init__(self, title: str, release_date: datetime, artist, tracks=None):
        if not isinstance(artist, Artist):
            raise Exception('Album artist must be "Artist" object')
        if not isinstance(release_date, datetime.date):
            raise Exception('Album release_date must be "datetime" object')
        super(Album, self).__init__(title, tracks)
        self.__title = title
        self.__release_date = release_date
        self.__artist = artist
        artist.addAlbum(self)

    def getReleaseDate(self):
        return self.__release_date

    def getArtist(self):
        return self.__artist

    def addTrack(self, track):
        if isinstance(track, Track) and track not in self.getTracks():
            track.setArtist(self.getArtist())
            self.getTracks().append(track)

    def setArtist(self, artist: Artist):
        if self.__artist != artist and isinstance(artist, Artist):
            self.__artist = artist
            artist.addAlbum(self)

    def __str__(self):
        s = f"Альбом \"{self.getTitle()}\", исполнителя \"{self.getArtist().getName()}\" записан: {self.getReleaseDate()}"
        if len(self.getTracks()) > 0:
            s = self.__addTracksToStr__(s)
        return s

    def __addTracksToStr__(self, text):
        text = text + ", содержит следующие трэки:"
        for i in range(len(self.getTracks())):
            current_track = self.getTracks()[i]
            title = current_track.getTitle()
            duration = current_track.getDuration()
            text = text + f"\n {i + 1}. {title} - {duration} сек"

        return text


class Track:
    def __init__(self, title: str, duration: int, album=None, artist=None):
        self.__title = title
        self.__duration = duration if isinstance(duration, int) else 0
        self.__album = album if isinstance(album, Album) else None
        self.__artist = artist if isinstance(artist, Artist) else None
        if isinstance(album, Album):
            album.addTrack(self)
            self.__artist = album.getArtist()

    def getTitle(self):
        return self.__title

    def getDuration(self):
        return self.__duration

    def getAlbum(self):
        return self.__album if self.__album is not None else "Без альбома"

    def setAlbum(self, album):
        if isinstance(album, Album):
            album.addTrack(self)
            self.__artist = album.getArtist()
            self.__album = album

    def getArtist(self):
        return self.__artist if self.__artist is not None else "Неизвестный исполнитель"

    def setArtist(self, artist):
        self.__artist = artist if isinstance(artist, Artist) else None

    def getInfo(self):
        artist_name = self.getArtist().getName() if isinstance(self.getArtist(), Artist) else self.getArtist()
        s = f"Композиция: \"{self.getTitle()}\", исполняется \"{artist_name}\" продолжительностью: {self.getDuration()} секунд "
        if self.__album:
            s = s + f" из альбома \"{self.__album.getTitle()}\""
        return s

    def __str__(self):
        return self.getInfo()

    def __add__(self, other):
        return Playlist(tracks=[self, other])


print("\tСоздадим несколько исполнителей и выведем их на экран:")
pinkFloyd = Artist("Pink Floyd", Genre.Rock)
beatles = Artist("Beatles", Genre.Rock)
justinBieber = Artist("Justin Bieber", Genre.Pop)
print(pinkFloyd)
print(beatles)
print(justinBieber)
print("=============================================================")
print("\tСоздадим несколько альбомов и выведем их на экран:")
album1 = Album("The Piper at the Gates of Dawn", datetime.date(1967, 8, 5), pinkFloyd)
album2 = Album("The Dark Side of the Moon", datetime.date(1973, 3, 10), pinkFloyd)
album3 = Album("Sgt. Pepper’s Lonely Hearts Club Band", datetime.date(1967, 6, 1), beatles)
album4 = Album("Believe", datetime.date(2012, 6, 19), justinBieber)
print(album1)
print(album2)
print(album3)
print(album4)
print("=============================================================")

print("\tСоздадим несколько трэков и выведем их на экран:")
print("\tПолностью заполненные при создании объекты:")
track1 = Track("Astronomy Domine", 252, album1, pinkFloyd)
track2 = Track("Lucifer Sam", 307, album1, pinkFloyd)
track3 = Track("Interstellar Overdrive", 581, album1, pinkFloyd)
track4 = Track("A Day in the Life", 337, album3, beatles)
print(track1)
print(track2)
print(track3)
print(track4)
print("\tЧастично заполненные при создании объекты:")
track5 = Track("Lovely Rita", 182, artist=beatles)
track6 = Track("Speak to Me", 150)
track7 = Track("All Around the World", 360)
print(track5)
print(track6)
print(track7)
print("\tКак видим трэки, где мы не указывали альбомы и исполнителей, отображаются как трэки Неизвестного исполнителя.")
print("=============================================================")
print("\tПоскольку при добавлении трэков мы указывали альбом, трэки привязались к этому альбому и теперь, "
      "если мы распечатаем информацию об альбоме, то увидим их там:")
print(album1)
print("=============================================================")
print("\tСоздадим плэйлист и выведим на экран:")
playlist1 = Playlist("Самые крутые песни")
print(playlist1)
print("\tДобавим в него песен и опять выведим на экран:")
# Различные способы добавления в плэйлист
playlist1.addTrack(track1)  # Способ 1
playlist1 + track7  # Способ 2
playlist1 + Playlist(tracks=[track2, track3, track4, track5, track6])  # Способ 3
print(playlist1)
print("\tУдалим некоторые трэки из него выведим на экран:")
playlist1.removeTrackByIndex(3)  # Удаление по индексу
playlist1.removeTrack(track4)  # Удаление по значению
print(playlist1)
print("=============================================================")
print("\tЗаполним неизвестные части трэков и добавим их по альбомам и выведим итоговый результат наших манипуляций")
album2.addTrack(track6)
album3.addTrack(track4)  # Вариант 1 присвоения альбома
track5.setAlbum(album3)  # Вариант 2 присвоения альбома
album4.addTrack(track7)
print("\n========================ИСПОЛНИТЕЛИ=========================")
print(pinkFloyd)
print(beatles)
print(justinBieber)
print("\n==========================АЛЬБОМЫ===========================")
print(album1)
print(album2)
print(album3)
print(album4)
print("\n=========================ПЛЭЙЛИСТЫ==========================")
print(playlist1)