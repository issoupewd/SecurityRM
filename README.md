
# **FSM Key Generator (LFSR-based)**

A small tool for generating keystreams using **3 LFSRs** and an **alternating-step FSM**.

<p align="center">
  <img src="arch.png" width="1000" />
</p>

All calculations are performed **entirely in the Python backend**.

---

## **🔐 What It Does**

* Configure **R1, R2, R3**:

  * Initial state (bit buttons)
  * Tap positions (S0, S1, S2…)
* Backend generates for each register:
  ✔ Output sequence
  ✔ Practical period
  ✔ Theoretical period
  ✔ Full state table
* Runs the **FSM keystream generator** (alternating-step controlled by R1)
* Export FSM output to **CSV**


---

## **📥 Clone the Repository**

```bash
git clone https://github.com/issoupewd/SecurityRM
cd SecurityRM
```

---

## **🌐 Frontend Setup**

### **Linux **

```bash
npm install react@18.2.0 react-dom@18.2.0 @types/react@18 @types/react-dom@18
npm install
ls -l node_modules/.bin/next
npm run dev
```

### **Windows (PowerShell / CMD)**

```powershell
npm install react@18.2.0 react-dom@18.2.0 @types/react@18 @types/react-dom@18
npm install
dir node_modules\.bin\next.cmd
npm run dev
```

Frontend runs at:
**[http://localhost:3000](http://localhost:3000)**

<p align="center">
  <img src="site.png" width="700" />
</p>

---

## **🧠 Backend Setup (Python + Flask)**

### **Linux **

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

### **Windows (PowerShell / CMD)**

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Backend runs at:
**[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---
