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

You can run the servers either manually or via the provided helper script.

### 1. Manual start

Run the following commands from the repository root:

```bash
# install backend dependencies
pip install -r backend/requirements.txt

# start the Flask API on http://localhost:5000
python -m backend.run &

# install frontend dependencies
npm install

# serve the static pages on http://localhost:8000
cd frontend
python -m http.server 8000 &
cd ..
```

### 2. Helper script

Instead of manually running each command you can execute:

```bash
./setup_and_run.sh
```

The frontend's `api.js` module prefixes all requests with the backend URL. It
defaults to `http://localhost:5000`, but you can override this by defining a
`window.API_BASE` variable **before** loading `assets/js/api.js` when deploying
against a different backend address.

The script performs the same steps as above and launches both servers.

Once running, open `http://localhost:8000/pages/register.html` to register the
first manufacturer account or use the seeded credentials below to sign in via
`http://localhost:8000/pages/login.html`. The page will redirect to the
appropriate dashboard based on the authenticated user's role.  The backend seeds
a sample manufacturer account on first run:

  ```
  username: samplemanufacturer
  password: samplepass
  ```

## URL Health Check

To verify that both the backend API and frontend pages are reachable you can run
the helper script:

```sh
./scripts/curl_test_all.sh
```

By default it checks `http://localhost:5000` for API endpoints and
`http://localhost:8000` for frontend pages. Set the `BACKEND` or `FRONTEND`
environment variables to override the base URLs.

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
