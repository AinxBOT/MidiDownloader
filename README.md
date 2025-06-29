# 🎵 MIDI Downloader
A simple CLI tool to search and download MIDI files from [Hamienet](https://www.hamienet.com), directly via terminal.

> ✅ Built for Termux/Linux with Python  
> 🔍 Features single, multiple, and range selection downloads

---

## 📸 Screenshot

![Image](https://github.com/user-attachments/assets/20b6a464-1562-4a57-b12f-f0bf4ce835b1)

---

## ⚙️ Features

- 🔍 Search MIDI by title
- 📥 Download single or multiple tracks
- 🧠 Smart input: `1`, `1,2,3`, or `1-5`
- 📁 Auto-save to `/sdcard/midi`
- ✅ No API required

---

## 📦 Requirements

Make sure you have these installed:

```bash
pkg update && pkg upgrade
pkg install git
pkg install python
git clone https://github.com/AinxBOT/MidiDownloader
cd MidiDownloader
termux-setup-storage
pip install -r requirements.txt
python midi.py
