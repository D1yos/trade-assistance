 PoE 2 Trade Assistant

A desktop application designed for **Path of Exile 2** players to monitor currency exchange rates, manage a local database of trades, and calculate the most profitable conversion paths using graph theory.


## Features
* **Smart Pathfinding:** Implements **Dijkstra's Algorithm** to find the most efficient exchange route between any two currencies.
* **Local Database:** Persistent storage of exchange rates using **SQLite**, featuring a secure User Authentication system (SHA-256 hashing).
* **Dynamic UI:** Modern and responsive interface built with **CustomTkinter**, featuring real-time autocomplete search.
* **Data Integrity:** Prevents calculation loops and handles complex exchange spreads (bid/ask) by allowing manual directional input.
* **External Integration:** Built-in capability to fetch and update prices from external sources (e.g., PoE.Ninja style parsers).

## Tech Stack
* **Language:** Python 3.x
* **GUI:** CustomTkinter (Modern UI)
* **Database:** SQLite3
* **Algorithms:** Dijkstra's Shortest Path (Graph Theory)
* **Security:** Hashlib (Password Encryption)


## Installation & Usage
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/poe2-trade-assistant.git](https://github.com/YOUR_USERNAME/trade-assistant.git)
    ```
2.  **Install dependencies:**
    ```bash
    pip install customtkinter
    ```
3.  **Run the application:**
    ```bash
    python gui.py
    ```

## Logic Breakdown
The core of the application treats each currency as a **Node** and each exchange rate as an **Edge** in a directed graph. 
To find the "best" rate (which is a multiplication of rates), the app converts rates into negative logarithms:
-log(rate)
This transformation allows the use of **Dijkstra's Algorithm** to find the "shortest" path, which mathematically corresponds to the highest possible conversion output.
