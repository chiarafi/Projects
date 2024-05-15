#include <iostream>
#include <iomanip>
#include <string>
#include <fstream>
using namespace std;

typedef enum { Poor, Regular, Good, Extra } tQuality;

const int MaxVid = 100;

struct tVideo {
	string name;
	tQuality quality;
	int kiloBytes; // Kilobytes
};

typedef tVideo tVideoArray[MaxVid];

struct tVideoList {
	tVideoArray videos;
	int counter = 0;
};

const int MaxDisk = 20;

struct tDisk {
	string id;
	int capacity = 0; // kiloBytes
	int available = 0;
	tQuality quality = Extra;
	tVideoList videoList;
};

typedef tDisk tDiskArray[MaxDisk];

struct tStorage {
	tDiskArray disks;
	int counter = 0;
};

const string Names[4] = { "Poor", "Regular", "Good", "Extra" };

bool load(tStorage& storage); // Loads the list of disks (already provided)
bool load(tVideoList& toAllocate);
void delVideo(tVideoList& toAllocate, int index);
tVideo getNext(tVideoList& toAllocate);
int find(const tStorage& storage, tVideo video);
void assign(tStorage& storage, tVideoList& toAllocate, tVideoList& unallocated);
void display(const tVideoList& toAllocate); // Provided
void display(const tStorage& storage); // Provided
tQuality charToQuality(char qualityChar); // Provided
char qualityToChar(tQuality quality); // Provided


int main() {
	tStorage storage;
	tVideoList toAllocate, unallocated;

	if (load(storage)) {
		if (load(toAllocate)) {
			assign(storage, toAllocate, unallocated);
			display(storage);
			cout << "Videos that couldn't be stored..." << endl;
			display(unallocated);
		}
		else
			cout << "Sorry, list of videos couldn't be loaded!" << endl;
	}
	else
		cout << "Sorry, storage couldn't be loaded!" << endl;

	return 0;
}

bool load(tStorage& storage) {
	bool ok = false;
	tDisk disk;
	ifstream file;
	char qualityChar;
	string str;

	storage.counter = 0;
	file.open("disks.txt");
	if (file.is_open()) {
		ok = true;
		file >> str;
		while ((str != "XXX") && (storage.counter < MaxDisk)) {
			disk.id = str;
			file >> qualityChar;
			disk.quality = charToQuality(qualityChar);
			file >> disk.capacity;
			disk.available = disk.capacity;
			storage.disks[storage.counter] = disk;
			storage.counter++;
			file >> str;
		}
		file.close();
	}

	return ok;
}

bool load(tVideoList& toAllocate) {
	bool ok = false;
    char quality;
    string name;
    int i = 0, kb;
    ifstream file;
    file.open("videos.txt");
    if(file.is_open()) {
        ok = true;
        file >> quality;
        while(quality != 'X' && toAllocate.counter < MaxVid) {
            toAllocate.videos[i].quality = charToQuality(quality);
            file >> name >> kb;
            toAllocate.videos[i].name = name;
            toAllocate.videos[i].kiloBytes = kb;
            file >> quality;
            toAllocate.counter += 1;
            i += 1;
        } 
        file.close();
    }
	return ok;
}

void delVideo(tVideoList& list, int index) { // Deletes from the list the video in index (it do exists)...
	for(int i = index; i < MaxVid - 1; i++) {
        list.videos[i] = list.videos[i + 1];
    }
    list.counter -= 1;
}

tVideo getNext(tVideoList& toAllocate) { // Returns the biggest video... (toAllocate has videos)
	tVideo video;
    int size = 0;
    for(int i = 0; i < toAllocate.counter; i++) {
        if(toAllocate.videos[i].kiloBytes > size) {
            video = toAllocate.videos[i];
        }
    }
	return video;
}

int find(const tStorage& storage, tVideo video) { // Tries to find a suitable disk for the video...
	int disk = -1;
    int i = 0;
    while(disk == -1 && i < storage.counter) {
        if(storage.disks[i].videoList.counter < MaxVid && storage.disks[i].quality == video.quality) { // enough space? capacty noch testen?
            disk = i;
        }
    }
    return disk;
}

void assign(tStorage& storage, tVideoList& toAllocate, tVideoList& unallocated) { // Processes the list of videos to allocate...
// Returns the storage with the allocated videos, toAllocate empty and the list of unallocated
    tVideo video = getNext(toAllocate);
    int disk = find(storage, video);
    if(disk == -1) {
        if(unallocated.counter < MaxVid) {
            unallocated.videos[unallocated.counter] = video;
            unallocated.counter += 1;
        }
    } else {
        storage.disks[disk].videoList.videos[storage.disks[disk].videoList.counter] = video;
        storage.disks[disk].videoList.counter += 1;
    }
}

void display(const tVideoList& list) { // Displays the list of videos...
	for (int i = 0; i < list.counter; i++)
		cout << "     " << qualityToChar(list.videos[i].quality) << " "
		<< list.videos[i].name << " " << list.videos[i].kiloBytes << " Kbytes" << endl;
	cout << endl;
}

void display(const tStorage& storage) {
	for (int i = 0; i < storage.counter; i++) {
		cout << storage.disks[i].id << " (" << Names[storage.disks[i].quality] << " quality)"
			<< " Disk usage: " << storage.disks[i].capacity - storage.disks[i].available
			<< "/" << storage.disks[i].capacity << endl;
		display(storage.disks[i].videoList);
	}
}

tQuality charToQuality(char qualityChar) {
	tQuality quality = Poor;

	if (qualityChar == 'R')
		quality = Regular;
	else if (qualityChar == 'G')
		quality = Good;
	else if (qualityChar == 'E')
		quality = Extra;

	return quality;
}

char qualityToChar(tQuality quality) {
	char qualityChar = 'P';

	if (quality == Regular)
		qualityChar = 'R';
	else if (quality == Good)
		qualityChar = 'G';
	else if (quality == Extra)
		qualityChar = 'E';

	return qualityChar;
}
