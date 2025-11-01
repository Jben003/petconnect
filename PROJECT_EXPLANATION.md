# PetConnect - Project Explanation

## 📋 Project Overview

**PetConnect** is a comprehensive Django-based web platform that connects pet adopters with shelters and service providers. It facilitates pet adoption, service bookings (grooming, veterinary care, etc.), and manages the entire workflow from listing to delivery completion.

---g

## 🏗️ Architecture & Technology Stack

### **Framework & Backend:**
- **Django 5.2.7** - Web framework
- **SQLite** - Database (development)
- **Python** - Programming language

### **Key Libraries:**
- **Pillow** - Image handling for pet/service photos
- **Razorpay** - Payment gateway integration
- **Django Authentication** - User management

### **Project Structure:**
```
petconnect/
├── accounts/          # User authentication & profiles
├── adoption/          # Pet adoption module
├── services/          # Service booking module
├── petconnect/        # Main project settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
└── media/             # User-uploaded files (pet images, service images)
```

---

## 👥 User Roles & Permissions

The platform supports **3 types of users**:

### 1. **Adopter** (`role='adopter'`)
- Can browse and search pets
- Submit adoption requests
- Book pet services (grooming, veterinary, etc.)
- Manage their adoption requests
- Process payments for adoptions
- View notifications

### 2. **Shelter/Service Provider** (`role='shelter'`)
- Create and manage pet listings
- View and manage adoption requests
- Approve/reject adoption requests
- Manage delivery process
- Create and manage services
- View and manage service bookings
- Receive notifications

### 3. **Admin** (`is_superuser=True`)
- Access admin dashboard
- View platform statistics
- Manage all users, pets, and services
- Full system access

---

## 🗄️ Database Models & Relationships

### **1. Profile Model** (`accounts/models.py`)
- **Purpose:** Extends Django User model with role-based information
- **Key Fields:**
  - `user` - OneToOne relationship with User
  - `role` - 'adopter' or 'shelter'
  - `address` - For delivery purposes
  - `phone_number` - Contact information
- **Auto-creation:** Automatically created when a new user registers

### **2. Pet Model** (`adoption/models.py`)
- **Purpose:** Stores pet information
- **Key Fields:**
  - `name`, `pet_type`, `breed`, `age`, `gender`, `size`
  - `description`, `image`
  - `price` - Adoption fee (can be 0 for free adoption)
  - `is_available` - Availability status
  - `shelter` - ForeignKey to User (must have shelter role)
- **Special Methods:**
  - `get_age_display()` - Formats age in years/months
  - `age_in_years` / `age_in_months` - Properties

### **3. AdoptionRequest Model** (`adoption/models.py`)
- **Purpose:** Tracks adoption requests through the entire lifecycle
- **Key Fields:**
  - `adopter` - ForeignKey to User
  - `pet` - ForeignKey to Pet
  - `status` - pending → approved → in_delivery → completed
  - `payment_status` - pending → completed
  - `payment_amount` - Auto-set from pet price
  - `delivery_address` - Delivery location
  - `estimated_delivery_date` / `actual_delivery_date`
- **Status Flow:**
  ```
  pending → (approve/reject) → approved → (payment) → in_delivery → completed
  ```
- **Validation Methods:**
  - `can_be_cancelled()`, `can_be_approved()`, `can_process_payment()`, etc.

### **4. Service Model** (`services/models.py`)
- **Purpose:** Pet care services (grooming, veterinary, etc.)
- **Key Fields:**
  - `name`, `description`, `price`, `category`
  - `duration` - Service duration
  - `image` - Service image
  - `shelter` - ForeignKey to User (service provider)
  - `is_available` - Availability

### **5. Booking Model** (`services/models.py`)
- **Purpose:** Service booking requests
- **Key Fields:**
  - `adopter` - ForeignKey to User
  - `service` - ForeignKey to Service
  - `status` - pending → confirmed → in_progress → completed
  - `booking_date` - Scheduled date/time
  - `address` - Service location
  - `special_instructions`

### **6. Notification Model** (`adoption/models.py`)
- **Purpose:** In-app notifications for users
- **Key Fields:**
  - `user` - ForeignKey to User
  - `message` - Notification text
  - `related_url` - Link to relevant page
  - `is_read` - Read status
  - `created_at` - Timestamp

---

## 🔄 Core Workflows

### **A. Pet Adoption Workflow**

#### **Step 1: Pet Listing (Shelter)**
1. Shelter logs in
2. Navigates to "Add New Pet"
3. Fills pet details (name, type, breed, age, gender, size, description, image, price)
4. Pet is listed and available for adoption

