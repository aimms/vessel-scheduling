# vessel-scheduling

![WebUI](https://img.shields.io/badge/UI-WebUI-success)

**Mirrored in:** https://github.com/aimms/vessel-scheduling

**How-to:** https://how-to.aimms.com/Articles/590/590-vessel-scheduling.html

## Story

In this practical example, an efficient plan is developed for delivering large cargoes using oil tankers.

The model assumes each ship can carry only one cargo at a time, and once the time horizon begins, 
all vessels head directly to the loading port. 
Upon loading, each vessel proceeds directly to the delivery location within its designated time window.

Constraints include: 
   * cargo's are loaded inside the determined time window, 
   * each cargo being transported by only one vessel, and
   * charter vessels being assigned to only one route at a time.

The objective is to minimize costs associated to combinations of cargoes and routes.

**Reference:** Gustavo Diz, Luiz Felipe Scavarda, Roger Rocha, Silvio Hamacher (2014) Decision Support System for 
PETROBRAS Ship Scheduling. Interfaces 44(6):555-566.