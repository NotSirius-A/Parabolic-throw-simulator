# Parabolic-throw-simulator

## Description
A Python app with a GUI that simulates parabolic throws based on user given variables (angle, velocity etc.).

## Notes
- All user input sanitized (only numbers, that belong to the domain are allowed, also input can be non integer).
- Opening an app will create a window, where user can enter necessary variables (SI units). Then, based on previously given variables, either a sketch can be generated ("Update Sketch" button) or a new simulation run ("Run simulation" button).
- User is able to choose whether the simulation will be run in real time or accelerated/slowed time. It is determined through the "time multiplier" variable. A Time multiplier of >1 will accelerate and <1 will slow the simulation.
- Many simulations can be run simultaneously (only one parent window needed).
- All calculations are based on Newtonian physics, while all external forces (e.g. air drag) are omitted.
- I have not encountered any problems, but the app can possibly stutter on low-end computers as computations are done very frequently (200 times per second) in order to maintain a smooth animation, therefore the app is fairly resource intensive. Also, python runs only on one CPU core, which further reduces the performance.

## Video demonstration
- https://youtu.be/-T8Okm5F4Hk
