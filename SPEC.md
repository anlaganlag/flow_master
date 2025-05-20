# FlowMaster - Technical Specification Document

## 1. Introduction

This specification document outlines the technical implementation details for the FlowMaster MVP (Minimum Viable Product). Based on the requirements in the PRD, this document focuses on delivering the core functionality that will provide immediate value to users while establishing a foundation for future enhancements.

## 2. System Architecture

### 2.1 Architecture Overview

FlowMaster will be implemented as a web application with a client-server architecture:

- **Frontend**: Single-page application (SPA) built with Vue.js 3
- **Backend**: RESTful API service built with FastAPI (Python)
- **Database**: MongoDB for data persistence
- **Authentication**: JWT-based authentication system

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│             │      │             │      │             │
│  Frontend   │◄────►│   Backend   │◄────►│  Database   │
│  (Vue.js 3) │      │  (FastAPI)  │      │ (MongoDB)   │
│             │      │             │      │             │
└─────────────┘      └─────────────┘      └─────────────┘
```

### 2.2 Technology Stack

#### 2.2.1 Frontend
- **Framework**: Vue.js 3 with Composition API
- **Build Tool**: Vite
- **UI Framework**: Tailwind CSS
- **State Management**: Pinia
- **Routing**: Vue Router
- **HTTP Client**: Axios

#### 2.2.2 Backend
- **Framework**: FastAPI (Python 3.9+)
- **Authentication**: PyJWT for JWT implementation
- **Database ORM**: Motor (async MongoDB driver)
- **API Documentation**: Swagger UI (built into FastAPI)

#### 2.2.3 Database
- **Database**: MongoDB
- **Schema Validation**: JSON Schema validation in MongoDB

## 3. MVP Feature Specifications

### 3.1 User Authentication

#### 3.1.1 User Registration
- Simple registration form with username, email, and password
- Password hashing using bcrypt
- Email validation (format only, no verification email for MVP)
- JWT token generation upon successful registration

#### 3.1.2 User Login
- Login with email/username and password
- JWT token generation with 24-hour expiry
- Refresh token mechanism for extending sessions

#### 3.1.3 User Profile
- Basic profile information storage
- User preferences (theme preference only for MVP)

### 3.2 Task Management System

#### 3.2.1 Three-List System

**Todo List**
- Create, read, update, delete (CRUD) operations for tasks
- Required fields: title, description (optional), priority (1-5)
- Optional fields: due date
- Status tracking (incomplete/complete)

**Watch List**
- Same CRUD operations as Todo List
- Focus on follow-ups and reminders
- Optional reminder date

**Later List**
- Simplified task structure for future ideas
- Minimal fields: title and description

#### 3.2.2 Task Operations
- Move tasks between lists via drag-and-drop
- Mark tasks as complete
- Archive completed tasks
- Basic filtering by status and priority

### 3.3 Daily 3x5 Card System

#### 3.3.1 Card Creation
- Interface for creating daily cards limited to 3-5 tasks
- Task selection from existing Todo and Watch lists
- Option to create new tasks directly on the card

#### 3.3.2 Card Management
- View for today's card
- Simple flip animation between tasks (front) and accomplishments (back)
- Manual addition of accomplishments
- Automatic population of accomplishments from completed tasks

### 3.4 User Interface

#### 3.4.1 Dashboard
- Overview of all three lists with task counts
- Quick access to today's 3x5 card
- Task completion progress indicator
- Responsive design for desktop and mobile

#### 3.4.2 Task Views
- List view with drag-and-drop capability
- Task detail view for editing
- Simple visual indicators for priority levels

#### 3.4.3 Daily Card View
- Visual 3x5 card representation
- Front/back toggle
- Task completion checkboxes
- Accomplishment recording interface

## 4. Database Schema

### 4.1 Collections

#### 4.1.1 Users Collection
```json
{
  "_id": "ObjectId",
  "username": "String",
  "email": "String",
  "password": "String (hashed)",
  "preferences": {
    "theme": "String"
  },
  "created_at": "Date",
  "last_login": "Date"
}
```

#### 4.1.2 Tasks Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "title": "String",
  "description": "String",
  "list_type": "String (todo, watch, later)",
  "priority": "Number (1-5, optional)",
  "due_date": "Date (optional)",
  "is_completed": "Boolean",
  "completed_at": "Date",
  "created_at": "Date",
  "updated_at": "Date"
}
```

#### 4.1.3 Daily Cards Collection
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId (ref: users)",
  "date": "Date",
  "tasks": [
    {
      "task_id": "ObjectId (ref: tasks)",
      "title": "String",
      "is_completed": "Boolean"
    }
  ],
  "accomplishments": [
    {
      "title": "String",
      "source": "String (manual, task)",
      "task_id": "ObjectId (optional, ref: tasks)"
    }
  ],
  "created_at": "Date",
  "updated_at": "Date"
}
```

## 5. API Endpoints

### 5.1 Authentication API

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user profile

### 5.2 Tasks API

- `GET /api/tasks` - Get all tasks (filterable by list_type)
- `POST /api/tasks` - Create new task
- `GET /api/tasks/{id}` - Get specific task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task
- `PUT /api/tasks/{id}/complete` - Mark task as complete
- `PUT /api/tasks/{id}/move` - Move task to different list

### 5.3 Daily Cards API

- `GET /api/daily-cards/today` - Get today's card
- `POST /api/daily-cards` - Create new daily card
- `PUT /api/daily-cards/{id}` - Update daily card
- `POST /api/daily-cards/{id}/accomplishments` - Add accomplishment

## 6. Implementation Plan

### 6.1 Phase 1: Setup and Authentication (Week 1)
- Project scaffolding (frontend and backend)
- Database setup and connection
- User authentication implementation
- Basic UI components and layouts

### 6.2 Phase 2: Task Management (Week 2)
- Task CRUD operations
- Three-list system implementation
- Task movement between lists
- Basic filtering and sorting

### 6.3 Phase 3: Daily Card System (Week 3)
- Daily card creation and management
- Task selection for daily cards
- Accomplishment tracking
- Card flip animation

### 6.4 Phase 4: UI Refinement and Testing (Week 4)
- Responsive design implementation
- UI polish and animations
- End-to-end testing
- Bug fixes and performance optimization

## 7. Technical Considerations

### 7.1 Performance
- Implement pagination for task lists
- Use efficient MongoDB queries with proper indexing
- Optimize frontend rendering with Vue.js best practices

### 7.2 Security
- Implement proper JWT authentication flow
- Secure API endpoints with appropriate authorization
- Sanitize user inputs to prevent injection attacks
- Implement CORS policies

### 7.3 Scalability
- Design database schema for future growth
- Structure code for easy addition of future features
- Implement proper error handling and logging

## 8. Testing Strategy

### 8.1 Frontend Testing
- Unit tests for Vue components using Vue Test Utils
- End-to-end tests using Cypress

### 8.2 Backend Testing
- Unit tests for API endpoints using pytest
- Integration tests for database operations

## 9. Deployment Considerations

### 9.1 Development Environment
- Local development using Docker containers
- MongoDB running in Docker for development

### 9.2 Production Environment
- Frontend: Netlify or Vercel
- Backend: Heroku or DigitalOcean
- Database: MongoDB Atlas

---

This specification document provides a comprehensive guide for implementing the FlowMaster MVP. It focuses on delivering core functionality while establishing a solid foundation for future enhancements.
