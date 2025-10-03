# NIC Control Panel (Windows) — MVC

Windows 10/11 • Python 3.8+ • Tkinter • Admin (UAC)

## Run
```bash
cd nic_control_panel
python app.py
```
> The app will auto-prompt for admin via UAC.

## Structure
```
nic_control_panel/
├─ app.py
├─ controller/
│  ├─ __init__.py
│  └─ controller.py
├─ model/
│  ├─ __init__.py
│  ├─ network.py
│  └─ types.py
└─ view/
   ├─ __init__.py
   ├─ app_view.py
   └─ widgets.py
```
