# NetSync-Core
High-availability synchronization engine for distributed retail databases.


### 🧠 The Logic Behind the Code

**Why use UI Automation (RPA) instead of SQL?**
I get asked this a lot. The ERP we use is a "black box." Messing directly with the SQL database is risky because you can easily bypass their internal validation logic and corrupt the data. 
- **The choice:** I used `pywinauto` to click through the actual UI. 
- **The result:** It’s safer. The system thinks a human is doing the work, so all the built-in checks stay active. No database headaches.

**Fixing the "Unfixable" Wi-Fi**
In retail, Windows sometimes just "gives up" on a Wi-Fi adapter if the signal is bad. A simple software restart doesn't always cut it.
- **The Fix:** The script uses a PowerShell command to hard-reset the wireless adapter and then simulates the `Win+A` shortcut to toggle the connection. 
- **Impact:** It solved the constant "connectivity lost" calls from the field, reducing manual intervention by more than 60%.
