# Vessel Scheduling

[![Downloads](https://img.shields.io/github/downloads/aimms/vessel-scheduling/total?style=for-the-badge&logo=github&labelColor=000081&color=1847c9)](https://github.com/aimms/vessel-scheduling/releases)
![AIMMS Version](https://img.shields.io/badge/AIMMS-26.1-white?style=for-the-badge&labelColor=009B00&color=00D400)
![WebUI Version](https://img.shields.io/badge/WebUI-26.5.1.1-white?style=for-the-badge&labelColor=009B00&color=00D400)
![pyaimms Version](https://img.shields.io/badge/pyaimms-26.1.3.1-white?style=for-the-badge&labelColor=009B00&color=00D400) 
![AimmsDEX Version](https://img.shields.io/badge/AimmsDEX-26.1.9.1-white?style=for-the-badge&labelColor=009B00&color=00D400)

This repository contains a high-performance AIMMS example for **Vessel Scheduling and Route Optimization**. It demonstrates how to manage complex maritime logistics, delivering large cargoes using oil tankers while minimizing operational and spot-market costs.

## 🎯 Business Problem 

Maritime scheduling is a combinatorial challenge where the number of possible routes grows exponentially with the number of vessels and cargoes. This model solves:

* **Cost Optimization:** Minimizing the sum of operational costs, vessel idle costs, and spot-market penalties.
* **Route Generation:** Dynamically generating valid routes based on cargo loading windows and vessel availability.
* **Strategic Allocation:** Deciding whether to assign a cargo to a time-chartered vessel or leave it for the voyage-charter (spot) market.



## 📖 How to Use This Example

To get the most out of this model, including the details on route generation logic and Python integration, we highly recommend our dedicated guide:

👉 **[Read the Full Article: Vessel Scheduling](https://how-to.aimms.com/Articles/590/590-vessel-scheduling.html)**

### Prerequisites
* **AIMMS:** You will need AIMMS installed to run the model. [Download the Free Academic Edition here](https://www.aimms.com/support/licensing/).
* **Python:** Python 3.11+ is required to run the `searoute` and `pandas` integration.
* **WebUI:** This model is optimized for the AIMMS WebUI, featuring editable Gantt Charts and data-dependent CSS styling.


## 🚀 Getting Started

1.  **Download the Release:** Go to the [Releases](https://github.com/aimms/vessel-scheduling/releases) page and download the latest `.zip`.
2.  **Setup Python:** Ensure your Python environment has `searoute` and `pandas` installed.
3.  **Open the Project:** Launch the `.aimms` file.
4.  **Generate & Solve:** Use the WebUI status bar to first generate the maritime routes and then solve the mathematical optimization.

## 🤝 Support & Feedback

This example is maintained by the **AIMMS User Support Team**.
* Found an issue? [Open an issue](https://github.com/aimms/vessel-scheduling/issues).
* Questions? Reach out via the [AIMMS Community](https://community.aimms.com).

---
*Maintained by the AIMMS User Support Team. We optimize the way you build optimization.*
