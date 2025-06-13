# AI Snake Game — Pathfinding Intelligence in Action

This is a self-playing Snake game fully designed and implemented by **Ghala Hazazi**, using Python and Pygame — integrating multiple pathfinding AI strategies to autonomously guide the snake towards food while avoiding collisions.

>  **All code, gameplay, logic, and algorithm  implementation were written from scratch by me, Ghala Hazazi.**  
>  **The comparison video and algorithm demo are also my original work.**  

---

##  Algorithms Implemented

| Mode Key | Algorithm | Description |
|----------|-----------|-------------|
| A        | **A\*** (astar.py) | Standard optimal pathfinding using Manhattan distance |
| S        | **Safe A\*** + Flood Fill | A* with flood-fill safety check to avoid traps |
| B        | **BFS + A\*** | Path with backup BFS to ensure space sufficiency |
| L        | **Longest Safe Path** | DFS-based path prioritizing survival over speed |
| D        | **Dynamic Mode** | AI dynamically switches between safe/risky/longest modes |
| M        | **Manual** | Player control via keyboard (for comparison) |

---

## Features

- Full game logic and graphics **written from scratch by me**  
- Real-time mode switching between AI strategies  
- Tracks **score, time, best runs** for each algorithm  
- Displays best-performing algorithm on Game Over  
- Supports dynamic difficulty adaptation and risk analysis  

---

## Controls

- `A` – A* Pathfinding  
- `S` – Safe A* + Flood Fill  
- `B` – BFS + A*  
- `L` – Longest Path  
- `D` – Dynamic AI (auto switching)  
- `M` – Manual Play (Arrow Keys)

---

## ⚠ Known Issues

- Some algorithms, such as **BFS+DFS-based strategies**, may cause excessive memory usage or performance degradation — especially on smaller grid sizes.  
  These modes are not ideal for real-time gameplay and may occasionally result in application crashes depending on the system and configuration.

- **Dynamic Mode**, while intelligent in theory, can exhibit slow or unstable behavior in maps with high obstacle density.  
  It is not currently the most reliable or recommended mode for active use.

> These modes are kept in the project for educational and comparative purposes — to observe algorithm behavior and limitations in practical environments.
---

##  Performance Tracking

Using the integrated `reviewer.py`, the game logs:
- Average Score
- Average Survival Time
- Best Runs per Mode


## Future Enhancements

- Add GUI for mode selection  
- Dynamic grid scaling  
- Smarter trap detection  
- Export performance logs as CSV


