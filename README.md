# 📘 Dersmatik

Meet **Dersmatik** — a lesson planner system designed specifically for middle school students. An admin manages the central system and creates class rooms. Students can join classes using unique codes, or simply use the app on their own.

## 📓 Lesson Agendas

Dersmatik acts as a smart notebook where students can log their daily assignments. Normally, students tend to stop keeping track over time, thinking "What’s the point?" This app solves that by making tracking easier and also supports teachers in analyzing classroom performance.

## 🚀 Usage

You can use the application in **two modes**:  
- Without Firebase (offline)  
- With Firebase (online, with cloud sync)  

It can also be used on Android devices via the **Pydroid 3** app.

### 🔑 Getting a Firebase Key

All three main program files require a Firebase key:

1. Go to [Firebase Console](https://console.firebase.google.com/u/0/) and create a new project.
2. Add a new **Web App**, give it any name, then skip the SDK configuration and proceed to the console.
3. In the left menu, under **Build**, choose **Realtime Database** and set it up as default.
4. In the database, go to the **Rules** tab and update it to:

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

5. Save the rules.
6. Go to **Project Settings** via the gear icon near Project Overview.
7. Switch to the **Service Accounts** tab.
8. Click **Generate New Private Key** to download a JSON file.
9. Copy the contents of that JSON file into the `"insert credentials here"` sections in all three program files.
10. Copy your Realtime Database **URL** and replace the `< url here >` placeholder in all three files.

💡 Need an example file? Just contact me.

## 📱 Mobile Use (Android)

1. Open your phone’s **Download** folder and create a folder called `Dersmatik`.
2. Place all the source code files inside this folder.
3. Install the **Pydroid 3** app.
4. In the app terminal, run the following command:

```bash
pip install tk firebase_admin matplotlib requests subprocess json
```

5. In each file, find the line:

```python
conn = sqlite3.connect("databases.db")
```

And replace it with:

```python
conn = sqlite3.connect("/storage/emulated/0/Download/Dersmatik/databases.db")
```

Tip: Use **ZArchiver** to create folders on Android.

## 💻 Desktop Use (Windows)

1. Install Python 3.11 (optional but recommended).
2. During installation, check **"Add Python to environment variables"** under “Customize installation.”
3. Open `cmd` and run:

```bash
pip install tk firebase_admin matplotlib requests subprocess json
```

Now you're ready to run the app!

> 💡 Ask your school’s IT department if you need help with the setup.

## 🧠 How It Works

The app consists of three main Python files:

- `dersmatik.py` – For student use: enter data, view reports, and send weekly progress.
- `admin.py` – Used by the teacher/admin to manage students and evaluations.
- `online.py` – For joining online classrooms and syncing data.

With the classroom system, admins can see how the whole class is doing and check student progress.

![Class](https://i.ibb.co/nncDmsv/resim-2024-03-02-210433626.png)

The main app helps students self-analyze and view teacher feedback. The **Send Week** feature allows them to submit progress for evaluation.

![Main](https://i.ibb.co/N9fjPj7/resim-2024-03-02-210711881.png)

## 📜 License

Dersmatik is released under the **MIT License**.  
For institutional use or support, feel free to reach out:

📧 **mefeocal455@gmail.com**
