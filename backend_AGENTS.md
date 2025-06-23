# **backend\_agents.md: Backend Interactions for Pharmaceutical Supply Chain Management System**

This document details the proposed backend architecture and how it will facilitate interactions between the three user roles (Manufacturer, CFA, Stockist) within the Pharmaceutical Supply Chain Management System.  At present no backend code exists in this repository; the design below serves as a blueprint for future implementation.  The intended Flask backend will act as the central hub, managing data, enforcing business rules, and controlling access via a RESTful API.

## **1\. Core Backend Principles**

* **Project Structure:** Flask backend organized as a Python package (app/) with an application factory, Blueprints for modularity (app/blueprints/auth, products, inventory, requests), app/models.py for SQLAlchemy ORM models, and app/services/ for business logic.  
* **Database:** SQLAlchemy ORM for defining models and interacting with the database.  
* **Authentication:** JWTs (JSON Web Tokens) for stateless authentication using Flask-JWT-Extended.  
* **Authorization:** Role-Based Access Control (RBAC) enforced via JWT claims and custom decorators.  
* **API Design:** RESTful principles with clear URI naming and appropriate HTTP verbs (GET, POST, PUT, PATCH, DELETE).  
* **Security:** Input validation, password hashing, HTTPS enforcement, CSP, and server-side permission checks.

## **2\. Database Models and Their Roles in Interaction**

The SQLAlchemy ORM models form the foundation of how different entities in the supply chain interact.

* **User Model:**  
  * Fields: id, username, email, password\_hash.  
  * Relationship: Linked to the Role model via role\_id.  
  * **Interaction:** Stores user credentials and links users to their specific roles, which dictates their access permissions.  
* **Role Model:**  
  * Fields: id, name (e.g., "Manufacturer", "CFA", "Stockist").  
  * **Interaction:** Defines the different access levels. All access control logic hinges on the role assigned to a user.  
* **Product Model:**  
  * Fields: id, name, description, price, manufacturer\_id (foreign key to User).  
  * **Interaction:** Manufacturers create and manage products. CFAs and Stockists view products.  
* **Inventory Model:**  
  * Fields: id, product\_id, location\_id (e.g., Stockist ID), quantity.  
  * **Interaction:** Tracks stock levels. Manufacturers directly adjust. CFAs and Stockists initiate Approval Requests to affect inventory, which are then approved by Manufacturers.  
* **Approval Request Model:**  
  * Fields: id, requester\_id (who initiated, e.g., CFA), approver\_id (e.g., Manufacturer), product\_id, action (e.g., "ship", "restock"), status (pending, approved, denied), timestamps.  
  * **Interaction:** The central model for inter-role workflow. CFAs create these; Manufacturers approve/deny.

## **3\. API Endpoints and Role-Based Access Control (RBAC)**

The backend provides distinct API endpoints for each resource, with stringent RBAC enforced on every protected route.

### **3.1. Auth Blueprint (**/auth**)**

* /auth/register **(POST):** Creates a new user. The backend must assign a default role or handle role assignment during registration based on logic.  
* /auth/login **(POST):** Authenticates a user and issues a JWT containing user\_id and role claims.  
* **Role in Interaction:** Enables all users to authenticate and receive their role token, which is crucial for subsequent authorized actions.

### **3.2. Products Blueprint (**/products**)**

* /products **(GET):** List all products.  
  * **Access:** Manufacturer, CFA, Stockist (read-only).  
  * **Interaction:** Frontend dashboards (Manufacturer, CFA, Stockist) fetch this to display product catalogs.  
* /products **(POST):** Add a new product.  
  * **Access:** Manufacturer only.  
  * **Interaction:** Manufacturer dashboard sends a POST request. Backend verifies role via JWT.  
* /products/\<id\> **(GET):** View a single product.  
  * **Access:** Manufacturer, CFA, Stockist (read-only).  
* /products/\<id\> **(PUT/PATCH/DELETE):** Update/Delete a product.  
  * **Access:** Manufacturer only.  
  * **Interaction:** Manufacturer dashboard sends these requests. Backend enforces role.

### **3.3. Inventory Blueprint (**/inventory**)**

* /inventory **(GET):** View all inventory levels.  
  * **Access:** Manufacturer, possibly System Admins (read-only). Limited access for CFAs/Stockists, potentially only to inventory relevant to them.  
  * **Interaction:** Manufacturer dashboard fetches this for stock oversight.  