#### **Step 2: Browse & Search (Adopter)**
1. Adopter browses pets on `/adoption/`
2. Can filter by:
   - Pet type (dog, cat, bird, etc.)
   - Gender, size, age range, price range
   - Search by name/breed/description
3. Can sort by name, price, age, newest

#### **Step 3: Submit Adoption Request (Adopter)**
1. Adopter clicks "Adopt" on a pet
2. Fills adoption request form (optional message)
3. System creates `AdoptionRequest` with:
   - Status: `pending`
   - Payment amount: Auto-set from pet price
   - Delivery address: From user profile
4. **Notification sent to shelter**

#### **Step 4: Approve/Reject (Shelter)**
1. Shelter views requests at `/adoption/shelter/requests/`
2. Can approve or reject
3. If approved:
   - Request status → `approved`
   - Pet `is_available` → `False`
   - Other pending requests for same pet → `rejected`
   - **Notification sent to adopter**
4. If rejected:
   - Request status → `rejected`
   - **Notification sent to adopter**

#### **Step 5: Payment Processing (Adopter)**
1. If payment required (price > 0):
   - Adopter visits payment page
   - Razorpay order created
   - Redirected to Razorpay payment gateway
   - Payment processed
   - Signature verified
   - Payment status → `completed`
   - **Notification sent to shelter**
2. If free adoption (price = 0):
   - Payment auto-completed
   - Payment status → `completed` immediately

#### **Step 6: Delivery Management (Shelter)**
1. After payment completion, shelter can start delivery:
   - Sets `estimated_delivery_date`
   - Status → `in_delivery`
   - **Notification sent to adopter**
2. Upon delivery completion:
   - Sets `actual_delivery_date` and `delivery_notes`
   - Status → `completed`
   - **Notification sent to adopter**

### **B. Service Booking Workflow**

#### **Step 1: Service Listing (Shelter)**
1. Shelter creates service listing
2. Sets: name, description, price, category, duration, image
3. Service available for booking

#### **Step 2: Book Service (Adopter)**
1. Adopter browses services at `/services/`
2. Clicks "Book Service"
3. Selects booking date/time and special instructions
4. Booking created with status: `pending`
5. **Notification sent to shelter**

#### **Step 3: Confirm Booking (Shelter)**
1. Shelter views bookings at `/services/shelter/bookings/`
2. Can confirm booking
3. Status → `confirmed`
4. **Notification sent to adopter**

#### **Step 4: Service Execution**
1. Shelter starts service:
   - Status → `in_progress`
   - **Notification sent to adopter**
2. Shelter completes service:
   - Status → `completed`
   - **Notification sent to adopter**

---

## 💳 Payment Integration (Razorpay)

### **Payment Flow:**
1. **Order Creation:**
   - `create_razorpay_order()` converts amount to paise
   - Creates Razorpay order
   - Returns order ID

2. **Payment Gateway:**
   - User redirected to Razorpay checkout
   - Payment processed via Razorpay

3. **Payment Verification:**
   - After payment, Razorpay sends callback
   - `verify_razorpay_payment()` verifies signature
   - Updates `AdoptionRequest.payment_status` to `completed`
   - Stores payment reference

### **Payment Statuses:**
- `pending` - Initial state
- `processing` - Payment in progress
- `completed` - Payment successful
- `failed` - Payment failed
- `refunded` - Payment refunded

---

## 🔔 Notification System

### **How It Works:**
1. **Context Processor:** (`adoption/context_processors.py`)
   - Automatically adds notification count to all templates
   - Available as `unread_notifications_count` in templates

2. **Notification Creation:**
   - Various helper functions create notifications
   - Examples: `create_adoption_request_notification()`, `create_payment_completed_notification()`

3. **Notification Display:**
   - Notification icon in navigation bar
   - Full list at `/adoption/notifications/`
   - Users can mark as read individually or all at once

### **Notification Types:**
- Adoption request received (shelter)
- Adoption approved/rejected (adopter)
- Payment completed (shelter)
- Delivery started/completed (adopter)
- Booking created/confirmed/started/completed (both)

---

## 🔐 Authentication & Authorization

### **Registration:**
1. User fills registration form
2. Selects role: Adopter or Shelter
3. Profile automatically created with selected role
4. Email validation (unique email check)

### **Login:**
- Supports username OR email login
- Role-based redirect:
  - Adopter → `/dashboard/adopter/`
  - Shelter → `/dashboard/shelter/`
  - Admin → `/dashboard/admin/`

