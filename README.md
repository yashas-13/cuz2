# Advanced Supply Chain Management System

## Overview

This repository contains plans for an advanced, enterprise-level Supply Chain Management (SCM) system designed specifically for pharmaceutical manufacturers, Clearing & Forwarding Agents (CFAs), and stockists. The system ensures a tightly controlled in-house process flow where the Manufacturer retains authoritative oversight, with all CFA actions requiring explicit Manufacturer approval.

## Project Status

The repository now includes the initial Flask backend and a placeholder frontend structure.  Core modules, models, and routes are scaffolded, providing a working API for basic product and inventory management.  Further development will flesh out the remaining functionality.

## Key Functionalities

- **Manufacturer as Admin:**

  - Full administrative authority and audit access.
  - Approval gateway for all downstream processes initiated by CFA.
  - System-wide configuration access, including user role management, scheme setup, and batch tracking.

- **CFA (Clearing & Forwarding Agent):**

  - Role-restricted dashboard. All critical actions (stock update, dispatch) await manufacturer approval.
  - Live inventory sync with manufacturer database.
  - Order processing and logistics interface.

- **Stockists:**

  - Place and manage orders with real-time status.
  - View product availability and eligibility for offers.
  - Maintain a usage log for reorder forecasting.

## Product Catalog

| Product Name    | Description                                            |
| --------------- | ------------------------------------------------------ |
| PANSZ-DSR       | Pantoprazole 40mg + Domperidone 30mg SR (Capsules)     |
| XIMPRAZ         | Esomeprazole 40mg + Domperidone 30mg SR (Capsules)     |
| SOOKRAL SUSP    | Sucralfate 500mg + Oxetacaine 10mg Suspension (100ml)  |
| ZEKMOL 250 SUSP | Paracetamol 250mg Suspension (60ml)                    |
| ZOACE-P         | Aceclofenac 100mg + Paracetamol 325mg (Tablet)         |
| ZOACE-SP        | Aceclofenac + Paracetamol + Serratiopeptidase (Tablet) |
| CAVIZIC         | Calcium Citrate + Magnesium + Vitamin K2 + D3 etc.     |
| ZIFLOZIN        | Dapagliflozin 10mg (Tablet)                            |

## Tech Stack

### Backend

- Python REST API (Flask)
- MySQL Database via SQLAlchemy ORM
- JWT Authentication with Role-Based Access Control
- Native validation and sanitization mechanisms
- Rate limiting, retry logic, and error trace logging (file-based)

### Frontend

- HTML5, CSS, Vanilla JavaScript (modular structure)
- Chart.js for interactive analytics
- Fully responsive design optimized for mobile-first users
- LocalStorage for persisting session cache where needed
- Notification banner & snackbar system for feedback

## Repository File Structure

The project now follows the directory structure shown below.

```
supply-chain-management/
├── backend/
│   ├── app/
│   │   ├── controllers/           # Business logic and workflow control
│   │   ├── models/                # ORM Models using SQLAlchemy
│   │   ├── services/              # Reusable service layer logic
│   │   └── routes/                # HTTP route definitions
│   ├── migrations/                # Database schema migrations
│   ├── tests/                     # Unit & integration test cases
│   ├── utils/                     # Helper modules (auth, logging, etc.)
│   ├── config.py                  # Environment and DB settings
│   ├── requirements.txt           # Python dependencies
│   └── run.py                     # Application entry point
├── frontend/
│   ├── assets/
│   │   ├── css/                   # Stylesheets
│   │   ├── js/                    # Modular scripts
│   │   └── images/                # Static images and logos
│   ├── pages/
│   │   ├── manufacturer.html      # Admin interface
│   │   ├── cfa.html               # CFA dashboard
│   │   └── stockist.html          # Stockist view
│   ├── index.html
│   └── charts/
│       └── inventory.js
├── .gitignore
└── README.md
```

## Dashboard Features

### Manufacturer Dashboard (Admin)

- **Production Analytics:** Real-time manufacturing batch progress
- **Order Lifecycle Control:** Review & approve orders before CFA sees them
- **Stock Heatmaps:** Visual warehouse levels per CFA/region
- **Audit Logs:** Every action logged by time/user/device
- **Scheme & Offer Management:** Manage BOGO, discounts, etc.

### CFA Dashboard

- **Approval Gating:** Cannot dispatch without manufacturer sign-off
- **Live Dispatch Board:** Status across all active orders
- **QR Verification:** Validate physical packages before shipment
- **Task Tracker:** Daily goals for packing, checking, dispatching

### Stockist Dashboard

- **Order Cart with Auto-save:** Draft and resume
- **Smart Reorder Alerts:** Suggestions based on stock usage
- **Live Delivery Tracker:** Stage-wise update from request to delivery
- **Receipts & Order History:** Downloadable invoices & logs

## Installation and Setup

All dependencies can be installed and the development servers started with a
single helper script:

```sh
./setup_and_run.sh
```

The script installs the Python packages in `backend/`, installs the frontend
Node.js packages and then launches the Flask API on
`http://localhost:5000` and a simple static server for the frontend on
`http://localhost:8000`.

After running the script you can open `http://localhost:8000/pages/register.html`
to register the first manufacturer account.  The backend also seeds a sample
manufacturer account on first run:

  ```
  username: samplemanufacturer
  password: samplepass
  ```

## Authentication and Security

- JWT-based token validation
- Custom middleware for route-level role validation
- Token expiry and refresh pipeline
- All sensitive endpoints protected with layered access control

## Mobile-First Experience

- Tailored for mobile-first experience
- Toggle-based navigation drawer
- Toast/snackbar feedback for all interactions
- Lightweight and fast UI interactions

## Future Upgrades

- ✅ **Searchable Product Master with Barcode Generator**
- ✅ **Offline Sync with Local Storage Queue**
- 🔜 **Role-based Notification Broadcast System**
- 🔜 **Integrated BI Dashboard (Heatmaps, Forecasting, etc.)**
- 🔜 **Multi-lingual Support (starting with Hindi, Kannada)**
- 🔜 **Scheduled Order Reminders with SMS/Email**
- 🔜 **CFA Route Optimization Module (AI-driven)**
- 🔜 **Manufacturer App (Android/iOS Progressive Web App)**

## Contributing

Follow standard Git workflows:

- Fork this repository
- Create your feature branch: `git checkout -b feature/new-feature`
- Commit your changes: `git commit -am 'Add new feature'`
- Push to the branch: `git push origin feature/new-feature`
- Create a Pull Request for review

## Licensing

This project is licensed under the MIT License - see the LICENSE file for details.


## PWA Groundwork
Service worker and offline queueing added to prepare for future mobile app support.