* /inventory/\<id\> **(GET):** View inventory for a specific product.  
  * **Access:** Manufacturer, possibly System Admins (read-only).  
* /inventory **(POST/PUT/PATCH):** Adjust inventory levels directly.  
  * **Access:** Manufacturer only.  
  * **Interaction:** Manufacturer dashboard sends these requests. Backend directly updates Inventory model. This is distinct from requests initiated by CFAs/Stockists that need approval.

### **3.4. Requests Blueprint (**/requests**)**

This is the core for inter-role workflow, particularly between CFAs and Manufacturers.

* /requests **(GET):** List all approval requests. Can be filtered by status (e.g., ?status=pending) or requester\_id.  
  * **Access:** Manufacturer (view all requests, filter by status). CFA (view their own requests).  
  * **Interaction:** Manufacturer dashboard fetches ?status=pending to display pending approvals. CFA dashboard fetches requests where requester\_id matches their own user\_id from the JWT.  
* /requests **(POST):** Create a new approval request.  
  * **Access:** CFA (to request stock movements), possibly Stockist (to place orders that require approval).  
  * **Interaction:** CFA dashboard sends a POST request with product, quantity, action, etc. Backend creates a new Approval Request entry with status "pending" and sets requester\_id from the JWT.  
* /requests/\<id\>/approve **(PUT):** Approve a pending request.  
  * **Access:** Manufacturer only.  
  * **Interaction:** Manufacturer dashboard sends this request. Backend verifies Manufacturer role, updates Approval Request status to "approved", and **atomically** executes the requested action (e.g., updates Inventory levels).  
* /requests/\<id\>/deny **(PUT):** Deny a pending request.  
  * **Access:** Manufacturer only.  
  * **Interaction:** Manufacturer dashboard sends this request. Backend updates Approval Request status to "denied".

## **4\. Inter-User Interaction Through the Backend**

The backend acts as the intermediary and enforcer for all user interactions:

1. **CFA Initiates Action:** A CFA, logged into cfa.html, submits a request for stock transfer. The cfa.js sends a POST request to /requests. The backend creates a new Approval Request entry, linking it to the CFA (as requester\_id) and setting its status to "pending".  
2. **Manufacturer Reviews and Approves:** A Manufacturer, logged into manufacturer.html, refreshes their dashboard. manufacturer.js fetches pending requests from /requests?status=pending. The Manufacturer sees the CFA's request. Upon clicking "Approve", manufacturer.js sends a PUT request to /requests/\<id\>/approve.  
3. **Backend Executes Approved Action:** The backend receives the approval request. It verifies the Manufacturer's role. It then *atomically* updates the Approval Request status to "approved" and simultaneously modifies the Inventory (e.g., decrements stock at one location, increments at another, or updates total quantity). This atomicity is crucial for data consistency.  
4. **Status Propagation:**  
   * The CFA's dashboard (cfa.html), upon refreshing or an event-driven update, fetches its requests again. It will now see the Approval Request status as "approved" or "denied".  
   * The Manufacturer's dashboard (manufacturer.html) will no longer show the approved request as "pending" and will reflect the updated inventory.  
   * The Stockist's dashboard (stockist.html) could potentially see changes in product availability if inventory is directly impacted by these transfers, assuming the stockist's view also reflects current inventory levels.  
5. **Stockist Ordering:** A Stockist, on stockist.html, places an order. This POST request to /orders (or /requests, depending on exact workflow) would either directly update inventory (if no approval needed) or create a new Approval Request for a CFA or Manufacturer to review, completing a cycle.

## **5\. Security in Interaction**

* **Server-Side Validation:** All input data is validated and sanitized on the backend.  
* **Role Enforcement:** Every protected API endpoint explicitly checks the role claim in the JWT to ensure the requesting user has the necessary permissions. Frontend UI elements might be hidden, but backend checks are the ultimate security layer.  
* **Password Hashing:** User passwords are never stored in plaintext, only as secure hashes.  
* **Transactional Integrity:** Critical operations (like approval leading to inventory updates) are handled within database transactions to ensure data consistency.

This robust backend design ensures that all interactions between different user roles are managed securely, consistently, and according to predefined business rules, making the supply chain management system reliable.