### **Access Control:**
- Decorators: `@login_required` for protected views
- Role checks: Views verify user role before allowing actions
- Example: Only shelters can create pets, only adopters can submit adoption requests

---

## 📍 URL Structure

### **Main URLs:**
```
/                                    - Home page (featured pets)
/accounts/register/                  - Registration
/accounts/login/                     - Login
/accounts/profile/                   - User profile
/accounts/dashboard/                 - Role-based dashboard
```

### **Adoption URLs:**
```
/adoption/                           - Pet listing (browse pets)
/adoption/pet/<id>/                  - Pet detail page
/adoption/pet/<id>/adopt/            - Submit adoption request
/adoption/my-requests/               - Adopter's adoption requests
/adoption/shelter/requests/          - Shelter's adoption requests
/adoption/request/<id>/payment/      - Payment page
/adoption/notifications/             - Notification list
```

### **Service URLs:**
```
/services/                           - Service listing
/services/service/<id>/              - Service detail
/services/service/<id>/book/         - Book service
/services/my-bookings/               - Adopter's bookings
/services/shelter/bookings/          - Shelter's bookings
```

---

## 🎨 Key Features

### **1. Advanced Pet Search & Filtering:**
- Filter by type, gender, size, age, price
- Search by name, breed, description
- Sort by multiple criteria

### **2. Payment Integration:**
- Razorpay payment gateway
- Supports both paid and free adoptions
- Secure payment verification

### **3. Delivery Tracking:**
- Estimated delivery date
- Actual delivery date
- Delivery notes
- Status tracking through delivery process

### **4. Real-time Notifications:**
- In-app notifications
- Unread count badge
- Links to related actions

### **5. Role-based Dashboards:**
- Different views for adopters, shelters, and admins
- Quick access to relevant information
- Statistics and overview

### **6. Image Handling:**
- Pet images stored in `media/pet_images/`
- Service images in `media/service_images/`
- Image display in listings and detail pages

---

## 🔧 Technical Implementation Details

### **Form Validation:**
- Custom form validation in `forms.py`
- Email uniqueness checks
- Date validation (no past dates for deliveries/bookings)
- Password strength validation

### **Database Queries:**
- Uses `select_related()` for efficient foreign key queries
- Filtering and searching with Django ORM
- Unique constraints prevent duplicate adoption requests

### **Error Handling:**
- Try-except blocks for payment operations
- User-friendly error messages
- Form error display

### **Session Management:**
- Payment order IDs stored in session
- Session cleanup after payment completion/failure

---

## 🚀 How to Run

### **Prerequisites:**
```bash
pip install -r requirements.txt
```

### **Required Packages:**
- Django==5.2.7
- Pillow==11.3.0 (for images)
- razorpay (for payments) - **Note: Add to requirements.txt**
- asgiref, sqlparse, tzdata

### **Setup:**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py runserver
```

### **Access:**
- Home: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

---

## 📊 Data Flow Summary

1. **Pet Adoption:**
   ```
   Shelter creates Pet → Adopter views → Adopter submits request → 
   Shelter approves → Adopter pays → Shelter starts delivery → 
   Shelter completes delivery → Adoption complete
   ```

2. **Service Booking:**
   ```
   Shelter creates Service → Adopter views → Adopter books → 
   Shelter confirms → Shelter starts service → Shelter completes service
   ```

3. **Notifications:**
   ```
   Action occurs → Notification created → User sees badge → 
   User views notification → User clicks link → Action page loads
   ```

---

## 🔍 Important Notes

1. **Free Adoptions:** If pet price is 0, payment is auto-completed
2. **Unique Constraints:** One adopter can only have one request per pet
3. **Role Restrictions:** Views check user roles before allowing actions
4. **Auto-profile Creation:** Profile created automatically when user registers
5. **Pet Availability:** When approved, pet is marked unavailable automatically
6. **Other Requests:** When approving, other pending requests for same pet are auto-rejected

---

## 🎯 Summary

**PetConnect** is a full-featured pet adoption and service platform with:
- ✅ User role management (Adopter, Shelter, Admin)
- ✅ Complete adoption workflow with payment integration
- ✅ Service booking system
- ✅ Real-time notifications
- ✅ Payment gateway (Razorpay)
- ✅ Delivery tracking
- ✅ Advanced search and filtering
- ✅ Image upload and management
- ✅ Secure authentication and authorization

The platform provides a seamless experience for connecting pet lovers with shelters and service providers, managing the entire process from discovery to completion.

