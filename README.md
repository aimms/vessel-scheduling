# vessel-scheduling

![WebUI](https://img.shields.io/badge/UI-WebUI-success)

**Mirrored in:** https://github.com/aimms/vessel-scheduling

**How-to:** https://how-to.aimms.com/Articles/590/590-vessel-scheduling.html

## Story

In this practical example, an efficient plan is developed for delivering oil tankers already coupled with cargoes. Prior to optimization, all possible routes are generated following data import. Route creation considers each cargo's loading window to ensure timely delivery. Subsequently, each cargo is assigned to either a time-chartered or voyage-chartered vessel within the model. The objective is to minimize costs for combinations of cargoes and routes.

The model operates under several assumptions and constraints. It assumes each ship can carry only one cargo at a time and that all vessels head directly to the loading port once the time horizon begins. Constraints include: each cargo being transported by only one vessel, and charter vessels being assigned to only one route at a time.


**Reference**
Gustavo Diz, Luiz Felipe Scavarda, Roger Rocha, Silvio Hamacher (2014) Decision Support System for PETROBRAS Ship Scheduling. Interfaces 44(6):555-566.