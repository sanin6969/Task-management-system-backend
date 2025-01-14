# Task-management-system-backend


## Overview

This project is a **Task Management System** developed using **Django REST Framework** for the backend and **React Vite** with **TanStack Query** for the frontend. It implements JWT authentication for secure user login and provides role-based features for Admin and Users. The system allows task assignment, tracking, and status updates while maintaining a clean and user-friendly interface with **Tailwind CSS** and  **Material-UI** .


## Features

### 1. **Authentication**

* **JWT Authentication** :
* Secure login using access and refresh tokens.
* Custom claims included in JWT tokens (username, email, is_superuser).
* **User Registration** :
* Validation for unique usernames and emails.
* Password validation for length, complexity, and special character requirements.

### 2. **Role-Based Access**

* **Admin** :
* Create tasks for one or multiple users.
* View all tasks and their statuses.
* **Users** :
* View only their assigned tasks.
* Update task status (e.g., Accept, Work in Progress, Complete, Decline).

### 3. **Task Management**

* Tasks include fields for title, description, due date, status, and assigned users.
* Task statuses:
  * `Pending` (default)
  * `Work in Progress`
  * `Completed`
  * `Declined`
  * `Not Completed` (auto-updated if not completed by the due date).

### 4. **Documentation**

* **Swagger UI** and **Redoc** for API documentation.
* Postman collection for easy testing.

### 5. **Frontend**

* **React Vite** for a fast and modular development experience.
* **TanStack Query** for data fetching and state management.
* **Tailwind CSS** and **Material-UI** for responsive and modern UI design.

## Backend Details

### **Models**

1. **User** : Provided by `django.contrib.auth.models.User`.
2. **Task** :

* Fields: `id`, `title`, `description`, `due_date`, `status`, `created_by`, `created_at`, `users`.
* Relationships: Many-to-Many with `User` for task assignment.

### **Serializers**

1. **RegistrationSerializer** :

* Validates unique usernames/emails and password complexity.

1. **TaskSerializer** :

* Serializes task data including assigned users.

1. **MyTokenObtainPairSerializer** :

* Custom JWT claims for user-specific data.

1. **UserSerializer** :

* Serializes user data, excluding passwords.

### **Permissions**

* `AllowAny`: For public endpoints like registration.
* `IsAuthenticated`: For task management.
* `IsAdminUser`: For admin-only features.

### **Swagger Documentation**

* Integrated with `drf_yasg` for easy API visualization.
* Endpoints:

  * `/swagger/`: Swagger UI.
  * `/redoc/`: Redoc documentation.

  ## Frontend Details

  ### **Technologies**


  * **React** : Core framework.
  * **Vite** : Fast development server.
  * **TanStack Query** : Simplifies data fetching and caching.
  * **Tailwind CSS** : Provides a modern and responsive UI.
  * **Material-UI** : Additional UI components.

  ### **Features**

  * **Login/Registration** : Authentication using JWT.
  * **Task Views** :
  * Admin: All tasks with their statuses.
  * Users: Assigned tasks only.
  * **Task Actions** :
  * Users can update the status of their tasks.
  * Dynamic UI changes based on task status.

  ## Validation and Error Handling

  1. **User Registration** :

  * Duplicate usernames or emails are rejected.
  * Passwords must meet complexity requirements.

  1. **Task Management** :

  * Only admins can create tasks.
  * Users can only view or update their assigned tasks.

  1. **Task Status Updates** :

  * Status changes are validated to ensure proper transitions.

  1. **Error Responses** :

  * Consistent and detailed error messages for invalid requests.

  ## Postman Collection

  * A Postman collection has been created for testing all endpoints. It includes:

    * Authentication flow.
    * Task creation, retrieval, and status updates.
    * User management.

    ## How to Run

    ### Backend


    1. Install dependencies:
       pip install -r requirements.txt
    2. Run migrations:
       python manage.py makemigrations
    3. python manage.
       py migrate
    4. Start the server:
       python manage.py runserver

    ### Frontend

    1. Install dependencies:
       npm install
    2. Start the development server:
       npm run dev

    ## Conclusion

    This Task Management System provides a robust solution for task assignment and tracking with a clear separation of roles between admin and users. The integration of Swagger documentation and Postman collection ensures ease of testing and API exploration.
